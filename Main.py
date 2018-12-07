'''
Created on Nov 8, 2018

@author: josephbaca
'''
import re

secret_Word_Length = -1
correctGuesses = 0
incorrectGuesses =0
characterExistsInPositions =[]
ignoreLetters = []
secretWord = []

def load_words():
    # With taking all the information from the dictionary it is important to remove 
    # all punctuation and anything that is not a character to have cleaner game execution.
    with open('words.txt') as word_file:
        dictionary = list(word_file.read().split())
        filteredDictionary = set()
        
        for word in dictionary:
            word = word.lower()
            word = re.sub('[^a-z]+', '', word)
            filteredDictionary.add(word)

    return dictionary


def filterWordLength(dictionary, length ):
    
    filteredDictionary = set()
    
    for word in dictionary:
        if len(word) == length:
            filteredDictionary.add(word)
            
    print("Now let me guess a letter... Hmmm")
    print()
        
    return filteredDictionary

def filterByCharacter(dictionarySet, character):
    
    filteredSet =set()
        
    for word in dictionarySet:
        if character not in word:
            filteredSet.add(word)
    
    #print("Line 51", filteredSet)
    return filteredSet

def filterByPositions(dictionarySet, character, positions):
    
    filteredSet = set()
    
    for word in dictionarySet:
        for i in range(len(positions)):
            if word[positions[i]] != character:
                break
            if i == len(positions)-1 and word[positions[i]] == character:
                #print("This is the word being added to the filteredSet:", word)
                filteredSet.add(word)
                
    return filteredSet

    
def openingStatement(wordLength):
    global secretWord
    
    secretWord = ['_'] * wordLength
    
    for i in range(len(secretWord)):
        print(secretWord[i], end = " ")
    print()
    print()

def printSecretWord():
    
    global secretWord
    for i in range(len(secretWord)):
        print(secretWord[i], end = " ")
    
def GetmostCommonLetters(filteredDictionary):
    
    # This function is quite interesting. What's happening is that its counting all the letters
    # of all the words in the dictionary and sorting them by how frequent they appear.
    # that way the computer can guess the most common letter that exist in all the words.
    # This is for a more accurate guess and not randomized.
    
    
    letters_and_freqeuncy ={}
    
    for word in filteredDictionary:
        for letter in word:
            if letter in letters_and_freqeuncy:
                letters_and_freqeuncy[letter] += 1
            else:
                letters_and_freqeuncy[letter] = 1
                
    # sorts the actual Dict{} object
    letters_and_freqeuncy = sorted(letters_and_freqeuncy.items(), key = lambda t: t[1], reverse =True)
    
    #Debugging
    #print("Line 105 in code", letters_and_freqeuncy)
    print()
    
    return letters_and_freqeuncy
    
    
def getNextCommonLetter(letters):
    
    try:
        if len(letters) != 1:
            index = letters[0]
            del letters[0]
        
        return index[0]
    
    except:
        defeat()



