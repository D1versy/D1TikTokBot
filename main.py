import telegram
from telegram import ParseMode
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters
)
import os
import logging
import tiktok_downloader
from random import randint

# Your BOT Token
BOT_TOKEN = os.getenv("BOT_TOKEN")

# TikTok Video URL Types
tikTok_link_types = ['https://m.tiktok.com', 'https://vt.tiktok.com', 'https://tiktok.com', 'https://www.tiktok.com', 'https://vm.tiktok.com']
del_text = []

# ParseMode Type For All Messages
_ParseMode = ParseMode.MARKDOWN

# just add the logger if you need to collect logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start_handler(update, context):
    update.message.reply_text('Hey! I am TikTok downloader Bot. I am here to help you send video in video format ✌️\nAdd me in your Telegram group and share any video from TikTok.\nMore details: /help', parse_mode=_ParseMode)


def about_handler(update, context):
    update.message.reply_text('Just send any video to me from TikTok, I will generate this video to watch it in Telegram', parse_mode=_ParseMode)


def devs_handler(update, context):
    update.message.reply_text('`dev` : @d1versy', parse_mode=_ParseMode)


def help_handler(update, context):
    update.message.reply_text('BOT Commands : /start , /about , /devs\n"Availables D1 bots:\nhttps://t.me/D1VideoBot\nhttps://t.me/D1GptBot\nhttps://t.me/D1TikTokBot"', parse_mode=_ParseMode)


# Download Task
def Download_Video(Link, update, context):
    message = update.message
    status_msg = message.reply_text('🚀 Downloading ....')

    # Getting Download Links
    try:
        path = f'./videos/result_{message.from_user.id}_{randint(0, 10000)}.mp4'
        tiktok_downloader.Mdown(Link)[0].download(path)
        print(f'Downloading Videos from {message.from_user}')
        with open(path, 'rb') as file:
            f = file.read()
        print('Uploading Videos')
        status_msg.edit_text('🚀 Uploading....')
        caption_text = f'sent by : @{message.from_user.username}'
        message.reply_video(video=f, supports_streaming=True, caption=caption_text, parse_mode=_ParseMode)
        os.remove(path)
    except Exception as ex:
        print(f'Download Links Generate Error !!!!!!!!!!!!!!!!!!!!!! {ex}')
        status_msg.edit_text(f'⁉️{ex} \nkeep calm and waiting for maintenance')
        return

    # Deleting Status Messages
    status_msg.delete()
    message.delete(message.message_id)


# delete not allowed message + delete user from the group
def del_not_allowed_text(none, update, context):
    message = update.message
    try:
        message.delete(message.message_id)
        message.bot.kick_chat_member(message.chat.id, message.from_user.id)
    except Exception as ex:
        message.reply_text(f'{ex} @{message.from_user.username}')
        print(ex)
        return


def incoming_message_action(update, context):
    message = update.message
    if any(word in str(message.text) for word in tikTok_link_types):
        context.dispatcher.run_async(Download_Video, str(message.text), update, context)
    elif any(word in str(message.text) for word in del_text):
        context.dispatcher.run_async(del_not_allowed_text, str(message.text), update, context)


def main() -> None:
    """Run the bot."""

    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    # Commands Listning
    dispatcher.add_handler(CommandHandler('start', start_handler, run_async=True))
    dispatcher.add_handler(CommandHandler('about', about_handler, run_async=True))
    dispatcher.add_handler(CommandHandler('devs', devs_handler, run_async=True))
    dispatcher.add_handler(CommandHandler('help', help_handler, run_async=True))

    # Message Incoming Action
    dispatcher.add_handler(MessageHandler(Filters.text, incoming_message_action,run_async=True))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
