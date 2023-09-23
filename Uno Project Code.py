import random
from termcolor import colored
import time

#Class card is a new class created to store card objects, which contain a color (Red, Green, Blue, or Yellow) and a number (any integer between 0-9 or a +2) or contain a Wild card (Wild Card or Wild +4)
class card:
  def __init__(self, color, number):
    self.color = color
    self.number = number

  def getColor(self):
    return str(self.color)

  def getNumber(self):
    return self.number

  def __repr__(self):
    return card()

  def __str__(self):
    return ("{} {}".format(self.color, self.number))

#The different colors of the cards in Uno
colors = ["Red", "Green", "Blue", "Yellow"]

#The differentCards function creates card objects with the colors from the list 'colors' and appends them to the list represented by the parameter 'list'
#It creates different types of cards based on probability: regular cards are the most probable, then +2 cards, then Wild cards
def differentCards(list, numberOfTimes):
  for count in range(numberOfTimes):
    color = ""
    if random.random() < 0.26:
      color = "Red"
    elif random.random() > 0.25 and random.random() < 0.51:
      color = "Green"
    elif random.random() > 0.50 and random.random() < 0.76:
      color = "Blue"
    elif random.random() > 0.75:
      color = "Yellow"
    else:
      color = random.choice(colors)
    if random.random() < 0.61:
      list.append(card(color, random.randint(0,9)))
    elif random.random() > 0.60 and random.random() < 0.76 :
      list.append(card(color, "+2"))
    elif random.random() > 0.75 and random.random() < 0.87:
      list.append(card("Wild", "Card"))
    elif random.random() > 0.86:
      list.append(card("Wild", "+4"))
    else:
      list.append(card(color, random.randint(0,9)))

#The moveCards function takes all cards of the same type as the parameter 'type' and moves them to the bottom of the list represented by the parameter 'list'
def moveCards(type, list):
  count = 0
  for i in list:
    if str(i.getNumber()) == type:
      count = count + 1
      list.remove(i)
  for count in range(count):
    new = card("Wild", type)
    list.append(new)

#The computer's hand of cards is created
computerHand = []
differentCards(computerHand, 7)
moveCards("Card", computerHand)
moveCards("+4", computerHand)

#The user's hand of cards is created
userHand = []
differentCards(userHand, 7)
moveCards("Card", userHand)
moveCards("+4", userHand)

#The foundIn function returns a boolean value depending on whether the parameter 'element' is found in the parameter 'list'
#It returns true if the element is found in the list, and false otherwise
def foundIn(element, list):
  if element != "Draw":
    if isinstance(element, str):
      element = card(element.split()[0], element.split()[1].capitalize())
    for i in list:
      if i.getColor() == element.getColor() and str(i.getNumber()) == element.getNumber():
        return True
  return False

#The removeCard function removes a card object with the same color as the parameter 'color' and the same number as the parameter 'number' from the parameter 'list'
def removeCard(color, number, list):
  for i in list:
    if i.getColor() == color and str(i.getNumber()) == str(number):
      list.remove(i)
      break
  
#The removeWildCard function removes a Wild card of the same type as the parameter 'type' from the parameter 'list'
def removeWildCard(type, list):
  for i in list:
    if str(i.getNumber()) == type:
      list.remove(i)
      break

#The dividingLine function prints a line across the program to improve readability and divide the text
def dividingLine(upperLine, lowerLine):
  if upperLine:
    print("")
  line = ""
  for count in range(80):
    line = line + "-"
  print(line)
  if lowerLine:
    print("")

