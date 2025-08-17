import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from vtuber.sender import VTubeSender

# Dummy hotkey object
class DummyHotkey:
    def __init__(self, repeat=False, repeatCount=0, actions=None):
        self.repeat = repeat
        self.repeatCount = repeatCount
        self.actions = actions or ["wave"]

@pytest.mark.asyncio
async def test_initialize_connection_success():
    with patch("model.utils.vtube_sender.pyvts.vts") as mock_vts_class:
        mock_vts = AsyncMock()
        mock_vts_class.return_value = mock_vts

        sender = VTubeSender()
        await sender.initialize_connection()

        assert mock_vts.connect.called
        assert mock_vts.request_authenticate_token.called
        assert mock_vts.request_authenticate.called

@pytest.mark.asyncio
async def test_send_emote_to_api_repeat():
    with patch("model.utils.vtube_sender.pyvts.vts") as mock_vts_class, \
         patch("model.utils.vtube_sender.get_emote_by_key") as mock_get_emote:

        dummy_hotkey = DummyHotkey(repeat=True, repeatCount=2, actions=["smile"])
        mock_get_emote.return_value = dummy_hotkey

        mock_vts = AsyncMock()
        mock_vts_class.return_value = mock_vts
        mock_vts.vts_request.requestTriggerHotKey.return_value = "trigger"

        sender = VTubeSender()
        await sender.send_emote_to_api("smile")

        assert mock_get_emote.called
        assert mock_vts.request.call_count == dummy_hotkey.repeatCount + 1  # includes clear_last_emote

@pytest.mark.asyncio
async def test_send_emote_to_api_once():
    with patch("model.utils.vtube_sender.pyvts.vts") as mock_vts_class, \
         patch("model.utils.vtube_sender.get_emote_by_key") as mock_get_emote:

        dummy_hotkey = DummyHotkey(repeat=False, actions=["nod"])
        mock_get_emote.return_value = dummy_hotkey

        mock_vts = AsyncMock()
        mock_vts_class.return_value = mock_vts
        mock_vts.vts_request.requestTriggerHotKey.return_value = "trigger"

        sender = VTubeSender()
        await sender.send_emote_to_api("nod")

        assert mock_get_emote.called
        assert mock_vts.request.call_count == 2  # nod + clear

@pytest.mark.asyncio
async def test_send_emote_to_api_invalid_key():
    with patch("model.utils.vtube_sender.pyvts.vts"), \
         patch("model.utils.vtube_sender.get_emote_by_key", return_value=None):

        sender = VTubeSender()
        with pytest.raises(KeyError):
            await sender.send_emote_to_api("invalid_key")

@pytest.mark.asyncio
async def test_send_emote_to_api_empty_key():
    with patch("model.utils.vtube_sender.pyvts.vts"):
        sender = VTubeSender()
        with pytest.raises(ValueError):
            await sender.send_emote_to_api("")
