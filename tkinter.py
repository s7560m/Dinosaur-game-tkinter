# this means that you're importing everything from tkinter library
from tkinter import *

# imports keyboard module to check for key events
import keyboard

# create a pop-up box
root = Tk()

# create canvas
canvas = Canvas(root, width=1000, height=500, bg="white")
canvas.pack()

# draw on canvas
# x1, y1, x2, y2
#canvas.create_line(20,20, 200,400, fill="black")

# draw rectangle => canvas.create_rectangle(x0, y0, x1, y1, fill="black")

# dinosaur

# head
#canvas.create_rectangle(13, 20, 40, 60, fill="black", outline="")

# nose
#canvas.create_rectangle(40, 20, 70, 45, fill="black", outline="")

# mouth
#canvas.create_rectangle(40, 53, 65, 60, fill="black", outline="")

# body
#canvas.create_rectangle(13, 60, 35, 90, fill="black", outline="")

# created dino class with offset properties so we can place it wherever we want on the canvas, with its initial drawing properties intact
class Dino:
    def __init__(self, offset_X, offset_Y):
        self.offset_X = offset_X
        self.offset_Y = offset_Y

        '''
        The dinosaur is going to have multiple states. These states represent a
        state of animation. The animation could be the dinosaur idling (not moving),
        it could be the dinosaur running and his legs are moving really really fast (alternating).
        It could also be jumping, which means he's going to be going up and down, maybe with gravity.
        '''

        # possible animation states -> "idle", "run", "jump"
        self.animation_state = "idle"

        '''
         position variable -> going to manage the positions of the legs
        "init" position is where both legs are on the ground
        "left" position is where the left leg is extended, but the right leg is shortened
        "right" position is where the right leg is shortened and the left leg is extended
        '''
        self.position = "init"

        '''
        Jump variables
        1. initial jump speed (constant -> this is how fast the dinosaur is going to propel off the ground initially)
        2. variable jump speed (variable -> changes because of gravity)
        3. gravity (constant -> variable jump speed is going to decrease by the gravity amount)
        '''

        self.init_jump_speed = 15 # constant
        self.var_jump_speed = self.init_jump_speed # variable
        self.gravity = 1 # constant 
        
        
    # top left ->  bottom right
    def __drawRectangleOffset(self, x0, y0, x1, y1, color):
        canvas.create_rectangle(self.offset_X + x0, self.offset_Y + y0, self.offset_X +  x1, self.offset_Y + y1, fill=color, outline="")

    def draw(self):
        # head
        self.__drawRectangleOffset(13, 20, 40, 60, "black")

        # nose
        self.__drawRectangleOffset(40, 20, 70, 45, "black")

        # mouth
        self.__drawRectangleOffset(40, 53, 65, 60, "black")

        # neck
        self.__drawRectangleOffset(13, 60, 35, 90, "black")

        # body
        self.__drawRectangleOffset(-15, 70, 30, 105, "black")

        # legs and feet are drawn based on positions
        if (self.position == "init"):
            self.__drawRectangleOffset(-15, 105, -5, 115, "black")
            self.__drawRectangleOffset(20, 105, 30, 115, "black")
            self.__drawRectangleOffset(-15, 115, 0, 120, "black")
            self.__drawRectangleOffset(20, 115, 35, 120, "black")

        elif (self.position == "left"):
            self.__drawRectangleOffset(-15, 105, -5, 110, "black")
            self.__drawRectangleOffset(20, 105, 30, 115, "black")
            self.__drawRectangleOffset(-15, 110, 0, 115, "black")
            self.__drawRectangleOffset(20, 115, 35, 120, "black")

        elif (self.position == "right"):
            self.__drawRectangleOffset(-15, 105, -5, 115, "black")
            self.__drawRectangleOffset(20, 105, 30, 110, "black")
            self.__drawRectangleOffset(-15, 115, 0, 120, "black")
            self.__drawRectangleOffset(20, 110, 35, 115, "black")

        # arms
        arm_offset_x = -5
        self.__drawRectangleOffset(arm_offset_x + 35, 85, arm_offset_x + 45, 90, "black")
        self.__drawRectangleOffset(arm_offset_x + 40, 90, arm_offset_x + 45, 95, "black")

        # eyes
        # TWO THINGS: 1. we had to make __drawRectangleOffset support custom colors
        #             2. make the eyes using our custom function
        eye_offset_x = 3
        eye_offset_y = 3
        size = 3
        self.__drawRectangleOffset(13 + eye_offset_x, 20 + eye_offset_y, 16 + eye_offset_x + size, 23 + eye_offset_y + size, "white")

    # when our animation_state is jump, it's going to call this function
    def jump(self):
        
        # we start at the initial speed, but we want to end at that same speed, but in the downwards direction
        if (self.var_jump_speed >= -1 * self.init_jump_speed):

            # print(self.offset_Y)

            # adjust the offset_Y to shift the dinosaur up based on the var_jump_speed
            self.offset_Y -= self.var_jump_speed

            # "decelerate" the speed of the dinsoaur in the y direction to simulate gravity
            self.var_jump_speed -= self.gravity

        # when the dinsoaur has fallen to ground
        else:

            # reset variable jump speed to the initial jump speed
            self.var_jump_speed = self.init_jump_speed

            # reset the state from jump back to run
            self.animation_state = "run"
            
    # get the key events for the dinosaur
    def getKeyEvents(self):
        if (keyboard.is_pressed("space")):

            # this is when we're starting the game. The dinsoaur is in idle, but when we press state he starts running
            if (self.animation_state == "idle"):
                self.animation_state = "run"

            elif (self.animation_state == "run"):   
                self.animation_state = "jump"
    
    # animate the dinosaur    
    def animate(self):
        self.draw()

        # check which state the dinosaur is in, and animate accordingly
        if (self.animation_state == "idle"):
            self.position = "init"
        elif (self.animation_state == "run"):

            # toggling through the left and right positions
            if (self.position == "init"):
                self.position = "left"
            elif (self.position == "left"):
                self.position = "right"
            elif (self.position == "right"):
                self.position = "left"

        elif (self.animation_state == "jump"):
           # print("we're jumping!")
           self.jump()

    # Coordinates that determine collision detection
    def getCoordinates(self):
        return [self.offset_X, self.offset_Y]

