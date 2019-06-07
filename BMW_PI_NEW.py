
#!/usr/bin/python3
import pygame, sys, time
from pygame.locals import *
import pygame.gfxdraw
from subprocess import run
from gpiozero import LED, Button
from time import sleep
from threading import Thread


def message_display(text, fclr=(255, 0, 0), bclr=(128, 128, 128), font=None, fsize=20, loc=(0, 0)):
    AA = 1  # Anti Alias
    # no AA, no transparancy, normal
    sys_font = pygame.font.SysFont(font, fsize)
    size = sys_font.size(text)
    ren = sys_font.render(text, AA, fclr, bclr)
    # DISPLAYSURF.blit(ren, ((dis_w/2-size[0]/2), (dis_h/2 - size[1]) ))
    DISPLAYSURF.blit(ren, (loc[0]-(size[0]/2), (loc[1]-size[1])))

def evenodd(eo):
    #replace by (eo+1) %2; this is silly
    if eo >0:
        eo = 0
        return eo
    return eo + 1


def fakespd(tmint):
# replace by reading actual speed
# thread; updates spd every tmint seconds
# tmint is timer in ms; acc is rate to accelerate

    # print ('time int = " + str(timint))
    global spdrdg
    
    while True:
        time.sleep(tmint)
        spdrdg = (spdrdg +1) % 150
        
        
def speedodisplay():
    # uses global defined everything?
    text1 = str(spdrdg)
    tcol = RED
    if spdrdg <= 55:
        tcol = WHITE
    message_display(text1, tcol, None, font="Arial Black", fsize=400, loc=SpeedoLoc)
 

# GPIO setup
ledlt= LED(17)
ledrt = LED(27)
buttonlt = Button(10)
buttonrt = Button(22)


# set up the window
# DISPLAYSURF = pygame.display.set_mode((400, 300), 0, 32)
dis_h = 1000
dis_w = 1000
# NOFRAME removes frame.
DISPLAYSURF = pygame.display.set_mode((dis_w,dis_h), NOFRAME, 32)

# Set up feature locations

SpeedoLoc = (dis_w / 2 , int(dis_h *0.55))
BatDistLoc = (dis_w/2, int(dis_h * 0.85))
BatTextLoc = (dis_w/2, int(dis_h * 0.9))

# arrows
FLASH_RATE = 2 # FOR TURN SIGS; PER SEC
ArrowLtXPos = int(0.25 * dis_w)
ArrowRtXPos = int(0.75 * dis_w)
ArrowYPos = int(0.75 * dis_h)
ArrowH = int(0.065 * dis_h)
ArrowW = int(0.065 * dis_w)
TIME_MS = int( 1000/(((FLASH_RATE)/2)/2))

# Charge Rectangle location
ChgRectX = int(0.1*dis_w)
ChgRectY = int(0.55*dis_h)
ChRectH = int(0.05 * dis_h)
ChgTextLoc = (int(0.5 *dis_w ), (ChgRectY + ChRectH + int(0.05*dis_h) ))

# set up the colors  ?? Put a palette in place
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0, 0)
BLUE = (0, 0, 255)
# GREY = pygame.color('grey67') # why doesn't this work?
GREY = (128,128,128)
FUSCHIA = (255, 0, 255)  # fuschia

# The background image.
# image  = pygame.image.load('/home/pi/Desktop/CSEDashDisplay_sq_1k.png')
image  = pygame.image.load('/home/pi/Desktop/NewBkGnd.png')



# set up custom time event

TIMEEVENT_1 = pygame.USEREVENT
# TIME_MS = 700   # ms to update screen--this will be turn signal On/Off


is_running = True
eo = 0



#videoPath = "/home/pi/Desktop/BMW.mov"
#omx = run(["omxplayer",videoPath])
# Uncomment above for flash video

pygame.init()



pygame.time.set_timer(TIMEEVENT_1, TIME_MS)
DISPLAYSURF.blit(image, (0, 0))
pygame.display.update()

spdrdg = 0  # make it global
speedupdate = 4
t = Thread(target=fakespd, args=(speedupdate,))
t.start()

# is_running is bailout; replace by True & pygame.quit?
while is_running:
    # gets events from the event queue; this doesn't work in below while
    for event in pygame.event.get():
        # if the 'close' button of the window is pressed
        if (event.type == pygame.QUIT or event.type == K_ESCAPE):
            pygame.quit()
            sys.exit()
            # stops the application
            
#        
#    keys = pygame.key.get_pressed()
#    if keys[K_ESCAPE]:
#        # bail
#        is_running = False
            
# TODO fix this loop so bail out conditions are included    
    while not (buttonlt.is_pressed or buttonrt.is_pressed):
        # until a turn signal depressed, just update speedo
        # and range, etc.  Other stuff that changes
        # TODO add range, etc. update pgms here
        DISPLAYSURF.blit(image, (0, 0))
        speedodisplay()
        pygame.display.update()                    

        # captures the custom event 'TIMEEVENT_1'
    if event.type == TIMEEVENT_1:
        # prints on the console that 'TIME EVENT_1' has been captured and the capture time
        mod = pygame.time.get_ticks()
##            print ('custom event "TIMEEVENT_1" captured ({}) sec)'.format(mod/1000.))
        # DISPLAYSURF.fill(GREY)
        DISPLAYSURF.blit(image, (0, 0))
##            pygame.display.update()
    # display speed
        spdrdg = fakespd(spdrdg,mod, 1)
        eo = evenodd(eo)   # toggles every call
        text1 = str(spdrdg)
        tcol = RED
        if spdrdg <= 55:
            tcol = WHITE
        message_display(text1, tcol, None, font="Arial Black", fsize=400, loc=SpeedoLoc)
        if eo==1 and buttonlt.is_pressed:
            pygame.draw.polygon(DISPLAYSURF, GREEN, (
                (ArrowLtXPos, (ArrowYPos + ArrowH / 2)), ((ArrowLtXPos - ArrowW), ArrowYPos),
                (ArrowLtXPos, (ArrowYPos - ArrowH / 2))))
            ledlt.on()
        if eo==1 and buttonrt.is_pressed:
            pygame.draw.polygon(DISPLAYSURF, GREEN, (
                (ArrowRtXPos, (ArrowYPos + ArrowH / 2)), ((ArrowRtXPos + ArrowW), ArrowYPos),
                (ArrowRtXPos, (ArrowYPos - ArrowH / 2))))
            ledrt.on()    
        if eo==0:
            ledlt.off()
            ledrt.off()
                
        pygame.display.update()



# finalizes Pygame
pygame.quit()


