"""

This program displays a P300 GUI for trial performance. It also opens
an LSL stream which streams (currently) 37 stimuli keys indicating
whether or not a given key was chosen when a group stimulus was
initiated (bool) as well as 1 target key which the trial user was
instructed to focus on (0-36) and a local-clock timestamp, in seconds.

The state of this code is highly disorganized and not appropriately
commented in some areas. This commit is to ensure the group has some
working-level copy of this program on the github repo.

CruX UCLA Fall 2021
Darren Vawter

"""



"""
Major things to change/add (some of them...):
    -currently, stimuli are selected at random <-- change this to bucketing
        (each key has an X% chance of being displayed during each stimulation)
    -word prediction
        (offer words on the top row as alternatives to typing one character)
    -letter prediction
        (calculate PMF of next letter given previous letters)
        (use to aid stimuli selection)
    -choice offering (maybe?)
        (not for training phase?)
        (offer a potential selection to the user)
            (if user performs X, then accept offered selection)
            (e.g. X = close-eyes/move-eyes/clench/other)
    -create backspace (maybe)
        (to reduce error, allow user to X to erase their last selection)
        (e.g. X = stare-at-backspace/hold eyes closed/clench)
    -reconsider paradigm (much of this depends on the competition demands)
        (how long should each stimulus be presented)
        (how to stimulate? --> images/colors/hide vs show letter/random/etc.)
        (breaks between stimulus (y/n)? --> if yes, how long?)
        (character and key sizes)
        (for training: how long should each character be requested as focus)
        (should sound be incorporated?)
    -cleanup
        (reduce hardcoding)-->(there's a lot rn...)
        (review+add comments/explanations)
        (optimize some of the lazier portions of the code (might not need to))

"""
import pygame
import time
import random
from pylsl import StreamInfo, StreamOutlet

# Set initial value for all keys
def init_keys():

    # initialize static keys
    
    #rd = 80
    r0 = 280
    r1 = 480
    r2 = 680
    r3 = 880
    
    # row 3
    a = 100
    txt = font.render("1", True, WHITE)
    keys[27] = (txt,[a+170*0,r0],False)
    txt = font.render("2", True, WHITE)
    keys[28] = (txt,[a+170*1,r0],False)
    txt = font.render("3", True, WHITE)
    keys[29] = (txt,[a+170*2,r0],False)
    txt = font.render("4", True, WHITE)
    keys[30] = (txt,[a+170*3,r0],False)
    txt = font.render("5", True, WHITE)
    keys[31] = (txt,[a+170*4,r0],False)
    txt = font.render("6", True, WHITE)
    keys[32] = (txt,[a+170*5,r0],False)
    txt = font.render("7", True, WHITE)
    keys[33] = (txt,[a+170*6,r0],False)
    txt = font.render("8", True, WHITE)
    keys[34] = (txt,[a+170*7,r0],False)
    txt = font.render("9", True, WHITE)
    keys[35] = (txt,[a+170*8,r0],False)
    txt = font.render("0", True, WHITE)
    keys[36] = (txt,[a+170*9,r0],False)
    #backspace key
    keys[37] = (bkspc,[a+170*10,r0],False)

    # row 1
    a = 100
    txt = font.render("Q", True, WHITE)
    keys[0] = (txt,[a+170*0,r1],False)
    txt = font.render("W", True, WHITE)
    keys[1] = (txt,[a+170*1,r1],False)
    txt = font.render("E", True, WHITE)
    keys[2] = (txt,[a+170*2,r1],False)
    txt = font.render("R", True, WHITE)
    keys[3] = (txt,[a+170*3,r1],False)
    txt = font.render("T", True, WHITE)
    keys[4] = (txt,[a+170*4,r1],False)
    txt = font.render("Y", True, WHITE)
    keys[5] = (txt,[a+170*5,r1],False)
    txt = font.render("U", True, WHITE)
    keys[6] = (txt,[a+170*6,r1],False)
    txt = font.render("I", True, WHITE)
    keys[7] = (txt,[a+170*7,r1],False)
    txt = font.render("O", True, WHITE)
    keys[8] = (txt,[a+170*8,r1],False)
    txt = font.render("P", True, WHITE)
    keys[9] = (txt,[a+170*9,r1],False)
    
    # row 2
    a = 145
    txt = font.render("A", True, WHITE)
    keys[10] = (txt,[a+170*0,r2],False)
    txt = font.render("S", True, WHITE)
    keys[11] = (txt,[a+170*1,r2],False)
    txt = font.render("D", True, WHITE)
    keys[12] = (txt,[a+170*2,r2],False)
    txt = font.render("F", True, WHITE)
    keys[13] = (txt,[a+170*3,r2],False)
    txt = font.render("G", True, WHITE)
    keys[14] = (txt,[a+170*4,r2],False)
    txt = font.render("H", True, WHITE)
    keys[15] = (txt,[a+170*5,r2],False)
    txt = font.render("J", True, WHITE)
    keys[16] = (txt,[a+170*6,r2],False)
    txt = font.render("K", True, WHITE)
    keys[17] = (txt,[a+170*7,r2],False)
    txt = font.render("L", True, WHITE)
    keys[18] = (txt,[a+170*8,r2],False)
    #the quick brown fox key
    keys[38] = (tqbfjotld,[100+170*10,r2],False)
    
    # row 3
    a = 220
    txt = font.render("Z", True, WHITE)
    keys[19] = (txt,[a+170*0,r3],False)
    txt = font.render("X", True, WHITE)
    keys[20] = (txt,[a+170*1,r3],False)
    txt = font.render("C", True, WHITE)
    keys[21] = (txt,[a+170*2,r3],False)
    txt = font.render("V", True, WHITE)
    keys[22] = (txt,[a+170*3,r3],False)
    txt = font.render("B", True, WHITE)
    keys[23] = (txt,[a+170*4,r3],False)
    txt = font.render("N", True, WHITE)
    keys[24] = (txt,[a+170*5,r3],False)
    txt = font.render("M", True, WHITE)
    keys[25] = (txt,[a+170*6,r3],False)
    txt = font.render("_", True, WHITE)
    keys[26] = (txt,[a+170*7,r3],False)
    #the quick brown fox key
    keys[39] = (nlp_toggle,[100+170*10,r3],False)
    
    # other keys

    pass

