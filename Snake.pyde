"""
Snake.
by Antonia Calia-Bogan

https://github.com/Alfriadox/Snake

last updated 12-27-17:
    * Bugfixes
    * Comments
    * Code refactoring and reformating

    My implementation of the classic video game "Snake",
in python (version 3) using the processing development environment.

    The main purpose of this project is to showcase my programming 
experiences on my college applications through a programming portfolio.

    While I was brainstorming for this program, I considered using other
languages sucha as Java, JavaScript, and Rust, as well as not using the 
processing development environment.  I settled on python and processing
because my goal with this project is to show my ability to write code, 
and do not need the C-like performance or Memory safety of Rust, nor the 
versatility and "write once, run anywhere" abilities from Java or JS.
Python has more legibility than those other languages, so I chose it. 
I chose to use processing to avoid writing too many lines of glue code 
between the logic I want to showcase and someone elses' graphics API
(Application Programming Interface).

    This program shows mastery of all parts of programming, including
variables, functions, classes/objects, iteration, and conditionals. The 
accompanying video shows the program running and showcases some of the 
features. The programming paradigm in this project is best described as 
procedural, event driven, and slightly object oriented. 
"""

# ----- Edit this to customize / change difficulty / debug -----
grid_size = 24    # number of squares in the snake grid
start_len = 6     # starting length of the snake
frame_rate = 60   # frame rate of the application (refreshrate of window)
snake_rate = 6    # frames between snake updates (refreshrate of snake)
debug = False     # if True, bend-points in snake will be displayed as gray spaces
colors = {        # color and style dictionary.
    "background" : color(100,100,100),
    "gift" : color(250,50,50),
    "gift weight" : 0,
    "ingame score" : color(255,255,255),
    "final score" : color(0,0,0),
    "snake head" : color(120,120,250),
    "snake body" : color(120,250,120),
    "snake weight" : 0,
    "grid color" : color(10,10,10),
    "grid weight": 1,
}
# ----- Do not edit past here -----

import time # imports the time module
snake = [] # list of Blocks which stores the snake, where the last element is the head
bends = [] # list of Turns for the bend points
gift  = [int(random(1,grid_size)), int(random(1, grid_size))] # gift location

# Setup function, runs once when the program is started.
def setup():   
    size(800,800)         # defines the window size to be 800 pixels by 800 pixels
    frameRate(frame_rate) # sets window frame rate
    # iteration that generates the initial snake, at the initial location
    for x in range(start_len): 
        snake.append(Block())       # adds block to end of snake
        snake[-1].loc = [x,1]       # sets block location to location on grid
        snake[-1].pos = start_len-x # sets block position to its position in the snake sequence
        snake[-1].dir = 3           # sets direction of block to right
        
# Draw function, runs repeatedly after setup.
def draw():
    background(colors["background"])       # set background
    grid()                                 # draw grid
    if snake[-1].loc == gift:              # check if the snake has eaten a gift
        gift[0] = int(random(1,grid_size)) # reset the gift location
        gift[1] = int(random(1,grid_size))
        checkGift()                        # check gift location validity
        fill(colors["gift"])               # draw the gift (set colors, outline, and draw to location)
        stroke(colors["gift weight"])
        rect((gift[0]-1)*width/grid_size, (gift[1]-1)*height/grid_size, width/grid_size, height/grid_size)
        noStroke()
        snake.append(Block())              # elongate the snake
        snake[-1].dir = snake[-2].dir      # set direction of the new block
        snake[-1].loc = list(snake[-2].loc)# set location of the new block (and adjust for direction)
        if snake[-2].dir == 1:
            snake[-1].loc[0] -= 1
        elif snake[-2].dir == 2:
            snake[-1].loc[1] += 1
        elif snake[-2].dir == 3:
            snake[-1].loc[0] += 1
        elif snake[-2].dir == 4:
            snake[-1].loc[1] -= 1
        updatePos()                       # update the `pos` field of every block in the snake.
    else:                                 # else - if the snake has not eaten a gift:
        fill(colors["gift"])              # draw the gift at its current location. 
        stroke(colors["gift weight"])
        rect((gift[0]-1)*width/grid_size, (gift[1]-1)*height/grid_size, width/grid_size, height/grid_size)
        noStroke()
        if debug:                         # if debugging is on, show the bend points in the snake as grey spaces on the grid
            for b in bends:
                b.show()
    if frameCount%snake_rate == snake_rate-1: # if the game is on the right frame cycle, move the snake forward one space
        for s in snake:
            s.update()
    drawSnake()                               # draw the snake
    textSize(height/grid_size/2)              # display the ingame score in the top lefthand corner of the screen.
    fill(colors["ingame score"])
    text(str(len(snake)-start_len),width/grid_size/8, height/grid_size/2 )
    for s in snake[0:-1]:                     # if the snake has bitten itself, end the game and display the death message.
        if snake[-1].loc == s.loc:
            die()

