import random, sys, pygame
from pygame.locals import *
from random import randint as rand

# Create a function for picking a random direction.
def randDir():
    r = rand(0,3)
    if r == 0: rv = (0,-1) # Up.
    if r == 1: rv = (0,1) # Down.
    if r == 2: rv = (-1,0) # Left.
    if r == 3: rv = (1,0) # Right.
    return rv

# Create a function to initialize the maze.
# w and h are the width and height respectively.
def initMaze(w,h):
    global maze,spl

    # Create a 2 dimensional array.
    maze = [[0]*h for x in range(w)]

    # Create four walls around the maze.
    # 1=wall, 0=walkway.
    for x in range(0,w):
        maze[x][0] = maze[x][h-1] = 1
    for y in range(0,mazeYSize):
        maze[0][y] = maze[w-1][y] = 1

    # Make every other cell a starting point.
    # 2=starting point.
    # Also create a list of these points to speed up the main loop.
    spl = []
    for y in range(2,h-2,2):
        for x in range(2,w-2,2):
            maze[x][y] = 2
            spl.append((x,y))
    # Shuffle the list of points and we can choose a random point by
    # simply "popping" it off the list.
    random.shuffle(spl)

# Quick and dirty function to see if user has closed the app.
def hasQuit():
    for e in pygame.event.get():
        if e.type == QUIT: return True
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE: return True
    return False

# Define the X and Y size of the maze including the outer walls.
# These values aren't checked but must be positive odd integers above 3.
mazeXSize = 65
mazeYSize = 45

# Set the maximum length of a wall, the main improvement on the first version.
# The smaller this value, the more complex the maze.
# A large value will produce a quite boring maze with long walls.
# A small value (try 1) will produce a more labyrinthine structure, something
# you wouldn't like to get trapped in with a Minotaur!!!
maxWallLen = 1

# Set a "pixel multiplier" for display purposes.
# This is the size of eack block drawn.
mult = 10

# Fairly standard PyGame initialization.
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)

pygame.init()
screen = pygame.display.set_mode((mazeXSize*mult,mazeYSize*mult))
pygame.display.set_caption('Maze Creation Algorithm')
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(black)
screen.blit(background,(0,0))
pygame.display.flip()

ss = screen.get_size()
pygame.draw.rect(screen,red,(0,0,ss[0],ss[1]),mult*2)
pygame.display.update()

# Create an empty maze.
initMaze(mazeXSize,mazeYSize)

# Loop until we have no more starting points (2's in the empty maze)
while filter(lambda x: 2 in x, maze):
    # Get the X and Y values of the first point in our randomized list.
    rx = spl[0][0]
    ry = spl[0][1]
    # Pop the first entry in the list, this deletes it and the rest move down.
    spl.pop(0)
    # Check to see if our chosen point is still a valid starting point.
    if maze[rx][ry] == 2:
        # Pick a random wall length up to the maximum.
        rc = rand(0,maxWallLen)
        # Pick a random direction.
        rd = randDir()
        fc = rd
        loop = True
        while loop:
            # Look in each direction, if the current wall being built is stuck inside itself start again.
            if maze[rx][ry-2] == 3 and maze[rx][ry+2] == 3 and maze[rx-2][ry] == 3 and maze[rx+2][ry] == 3:
                screen.fill(black)
                pygame.draw.rect(screen,red,(0,0,ss[0],ss[1]),mult*2)
                initMaze(mazeXSize,mazeYSize)
                break
            # Look ahead to see if we're okay to go in this direction.....
            cx = rx + (rd[0]*2)
            cy = ry + (rd[1]*2)
            nc = maze[cx][cy]
            if nc != 3:
                for i in range(0,2):
                    maze[rx][ry] = 3
                    block = (rx*mult,ry*mult,mult,mult)
                    pygame.draw.rect(screen,red,block,0)
                    rx += rd[0]
                    ry += rd[1]
                pygame.display.update()
            # .....if not choose another direction.
            else: rd = randDir()
            # If we hit an existing wall break out of the loop.
            if nc == 1: loop = False
            # Update our wall length counter. When this hits zero pick another direction.
            # This also makes sure the new direction isn't the same as the current one.
            rc -= 1
            if rc <= 0:
                rc = rand(0,maxWallLen)
                dd = rd
                de = (fc[0]*-1,fc[1]*-1)
                while dd == rd or rd == de:
                    rd = randDir()
    # The latest wall has been built so change all 3's (new wall) to 1's (existing wall)
    for x in range(0,mazeXSize):
        for y in range(0,mazeYSize):
            if maze[x][y] == 3: maze[x][y] = 1
    # Have we got bored and just want to leave the loop?
    if hasQuit() == True: pygame.quit()

# Loop until escape is pressed or the window has been closed
while hasQuit() == False:
    # Do stuff here.
    c = pygame.time.Clock()
    c.tick(60)
    pygame.display.update()

# Uncomment the line below to save a snapshot of the maze.
#pygame.image.save(screen,"maze_grab.jpeg")
pygame.quit()
