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
"""DiastaticMalt is a tool for source-to-source transformations and operator
overloading in Python, including the overloading built-in Python keywords.
It can be utilized to transform regular Python code into a new form better
suited for specific purposes, such as program capture.

The contents of DiastaticMalt are copied with modification from the TensorFlow project,
in particular the `AutoGraph <https://www.tensorflow.org/versions/r2.0/api_docs/python/tf/autograph>`__
module, under the Apache 2.0 license, allowing the use of AutoGraph functionality without
depending on TensorFlow. The modifications made here may eventually be contributed
to TensorFlow.
"""

import types as _types

# (dime10) Replacement for tf_export to generate the AutoGraph API.
from malt.core.ag_ctx import control_status_ctx
from malt.core.converter import Feature as _Feature
from malt.impl.api import internal_convert as _internal_convert
from malt.impl.api import convert
from malt.impl.api import do_not_convert as _do_not_convert
from malt.impl.api import to_graph, to_code
from malt.lang.directives import set_loop_options as _set_loop_options

experimental = _types.ModuleType('malt.experimental')
experimental.__dict__["Feature"] = _Feature
experimental.__dict__["do_not_convert"] = _do_not_convert
experimental.__dict__["set_loop_options"] = _set_loop_options
internal = _types.ModuleType('malt.internal')
internal.__dict__["convert"] = _internal_convert

# (dime10) additional imports for public API
from malt.impl.api import AutoGraphError
from malt.core.converter import ConversionOptions

__all__ = [
    # Main API
    'AutoGraphError',
    'ConversionOptions',
    # tf_export
    'control_status_ctx',
    'convert',
    'to_code',
    'to_graph',
    'experimental',
    'internal',
]
