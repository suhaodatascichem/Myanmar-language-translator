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

### 4. Running the Bot Locally

Run the bot locally for testing:

```bash
python main.py
```

### 5. Deploying to Google Cloud (Compute Engine)

Since the bot needs to run 24/7, deploying it to a Google Cloud Compute Engine instance is ideal.

1. **SSH into your VM:**
   Open the Google Cloud Console, go to Compute Engine, and click the "SSH" button next to your instance.

2. **Clone the repository:**
   ```bash
   git clone https://github.com/suhaodatascichem/Myanmar-language-translator.git
   cd Myanmar-language-translator
   ```

3. **Install Dependencies:**
   ```bash
   sudo apt update
   sudo apt install python3-pip -y
   pip3 install -r requirements.txt
   ```

4. **Create the `.env` file on the server:**
   Use a text editor like `nano` to create the configuration file:
   ```bash
   nano .env
   ```
   Paste your keys:
   ```env
   TELEGRAM_BOT_TOKEN=your_telegram_token
   GEMINI_API_KEY=your_gemini_key
   ```
   Press `Ctrl+O`, `Enter`, and `Ctrl+X` to save and exit.

5. **Run the Bot in the Background (nohup):**
   To keep the bot running even after you close the SSH terminal, use `nohup`:
   ```bash
   nohup python3 main.py > bot.log 2>&1 &
   ```
   You can verify it's running by checking the log:
   ```bash
   tail -f bot.log
   ```
## update code
```
cd ~/Myanmar-language-translator
nano .env
(Add ALLOWED_CHAT_IDS=6415248406, then save with Ctrl+O, Enter, Ctrl+X)
pkill -f "python3 main.py"
nohup python3 main.py > bot.log 2>&1 &
```

## How It Works

The bot's personality, rules, and system prompt constraints are defined in the `prompts/` directory (`AGENTS.md`, `SOUL.md`, `USER.md`). The bot reads these files on startup and passes them to the Gemini model as system instructions, ensuring it acts as a focused translator and not a general assistant.
