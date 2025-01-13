import os
import tempfile
from assembly_ai import AssemblyAI
from llm import llm
from elevenlabs import ElevenLabs
from io import BytesIO

from icecream import ic #for logging
from dotenv import load_dotenv

from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ASSEMBLYAI_TOKEN = os.getenv("ASSEMBLY_API_KEY")
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_BASE_URL = os.getenv("LLM_BASE_URL")

assemblyai = AssemblyAI(ASSEMBLYAI_TOKEN)
llm_instance = llm(base_url=LLM_BASE_URL, api_key=LLM_API_KEY)
elevenlabs = ElevenLabs()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text("Hi! I’m your bot. How can I assist you?")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text("Use /start to begin and /help to view this message.")
    
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  text = update.message.text.lower()
  # tambahkan kirim ke LLM
  await update.message.reply_text(text)
  
# async def voice_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
#   ic(update.message)

#     # Mendapatkan file voice dari Telegram
#     new_file = await context.bot.get_file(update.message.voice.file_id)

#     # Menggunakan temporary file untuk menyimpan suara yang diunduh
#     with tempfile.NamedTemporaryFile(suffix=".ogg") as temp_voice_file:
#         await new_file.download_to_drive(temp_voice_file.name)

#         # Mengirim file suara ke LLM untuk transkripsi
#         transcription = await process_with_llm(temp_voice_file.name)

#         # Membuat audio baru berdasarkan hasil transkripsi
#         with tempfile.NamedTemporaryFile(suffix=".ogg") as temp_response_file:
#             convert_text_to_audio(transcription, temp_response_file.name)

#             # Kirim file audio hasil ke Telegram sebagai voice
#             with open(temp_response_file.name, "rb") as audio_file:
#                 await update.message.reply_voice(InputFile(audio_file))

#     # Membalas dengan teks transkripsi (opsional)
#     await update.message.reply_text(f"Transkripsi suara Anda: {transcription}")

async def voice_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  ic(update.message)

  # Mendapatkan file voice dari Telegram
  new_file = await context.bot.get_file(update.message.voice.file_id)
  
  # Mendapatkan URL file dari Telegram
  full_url = new_file.file_path

  # Gunakan URL ini untuk mengirim permintaan ke AssemblyAI
  question = assemblyai.sound_to_text(full_url)
  ic(question)
  
  llm_response = llm_instance.call(question)
  clear_response = llm_response.get("text")
  
  mp3_audio = elevenlabs.text_to_speech(clear_response)
  if mp3_audio:
    audio_file = InputFile(BytesIO(mp3_audio), filename="audio.mp3")
    await update.message.reply_voice(voice=audio_file)  # Use 'voice' instead of 'audio'
  

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))

# Add message handler
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

# Add voide message handler
app.add_handler(MessageHandler((filters.AUDIO | filters.VOICE) & ~filters.COMMAND, voice_message_handler))

ic("Bot is running...")

app.run_polling()