import telegram, praw
import configparser
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import random

# Use configparser to read the ini files and fetch the credentials to access TG and reddit
cf_parser = configparser.ConfigParser()

# The objects that the telegram bot needs to work
# Telegram bot name: Reddit_pictures_bot
cf_parser.read('telegram.ini')
bot_token = cf_parser['CREDENTIALS']['bot_token']
updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher

# Read the reddit credentials from the .ini file
cf_parser.read('reddit.ini')

# Create an instance of reddit (connect to account)
reddit = praw.Reddit(client_id=cf_parser['CREDENTIALS']['client_id'],
                     client_secret=cf_parser['CREDENTIALS']['client_secret'],
                     username=cf_parser['CREDENTIALS']['username'],
                     password=cf_parser['CREDENTIALS']['password'],
                     user_agent=cf_parser['CREDENTIALS']['user_agent'])

# Minimum amount of upvotes by default to download an image
cf_parser.read('config.ini')
MINUPS = int(cf_parser['REDDIT_FILTERS']['min_ups'])


# ------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------
# Function that returns a list of urls for the pictures on a given sub (max = quantity)
# min_ups stands for the minimum amount of upvotes that a post needs to be valid.
def GetUrlsList(quantity, sub, min_ups=MINUPS):
    hot_generator = reddit.subreddit(sub).hot()
    counter = 0
    urls_list = []
    for post in hot_generator:
        if counter < quantity and post.url != None and post.ups > min_ups and not post.stickied:
            urls_list.append(post.url)
            counter += 1
        elif counter >= quantity:
            break  # break the for loop and stop adding urls
    print("Got total amount of {} urls.".format(len(urls_list)))
    print("")
    return urls_list


def SendPhotos(update, context, the_urls):
    for url in the_urls:
        try:
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=url)
        except:
            print("Exception, could not sent url: {}".format(url))


def Send_Rand_Photos(update, context, the_urls):
    for url in the_urls:
        rand = random.choice(url)
        try:
            context.bot.send_photo(chat_id=update.effective_chat.id, photo= rand)
        except:
            print("Exception, could not sent url: {}".format(rand))

# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------
# /start directly displays the GUI.
def start(update, context):
    print("Received start command from chat_id: {}".format(update.effective_chat.id))
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sending menu. Select:")

dispatcher.add_handler(CommandHandler("start", start))


def send(update, context):
    chat_id = update.effective_chat.id
    print("Received request to send images from {} in chat {}".format(context.args[0], chat_id))
    # quantity = int(context.args[1])
    #quantity = int(1)
    # The subreddit is the first parameter of the command (n_ 0)
    sub = context.args[0]
    quantity = 2
    Send_Rand_Photos(update, context, GetUrlsList(quantity, sub))

dispatcher.add_handler(CommandHandler("send", send))



def agebeauty(update, context):
    chat_id = update.effective_chat.id
    print("Received request to send images f rom {} in chat {}".format(context.args[0], chat_id))
    # quantity = int(context.args[1])
    #quantity = int(1)
    # The subreddit is the first parameter of the command (n_ 0)
    sub = context.args[0]
    quantity = 1
    Send_Rand_Photos(update, context, GetUrlsList(quantity, sub))

dispatcher.add_handler(CommandHandler("agebeauty", agebeauty))


# def advSend(update, context):
#     try:
#         print("User using the advanced mode (chat ID {})".format(update.effective_chat.id))
#         sub = context.args[0]
#         amount = int(1)
#         min_ups = int(0)
#         print("\tRequested {} images from {} with min_ups {}.".format(amount, sub, min_ups))
#         SendPhotos(update, context, GetUrlsList(amount, sub, min_ups=min_ups))
#     except:
#         print("Advanced mode went wrong.")
#         context.bot.send_message(chat_id=update.effective_chat.id, text="Incorrect parameters.")
#
#
# dispatcher.add_handler(CommandHandler("advsend", advSend))



# adding direct commands to get subreddit
def bigdickgirl(update, context):
    chat_id = update.effective_chat.id
    print("Received request to send images from {} in chat {}".format(context.args[0], chat_id))
    sub = int(context.args[0])
    quanlity = 1
    Send_Rand_Photos(update, context, GetUrlsList(quanlity, sub))


dispatcher.add_handler(CommandHandler("bigdickgirl", bigdickgirl))



# def OnButtonPress(update, context):
#
#     query = update.callback_query
#
#     if query.data == "other":
#         # Redirect user to command /send <subreddit> <amount>
#         other_explanation = """
#     		-----------------
#     		Use /send <subreddit> <amount> to receive the <amount> top imagesfrom <subreddit>.\n
#     		By default this filters out everything under {} upvotes, use advanced mode to change this.
#     		-----------------
#     		""".format(MINUPS)
#         context.bot.send_message(chat_id=update.effective_chat.id, text=other_explanation)
#     else:
#         try:
#             suggested_sub = str(query.data.split()[0])
#             chosen_amount = int(query.data.split()[1])
#             print("Sending: \n\tSub = {} \n\tamount = {}".format(suggested_sub, chosen_amount))
#             print("\t(Chat ID = {})".format(update.effective_chat.id))
#             minUps = int(cf_parser['REDDIT_FILTERS']['min_ups'])
#             SendPhotos(update, context, GetUrlsList(chosen_amount, suggested_sub, min_ups=minUps))
#         except:
#             print("Exception!")
#             print("Couldn't do anything with callback data. Callback data: {}".format(query.data))
#             print("")
#
#
# dispatcher.add_handler(CallbackQueryHandler(OnButtonPress))

# Start the bot ----------------------------------------------------------------------------------
print("Bot starting to poll")
updater.start_polling()
print("")