def playGame(dictionarySet, character):
    
    global characterExistsInPositions
    global ignoreLetters
    global secret_Word_Length
    global correctGuesses 
    global secretWord
    global incorrectGuesses
    #print(dictionarySet)
    

    print("Does your word have the letter |", character, "| DOES IT ????? I BET IT DOES!!")
    print("Answer can either be (y/n)")
        
    yes_or_no = input()
    

    #when the game hasn't ended yet and guessed character is incorrect
    if yes_or_no == "n":
        incorrectGuesses +=1
        
        print("----------")
        displayPicture(incorrectGuesses)
        print("----------")
        
        print("Ohh okay... so were going to be lying today is that what's going on? Well then...")
        
        filteredSet = filterByCharacter(dictionarySet, character)
        
        # You have 6 tries to win the game, if not: Hangman!
        if incorrectGuesses == 6:
            defeat()
            return
        
        if len(filteredSet) == 1:
            finalWord = ""
            for word in filteredSet:
                finalWord = word
            victory(finalWord)
            return
        
        #If we no longer have Words in the DictionarySet after filtering then computer loses.
        if len(filteredSet) == 0:
            defeat()
            return
        
        letters = guessNextFrequentLetterAndIgnore(filteredSet, ignoreLetters)
        
        #The computer had somehow guessed all the letters and is still wrong...Hello?
        #In this case the game ends with a defeat, but something must have gone wrong.
        #On the user end or the dictionary ran out of words 
        if letters == {}:
            defeat()
            return
        
        character = getNextCommonLetter(letters)
        playGame(filteredSet, character)
        
        
        
    #when the game is going to continue and the character guessed is correct.
    elif yes_or_no == "y":
        
        correctGuesses+=1
        #The computer keeps track of how many correct guesses it has.
        #If That Number = length of the secret Word, then computer wins.
        if correctGuesses == secret_Word_Length:
            finalWord = ""
            for char in secretWord:    
                if char == '_':
                    char = character
                finalWord += char
            victory(finalWord)
            return
        
        
        
        notDone = True
        ignoreLetters.append(character)
        # This While makes sure if it guessed a letter Correctly 
        # it puts that letter in its designated positions 
        # In any case where the letter correctly guessed has multiple 
        # positions.
        print("In what indice(s) does your character exist? ")
        print("Enter one at a time or type 'done' when you are done.")
        print("Example:    0|1|2|3    O: '1' enter, '2', enter, 'done'")
        print("            C|O|O|L   ")
        
        while notDone:
            
            position = input()
            
            try:
                if position == "done":
                    notDone = False
                elif int(position) >= secret_Word_Length or int(position) < 0:
                    print("Ohh that number's out of bounds! Lets try again")
                else:
                    #So the computer has an understanding of where the users correct letters are
                    characterExistsInPositions.append(int(position))
            except:
                print("I Think you made a mistake somewhere, Lets try again.")
                continue 
               
                
        #This just lets the user understand where we are at in terms of  ' _ _ _ _ '
        for num in characterExistsInPositions:
            secretWord[num] = character
        print()
        printSecretWord()
        print()
        print()
        
        
        #Filters the words in the dictionary depending on where the positions of the letters lay
        filteredSet = filterByPositions(dictionarySet, character, characterExistsInPositions)
        
        #If one more word in the set after filtering
        if len(filteredSet) == 1:
            victory(filteredSet)
            return
        
        #gets most frequent letter while ignoring previous letters
        letters = guessNextFrequentLetterAndIgnore(filteredSet, ignoreLetters)
        
        #In the case where the computer Somehow ran out of letters to guess
        if letters == None:
            defeat()
            return
        
        #Clearing the positions on which a specific character laid
        characterExistsInPositions=[]
        
        #gets most common letter and removes it from the dictionary of letters
        character = getNextCommonLetter(letters)
        
        #continues the game recursively while guessing a new character
        playGame(filteredSet, character)
        
        
        
def guessNextFrequentLetterAndIgnore(filteredSet, ignoreList):
    
    dictio = {}
    for word in filteredSet:
        for i in range(len(word)):
            
            if word[i] in ignoreList:
                continue
            
            elif word[i] in dictio:
                dictio[word[i]] +=1
                
            else:
                dictio[word[i]] = 1
                
    dictio = sorted(dictio.items(), key = lambda t: t[1], reverse = True)    
        
    return dictio
    
def guessNextFreqeuentLetter(dictionarySet):
    
    mostFrequentLetters = GetmostCommonLetters(dictionarySet)
    guessLetter = getNextCommonLetter(mostFrequentLetters)
    playGame(dictionarySet, guessLetter)
    
    
    
def victory(finalWord):

    print("is your word: ", *finalWord, "(y/n) ?")
    inp = input()
    
    if inp == 'y':
        print("Alrighty! Thanks for playing! ")
    else:
        defeat()
    
def defeat():
    
    print("Well it looks like You beat me!")
    print("Great game hope you play again soon!")
        
def displayPicture(incorrectGuesses):
    
    if incorrectGuesses == 1:
        print("_____     ")
        print("|    |    ")
        print("|    O    ")
        print("|         ")
        print("|         ")
    if incorrectGuesses == 2:
        print("_____     ")
        print("|    |    ")
        print("|    O    ")
        print("|    |    ")
        print("|         ")
    if incorrectGuesses == 3:
        print("_____     ")
        print("|    |    ")
        print("|    O    ")
        print("|   -|    ")
        print("|         ")
    if incorrectGuesses == 4:
        print("_____     ")
        print("|    |    ")
        print("|    O    ")
        print("|   -|-   ")
        print("|         ")
    if incorrectGuesses == 5:
        print("_____     ")
        print("|    |    ")
        print("|    O    ")
        print("|   -|-   ")
        print("|   /     ")
    if incorrectGuesses == 6:
        print("_____     ")
        print("|    |    ")
        print("|    O    ")
        print("|   -|-   ")
        print("|   / \   ")


def main():
    global secret_Word_Length
    
    dictionary = load_words()
    
    print("Hey! Lets play a game of hang man :) ")
    secret_Word_Length = int(input("How long is your word? Example: car = 3 : ")) #ask the user for his word and opens a statement example: _ _ _ _ _
    openingStatement(secret_Word_Length)
    
    
    dictionarySet = filterWordLength(dictionary, secret_Word_Length) #filters the length of the words
    mostFrequentLetters = GetmostCommonLetters(dictionary)
    guessLetter = getNextCommonLetter(mostFrequentLetters)
    
    playGame(dictionarySet, guessLetter) #This actually plays the game and guesses the letter
    

main()



