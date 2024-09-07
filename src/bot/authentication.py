from telegram import Update

async def authenticate(update: Update):
    user = update.message.from_user
    with open('./validusernames.txt', 'r') as file:
        usernames = file.read().split(',')

    if user.username in usernames:
        return True
    return False