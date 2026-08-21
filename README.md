# NOVA AI

An offline AI voice assistant built in Python. NOVA listens for a wake word ("Nova"), then executes voice commands — from opening websites and playing music to system control and free-form conversational queries answered by a locally-running LLM via Ollama.

## Features

- **Wake-word activation** — listens continuously for "Nova" before accepting commands
- **Offline conversational AI** — uses Ollama (`phi3` model) to answer general queries with no internet-dependent API calls for the core AI response
- **Voice output** — responses converted to speech via gTTS
- **Web shortcuts** — opens Google, YouTube, Instagram, LinkedIn, Facebook, ChatGPT on command
- **Music playback** — plays songs from a local music library by voice command
- **Live weather lookup** — fetches current weather for a spoken city name (OpenWeatherMap API)
- **News headlines** — fetches and reads out top headlines (NewsAPI)
- **System control** — opens This PC, Settings, Notepad, Calculator via voice
- **System monitoring** — reports live CPU, RAM, and disk usage
- **File search** — searches the local filesystem for a file by voice-given name
- **Date & time** — tells the current date and time on request

## Tech Stack

- **Language:** Python
- **Speech Recognition:** `speech_recognition` (Google Speech API for transcription)
- **Text-to-Speech:** gTTS
- **Local LLM:** Ollama (`phi3` model)
- **System utilities:** `psutil`, `subprocess`, `webbrowser`
- **APIs:** OpenWeatherMap (weather), NewsAPI (headlines)
- **Config:** python-dotenv

## Project Structure

NOVA_AI/
├── nova.py # Main assistant logic — wake word, command routing, all features
├── musicLibrary.py # Local song-name-to-URL mapping for music playback
└── .gitignore


## Getting Started

### Prerequisites
- Python 3.x
- [Ollama](https://ollama.com) installed and running locally, with the `phi3` model pulled:
```bash
  ollama pull phi3
```
- A working microphone

### Installation

```bash
git clone https://github.com/Sharmarjun25/NOVA_AI.git
cd NOVA_AI
pip install speechrecognition gtts pygame requests python-dotenv psutil ollama
```

### Environment Variables

Create a `.env` file in the root with:

NEWS_API_KEY=your_newsapi_key
WEATHER_API_KEY=your_openweathermap_key


### Run

```bash
python nova.py
```

Say **"Nova"** to activate, then speak your command.

## Example Commands

- "Open YouTube"
- "Play [song name]"
- "What's the weather in Delhi"
- "Tell me the news"
- "System status"
- "What time is it"
- Any general question — answered by the local AI model

## Known Limitations

- **Windows-only system commands** — audio playback (`os.system("start temp.mp3")`) and some system controls rely on Windows-specific calls; not currently cross-platform.
- **Hardcoded search path** — file search defaults to scanning `C:\`, which is Windows-specific.
- **Internet-dependent speech-to-text** — voice transcription uses Google's Speech Recognition API, so an internet connection is required for command input even though the AI response itself runs offline via Ollama.

## License

ISC
