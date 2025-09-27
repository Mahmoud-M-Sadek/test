import os
import replicate
from PIL import Image, ImageOps, ImageDraw, ImageFont
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv

# تحميل التوكنات من ملف .env
load_dotenv()
TELEGRAM_TOKEN = "8247908876:AAHfXgu2du7fneMnr4XaVbeJD9_s_ulvw4w"
REPLICATE_TOKEN = "r8_56lL7Jc45SAHz2EXCQoYjNYymftvWMQ1NtlUT"
os.environ["REPLICATE_API_TOKEN"] = "r8_56lL7Jc45SAHz2EXCQoYjNYymftvWMQ1NtlUT"

# ---------- أوامر البوت ----------
async def start(update, context):
    await update.message.reply_text(
        "👋 أهلاً! ابعت نص لتوليد صورة بالذكاء الاصطناعي ✨\n"
        "أو ابعت صورة وأنا أعدلها لك."
    )

# توليد صور من نص
async def handle_text(update, context):
    prompt = update.message.text
    await update.message.reply_text("⏳ جاري إنشاء الصورة...")
    try:
        output = replicate.run(
            "stability-ai/stable-diffusion:db21e45cbaa500",
            input={"prompt": prompt}
        )
        await update.message.reply_photo(output[0])
    except Exception as e:
        await update.message.reply_text(f"❌ حصل خطأ: {e}")

# تعديل صورة مرفوعة
async def handle_image(update, context):
    photo = await update.message.photo[-1].get_file()
    file_path = "input.jpg"
    await photo.download_to_drive(file_path)

    # تعديل بسيط: قلب الصورة + نص
    img = Image.open(file_path)
    img = ImageOps.mirror(img)

    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    draw.text((10, 10), "تم التعديل ✅", font=font, fill=(255, 0, 0))

    out_path = "output.jpg"
    img.save(out_path)

    await update.message.reply_photo(open(out_path, "rb"))

# ---------- تشغيل البوت ----------
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))
    print("🚀 البوت شغال...")
    app.run_polling()

if __name__ == "__main__":
    main()
