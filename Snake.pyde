import time
# ----- Edit this to customize / change difficulty / debug
grid_size = 24
start_len = 6
frame_rate = 60
snake_rate = 6  # frames between snake updates
debug = False
colors = {
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
# ----- Do not edit past here

snake     = []
bends     = []
gift      = [int(random(1,grid_size)), int(random(1, grid_size))]

def setup():
    size(800,800)
    background(colors["background"])
    frameRate(frame_rate)
    grid()
    for x in range(start_len):
        snake.append(Block())
        snake[len(snake)-1].loc = [x,1]
        snake[len(snake)-1].pos = start_len-x
        #print(start_len-x)
        snake[len(snake)-1].dir = 3
        
def draw():
    background(colors["background"])
    grid()
    if snake[len(snake)-1].loc == gift:
        gift[0] = int(random(1,grid_size))
        gift[1] = int(random(1,grid_size))
        checkGift()
        fill(colors["gift"])
        stroke(colors["gift weight"])
        rect((gift[0]-1)*width/grid_size, (gift[1]-1)*height/grid_size, width/grid_size, height/grid_size)
        noStroke()
        snake.append(Block())
        snake[len(snake)-1].dir = snake[len(snake)-2].dir
        snake[len(snake)-1].loc = list(snake[len(snake)-2].loc)
        if snake[len(snake)-2].dir == 1:
            snake[len(snake)-1].loc[0] -= 1
        if snake[len(snake)-2].dir == 2:
            snake[len(snake)-1].loc[1] += 1
        if snake[len(snake)-2].dir == 3:
            snake[len(snake)-1].loc[0] += 1
        if snake[len(snake)-2].dir == 4:
            snake[len(snake)-1].loc[1] -= 1
        updatePos()
    else:
        fill(colors["gift"])
        stroke(colors["gift weight"])
        rect((gift[0]-1)*width/grid_size, (gift[1]-1)*height/grid_size, width/grid_size, height/grid_size)
        noStroke()
    if debug:
        for b in bends:
            b.show()
    if frameCount%snake_rate == snake_rate-1:
        for s in snake:
            s.update()
            #print(s.pos)
    drawSnake()
    textSize(height/grid_size/2)
    fill(colors["ingame score"])
    text(str(len(snake)-start_len),width/grid_size/8, height/grid_size/2 )
    for s in snake[0:len(snake)-1]:
        if snake[len(snake)-1].loc == s.loc:
            die()
    

def grid():
    fill(colors["grid color"])
    stroke(colors["grid weight"])
    for x in range(0,grid_size):
        line(0,x* height/grid_size, width, x* height/grid_size)
        line(x*width/grid_size,0, x*width/grid_size, height)
    noStroke()

class Block:
    def __init__(self):
        self.loc = [1,1]
        self.dir = 1
        self.pos = 0
    def update(self):
        for t in bends:
            if self.loc == t.loc:
                self.dir = t.new_dir
                if self.pos == len(snake): # if last, remove bend
                    #print("bend removed on: ", self.pos, len(snake))
                    bends.remove(t)
        if self.dir == 1: #left
            self.loc[0] -=1
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
            
class Turn:
    def __init__(self):
        self.new_dir = 0
        self.loc = [0,0]
    def show(self):
        fill(color(200,200,200))
        rect((self.loc[0]-1)*width/grid_size, (self.loc[1]-1)*height/grid_size, width/grid_size, height/grid_size)

def drawSnake():
    stroke(colors["snake weight"])
    fill(colors["snake head"])
    rect((snake[len(snake)-1].loc[0]-1)*width/grid_size, (snake[len(snake)-1].loc[1]-1)*height/grid_size, width/grid_size, height/grid_size)
    fill(colors["snake body"])
    for b in snake[0:len(snake)-1]:
        rect((b.loc[0]-1)*width/grid_size, (b.loc[1]-1)*height/grid_size, width/grid_size, height/grid_size)
    noStroke()

def keyPressed():
    if keyCode == UP:
        if snake[len(snake)-1].dir == 4 or snake[len(snake)-1].loc[1] == 1 or snake[len(snake)-1].dir == 2:
            pass
        else:
            bends.append(Turn())
            bends[len(bends)-1].new_dir = 4
            bends[len(bends)-1].loc = list(snake[len(snake)-1].loc)
            snake[len(snake)-1].dir = 4
            #time.sleep(0.001)
    elif keyCode == LEFT:
        if snake[len(snake)-1].dir == 1 or snake[len(snake)-1].loc[0] == 1 or snake[len(snake)-1].dir == 3:
            pass
        else:
            bends.append(Turn())
            bends[len(bends)-1].new_dir = 1
            bends[len(bends)-1].loc = list(snake[len(snake)-1].loc)
            snake[len(snake)-1].dir = 1
            #time.sleep(0.001)
    elif keyCode == DOWN:
        if snake[len(snake)-1].dir == 2 or snake[len(snake)-1].loc[1] == grid_size or snake[len(snake)-1].dir == 4:
            pass
        else:
            bends.append(Turn())
            bends[len(bends)-1].new_dir = 2
            bends[len(bends)-1].loc = list(snake[len(snake)-1].loc)
            snake[len(snake)-1].dir = 2
            #time.sleep(0.001)
    elif keyCode == RIGHT:
        if snake[len(snake)-1].dir == 3 or snake[len(snake)-1].loc[0] == grid_size or snake[len(snake)-1].dir == 1:
            pass
        else:
            bends.append(Turn())
            bends[len(bends)-1].new_dir = 3
            bends[len(bends)-1].loc = list(snake[len(snake)-1].loc)
            snake[len(snake)-1].dir = 3
            #time.sleep(0.001)

def die():
    noLoop()
    t = "You died with a score of "+str(len(snake)-start_len)
    fs = 60
    textSize(fs)
    fill(colors["final score"])
    text(t, (width - textWidth(t))/2, (height - fs)/2)

def updatePos():
    #print("\n")
    for n, s in enumerate(snake):
        s.pos = len(snake) - n
        #print(s.pos)
def checkGift():
    for s in snake:
        if s.loc == gift:
            gift[0] = int(random(1,grid_size))
            gift[1] = int(random(1,grid_size))
            checkGift()
            break