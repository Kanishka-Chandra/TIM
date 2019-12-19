from multiprocessing import Process
import pyautogui as auto
import pyttsx3
import speech_recognition as sr
from nltk.tokenize import word_tokenize


engine = pyttsx3.init()
screenWidthMax, screenHeightMax = auto.size()

action = ""

#Function to make the system to speek
#speaks audio passed as argument
def talkToMe(audio):
    engine.say(audio)
    engine.runAndWait()
    print(audio)


#Greating the user
def start():
    talkToMe('Hello Sir! \n All systems have started \n I am online sir and I am ready for your command!')
    ConfigureSpeechRecognition()

#Configuring speech recognition
def ConfigureSpeechRecognition():
    speechRecognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speechRecognizer.pause_threshold = 1
        speechRecognizer.adjust_for_ambient_noise(source, duration=1)


#listens for users command
def userCommand():

    with sr.Microphone() as source:
        audio = speechRecognizer.listen(source)

    try:
        command = speechRecognizer.recognize_google(audio).lower()
        print("You said: " + command + "\n")
        talkToMe(command)

    except sr.UnknownValueError:
        print("Your last command couldn\'t be heard")
        talkToMe("Your last command couldn\'t be heard")
        #loop back to continue to listen for commands if unrecognizable speech is received
        command = userCommand()

    return command


def check():

    while True:

        action = userCommand()


process = Process(target=check)


def move(X, Y):

    while True:

        mousePositionX, mousePositionY = auto.position()
        auto.moveRel(X, Y)

        if "stop" in action:
            print("limit")
            process.terminate()
            X = 0
            Y = 0
            return
        if mousePositionX == screenWidthMax or mousePositionX == 0:
            print("limit")
            process.terminate()
            return
        if mousePositionY == screenHeightMax or mousePositionY == 0:
            print("limit")
            process.terminate()
            return


def assistant(command):
    """if statements for executing commands"""

    if "move" in command:

        moveX = 0
        moveY = 0

        if "right" in command:
            moveX = 1
        if "left" in command:
            moveX = -1
        if ("up" or "top") in command:
            moveY = -1
        if "down" in command:
            moveY = 1
        if "upright" in command:
            moveX = 1
            moveY = -1

        process.start()
        move(X=moveX, Y=moveY)

    elif "click" in command:

        if "double click" in command:
            auto.doubleClick()
        elif "triple click" in command:
            auto.tripleClick()
        elif "right click" in command:
            auto.rightClick()
        elif ("middle click" or "center click") in command:
            auto.middleClick()
        else:
            auto.click()

    elif "press" in command:

        press = 0
        if "right" in command:
            auto.mouseDown(button='right')
            press = 3
        elif ("middle" or "center") in command:
            auto.mouseDown(button='middle')
            press = 2
        elif "left" in command:
            auto.mouseDown(button='left')
            press = 1
        else:
            button = word_tokenize(command)
            button.pop(0)
            auto.hotkey(button)

        if press > 0:

            process.start()

            if "release" in action:

                if press == 1:
                    auto.mouseUp(button='left')
                if press == 3:
                    auto.mouseUp(button='right')
                if press == 2:
                    auto.mouseUp(button='middle')
            process.terminate()

    elif ("drag" or "pick") in command:
        process.start()
        auto.mouseDown(button='left')
        if "move" in (command or action):
            process.terminate()
            moveX = 0
            moveY = 0

            if "right" in command:
                moveX = 1
            if "left" in command:
                moveX = -1
            if ("up" or "top") in command:
                moveY = -1
            if "down" in command:
                moveY = 1
            if "upright" in command:
                moveX = 1
                moveY = -1

            process.start()
            move(X=moveX, Y=moveY)

    elif "drop" in command:
        auto.mouseUp(button="left")

#Execution starts here
#loop to continue executing multiple commands

if __name__ == "__main__":
    start()

    while True:
        command = userCommand()
        assistant(command)
