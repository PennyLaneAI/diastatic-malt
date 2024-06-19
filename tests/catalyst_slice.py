from catalyst import qjit
import jax.numpy as jnp

import pytest

def test_slice():
    """Test transformation related to slice."""

    @qjit(autograph=True)
    def expand_by_two(x):
        first_dim = x.shape[0]
        result = jnp.empty((first_dim*2, *x.shape[1:]), dtype=x.dtype)

        for i in range(2):
            start = i * first_dim
            stop = start + first_dim
            result[start:stop] = x
        return result
    assert (expand_by_two(jnp.array([5, 3, 4])) == jnp.array([5, 3, 4, 5, 3, 4])).all()


if __name__ == "__main__":
    pytest.main(["-x", __file__])