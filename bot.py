import os
import replicate
from PIL import Image, ImageOps, ImageDraw, ImageFont
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv

async def start(update, context):
    await update.message.reply_text(
        "👋 أهلاً! \n"
        "✅ ابعت نص لتوليد صورة بالذكاء الاصطناعي.\n"
        "✅ ابعت صورة + تعليق (برومبت) علشان أعيد إنشائها بالكامل حسب طلبك.\n"
    )

# توليد صور من نص
async def handle_text(update, context):
    prompt = update.message.text
    await update.message.reply_text("⏳ جاري إنشاء الصورة...")
    try:
        output = replicate.run(
            "stability-ai/stable-diffusion:db21e45cbaa500",
            input={"prompt": prompt, "num_inference_steps": 50}
        )
        await update.message.reply_photo(output[0])
    except Exception as e:
        await update.message.reply_text(f"❌ حصل خطأ: {e}")

# تعديل صورة باستخدام Replicate (إعادة إنشاء كاملة)
async def handle_image(update, context):
    photo = await update.message.photo[-1].get_file()
    file_path = "input.jpg"
    await photo.download_to_drive(file_path)

    caption = update.message.caption  # النص المرفق مع الصورة
    if caption:
        await update.message.reply_text("⏳ جاري إعادة إنشاء الصورة بالكامل حسب البرومبت...")
        try:
            output = replicate.run(
                "stability-ai/stable-diffusion:db21e45cbaa500",
                input={
                    "image": open(file_path, "rb"),
                    "prompt": caption,
                    "strength": 0.9,  # إعادة رسم شبه كاملة
                    "num_inference_steps": 50
                }
            )
            await update.message.reply_photo(output[0])
        except Exception as e:
            await update.message.reply_text(f"❌ حصل خطأ: {e}")
    else:
        await update.message.reply_text("📌 لازم تبعت الصورة ومعاها برومبت علشان أعدلها بالكامل.")

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
