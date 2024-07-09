# Copyright 2024 Xanadu Quantum Technologies Inc.
# Copyright 2016 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Converter for slice operations."""

import gast

from malt.core import converter
from malt.lang import directives
from malt.pyct import templates


class SliceTransformer(converter.Base):
  """Converts slicing operations to their TF counterpart.

  Currently, relying on the default slice operator that Tensor uses is
  insufficient, because TensorArray and tensor lists use dedicated index read
  and write functions.
  """

  def _process_single_assignment(self, target, value):
    # (dime10) This function has been modified to support slices.
    if not isinstance(target, gast.Subscript):
      return None
    s = target.slice
    if isinstance(s, (gast.Tuple)):
      # multi-dimensional indices are not supported
      return None

    template = """
      target = ag__.set_item(target, key, item)
    """

    lower, upper, step = None, None, None

    if isinstance(s, (gast.Slice)):
      # Replace unused arguments in the string template with "None" to preserve each arguments' position.
      # malt.pyct.templates.replace ignores None and does not accept string so the change need to be applied here.
      lower_str = "lower" if s.lower is not None else "None"
      upper_str = "upper" if s.upper is not None else "None"
      step_str = "step" if s.step is not None else "None"
      template = template.replace("key", f"slice({lower_str}, {upper_str}, {step_str})")

      lower, upper, step = s.lower, s.upper, s.step

    return templates.replace(
      template, target=target.value, key=target.slice, lower=lower, upper=upper, step=step, item=value)

  def visit_Assign(self, node):
    node = self.generic_visit(node)
    # TODO(mdan): Support unpackings and multiple assignments.
    if len(node.targets) != 1:
      raise NotImplementedError('multiple assignment')
    replacement = self._process_single_assignment(node.targets[0], node.value)
    if replacement is not None:
      return replacement
    return node

  def visit_Subscript(self, node):
    node = self.generic_visit(node)
    s = node.slice
    if isinstance(s, (gast.Tuple, gast.Slice)):
      return node

    if not isinstance(node.ctx, gast.Load):
      # Index writes are handled at a higher level, one at which the rvalue is
      # also available.
      return node

    dtype = self.get_definition_directive(
        node.value,
        directives.set_element_type,
        'dtype',
        default=templates.replace_as_expression('None'))

    template = """
      ag__.get_item(
          target,
          key,
          opts=ag__.GetItemOpts(element_dtype=dtype))
    """
    return templates.replace_as_expression(
        template, target=node.value, key=s, dtype=dtype)

def transform(node, ctx):
  return SliceTransformer(ctx).visit(node)
