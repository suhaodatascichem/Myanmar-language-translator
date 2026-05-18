# Myanmar Language Translator Bot (Telegram)

This is a focused Telegram bot that acts as an automatic household translation agent for family groups. It seamlessly translates between English, Chinese, and Myanmar natively using the Google Gemini 2.5 Flash API.

## Features

- **Multilingual Support**: Translates between English, Chinese, and Myanmar.
  - Messages with Myanmar text are translated to English.
  - Messages with English or Chinese (or mixed) are translated to Myanmar.
- **Media Support**: Natively understands and translates text in images, and transcribes/translates voice notes.
- **Zero Config for End Users**: Automatically translates every message without needing prefix commands.
- **Commands**: Supports `/en`, `/cn`, and `/mm` commands when replying to specific messages to force a translation language.

## Setup & Installation

### Prerequisites

- Python 3.8+
- A Telegram Bot Token from [@BotFather](https://t.me/botfather)
- A Gemini API Key from [Google AI Studio](https://aistudio.google.com/)

### 1. Clone and Install Dependencies

```bash
git clone https://github.com/suhaodatascichem/Myanmar-language-translator.git
cd Myanmar-language-translator
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file in the root directory and add your API keys:

```env
TELEGRAM_BOT_TOKEN=your_telegram_token
GEMINI_API_KEY=your_gemini_key
```

### 3. Telegram Bot Privacy Settings

For the bot to read all messages in a group chat (instead of just commands), you must configure its privacy settings:
1. Message **@BotFather** on Telegram.
2. Send `/setprivacy`.
3. Select your bot.
4. Click **Disable**.

### 4. Running the Bot

Run the bot locally:

```bash
python main.py
```

To run the bot in the background on a Linux/cloud server:

```bash
nohup python3 main.py > bot.log 2>&1 &
```

## How It Works

The bot's personality, rules, and system prompt constraints are defined in the `prompts/` directory (`AGENTS.md`, `SOUL.md`, `USER.md`). The bot reads these files on startup and passes them to the Gemini model as system instructions, ensuring it acts as a focused translator and not a general assistant.
