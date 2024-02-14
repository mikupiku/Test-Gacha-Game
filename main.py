#general idea of this game: This game is practically 2 games in one. This is a mental math game where you do simple math problems and earn a currency called crystals. This game also features an extra rng mechanic used to try and exchange for rewards (gacha).

import random # for generaeting rates
import time #to add animation/latency for when the player does their summoning
import json #to turn a .json file into a python dictionary. A .json file contains a permanent dictionary that can save even after the python script closes (which is why we didn't define the inside the script.)  
from prettytable import PrettyTable # to make organized and neat tables to display information. (A UI I guess)

print('This game is a math "gacha" game (no p2w aspect). You are asked to do math questions (either an easy or hard question). After completing the math question correctly, you will be rewarded with a set amount of crystals (a currency).You will be awarded more crystals based on the diffulty of the math question. Crystals will be used to obtain gemstones. You will make a single summon using your crystals and you will be given gemstones that you will need to collect. Gemstones are ordered by rarity. When you have collected all the gemstones, the game will end and you win. You need 160 crystals to do 1 summon.                                To begin playing, type "Help". Pls Enjoy :)') # tells the player what to do. Essentially a Quickstart guide.

#here, I am going to start by coding the gacha aspect of the game. The mental math can be found at the bottom of the page as it links with the system. 
pity_distribution = [
  21.392, 21.863, 22.332, 22.799, 23.263, 23.724, 24.181, 24.637, 25.09, 25.538, 25.985, 26.43, 26.872, 27.748, 28.182, 28.612, 29.04, 29.446, 29.889, 30.309, 30.727, 31.143, 31.556, 31.966, 32.374, 32.78, 33.20, 33.89, 34.23, 35,97, 36.78, 37.57,38.23, 39.01, 60.343, 70.897, 80.326, 86.701, 91.007, 93.921, 95.891, 97.223, 98.124, 98.732, 99.143, 99.421, 99.608, 99.734, 100] # this is to calculate the rates/percentages that the player pulls a rare item. The chance that they get a mythical item is in between the rates. 

mythical = ['Mythical Gemstone I', 'Mythical Gemstone II', 'Mythical Gemstone III', 'Mythical Gemstone IV']
superrare = ['Superrare Gemstone I', 'Superrare Gemstone II', 'Epic Gemstone III', 'Epic Gemstone IV']
rare = ['Rare Gemstone I', 'Rare Gemstone II', 'Rare Gemstone III', 'Rare Gemstone IV']

#here, I am creating lists for each rarity of gemstone. Inside the list are the items obtainable from that specific rarity. 

with open('./data.json') as f: # opens the json file into a variable called f
  data = json.load(f)  # uses the json librarby to turn the file into a python dictionary called "data"


# extracts values from data dictionary and turns them into variables
pity = data['mythicalpity'] # get the "mythicalpity" value from the data dictionary (originally from .json file) and assign it to a variabe called pity
superrarepity = data['superrarepity']
crystal = data['crystals']
gemstones = data['gemstones']
nextpity = data['nextpity']

fourbase = 12 # base rate/percentage/chance of getting a "superrare" gemstone

def write(field, value): # define a function to make changing the json file easier
# eg. if field is "crystals" and value is 160, it will change crystals to 160
  data[field] = value # first, change the dictionary in python by assigning value to field
  with open('./data.json', 'w') as f: # open the .json file in writing mode (so we can edit it)
    json.dump(data, f, indent=4) # "dump" the changed python dictionary into the .json file (with 4 indent so it's easier to read)

def get_nextpity(): # define a function that generates the next pity where a mythical gemstone will be summoned
  global nextpity # make nextpity a global variable so that it will be the same inside and outside the function
  x = random.uniform(21.392,100) # generates a random number between the first number and last number in the pity distribution
  for index, i in enumerate(pity_distribution): # go through all numbers in pity distribution (index is the position of the number in the list, i is the actual number)
    if x < i: # if the random number is greater than the number its currently checking, then index + 1 is the pity
      nextpity = index + 1 # assign pity to next pity
      write('nextpity', nextpity) #write nextpity to json file
      return
if nextpity is None: # generate nextpity if one doesnt exist
  get_nextpity() 

