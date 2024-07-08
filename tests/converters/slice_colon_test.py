# Copyright 2024 Xanadu Quantum Technologies Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Unit tests for Python slice with SliceTransformer."""

import inspect

import pytest

from malt.core import converter
from malt.impl.api import PyToPy

OPTIONAL_FEATURES = [converter.Feature.BUILTIN_FUNCTIONS, converter.Feature.LISTS]
TOPLEVEL_OPTIONS = converter.ConversionOptions(
    recursive=True,
    user_requested=True,
    internal_convert_user_code=True,
    optional_features=OPTIONAL_FEATURES,
)


class Transformer(PyToPy):
    """Example source-to-source transformer."""

    def __init__(self):
        super().__init__()
        self._extra_locals = None

    def transform(self, obj, user_context):
        """Calling transform from malt api."""
        return self.transform_function(obj, user_context)


def test_slice_start_end():
    """Test if slice with start and end appears after transform."""
    tr = Transformer()

    def fn(x, y):
        x[0:10] = y
        return x

    user_context = converter.ProgramContext(TOPLEVEL_OPTIONS)
    new_fn, _, _ = tr.transform(fn, user_context)
    new_fn_source = inspect.getsource(new_fn)
    assert (
        "x = ag__.set_item(ag__.ld(x), ag__.converted_call(slice, (0, 10,), None, fscope), ag__.ld(y))"
        in new_fn_source
    )
    assert "[0:10]" not in new_fn_source


def test_slice_start_end_step():
    """Test if slice with start, end, and step appears after transform."""
    tr = Transformer()

    def fn(x, y):
        x[0:10:2] = y
        return x

    user_context = converter.ProgramContext(TOPLEVEL_OPTIONS)
    new_fn, _, _ = tr.transform(fn, user_context)
    new_fn_source = inspect.getsource(new_fn)
    assert (
        "x = ag__.set_item(ag__.ld(x), ag__.converted_call(slice, (0, 10, 2), None, fscope), ag__.ld(y))"
        in new_fn_source
    )
    assert "[0:10:2]" not in new_fn_source


def test_slice_start_only():
    """Test if slice with start only appears after transform."""
    tr = Transformer()

    def fn(x, y):
        x[5:] = y
        return x

    user_context = converter.ProgramContext(TOPLEVEL_OPTIONS)
    new_fn, _, _ = tr.transform(fn, user_context)
    new_fn_source = inspect.getsource(new_fn)
    assert (
        "x = ag__.set_item(ag__.ld(x), ag__.converted_call(slice, (5,,), None, fscope), ag__.ld(y))"
        in new_fn_source
    )
    assert "[5:]" not in new_fn_source


def test_slice_end_only():
    """Test if slice with end only appears after transform."""
    tr = Transformer()

    def fn(x, y):
        x[:10] = y
        return x

    user_context = converter.ProgramContext(TOPLEVEL_OPTIONS)
    new_fn, _, _ = tr.transform(fn, user_context)
    new_fn_source = inspect.getsource(new_fn)
    assert (
        "x = ag__.set_item(ag__.ld(x), ag__.converted_call(slice, (,10,), None, fscope), ag__.ld(y))"
        in new_fn_source
    )
    assert "[:10]" not in new_fn_source


def test_slice_step_only():
    """Test if slice with step only appears after transform."""
    tr = Transformer()

    def fn(x, y):
        x[::2] = y
        return x

    user_context = converter.ProgramContext(TOPLEVEL_OPTIONS)
    new_fn, _, _ = tr.transform(fn, user_context)
    new_fn_source = inspect.getsource(new_fn)
    assert (
        "x = ag__.set_item(ag__.ld(x), ag__.converted_call(slice, (,,2), None, fscope), ag__.ld(y))"
        in new_fn_source
    )
    assert "[::2]" not in new_fn_source


def test_slice_colon_only():
    """Test if slice with colon only appears after transform."""
    tr = Transformer()

    def fn(x, y):
        x[:] = y
        return x

    user_context = converter.ProgramContext(TOPLEVEL_OPTIONS)
    new_fn, _, _ = tr.transform(fn, user_context)
    new_fn_source = inspect.getsource(new_fn)
    assert (
        "x = ag__.set_item(ag__.ld(x), ag__.converted_call(slice, (,), None, fscope), ag__.ld(y))"
        in new_fn_source
    )
    assert "[:]" not in new_fn_source


def test_slice_two_colons():
    """Test if slice with two colons appears after transform."""
    tr = Transformer()

    def fn(x, y):
        x[::] = y
        return x

    user_context = converter.ProgramContext(TOPLEVEL_OPTIONS)
    new_fn, _, _ = tr.transform(fn, user_context)
    new_fn_source = inspect.getsource(new_fn)
    assert (
        "x = ag__.set_item(ag__.ld(x), ag__.converted_call(slice, (,,), None, fscope), ag__.ld(y))"
        in new_fn_source
    )
    assert "[::]" not in new_fn_source


if __name__ == "__main__":
    pytest.main(["-x", __file__])
