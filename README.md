# My First AI Agent

> A tool-using AI agent built with the **Anthropic Claude SDK** — it doesn't just chat, it *does things*.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Anthropic](https://img.shields.io/badge/Powered%20by-Claude-orange)

---

## What it can do

| Tool | Description |
|------|-------------|
| **Calculator** | Solves any math expression |
| **Weather** | Fetches real-time weather for any city in the world |
| **Image Generation** | Creates AI images from text descriptions |
| **Write Files** | Saves code or text to your computer automatically |
| **Run Code** | Executes Python scripts and shows the output |
| **Memory** | Remembers the full conversation history |

---

## Examples
```
You: what is the weather in Tokyo?
Claude: The current weather in Tokyo is 58°F with wind speed of 9 km/h. 

You: what is 1234 * 5678?
Claude: 1234 × 5678 = 7,006,652 

You: generate an image of a mongolian volleyball team on the steppe
Claude: Done! Saved as mongolian_volleyball_steppe.png 

You: write a python script that prints the fibonacci sequence, then run it
Claude: Done! Output: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34 
```

---

## Requirements

- Python 3.10+
- Node.js 18+

---

## Installation

**1. Clone the repo:**
```bash
git clone https://github.com/TulparJ/my-first-agent.git
cd my-first-agent
```

**2. Install dependencies:**
```bash
pip3 install -r requirements.txt
```

**3. Set your API keys:**
```bash
export ANTHROPIC_API_KEY="your-anthropic-key"
export HF_API_KEY="your-huggingface-key"
```

**4. Run it:**
```bash
python3 chatbot.py
```

---

## Getting API Keys

| Key | Where to get it |
|-----|----------------|
| `ANTHROPIC_API_KEY` | [console.anthropic.com](https://console.anthropic.com) |
| `HF_API_KEY` | [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) — use **Write** role |

---

## Built With

- [Anthropic Claude API](https://docs.anthropic.com) — the AI brain behind the agent
- [Open-Meteo](https://open-meteo.com) — free weather API, no key needed
- [FLUX by Black Forest Labs](https://huggingface.co/black-forest-labs/FLUX.1-schnell) — free AI image generation

---