print('Type "HELP" to see commands')

def summon(number): # define a function to summon gemstones. ake these vairables global so that they will be the sae inside and oustide 
  global pity 
  global crystal
  global superrarepity # make a list of obtained gestones (currently empty)
  obtained = []

  if crystal < 160 * number: # if there are not enough crystals to do the aount of summons then it tells the player to play more ( do ore oath)
    print('Insufficent amount of crystals. Type "play" to get more crystals.')

  else:
    crystal -= 160 * number # subtract cost of crystals for summoning and change json file (updates the save)
    write('crystals', crystal)
    for i in range(number): # repeat the next part the nuber of times you summon
      if pity == nextpity: # if nextpity is reached (mythical gemstone pity)
        wins = True # wins a mythical gemstone
        pity = 1 # reset pity to 1
        get_nextpity() #make new pity
      else:
        wins = False # the player doesn't win a mythical
          
      if wins:
        rarest = ['Mythical Gemstone I', 'Mythical Gemstone II', 'Mythical Gemstone III', 'Mythical Gemstone IV']
        # choose random from mythical list and add it to the obtained list
        won = random.choice(rarest)
        obtained.append(won)

      else: # if does not win a mythical
        pity += 1 # add 1 to pity
        if superrarepity == 10: # see if a superrare is guaranteed (10 pity is guaranteed)
          wins = True #wins a superrare
          get_nextpity()
        else: 
          wins = fourbase > random.uniform(0,100)
        if wins:
          superrarepity = 1 #resets superrare pity to 1
          rarestsr = ['Superrare Gemstone I', 'Superrare Gemstone II', 'Superrare Gemstone III', 'Superrare Gemstone IV']
          won = random.choice(rarestsr)
          obtained.append(won)
        else: # if does not win a superrare or mythical
          superrarepity += 1 #adds 1 to superrarepity
          # choose random rare gemstone and add it to the obtained list (bottom)
          rarestr = ['Rare Gemstone I', 'Rare Gemstone II', 'Rare Gemstone III', 'Rare Gemstone IV']
          sad = random.choice(rare)
          obtained.append(sad) 
          #puts new pities into json file
      write('mythicalpity', pity)
      write('superarepity', superrarepity)
      return obtained # return the final list of obtained gemstones

