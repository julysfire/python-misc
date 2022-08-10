import PIL
import pyautogui
import keyboard
import pygetwindow
from pytesseract import pytesseract
import pathlib

fullPath = pathlib.Path(__file__).parent.resolve()
charsFromText = []

#Get dictionary of words
f = open('scrabble.txt')
adict = f.read().split('\n')
f.close()
print("Dictionary loaded and ready.")


def getAllLetters():
    # Get game
    if len(pygetwindow.getWindowsWithTitle("Letter Quest Remastered")) == 0:  #Change this for the non-remastered version
        print("Game not running")
        return False
    else:
        game = pygetwindow.getWindowsWithTitle("Letter Quest Remastered")[0] #Change this for the non-remastered version

        # Get screenshot and crop
        p = pyautogui.screenshot()
        p.save(fullPath + "\\p.png")

        im = PIL.Image.open(fullPath + '\\p.png')
        im_crop = im.crop((game.left + 475, game.top + 510, game.right - 475, game.bottom - 16))
        im_crop.save(fullPath + '\\p.png', quality=100)
        return True

def getIndividualLetters():
    counter = 0

    #Full parameters for where to crop the picture to get each letter
    croppingParams = [[16, 2, 66, 58], [97, 2, 157, 58], [181, 2, 239, 58], [273, 2, 322, 58], [358, 2, 406, 58],
                      [16, 97, 66, 155], [97, 97, 157, 155], [181, 97, 239, 155], [273, 97, 320, 155], [358, 97, 406, 155],
                      [16, 193, 66, 249], [97, 193, 157, 249], [181, 193, 239, 249], [273, 193, 320, 249], [358, 193, 406, 249]]

    #Crop each letter
    for i in croppingParams:
        im = PIL.Image.open(fullPath + 'p.png')
        im_crop = im.crop((i[0], i[1], i[2], i[3]))

        #Save letter, increment counter as to not overwrite
        #NOTE: Might be able to move the OCR portion over here, would not need to save an image and would just use im_crop as the image to give to tesseract
        im_crop.save(fullPath + str(counter) + '.png', quality=100)
        counter += 1

def getListOfLetters():
    charsFromText.clear()

    path_to_tess = 'D:\\Programming\\Tesseract\\tesseract.exe'  #Point to your tesseract.exe location

    for i in range(0, 15):
        path_to_img = fullPath + str(i) + ".png"

        #Run tesseract to get the text
        pytesseract.tesseract_cmd = path_to_tess
        img = PIL.Image.open(path_to_img)
        text = pytesseract.image_to_string(img, lang='eng', config='--psm 7')

        #Help to OCR out
        if text[0] == "0":
            text = "O"
        elif text[0] == "5":
            text = "S"
        elif text[0] == "|":
            text = "I"
        elif text[0] == "-":
            text = "F"

        charsFromText.append(text[0].upper())

def scrabbleSolver():
    scoreTable = {"A": 1, "C": 3, "B": 3, "E": 1, "D": 2, "G": 2, "F": 4, "I": 1, "H": 4,
                  "K": 5, "J": 8, "M": 3, "L": 1, "O": 1, "N": 1, "Q": 10, "P": 3,
                  "S": 1, "R": 1, "U": 1, "T": 1, "W": 4, "V": 4, "Y": 4, "X": 8, "Z": 10}

    def score_word(w):
        return sum([scoreTable[c] for c in w])

    def can_form(lets, w):
        return all(w.count(c) <= lets.count(c) for c in w)

    charsFromText.sort()
    letters = ''.join(charsFromText)

    #Get words and scores
    words = [word for word in adict if can_form(letters, word)]
    words_scores = [(score_word(word), word) for word in words]

    for i in range(15, 2, -1):
        counter = 0
        outputString = ""

        print(str(i) + " Letter Words\n")
        for j in words_scores:
            if len(j[1]) == i:
                outputString = outputString + j[1] + " - " + str(j[0]) + "  "
                counter += 1
            if counter == 16:
                print(outputString)
                outputString = ""
                counter = 0
        print(outputString+"\n")


#Main
while True:
    try:
        if keyboard.is_pressed('F2'):
            if getAllLetters():
                print("Got screenshot of all letters")

                getIndividualLetters()
                print("Got screenshots of individual letters.")

                getListOfLetters()
                print("Got array of letters.")
                print(' '.join(charsFromText))

                scrabbleSolver()

        if keyboard.is_pressed('F3'):
            print("Program exiting...")
            break

        #Debugging
        if keyboard.is_pressed('F4'):
            getAllLetters()
            print("Got screenshot of all letters")
        if keyboard.is_pressed('F5'):
            getIndividualLetters()
            print("Got screenshots of individual letters.")
        if keyboard.is_pressed('F6'):
            getListOfLetters()
            print(" ".join(charsFromText))
            print("Got array of letters.")
        if keyboard.is_pressed('F7'):
            getListOfLetters()
            scrabbleSolver()
        if keyboard.is_pressed('F8'):
            charsFromText = ['U', 'A', 'F', 'E', 'E', 'T', 'O', 'S', 'E', 'A', 'Q', 'A', 'I', 'P', 'H']
            scrabbleSolver()
    except Exception as e:
        print("Exception: " + str(e))
        break
