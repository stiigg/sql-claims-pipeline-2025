"""Placeholder synthetic regression tests."""

import pathlib

import pytest


@pytest.mark.skip("Synthetic dataset not yet implemented")
def test_synthetic_pipeline_placeholder():
    assert pathlib.Path("data_synthetic").exists()