#The game function runs the game
def game():
  #The most recently played card is printed in color and set to the variable playedCard
  print("Last played card:")
  playedCard = card(random.choice(colors), random.randint(0,9))
  print(colored(playedCard.getColor(), playedCard.getColor().lower()) + " " + str(playedCard.getNumber()) + "\n")

  #The checkIfComputerCanPlay function examines the computer's hand of cards and determines whether or not they can play in response to the most recently played card
  #It returns true if the computer has an available card they can play, and false if they do not
  def checkIfComputerCanPlay(color, number):
    for i in computerHand:
      if i.getColor() == color or str(i.getNumber()) == str(number):
        return True
      if str(i) == "Wild Card" or str(i) == "Wild +4":
        return True
    return False

  #The computerDraw function draws cards to add to the computer's hand
  #Each time the function is called, the computer draws one card
  def computerDraw():
    differentCards(computerHand, 1)
    for count in range(2):
      moveCards("Card", computerHand)
      moveCards("+4", computerHand)
    print("Your opponent draws a card. They now have " + str(computerHand.__len__()) + " cards.")
    dividingLine(True, True)

  #The computerMultipleDraw function draws either two or four cards into the computer's hand depending on the most recently played card (a +2 or a Wild +4)
  def computerMultipleDraw(Play, numberOfTimes):
    differentCards(computerHand, numberOfTimes)
    moveCards("Card", computerHand)
    moveCards("+4", computerHand)
    dividingLine(True, False)
    if numberOfTimes == 2:
      removeCard(Play.getColor(), "+2", userHand)
      playedCard = card(Play.getColor(), "+2")
      print("\nYour opponent draws two cards. They now have " + str(computerHand.__len__()) + " cards.")
      return playedCard
    if numberOfTimes == 4:
      removeWildCard("+4", userHand)
      playedCard = card("Wild", "+4")
      print("\nYour opponent draws four cards. They now have " + str(computerHand.__len__()) + " cards.")
      return playedCard
  
  #The computerMove function has the computer play a card using several other functions to check if they can play and to draw cards to the computer's hand if they cannot
  #While the computer cannot play a card, they draw
  #When they draw a card they can play, it is played and the program prints out a message accordingly
  def computerMove(playedCard, play):
    while not checkIfComputerCanPlay(playedCard.getColor(), playedCard.getNumber()):
      time.sleep(0.5)
      computerDraw()
      checkIfComputerCanPlay(playedCard.getColor(),playedCard.getNumber())
    time.sleep(0.5)
    computerCard = 0
    for i in computerHand:
      if i.getColor() == playedCard.getColor() or str(i.getNumber()) == str(playedCard.getNumber()):
        computerCard = card(i.getColor(), str(i.getNumber()))
        removeCard(i.getColor(), i.getNumber(), computerHand)
        playedCard = card(computerCard.getColor(), computerCard.getNumber())
        if computerHand.__len__() != 1 and computerCard.getColor() != "Wild":
          print("The computer plays a " + colored(computerCard.getColor(), computerCard.getColor().lower()) + " " + str(computerCard.getNumber()) + ". They now have " + str(computerHand.__len__()) + " cards.\n")
        elif computerCard.getColor() != "Wild":
          print("The computer plays a " + colored(computerCard.getColor(), computerCard.getColor().lower()) + " " + str(computerCard.getNumber()) + ". They now have only 1 card. " + colored('Uno!', 'magenta') + "\n")
        if computerCard.getNumber() == "+2":
          dividingLine(False, False)
          if computerHand.__len__() == 0:
            break
          playedCard = userMultipleDraw(2, computerPlay, playedCard, play)
          play = str(playedCard)
        else:
          dividingLine(False, True)
        return playedCard
      if computerHand[0].getColor() != "Wild":
        numberOfWilds = 0
        for i in computerHand:
          if i.getColor() == "Wild":
            numberOfWilds = numberOfWilds + 1
        color = computerHand[random.randint(0, computerHand.__len__() - numberOfWilds - 1)].getColor()
      else:
        color = random.choice(colors)
      if str(i) == "Wild Card":
        playedCard = card(color, -1)
        print("The computer plays a Wild Card and they set the color to " + colored(color.lower(), color.lower()) + ". You can only put down " + colored(color.lower(), color.lower()) + " cards until it is changed again.\n")
        dividingLine(False, True)
        removeWildCard("Card", computerHand)
        return playedCard
      if str(i) == "Wild +4":
        playedCard = card(color, -1)
        print("The computer plays a Wild +4 and they set the color to " + colored(color.lower(), color.lower()) + ". You can only put down " + colored(color.lower(), color.lower()) + " cards until it is changed again.\n")
        dividingLine(False, True)
        removeWildCard("+4", computerHand)
        playedCard = userMultipleDraw(4, computerPlay, playedCard, play)
        play = str(playedCard)
        return playedCard

  #The cannotPlay function prints a warning to the user if they try to play a card they do not have in their hand, then prompts them to enter a different card
  def cannotPlay(Play, playedCard):
    play = ""
    while (not foundIn(Play, userHand)) and str(computerPlay.getNumber()) != "+2" and str(computerPlay.getNumber()) != "+4":
      print("\nThat card is not in your hand.")
      play = input("Pick a card from your hand.\n")
      play = play.capitalize()
      if play == "Draw Card" or play == "Draw card" or play == "Draw":
        return play
      Play = card(play.split()[0].capitalize(), play.split()[1].capitalize())
    return Play

  #The wrongColorOrNumber function prints a warning to the user if they try to play a card that is in their hand but is not compatible with the most recently played card, then prompts them to enter a different card
  def wrongColorOrNumber(playedCard, Play):
    play = ""
    while foundIn(Play, userHand) and (Play.getColor() != playedCard.getColor() and Play.getNumber() != str(playedCard.getNumber())):
      if play == "Draw Card" or play == "Draw card" or play == "Draw" or Play == "Draw Card" or Play == "Draw card" or Play == "Draw":
        return play
      if play == "Wild Card" or play == "Wild card" or play == "Wild +4":
        return card(play.split()[0].capitalize(), play.split()[1].capitalize())
      print("\nYou cannot play that card. Your card must have the same color or number as the last played card.")
      play = input("Pick another card.\n")
      play = play.capitalize()
      if play == "Draw":
        return play
      Play = card(play.split()[0].capitalize(), play.split()[1].capitalize())
    return Play

  #The drawCard function draws cards to the user's hand until they are able to play a card, displays their hand and asks them whether they would like to play that card or keep drawing, and then responds accordingly
  #If the user responds that they would like to keep drawing, the drawCard function is called recursively to begin drawing again
  #The cannotPlay function is created within the drawCard function; it returns true if the user does not have any cards available to play, and returns false otherwise
  def drawCard(playedCard):
    drawnCards = []
    def cannotPlay(playedCard):
      for i in drawnCards:
        if i.getColor() == playedCard.getColor() or str(i.getNumber()) == str(playedCard.getNumber()) or str(i) == "Wild Card" or str(i) == "Wild +4":
          return False
      return True

    while cannotPlay(playedCard):
      time.sleep(0.5)
      differentCards(userHand, 1)
      drawnCards.append(userHand[-1])
      print("\nYour new card is a " + str(drawnCards[-1]) + ".")
    moveCards("Card", userHand)
    moveCards("+4", userHand)
    time.sleep(0.5)
    print("\n\nYour hand:")
    index = 0
    for count in range(int(userHand.__len__())):
      if userHand[index].getColor() == "Wild":
        print(colored(userHand[index].getColor(), 'magenta') + " " + str(userHand[index].getNumber()))
      else:
        print(colored(userHand[index].getColor(), userHand[index].getColor().lower()) + " " + str(userHand[index].getNumber()))
      index = index + 1
    dividingLine(True, True)
    if playedCard.getNumber() == -1:
      print("The current color is " + colored(playedCard.getColor(), playedCard.getColor().lower()) + ".")
    else:
      print("The current card is a " + colored(playedCard.getColor(), playedCard.getColor().lower()) + " " + str(playedCard.getNumber()) + ".")
    if drawnCards[-1].getColor() == "Wild":
      Play = input("\nYou can play the " + colored(str(drawnCards[-1]), 'magenta') + ". Would you like to play this card or would you like to keep drawing?\n")
    else:
      Play = input("\nYou can play the " + colored(drawnCards[-1].getColor(), drawnCards[-1].getColor().lower()) +  " " + str(drawnCards[-1].getNumber()) + ". Would you like to play this card or would you like to keep drawing?\n")
    while True:
      Play = Play.capitalize()
      if Play == "Yes" or Play == "Play" or Play == str(drawnCards[-1]) or Play == "Wild" or Play == "Wild Card" or Play == "Wild card":
        moveCards("Card", userHand)
        moveCards("+4", userHand)
        if drawnCards[-1].getNumber() == "+2":
          playedCard = computerMultipleDraw(drawnCards[-1], 2)
          return playedCard
        elif str(drawnCards[-1].getNumber()) == "Card":
          playedCard = playWildCard(drawnCards[-1])
          removeWildCard("Card", userHand)
          return playedCard
        elif str(drawnCards[-1].getNumber()) == "+4":
          playedCard = playWildCard(drawnCards[-1])
          removeWildCard("+4", userHand)
          return playedCard
        else:
          removeCard(drawnCards[-1].getColor(), drawnCards[-1].getNumber(), userHand)
          return drawnCards[-1]
      elif Play == "No" or Play == "Draw Card" or Play == "Draw card" or Play == "Draw" or Play == "Keep Drawing" or Play == "Keep drawing":
        return drawCard(playedCard)
      else:
        Play = input("Please enter a more clear answer.\n")

  #The userMultipleDraw function draws two or four cards to the user's hand depending on the most recently played card (a +2 or Wild +4)
  #It then displays the user's hand and prompts them to play a card in response
  def userMultipleDraw(numberOfTimes, computerPlay, playedCard, play):
    differentCards(userHand, numberOfTimes)
    if numberOfTimes == 2:
      print(("\nYour new cards are a " + str(userHand[-2]) + " and a " + str(userHand[-1]) + ".\n"))
    if numberOfTimes == 4:
      print("Your new cards are a " + str(userHand[-4]) + ", a " + str(userHand[-3]) + ", a " + str(userHand[-2]) + ", and a " + str(userHand[-1]) + ".\n")
    moveCards("Card", userHand)
    moveCards("+4", userHand)
    print("\nYour hand:")
    index = 0
    for count in range(int(userHand.__len__())):
      if userHand[index].getColor() == "Wild":
        print(colored(userHand[index].getColor(), 'magenta') + " " + str(userHand[index].getNumber()))
      else:
        print(colored(userHand[index].getColor(), userHand[index].getColor().lower()) + " " + str(userHand[index].getNumber()))
      index = index + 1
    play = input("\nWhat would you like to play? If you are unable to play a card, enter Draw Card.\n")
    play = play.capitalize()      
    if play == "Draw":
      playedCard = drawCard(playedCard)
      Play = str(playedCard)
      dividingLine(True, True)
      playedCard = computerMove(playedCard, play)
    while not " " in play and play != "Draw":    
      play = input("\nPlease input your answer as two words. If you are trying to play a Wild Card or a Wild +4, please enter the full name of the card. You may enter Draw if you would like to draw.\n")
      play = play.capitalize()
    if " " in play:
      Play = card(play.split()[0].capitalize(), play.split()[1].capitalize())
    playedCard = userMove(playedCard, play, Play)
    if userHand.__len__() != 0:
      dividingLine(True, True)
      playedCard = computerMove(playedCard, play)
    return playedCard

  #The userMove function has the user play a card using several other functions to check if they can play, verify their choice of card, and respond accordingly if they choose to draw
  #When the user puts a card down, it is removed from their hand using other functions
  def userMove(playedCard, play, Play):
    wildPlay = False
    for count in range(5):
      if foundIn(Play, userHand) and Play.getColor() == "Wild":
        playedCard = playWildCard(Play)
        wildPlay = True
        return playedCard
      if foundIn(Play, userHand) and (Play.getColor() == playedCard.getColor() or Play.getNumber() == str(playedCard.getNumber())):
        playedCard = card(Play.getColor(), Play.getNumber())
        if Play.getColor() == playedCard.getColor() and Play.getNumber() == "+2":
          playedCard = computerMultipleDraw(Play, 2)
        if Play.getNumber() != "+2":
          removeCard(Play.getColor(), Play.getNumber(), userHand)
        return playedCard
        
      for count in range(5):
        if foundIn(Play, userHand) and Play.getColor() != playedCard.getColor() and Play.getNumber() != str(playedCard.getNumber()) and Play.getColor() != "Wild" and wildPlay == False:
          Play = wrongColorOrNumber(playedCard, Play)
        if (not foundIn(Play, userHand)) and str(play) != "Draw Card" and str(play) != "Draw card" and str(play) != "Draw" and str(Play) != "Draw Card" and str(Play) != "Draw card" and str(Play) != "Draw" and wildPlay == False and str(computerPlay.getNumber()) != "+2" and str(computerPlay.getNumber()) != "+4":
          Play = cannotPlay(Play, playedCard)
        if str(play) == "Draw Card" or str(play) == "Draw card" or str(play) == "Draw" or str(Play) == "Draw Card" or str(Play) == "Draw card" or str(Play) == "Draw":
          playedCard = drawCard(playedCard)
          return playedCard
        
  #The playWildCard function asks the user to decide on a color when they choose to play a Wild card, then calls the appropriate function to make the computer respond accordingly (play in response to a Wild Card or draw and then play in response to a Wild +4)
  def playWildCard(play):
    color = input("What color would you like to make this card?\n")
    color = color.capitalize()
    while color != "Red" and color != "Green" and color != "Blue" and color != "Yellow":
      color = input("Please enter red, green, blue, or yellow.\n")
      color = color.capitalize()
    playedCard = card(color.capitalize(), -1)
    play = str(play)
    play = play.split()[0].capitalize() + " " + play.split()[1].capitalize()    
    if foundIn(play, userHand) and play == "Wild Card":
      print("\nThe color is now " + colored(color.lower(), color.lower()) + ". The computer must put down a card of this color.")
      removeWildCard("Card", userHand)
    if foundIn(play, userHand) and str(play) == "Wild +4":
      print("\nThe color is now " + colored(color.lower(), color.lower()) + ". The computer must draw four cards and put down a card of this color.")
      computerMultipleDraw(playedCard, 4)
    return playedCard

  global computerPlay
  computerPlay = card("Purple", -1)
  #While the user's hand and the computer's hand have more than zero cards, the user's hand will be displayed, the user will be prompted to play a card, and the computer will play a card in response
  while userHand.__len__() > 0 and computerHand.__len__() > 0:
    print("Your hand:")
    index = 0
    for count in range(int(userHand.__len__())):
      if userHand[index].getColor() == "Wild":
        print(colored(userHand[index].getColor(), 'magenta') + " " + str(userHand[index].getNumber()))
      else:
        print(colored(userHand[index].getColor(), userHand[index].getColor().lower()) + " " + str(userHand[index].getNumber()))
      index = index + 1
    if userHand.__len__() == 1:
      print("\n" + colored('Uno!', 'magenta'))

    play = input("\nWhat would you like to play? If you are unable to play a card, enter Draw Card.\n")
    play = play.capitalize()      
    if play == "Draw":
      playedCard = drawCard(playedCard)
      Play = str(playedCard)
      dividingLine(True, True)
      playedCard = computerMove(playedCard, play)
      continue
    while not " " in play and play != "Draw":    
      play = input("\nPlease input your answer as two words. If you are trying to play a Wild Card or a Wild +4, please enter the full name of the card. You may enter Draw if you would like to draw.\n")
      play = play.capitalize()
    if " " in play:
      Play = card(play.split()[0].capitalize(), play.split()[1].capitalize())
      
    playedCard = userMove(playedCard, play, Play)
    dividingLine(True, True)

    if userHand.__len__() != 0:
      playedCard = computerMove(playedCard, play)
      computerPlay = card(playedCard.getColor(), playedCard.getNumber())

  #The appropriate ending is printed depending on who reached zero cards in their hand first
  if userHand.__len__() == 0:
    print("\n" + colored('You won!', 'magenta'))
  else:
    print("\n" + colored('You lose.', 'magenta') + " The computer has gotten rid of all of their cards.")

game()