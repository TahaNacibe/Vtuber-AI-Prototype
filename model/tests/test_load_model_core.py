import pytest
import os
from unittest.mock import patch, MagicMock
from model.core.model_core import load_model_core


def test_load_model_core_success(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test_api_key")

    dummy_response = {"text": "Mocked model output"}
    dummy_input = "Hello"
    dummy_memories = []
    dummy_context = []
    dummy_personality = {}

    with patch("model.load_model_core.call_gemini_model", return_value=dummy_response), \
         patch("model.load_model_core.response_transformer", return_value="transformed response"):
        result = load_model_core(dummy_input, dummy_memories, dummy_context, dummy_personality)
        assert result == "transformed response"


def test_load_model_core_no_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    result = load_model_core("Hi", [], [], {})
    assert result is None


def test_load_model_core_empty_input(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test_api_key")
    result = load_model_core("", [], [], {})
    assert result is None
