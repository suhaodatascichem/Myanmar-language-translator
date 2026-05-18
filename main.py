import os
import logging
from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# 1. Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 2. Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 3. Configure Gemini SDK
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# 4. Dynamically load the system instructions from the markdown files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPT_DIR = os.path.join(BASE_DIR, "prompts")

def load_system_instruction():
    prompt = "You are a focused household translation agent for one family group.\n\n"
    files_to_load = ["AGENTS.md", "SOUL.md", "USER.md"]
    
    for filename in files_to_load:
        filepath = os.path.join(PROMPT_DIR, filename)
        try:
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    prompt += f.read() + "\n\n"
            else:
                logging.warning(f"Could not find {filepath}. Skipping.")
        except Exception as e:
            logging.error(f"Error loading {filename}: {e}")
            
    return prompt

SYSTEM_INSTRUCTION = load_system_instruction()

# Initialize the Gemini Model with the loaded instructions
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=SYSTEM_INSTRUCTION
)

async def process_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles incoming messages, passes them to Gemini, and replies."""
    if not update.message:
        return

    text = update.message.text or update.message.caption or ""
    reply_to = update.message.reply_to_message
    
    # Check for translation commands
    is_command = False
    command_text = text.strip().lower()
    target_msg = update.message
    
    commands = ["/english", "/en", "/chinese", "/cn", "/myanmar", "/mm"]
    
    if command_text in commands:
        if reply_to:
            is_command = True
            target_msg = reply_to
        else:
            await update.message.reply_text("Please reply to a message with /en, /cn, or /mm.")
            return

    # Prepare contents for Gemini
    contents = []
    
    # If it's a command, add context
    if is_command:
        contents.append(f"User issued a command: {text}. Translate the following message according to the command rules.")

    msg_text = target_msg.text or target_msg.caption or ""
    
    # Handle Image Messages
    if target_msg.photo:
        # Telegram sends multiple sizes, get the largest one
        photo_file = await target_msg.photo[-1].get_file()
        file_path = f"temp_image_{update.message.message_id}.jpg"
        await photo_file.download_to_drive(file_path)
        
        gemini_file = genai.upload_file(file_path)
        contents.append(gemini_file)
        
        if msg_text:
            contents.append(msg_text)
            
        os.remove(file_path) # cleanup
        
    # Handle Voice / Audio Messages
    elif target_msg.voice or target_msg.audio:
        audio = target_msg.voice or target_msg.audio
        audio_file = await audio.get_file()
        file_path = f"temp_audio_{update.message.message_id}.ogg"
        await audio_file.download_to_drive(file_path)
        
        gemini_file = genai.upload_file(file_path)
        contents.append(gemini_file)
        
        if msg_text:
            contents.append(msg_text)
            
        os.remove(file_path) # cleanup
        
    # Handle normal Text Messages
    else:
        if not msg_text and not is_command:
            return # Empty message
        contents.append(msg_text)

    # Avoid empty API calls
    if not contents:
        return

    # Call Gemini API
    try:
        logging.info("Sending request to Gemini...")
        response = model.generate_content(contents)
        reply_text = response.text.strip()
        
        # Don't send internal NO_REPLY marker (OpenClaw handled this, we handle it here)
        if reply_text and "NO_REPLY" not in reply_text:
            await update.message.reply_text(reply_text)
            
    except Exception as e:
        logging.error(f"Gemini API error: {e}")
        await update.message.reply_text("Translation failed. Please try again.")

if __name__ == '__main__':
    if not TELEGRAM_BOT_TOKEN or not GEMINI_API_KEY:
        print("ERROR: Please set TELEGRAM_BOT_TOKEN and GEMINI_API_KEY in the .env file.")
        exit(1)
        
    # Build Telegram Bot Application
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Add handler for ALL message types (text, photo, voice)
    application.add_handler(MessageHandler(filters.ALL & ~filters.ChatType.CHANNEL, process_message))
    
    print("Bot is starting and listening for messages...")
    application.run_polling()
