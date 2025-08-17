# Vtuber AI Prototype

This repository contains a **proof-of-concept AI Vtuber system**. It demonstrates a basic AI-driven VTuber with text-to-speech, Discord integration, and memory capabilities.  

## Dependencies / Requirements

This project relies on a few external tools and services:

- **VTube Studio** – Required for controlling the VTuber avatar.  
- **Discord** – For chat interactions (requires a bot token).  
- **Gemini API** – AI model integration.  
- **ElevenLabs API** – Text-to-speech service.  
- **FISH Audio API** – Optional audio service.  
- **Python 3.12+** – All scripts are tested on this version.  
- **Required Python packages** – Listed in `requirements.txt`.


> **Note:** This prototype was developed on a machine with limited resources. Running a full-featured, high-performance VTuber AI requires significantly more computing power and memory. Until then, this system demonstrates a basic, resource-light proof-of-concept.


> ⚠️ **Important:** Current state-of-the-art systems use more advanced memory, model management, and speech synthesis methods. This project is primarily for educational and portfolio purposes.

---

## Prerequisites

### 1. Personality File
- The system requires a personality configuration file: `personality.txt`.  
- This file should contain the AI’s character traits, behavior guidelines, and any base prompts you want the AI to follow.  
- **Example:**  

Name: Someone
Style: Friendly, humorous, and curious
Tone: Playful but informative

### 2. Environment Variables
The following environment variables must be set for the AI to run:

| Variable | Purpose |
|----------|---------|
| `GEMINI_API_KEY` | API key for the Gemini AI model integration. |
| `ELEVEN_LABS_API_KEY` | API key for ElevenLabs text-to-speech service. |
| `DISCORD_TOKEN` | Token for the Discord bot to operate. |
| `FISH_AUDIO_API_KEY` | API key for the FISH audio service (if used). |
| `VOICE_MODEL_ID` | ID of the voice model to use with the TTS service. |

**How to set environment variables:**  

On **Linux/macOS**:
```bash
export GEMINI_API_KEY="your_gemini_api_key"
export ELEVEN_LABS_API_KEY="your_elevenlabs_api_key"
export DISCORD_TOKEN="your_discord_token"
export FISH_AUDIO_API_KEY="your_fish_audio_api_key"
export VOICE_MODEL_ID="voice_model_id_here"

On Windows (PowerShell):
$env:GEMINI_API_KEY="your_gemini_api_key"
$env:ELEVEN_LABS_API_KEY="your_elevenlabs_api_key"
$env:DISCORD_TOKEN="your_discord_token"
$env:FISH_AUDIO_API_KEY="your_fish_audio_api_key"
$env:VOICE_MODEL_ID="voice_model_id_here"


* Features (Prototype)

- Basic Discord integration for chat interactions.

- Text-to-speech using ElevenLabs API.

- Simple memory system (for storing temporary conversation context).

- Character personality support via personality.txt.

- Proof-of-concept AI-driven VTuber interactions.

* Limitations

- Memory and chat storage are very basic; modern AI systems use more advanced persistent memory and context management.

- Resource-limited: uses lightweight models and APIs rather than fully self-hosted large language models.

- Not intended for production use.