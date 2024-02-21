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
"""Logical boolean operators: not, and, or."""


def not_(a):
  """Functional form of "not"."""
  ### Implement your own operator here. ###
  return _py_not(a)


def _py_not(a):
  """Default Python implementation of the "not_" operator."""
  return not a


def and_(a, b):
  """Functional form of "and". Uses lazy evaluation semantics."""
  a_val = a()
  ### Implement your own operator here. ###
  return _py_lazy_and(a_val, b)


def _py_lazy_and(cond, b):
  """Lazy-eval equivalent of "and" in Python."""
  return cond and b()


def or_(a, b):
  """Functional form of "or". Uses lazy evaluation semantics."""
  a_val = a()
  ### Implement your own operator here. ###
  return _py_lazy_or(a_val, b)


def _py_lazy_or(cond, b):
  """Lazy-eval equivalent of "or" in Python."""
  return cond or b()


def eq(a, b):
  """Functional form of "equal"."""
  ### Implement your own operator here. ###
  return _py_equal(a, b)


def _py_equal(a, b):
  """Overload of "equal" that falls back to Python's default implementation."""
  return a == b


def not_eq(a, b):
  """Functional form of "not-equal"."""
  return not_(eq(a, b))
