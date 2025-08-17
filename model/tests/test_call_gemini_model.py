import pytest
import requests
from unittest.mock import patch
from model.core.model_api import call_gemini_model


def test_call_gemini_model_success():
    dummy_payload = {"contents": [{"parts": [{"text": "Hello"}]}]}
    dummy_api_key = "test_key"
    dummy_response = {"text": "Hi there!"}

    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = dummy_response

        result = call_gemini_model(dummy_payload, dummy_api_key)
        assert result == dummy_response


def test_call_gemini_model_failure():
    dummy_payload = {}
    dummy_api_key = "test_key"

    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 500
        mock_post.return_value.text = "Internal Server Error"

        with pytest.raises(RuntimeError) as exc_info:
            call_gemini_model(dummy_payload, dummy_api_key)

        assert "API call failed" in str(exc_info.value)
