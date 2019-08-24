from threading import Thread
import pyautogui as auto
import pyttsx3
import speech_recognition as sr


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
    count+=1
    
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
        print("You said: " + command + "\n")
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
    action = myCommand()


def move(X,Y):

    i = 1
    while i > 0:
        posX, posY = auto.position()
        auto.moveRel(X, Y)
        global action
        if "stop" in action:
            print("limit")
            i = 0
        if posX == screenWidthMax:
            print("limit")
            i = 0
        if posX == 0:
            print("limit")
            i = 0
        if posY == screenHeightMax:
            print("limit")
            i = 0
        if posY == 0:
            print("limit")
            i = 0

def assistant(command):
    """if statements for executing commands"""


    if "move" in command:

        moveX = 0
        moveY = 0
        
        Thread(target=check).start()

        if "right" in command:
            moveX = 1
        if "left" in command:
            moveX = -1
        if "up" in command:
            moveY = -1
        if "down" in command:
            moveY = 1

        move(X = moveX, Y =moveY)


talkToMe('I am ready for your command')

#loop to continue executing multiple commands
while True:
    assistant(myCommand())
