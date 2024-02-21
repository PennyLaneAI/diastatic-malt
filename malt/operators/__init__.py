# Copyright 2023 Xanadu Quantum Technologies Inc.
# Copyright 2018 The TensorFlow Authors. All Rights Reserved.
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
"""This module implements operators that AutoGraph overloads.

Note that "operator" is used loosely here, and includes control structures like
conditionals and loops, implemented in functional form, using for example
closures for the body.

(dime10) This module has been stripped of all TensorFlow related functionality, although
         Python versions of operators have been retained as a fallback / demonstration.
         Users of the AutoGraph package are expected to provide their own implementations
         of relevant operators.
"""

# Naming conventions:
#  * operator names match the name usually used for the respective Python
#    idiom; examples: for_stmt, list_append
#  * operator arguments match either of:
#    - the corresponding Python AST attribute (e.g. the condition of an if
#      statement is called test) if the operator represents an AST construct
#    - the names used in the Python docs, if the operator is a function (e.g.
#      list_ and x for append, see
#      https://docs.python.org/3.7/tutorial/datastructures.html)
#
# All operators may accept a final argument named "opts", of a type that
# subclasses namedtuple and contains any arguments that are only required
# for some specializations of the operator.

from malt.operators.conditional_expressions import if_exp
from malt.operators.control_flow import for_stmt
from malt.operators.control_flow import if_stmt
from malt.operators.control_flow import while_stmt
from malt.operators.data_structures import list_append
from malt.operators.data_structures import list_pop
from malt.operators.data_structures import list_stack
from malt.operators.data_structures import ListPopOpts
from malt.operators.data_structures import ListStackOpts
from malt.operators.data_structures import new_list
from malt.operators.exceptions import assert_stmt
from malt.operators.logical import and_
from malt.operators.logical import eq
from malt.operators.logical import not_
from malt.operators.logical import not_eq
from malt.operators.logical import or_
from malt.operators.py_builtins import float_
from malt.operators.py_builtins import int_
from malt.operators.py_builtins import len_
from malt.operators.py_builtins import print_
from malt.operators.py_builtins import range_
from malt.operators.slices import get_item
from malt.operators.slices import GetItemOpts
from malt.operators.slices import set_item
from malt.operators.variables import ld
from malt.operators.variables import ldu
from malt.operators.variables import Undefined
from malt.operators.variables import UndefinedReturnValue
from malt.operators.function_wrappers import FunctionScope
from malt.operators.function_wrappers import with_function_scope