# Update dynamic keys
def update_keys():    
    for i in range (len(keys)):
        stim = random.choice([False,False,False,False,False,True])
        keys[i] = (keys[i][0],keys[i][1],stim)

def display_keys():  
    
    # Display current target
    font = pygame.font.SysFont('Calibri', 250, True, False)
    txt = font.render(currentTarget, True, WHITE)
    screen.blit(txt, [835,10])

    # Display keys
    for key in keys:
        if(key[2] == True):
            
            #if drawing colors
            #pygame.draw.rect(screen,(random.randint(0,255),random.randint(0,255),random.randint(0,255)), [key[1][0]-20, key[1][1]-10, 100, 100])
            
            #if drawing images
            randImg = random.randrange(0,7)
            screen.blit(face[randImg],[key[1][0]-20, key[1][1]-10, 200, 200])
        else:
            screen.blit(key[0], key[1])
        pygame.draw.rect(screen, WHITE, [key[1][0]-20, key[1][1]-10, 100, 100], 3)

def pick_target(charList):
    if(not charList):
        charList = [char for char in panogram]
    
    currentTarget = random.choice(charList)
    charList.remove(currentTarget)
    return currentTarget

def menu_screen():
    
        # overwrite the screen with a background color
        screen.fill(BLACK)
        
        # write instruction sentences
        txt = font.render("Press '1' to enter training mode.", True, WHITE)
        screen.blit(txt, [400, 400])
        txt = font.render("Press '2' to enter user mode.", True, WHITE)
        screen.blit(txt, [400, 550])
        
        # render
        pygame.display.flip()
    
# Initialize the gui engine
pygame.init()
 
# Init outlet
info = StreamInfo("stimuli", "stimuli", 41, 125, "int8")
outlet = StreamOutlet(info)

# Define the colors we will use in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

#define Einstein's face
face = [None] * 8
for i in range(8):
    face[i] = pygame.image.load('face_images/'+str(i)+'.jpg')
bkspc = pygame.image.load('backspace_image.png')
tqbfjotld = pygame.image.load('tqbfjotld_image.png')
nlp_toggle = pygame.image.load('nlp_image.png')
 
# Set the height and width of the screen
#SCREEN_DIMENSIONS = [1152/2,648/2]
SCREEN_DIMENSIONS = [1920,1080]
screen = pygame.display.set_mode(SCREEN_DIMENSIONS)
 
pygame.display.set_caption("P300 GUI")

# Define key font
font = pygame.font.SysFont('Calibri', 90, True, False)

# Define key list
# each key --> (label-string,location-tuple,isTarget-bool)
keys = [None] * 40
init_keys()

#init timer
stimTime = time.time();
targetTime = time.time();

# Loop until the user clicks the close button.
mode = 0
menu_screen()
clock = pygame.time.Clock()

panogram = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
charList = [char for char in panogram]
currentTarget = pick_target(charList)
    
while (mode != -1):
 
    # check if window closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mode = -1
            
    # exit when esc is pressed
    pressed_keys = pygame.key.get_pressed()
    if(pressed_keys[pygame.K_ESCAPE]):
        pygame.quit()
        exit()
    if(pressed_keys[pygame.K_0]):
        mode = 0    #paused/menu screen
        menu_screen()       
    if(pressed_keys[pygame.K_1]):
        mode = 1    #training mode
    if(pressed_keys[pygame.K_2]):
        mode = 2    #user mode
    
        
    if(mode==1 or mode==2):
        # check timers
        end = time.time()        
        
        # Check stimuli timer
        if(end-stimTime>0.152):
            
            # Overwrite the screen with a background color
            screen.fill(BLACK)
            
            # reset timer
            stimTime = end
            
            # update key status
            update_keys()
            
            # display keys
            display_keys()
        
            # send stim codes after they have been displayed
            mysample = [0] * 41
            for i in range(len(keys)):
                mysample[i] = keys[i][2]
                mysample[40] = panogram.index(currentTarget) 
        
        # Check target char timer
        if(end-targetTime>20):
            
            # Overwrite the screen with a background color
            screen.fill(BLACK)
            
            # Pick a new target
            currentTarget = pick_target(charList)
            
            # reset timer
            targetTime = end
            
            # do not stimulate any keys
            for i in range(len(keys)):
                keys[i] = (keys[i][0],keys[i][1],False)
            
            # display keys
            display_keys()
            
            pygame.display.flip()
            time.sleep(2.69)
            
        # Go ahead and update the screen with what we've drawn.
        # This MUST happen after all the other drawing commands.
        pygame.display.flip()
     
        # This limits the while loop to a max of 10 times per second.
        # Leave this out and we will use all CPU we can.
        clock.tick(250)
    
# Be IDLE friendly
pygame.quit()