# draws the grid onto the window.
def grid():
    fill(colors["grid color"])     # set grid colors according to the color dictionary at the top.
    stroke(colors["grid weight"])
    for x in range(0, grid_size):  # some quick iterative math to draw all of the grid lines in.
        line(0,x* height/grid_size, width, x* height/grid_size)
        line(x*width/grid_size,0, x*width/grid_size, height)
    noStroke()

# class definition for what a Block is.
class Block:
    def __init__(self):   # constructor method to set fields of the object to default values.
        self.loc = [0,0]
        self.dir = 1
        self.pos = 0
    def update(self):     # move block one square in whatever its direction is, and check if it changes direction because of a bend.
        for t in bends:
            if self.loc == t.loc:
                self.dir = t.new_dir
                if self.pos == len(snake): # if last block in snake, remove bend
                    bends.remove(t)
        # if the snake hits the side of a window, end the game and display the death message.
        if self.dir == 1: #left
            self.loc[0] -= 1
            if self.loc[0] <= 0:
                die()
        elif self.dir == 2: #down
            self.loc[1] +=1
            if self.loc[1] > grid_size:
                die()
        elif self.dir == 3: #right
            self.loc[0] +=1
            if self.loc[0] > grid_size:
                die()
        elif self.dir == 4: # up
            self.loc[1] -=1
            if self.loc[1] <= 0:
                die()
            
# class definition for a Turn, the object used to represent bends in the snake.
class Turn:
    def __init__(self):             # Constructor method to initialize object fields to default values.
        self.new_dir = 0
        self.loc = [0,0]
    def show(self):                 # method to display a bend in the snake, used in debugging.
        fill(color(200,200,200))
        rect((self.loc[0]-1)*width/grid_size, (self.loc[1]-1)*height/grid_size, width/grid_size, height/grid_size)

# function that draws the snake onto the grid when executed.
def drawSnake():
    stroke(colors["snake weight"])
    fill(colors["snake head"]) # draws the snake head
    rect((snake[len(snake)-1].loc[0]-1)*width/grid_size, (snake[len(snake)-1].loc[1]-1)*height/grid_size, width/grid_size, height/grid_size)
    fill(colors["snake body"]) # draws the snake body
    for b in snake[0:len(snake)-1]:
        rect((b.loc[0]-1)*width/grid_size, (b.loc[1]-1)*height/grid_size, width/grid_size, height/grid_size)
    noStroke()

# key handler - function to handle keyboard input, run once whenever draw is run.
def keyPressed():
    for b in bends:                # avoids duplicated keypresses by ignoring keys pressed when there is already a bend at the snake's head.
        if b.loc == snake[-1].loc:
            return
    if keyCode == UP: # adds a bend going up if possible
        if snake[-1].dir == 4 or snake[-1].loc[1] == 1 or snake[-1].dir == 2:
            pass
        else:
            bends.append(Turn())
            bends[-1].new_dir = 4
            bends[-1].loc = list(snake[-1].loc)
            snake[-1].dir = 4
    elif keyCode == LEFT: # adds a bend going left if possible
        if snake[-1].dir == 1 or snake[-1].loc[0] == 1 or snake[-1].dir == 3:
            pass
        else:
            bends.append(Turn())
            bends[-1].new_dir = 1
            bends[-1].loc = list(snake[-1].loc)
            snake[len(snake)-1].dir = 1
    elif keyCode == DOWN: # adds a bend going down if possible
        if snake[-1].dir == 2 or snake[-1].loc[1] == grid_size or snake[-1].dir == 4:
            pass
        else:
            bends.append(Turn())
            bends[-1].new_dir = 2
            bends[-1].loc = list(snake[-1].loc)
            snake[-1].dir = 2
    elif keyCode == RIGHT: # adds a bend going right if possible
        if snake[-1].dir == 3 or snake[-1].loc[0] == grid_size or snake[-1].dir == 1:
            pass
        else:
            bends.append(Turn())
            bends[-1].new_dir = 3
            bends[-1].loc = list(snake[-1].loc)
            snake[-1].dir = 3

# Stops the game and displays the final score.
def die():
    noLoop()                                                  # stop draw() from being executed again.
    t = "You died with a score of "+str(len(snake)-start_len) # set death message to "You died with a score of ..."
    textSize(60)                                              # set the font size to 60
    fill(colors["final score"])                               # set text color to the one defined at the top in the colors dictionary.
    text(t, (width - textWidth(t))/2, (height - 60)/2)        # display message

# update the `pos` field of all the blocks in the snake to be consistient with the snake's length.
def updatePos():
    for n, s in enumerate(snake):
        s.pos = len(snake) - n

# checks if the gift is currently in a valid location,
# (not under the snake)
# if the location is invalid, reset the gift and check again.
def checkGift(): 
    for s in snake:
        if s.loc == gift:
            gift[0] = int(random(1,grid_size))
            gift[1] = int(random(1,grid_size))
            checkGift()
            break