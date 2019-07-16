from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, Updater, Filters
from atm_finder import ATM_finder
from urllib.request import urlopen
from os import environ

updater = Updater(token=environ["ATM_BOT_TOKEN"])
dispatcher = updater.dispatcher
atm_finder = ATM_finder()

def start(bot, update):
  update.message.reply_text("Use /link or /banelco to request near atms")

def link(bot, update):
  location_keyboard = KeyboardButton(text="Send location", request_location=True)
  reply_keyboard = [[location_keyboard]]
  reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
  update.message.reply_text("I need your location in order to find link atms", reply_markup=reply_markup)

def banelco(bot, update):
  location_keyboard = KeyboardButton(text="Send location", request_location=True)
  reply_keyboard = [[location_keyboard]]
  reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
  update.message.reply_text("I need your location in order to find banelco atms", reply_markup=reply_markup)

def build_map_url(user_location, atms):
  for atm in atms:
    print(atm)
  url = "https://maps.googleapis.com/maps/api/staticmap?zoom=15&size=600x300&markers=color:blue%7Clabel:%7C{0},{1}".format(user_location[0], user_location[1])
  additional_dots = "" 
  for atm in atms:
    additional_dots = additional_dots + "&markers=color:red%7Clabel:%7C{0},{1}".format(atm.lat, atm.long)
  key = "&key=" + environ["ATM_GOOGLE_MAPS_TOKEN"]
  url = url + additional_dots + key
  print(url)
  return url

def location(bot, update):
  location = (update.message.location.latitude, update.message.location.longitude)
  atms = []
  message_text = update.message.reply_to_message.text
  if "link" in message_text:
    atms = atm_finder.find_atms(location, "LINK")
  elif "banelco" in message_text:
    atms = atm_finder.find_atms(location, "BANELCO")
  if len(atms) == 0:
    update.message.reply_text("There are no atms near with available money")
    return    
  response = ""
  for atm in atms:
    response = response + "Bank: " + str(atm.bank) + ", Location: " + str(atm.location) + "\n"
  response = response
  update.message.reply_text(response)
  print(atms)
  locations_map = build_map_url(location, atms)
  bot.send_photo(chat_id=update.message.chat_id, photo=locations_map)

start_handler = CommandHandler('START', start)
link_handler = CommandHandler('LINK', link)
banelco_handler = CommandHandler('BANELCO', banelco)
location_handler = MessageHandler(Filters.location, location)

dispatcher.add_handler(link_handler)
dispatcher.add_handler(banelco_handler)
dispatcher.add_handler(location_handler)

updater.start_polling()