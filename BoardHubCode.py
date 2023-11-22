from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

# Standard MicroPython modules
from usys import stdin, stdout
from uselect import poll

# Initialize the hub.
hub = PrimeHub()

hub.light.on(Color(h=20, s=140, v=80))

presser = ForceSensor(Port.C)
spinner = ColorSensor(Port.B)
reader = ColorSensor(Port.A)

Color.BLACK = Color(h=0, s=0, v=0)
Color.PURPLE = Color(h=272, s=75, v=54)
Color.ORANGE = Color(h=30, s=100, v=100)

my_colors = (Color.GREEN, Color.ORANGE, Color.YELLOW, Color.PURPLE, Color.BLUE, Color.RED, Color.BLACK, Color.NONE)

spinner.detectable_colors(my_colors)

firstStage = False
secondStage = False
thirdStage = False

stageStarted = True

cardRead = False
spinComplete = False

card = reader.color()


# Optional: Register stdin for polling. This allows
# you to wait for incoming data without blocking.
keyboard = poll()
keyboard.register(stdin)

hub.light.on(Color.RED)

#print("Running...")

while True:
    
    # Optional: Check available input.
    #while not keyboard.poll(0):

        # Optional: Do something here.
        pressed = hub.buttons.pressed()

        hub.display.text("Hi",500)

        message = stdin.buffer.read(15)
        #hub.display.text(message,500)

        if message == b"video1_finished":
            # Go through all the colors.
            for hue in range(360):
                hub.light.on(Color(hue))
                wait(10)

        if message == b"video2_finished":
            hub.light.on(Color.GREEN)
            firstStage = True
            stageStarted = True
        
            while firstStage == True:
                if stageStarted == True:
                    #print("Stage 1 Iniated")
                    stageStarted = False
                if presser.pressed(force=3):
                    #print("Code Entered")
                    stdout.buffer.write(b"Play_Video_3")
                    hub.light.on(Color.RED)
                    firstStage = False

        if message == b"video3_finished":
            hub.light.on(Color.GREEN)
            secondStage = True
            stageStarted = True
        
            if secondStage == True:
                if stageStarted == True:
                    #print("Stage 2 Iniated")
                    stageStarted = False
                spinStarted = False
                spinFinished = False
                colourCheck = 0

                while not spinStarted:
                    currentColour = spinner.color()
                    wait(500)
                    prevColour = currentColour
                    currentColour = spinner.color()
                    #print("StartSpin Check: Prev " + str(prevColour) + " Cur" + str(currentColour))

                    if prevColour != currentColour:
                        spinStarted = True
                        #print("Spin Started")
                        
                        
                        while colourCheck < 4:
                            currentColour = spinner.color()
                            wait(250)
                            prevColour = currentColour
                            currentColour = spinner.color()
                            #print("FinishSpin Check: Prev " + str(prevColour) + " Cur" + str(currentColour))

                            if prevColour == currentColour:
                                colourCheck = colourCheck + 1
                                #print(colourCheck)
                            if prevColour != currentColour:
                                colourCheck = 0
            
                #print("Spin Finished")
                #print(currentColour)

                rolledNumber = 4
                if currentColour == Color.BLACK:
                    rolledNumber = 1
                elif currentColour == Color.PURPLE:
                    rolledNumber = 2
                elif currentColour == Color.GREEN:
                    rolledNumber = 3
                elif currentColour == Color.RED:
                    rolledNumber = 4
                elif currentColour == Color.BLUE:
                    rolledNumber = 5

                #print("You Spun a " + str(rolledNumber) + "!")
                spinComplete = True
                hub.display.text(str(rolledNumber),2000)
                secondStage = False

                thirdStage = True
                stageStarted = True
    
                while thirdStage == True:
                    if stageStarted == True:
                        #print("Stage 3 Iniated")
                        stageStarted = False
                        hub.light.on(Color.YELLOW)
                    if card == Color.RED:
                        stdout.buffer.write(b"Play_Video_4")
                        hub.light.on(Color.RED)
                        thirdStage = False           