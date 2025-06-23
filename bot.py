from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler,MessageHandler, filters,ContextTypes
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")

BOT_USERNAME:Final='@rickmango_bot'



#commands
async def start_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('burp Wubba Lubba Dub-Dub! 🛸 ' \
    'Welcome to the only bot inthe multiverse that actually knows what it’s doing.' \
    ' I’m Rick—yes, that Rick—and I’ll be your generator of the passwords.Please type in the word password or' \
    'use the tag /password_generator to generate password, genius.' 
    'If you need something, use /help')

async def help_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Ughhh, alright, fine.' \
    ' You need help? Of course you do, you are not exactly Einstein, are ya?' \
    ' To contact me:username:@vimbasic for any issues' \
    'Coming soon......')

async def custom_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    quotes = [
    "School's not a place for smart people, Morty.",
    "Sometimes science is more art than science.",
    "Fun fact: In one dimension, you're smart. This isn't that dimension.",
    "You're young, you have your whole life ahead of you, and your anal cavity is still taut yet malleable."
]
    await update.message.reply_text(random.choice(quotes))

async def password_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Default length is 12, but user can specify: /password 16 no_symbols
    try:
        args = context.args
        length = int(args[0]) if args else 12
        use_symbols = not ('no_symbols' in args)
    except:
        await update.message.reply_text("Ughh, use it right, Morty! Try: /password 16 no_symbols")
        return

    password = generate_password(length=length, use_symbols=use_symbols)
    await update.message.reply_text(f"🧬 Here’s your password, genius: `{password}`", parse_mode='Markdown')


#function to generate the password


import random
import string


def generate_password(length=12, use_symbols=True):
    characters = string.ascii_letters + string.digits
    if use_symbols:
        characters += string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))



#Handling responses
def handle_responses(text:str)-> str:
     processed:str=text.lower()
     
     
     if 'hello' in processed:
         return 'hey there,my man'
     

     if 'password' in processed:
        return f" Here is your password, genius: `{generate_password()}`"
     

     return 'i dont understand what you wrote.....'

async def handle_message(update:Update,context:ContextTypes.DEFAULT_TYPE):
    message_type:str=update.message.chat.type
    text:str=update.message.text

    print(f'User ({update.message.chat.id}) in {message_type} "{text}')


    if message_type=='group':
        if BOT_USERNAME in text:
            new_text:str=text.replace(BOT_USERNAME, '').strip()
            response:str=handle_responses(new_text)
        else:
            return
    else:
        response: str=handle_responses(text)
        print('Bot:',response)
        await update.message.reply_text(response)



async def error(update:Update,context:ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')






if __name__=='__main__':
    print('Starting bot......')
    app=Application.builder().token(TOKEN).build()


    #Commands
    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('help',help_command))
    app.add_handler(CommandHandler('custom',custom_command))


    #Messages
    app.add_handler(MessageHandler(filters.TEXT,handle_message))


    #Errors
    app.add_error_handler(error)



    #Polls the bot
    print('Polling....')
    app.run_polling(poll_interval=5)


    #Password command
    app.add_handler(CommandHandler('password', password_command))
