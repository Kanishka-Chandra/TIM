import pyautogui as auto
from threading import Thread

screenWidthMax, screenHeightMax = auto.size()
action = ""


def talkToMe(audio):
    """speaks audio passed as argument"""

    print(audio)


def myCommand():
    """listens for commands"""

    command = input("Enter command")
    return command

def check():
    global action
    action = input("Enter command")



def move(X, Y):

    i = 1
    while True:
        global action

        posX, posY = auto.position()

        if "stop" in action:
            print("limit")
            break
        if posX == screenWidthMax:
            print("limit")
            break
        if posX == 0:
            print("limit")
            break
        if posY == screenHeightMax:
            print("limit")
            break
        if posY == 0:
            print("limit")
            break

        auto.moveRel(20 * X, 20 * Y, 0.5)


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

        move(X=moveX, Y=moveY)



# loop to continue executing multiple commands
if __name__ == "__main__":
    while True:
        assistant(myCommand())
