from multiprocessing import Process
import pyautogui as auto
import pyttsx3
import speech_recognition as sr
from nltk.tokenize import word_tokenize


screenWidthMax, screenHeightMax = auto.size()
action = ""

engine = pyttsx3.init()
count = 0
# Dummy function marks the starting of the program


def start():

    engine.say('Hello Sir!')
    engine.say('installing all drivers')
    engine.say('Starting all system applications')
    engine.say('Drivers installed')
    engine.say('All systems have started')
    engine.say('I am online sir \n and')


if count == 0:

    start()
    global count
    count += 1


def talkToMe(audio):

    #speaks audio passed as argument

    engine.say(audio)
    engine.runAndWait()
    print(audio)


def myCommand():

    #listens for commands

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Ready...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).lower()
        print("Yo   u said: " + command + "\n")
        engine.say(command)
        engine.runAndWait()

    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print("Your last command couldn\'t be heard")
        engine.say("Your last command couldn\'t be heard")
        engine.runAndWait()
        command = myCommand()

    return command


def check():
    global action

    while True:

        action = myCommand()


process = Process(target=check)


def move(X, Y):

    while True:

        posX, posY = auto.position()
        auto.moveRel(X, Y)
        global action

        if "stop" in action:
            print("limit")
            process.terminate()
            return
        if posX == screenWidthMax or posX == 0:
            print("limit")
            process.terminate()
            return
        if posY == screenHeightMax or posY == 0:
            print("limit")
            process.terminate()
            return


def assistant(command):
    """if statements for executing commands"""

    global action

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


talkToMe('I am ready for your command')

#loop to continue executing multiple commands
if __name__ == "__main__":
    while True:
        assistant(myCommand())