while True: # starts an infinite loop of asking for input
  command = input().lower() # gets user input and convers it to all lowercase
  if command in ['summon']: # if the user input is "summon" (they did the sumon command)
    summoned = summon (1) # summon 1 tie
    if summoned is not None: # if they got something (if they didnt it eans they didn't have enough crystals)
      msg = f'Summoning...'
      print(f'{msg} /', end='') # starts a spinnign cursor to build suspsense (it's a cool animation)
      cycle = ['-', '\\', '|', '/'] # a list of all the stages of the spinning cursor
      for i in range(20): # repeat the following 20 times:
        time.sleep(0.25) # pause for 0.25 seconds
        i = i % 4 # get the index of the current stage of the cycle (because it is only length 4)
        print(f'\r{msg} {cycle[i]}', end='') # override the current line with the updated stage of the cycle (\r brings the cursor back to the beginning fo the line)
      print(f'\r{msg}') # remove the spinning cursor 
      i = 1 # start a counter for display reasons
      for item in summoned: # go through all the summoned gemstones
        time.sleep(1.5) # waits 1.5 seconds (to build more suspense)
          
        if item not in gemstones: # this means they do not already have the gemstone
          print(f'{i}: {item}') # this prints the sumoned gemstone along with the counter
          gemstones.append(item) # this adds the sumoned gemstone to all the gemstones (in total)
          write('gemstones', gemstones) # this is so it can save to the .json file

          hasall = True # start checking if the user has all the gemstones
          for gem in rare:
            if gem not in gemstones:
              hasall = False
              break # goes through all the superrare gemstones. If the user has one of them, hasall is false.
            if hasall:
              for gem in superrare:
                if gem not in gemstones:
                  hasall = False
                  break
                # if they still have all, repeat the same thing with mythical gemstones (below)
            if hasall:
              for gem in mythical:
                if gem not in gemstones:
                  hasall = False
                  break
              # this is if they have all the gemstones, the game should end.
            if hasall:
              print('Congradutions! You collected all the gemstones! The game has been beaten!')
              quit()

        else:
          # if they already have the gemstone
          print(f'{i}: {item} (Duplicate)') # say its a duplicate but dont add to gemstones

        i += 1 # increase i by one everytime a summon is over.

  elif command == 'inv': # if the user input is "inv" (they dif the inv command)
    table = PrettyTable() # start a prettytable
    table.add_row(['Crystals', crystal]) # add crystal to the table
    table = '\n'.join(str(table).splitlines()[2:])
    print(table) # format the table to remove the first two rows of the string (because it looks not good)
  
  elif command == 'pity': # if the user input is "pity", which means they did the pity command
    table = PrettyTable() #starts a prettytable
    table.add_row(['Mythical pity', pity - 1]) # add mythical and superarepity to the table
    table.add_row(['Superrare pity', superrarepity - 1])
    table = '\n'.join(str(table).splitlines()[2:]) # akes the table neater
    # 1. str(table).splitines() turns the table into a list of ines. the first two ines are what we want to remove
    #2. [2:] keeps everything after the first two lines (first two elements of the list)
    #3. '\n\.join() is the opposite of splitlines (it reconnects the list back into a string). \n is a newline so it puts each line of the table onto a new line (exactly how it started)
    print(table)
  
  elif command == 'help': # if they did the help command
    table = PrettyTable() # make a prettytable # add commands and descriptions
    table.add_row(['play', 'Increases your crystals by doing math problems'])
    table.add_row(['inv', 'Shows your currency'])
    table.add_row(['pity', 'Shows your pity'])
    table.add_row(['gemstones', 'Shows your gemstones'])
    table.add_row(['summon', 'Does 1 summon'])
    table = '\n'.join(str(table).splitlines()[2:]) # reforats, akes it less ugly
    print(table) # print the table

  elif command == 'gemstones': # if they did the gemstones command, show gemstones.
    table = PrettyTable()
    table.field_names = ['Your Gemstones:'] # add "your gemstones" as a title for the column (this was what we removed before)
    if len(gemstones) == 0: # if they have no gemstones, then say so
      print('You have no gemstones.') 
    else: # if the player has ore than 0 gestones
      for gem in gemstones: # go through all their gemstones
        table.add_row([gem]) # add each to the table
      table = '\n'.join(str(table).splitlines()[2:]) # make less ugly
      print(table) #prints

# here is the mental math (part of the) game.
  elif command == 'play':
    diff = input('Choose a difficuty (Easy/Hard): ')
    if diff.lower() == 'easy': #asks the user if they want an easy or hard question.
      a = random.randint(1, 9) #generates a random integer
      b = random.randint(1, 9) #twice
      s = a + b #sum question, the computer does the math first
      add = random.choice([True, False]) # 50% of the time, add is True, if it's not add, then subtract
      if add:
        ans = input(f'{a} + {b} = ') # the f-string allows the user's answer using input(). It lets you use curly brackets. 
        right = str(s) #right = right answer. The s is what the computer did. 
      else:
        right = str(b) #this is for subtract. Correct answer is b
        ans = input(f'{s} - {a} = ')
      if ans == right:
        crystal += 10 #awards the player with crystals that is stored in the .json file
        write('crystals', crystal) # to store in .json file
        print('Correct! You earned 10 crystals. Type "play" to earn more.')
      else:
        print('That is Incorrect...Please type "play" to run the command again.')
    elif diff.lower() == 'hard' :
      a = random.randint(1, 9) # this is the same thing just with multiplication and division
      b = random.randint(1, 9)
      p = a * b
      multiply = random.choice([True, False])
      if multiply:
        ans = input(f'{a} x {b} = ')
        right = str(p)
      else:
        right = str(b)
        ans = input(f'{p} / {a} = ')
      if ans == right:
        crystal += 50
        write('crystals', crystal)
        print('Correct! You earned 50 crystals. Type "play" to earn more.')
      else:
        print('That is Incorrect...Please type "play" to run the command again.')
    else: 
      print('You did not choose a difficulty') # if the player did not type "easy" or "hard"