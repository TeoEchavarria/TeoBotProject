from telegram import Update
import os

async def authenticate(update: Update):
    user = update.message.from_user
    usernames = os.getenv("USER_ACCESS").split(',')

    if user.username in usernames:
        return True
    return False