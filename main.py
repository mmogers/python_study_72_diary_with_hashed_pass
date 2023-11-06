from replit import db
import os
import time
import datetime
import pytz
import getpass
import random

rigaTZ = pytz.timezone("Europe/Riga")
LIMIT = 1 
#-------------------------------------------------
def myInputPrint(text):  #prints input text with green clolor
  result = input(f"""{text} \033[32m""")
  print("\033[0m", end="")
  return result
#--------------------------------------------------
def addEntry():
  entry = myInputPrint("\nEnter your update:\n> ").capitalize()
  timestamp = datetime.datetime.now(rigaTZ)
  db[timestamp] = entry
#---------------------------------------------------
def viewEntry():
  keys = list(db.prefix("2023")) #the list of all keys  - entries
  keys.sort(reverse=True) #sort in reverse order
  limitCounter = 0  #how much to show at once counter
  counter = 0 #printed tweets counter
  while True:
      entryList = []
      startIndex = limitCounter * LIMIT
      endIndex = (limitCounter + 1) * LIMIT

      for key in keys[startIndex:endIndex]:
        entryList.append({key: db[key]}) #key value pairs

      if not entryList:
          print("\nNo entries to display.")
          break

      for entry in entryList:
          entryKey = list(entry.keys())[0]
          print(f"{entryKey}: {entry[entryKey]}")
          counter += 1
          time.sleep(1)
      time.sleep(3)

      if counter < len(keys): #show next entry (amount to show - LIMIT)
        answer = myInputPrint(f"\nDo you want to see the next {LIMIT} entry? (y/n)\n> ").lower()
        if answer == "y":
          limitCounter += 1
        else:
            break
      else:
        print("\nNo more entries to display.")
        time.sleep(3)
        break
#---------------------------------------------------
def printMenu(user):  

  while True:
    os.system("clear")
    print(f"\033[1;32mWelcome to your secret diary, {user}!\033[0m")
    choice = int(myInputPrint("\nPress 1 to Add a new entry\nPress 2 to View a recent entry\n> ")) #check integer
    if choice == 1:
      addEntry()
      print("Added!")
      time.sleep(2)
    elif choice == 2:
      viewEntry()
      time.sleep(2)
    else:
      print("Invalid choice")
      time.sleep(2)
      continue
#----------------------------------------------------
def logIn(db):
  print("\033[1;32m\nLog in\033[0m")
  username = myInputPrint("Username: ")
  if username not in db:
    print("\nNo such username!\n")
    return 0
  password = myInputPrint("Password: ")
  salt = db[username]["salt"] 
  newPassword = f"{password} {salt}"
  newPassword = hash(newPassword)
  if newPassword == db[username]["password"]:
    print(f"\nHello {username}, welcome back!\n")
    return username
  else:
    print("\nIncorrect password\n")
    return 0
#---------------------------------------------------
def addNewUser(db):
  print("\033[1;32m\nAdd new user\033[0m\n")
  username = myInputPrint("Username: ")
  password = myInputPrint("Password: ")
  salt = random.randint(1000, 9999)
  newPassword = f"{password} {salt}"
  newPassword = hash(newPassword)
  db[username] = {"password": newPassword, "salt": salt}
  print("\nUser Added\n")
  time.sleep(1)
  return username
#-------------------------START--------------------

keys = db.keys()
print(keys)

if len(keys) == 0:
  user = addNewUser(db)
  printMenu(user)
else:
  user = logIn(db)
  if user:
    printMenu(user)
  
#----------------------END--------------------------