class Cactus:
    # initialize cactus with its x and y positions
    # __init__() initializes the Cactus object. This is called a constructor
    def __init__(self, offset_X, offset_Y):
        self.offset_X = offset_X
        self.offset_Y = offset_Y

    # top left ->  bottom right
    def __drawRectangleOffset(self, x0, y0, x1, y1, color):
        canvas.create_rectangle(self.offset_X + x0, self.offset_Y + y0, self.offset_X +  x1, self.offset_Y + y1, fill=color, outline="")

    # draw the cactus, and offset it based on the offset_X and offset_Y properties
    def drawVariantOne(self):

        # base (trunk) of the cactus
        self.__drawRectangleOffset(0, 40, 10, 120, "green")

        # first spike on left side of cactus
        self.__drawRectangleOffset(-10, 60, 0, 80, "green")

        # second spike on right side of cactus
        self.__drawRectangleOffset(10, 60, 20, 80, "green")

    def drawVariantTwo(self):
        # base (trunk) of the cactus
        self.__drawRectangleOffset(0, 40, 10, 120, "green")

        # first spike on left side of cactus
        self.__drawRectangleOffset(-10, 80, 0, 100, "green")

        # second spike on right side of cactus
        self.__drawRectangleOffset(10, 80, 20, 100, "green")

    # Coordinates that determine collision detection
    def getCoordinates(self):
        return [self.offset_X, self.offset_Y]

    def move(self, speed):
        self.offset_X -= speed
            

class Game:
    def __init__(self, framerate):
        self.framerate = framerate

        self.dino = Dino(100, 300)
        self.cactus1 = Cactus(180, 300)
        self.cactus2 = Cactus(600, 300)

    '''
    getHitbox function which will determine whether the dinosaur collided
    with the cacti based on their coordinates

    '''
    
    # run the game
    def run(self):
        # get key events of the dinosaur
        self.dino.getKeyEvents()
        
        # clear the canvas, and redraw the dinosaur
        canvas.delete("all")

        # animate the dinosaur, and draw the cactus
        self.dino.animate()
        self.cactus1.drawVariantOne() # TODO: change this to cactus.animate() when we implement the animation for the cactus
        self.cactus2.drawVariantTwo()

        # animate both of the cacti
        # self.cactus1.move(10)
        # self.cactus2.move(10)

        # get the dinosaur to respond to the cacti hitboxes
        print("Dino hitbox" + str(self.dino.getHitbox()))
        # print("Cactus 1 hitbox" + str(self.cactus1.getHitbox()))

        # loop the animate function with a delay to create a specified framerate
        root.after(self.framerate, self.run)

game = Game(50)
game.run()
        
