import pygame
import math
import time
from random import randint, choice

''' Variable Managment '''
#Colour libary
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
pink = (255,105,180)
orange = (255,165,0)
white = (255,255,255)
clear = (0,0,0,0)

#Screen display deminsions
(Screen_Width,Screen_Height) = (840,660) #Note this Both need to be Multiples of 60
Screen = pygame.display.set_mode((Screen_Width, Screen_Height))

#Used to control game speed linking it to FPS
Clock = pygame.time.Clock()
fps = 30

#Initializing Variables
xspeed = yspeed = xd = xa = ys = yw = dx = dy = 0
Player_Bullet_array = []
Tracker_Bullet_array = []
Bullet_array = []
Block_array = []
NPC_1_array = []
mouse_state = key_state = False
NPC_move = True
Do_not_change = False

#Positions and Other Variables
player_y = Screen_Height/2
player_x = Screen_Width/2
player_rad = npc_rad = 20
shoot_dist = 150
sheild_rad = 30
NPC_Number = 3
Bullet_rad = 3
Bullet_spray = 0.1
Block_size = 60
Block_number = 15
Block_x = [0]*Block_number
Block_y = [0]*Block_number

''' Where all the Bullets Live '''
class Bullet():
    def __init__(self,x_npc,y_npc,dx,dy,Bullet_rad,Colour):
        self.Bullet_rad = Bullet_rad
        self.x = x_npc
        self.y = y_npc
        self.Speed = 8
        self.Colour = Colour
        self.Thickness = 1
        self.Velocity_x = self.Speed*(-dx/(abs(dx)+abs(dy)))
        self.Velocity_y = self.Speed*(-dy/(abs(dx)+abs(dy)))
    def Position(self):
        self.x += self.Velocity_x
        self.y += self.Velocity_y
        pygame.draw.circle(Screen, self.Colour, (int(self.x), int(self.y)), self.Bullet_rad, self.Thickness)
    def Invisible(self,faster):
        self.x += self.Velocity_x*faster
        self.y += self.Velocity_y*faster

''' Where all the NPCs Live '''
class NPC_1():
    def __init__(self,x_pos,y_pos,npc_rad,Speed,Colour):
        self.Radius = npc_rad
        self.Colour = Colour
        self.x = self.last_seen_x = x_pos
        self.y = self.last_seen_y = y_pos
        self.Speed = Speed-3
        self.Thickness = 1
    def Movement(self,last_seen_x,last_seen_y):
        self.Velocity_x = self.Speed*(-last_seen_x/(abs(last_seen_x)+abs(last_seen_y)))
        self.Velocity_y = self.Speed*(-last_seen_y/(abs(last_seen_x)+abs(last_seen_y)))
        self.x += self.Velocity_x
        self.y += self.Velocity_y
        pygame.draw.circle(Screen, self.Colour, (int(self.x), int(self.y)), self.Radius, self.Thickness)
    #For When the NPC needs to stand stationary
    def Still(self):
        pygame.draw.circle(Screen, self.Colour, (int(self.x), int(self.y)), self.Radius, self.Thickness)

    ''' Spawning in a set of Blocks '''
    class Block():
        def __init__(self,x_pos,y_pos,Block_size):
            self.x = x_pos
            self.y = y_pos
            self.Colour = orange
            self.Size = Block_size #Note this is the Area of the Rectangle
        def Draw(self):
            pygame.draw.rect(Screen, self.Colour, (self.x, self.y, self.Size, self.Size), 1)

    ''' Random Spawning of Blocks '''
    #Breaking Up the Screen
    X_range = range(0, Screen_Width, Block_size)
    Y_range = range(0, Screen_Height, Block_size)

    #Creating the Spawn Locations in an Array
    for i in range(0,Block_number):
        X_value = choice(X_range)
        Y_value = choice(Y_range)
        block = Block(X_value, Y_value, Block_size)
        Block_array.append(block)

#Initializing Pygame cus reasons
pygame.init()

last_seen_x = Screen_Width/2
last_seen_y = Screen_Height/2

while True:
    Screen.fill(white)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            break

        ''' Tracking User Inputs '''
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            key_state = pygame.key.get_pressed()
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            mouse_state = pygame.mouse.get_pressed()

    ''' Moving the Player '''
    if key_state != False:
        xspeed = 6*(key_state[100] - key_state[97])
        yspeed = 6*(key_state[115] - key_state[119])

    #Used to Determine if 1D or 2D movement
    if abs(xspeed) == abs(yspeed):
        player_x += xspeed*0.5
        player_y += yspeed*0.5
    else:
        player_x += xspeed
        player_y += yspeed

    #Checking for player Collosion with Blocks and Drawing the BLocks
    for block in Block_array:
        block.Draw()
        if player_x in range(block.x - player_rad, block.x + Block_size + player_rad) and player_y in range(block.y - player_rad, block.y + Block_size  + player_rad):
            if xspeed > 0:
                player_x = block.x - player_rad
            elif xspeed < 0:
                player_x = block.x + Block_size + player_rad
            elif yspeed > 0:
                player_y = block.y - player_rad
            elif yspeed < 0:
                player_y = block.y + Block_size + player_rad

    pygame.draw.circle(Screen,red,(int(player_x),int(player_y)),player_rad, 1)

    ''' Managing Mouse Inputs for Sheild and Shoot '''
    mouse_pos = pygame.mouse.get_pos()
    mouse_x = player_x - mouse_pos[0]
    mouse_y = player_y - mouse_pos[1]

    if mouse_state != False:
        #Spawning Player Sheild
        if mouse_state[2] == 1:
            pygame.draw.circle(Screen,green,(int(player_x),int(player_y)),sheild_rad, 1)
        elif mouse_state[0] == 1:
            #Creating Players Bullets
            player_bullet = Bullet(player_x,player_y, mouse_x + randint(-abs(int(Bullet_spray*mouse_x)),abs(int(Bullet_spray*mouse_x))), mouse_y + randint(-abs(int(Bullet_spray*mouse_y)),abs(int(Bullet_spray*mouse_y))), Bullet_rad,green)
            Player_Bullet_array.append(player_bullet)

    ''' Creating NPCs '''
    if len(NPC_1_array) < NPC_Number:
        npc_1 = NPC_1(randint(2*npc_rad, Screen_Width-2*npc_rad),randint(2*npc_rad, Screen_Height-2*npc_rad),npc_rad,4,blue)
        NPC_1_array.append(npc_1)

    ''' Updating all of the Bullets and NPCs'''
    #Moves the NPCs and Determins if they should shoot
    for npc_1 in NPC_1_array:
        #Create the NPC Bullet
        distance_player = math.hypot(dx, dy)
        dx = npc_1.x - player_x
        dy = npc_1.y - player_y
        if distance_player < player_rad + npc_rad + shoot_dist:
            bullet = Bullet(npc_1.x ,npc_1.y, dx + randint(-abs(int(Bullet_spray*dx)),abs(int(Bullet_spray*dx))), dy+ randint(-abs(int(Bullet_spray*dy)),abs(int(Bullet_spray*dy))), Bullet_rad,black)
            Bullet_array.append(bullet)
        #Invisible Bullets Check
        tracker_bullet = Bullet(npc_1.x ,npc_1.y, dx, dy, 1, clear)
        Tracker_Bullet_array.append(tracker_bullet)
        for tracker_bullet in Tracker_Bullet_array:
            tracker_bullet.Invisible(2)
            #tracker_bullet.Position()
            for block in Block_array:
                if tracker_bullet.x in range(block.x, block.x + Block_size) and tracker_bullet.y in range(block.y, block.y + Block_size):
                    Tracker_Bullet_array.remove(tracker_bullet)
            if tracker_bullet.x > Screen_Width or tracker_bullet.x < 0 or tracker_bullet.y > Screen_Height or tracker_bullet.y < 0:
                Tracker_Bullet_array.remove(tracker_bullet)
            distance_tracker = math.hypot((tracker_bullet.x - player_x),(tracker_bullet.y - player_y))
            if distance_tracker < player_rad:
                last_seen_x = player_x
                last_seen_y = player_y
                Do_not_change = True
        if Do_not_change == True:
            diffx = npc_1.x - last_seen_x
            diffy = npc_1.y - last_seen_y
            npc_1.Movement(diffx,diffy)
        if npc_1.x == last_seen_x or npc_1.y == last_seen_y:
            Do_not_change = False
            npc_1.Still()

    #The Players Bullets
    for player_bullet in Player_Bullet_array:
        player_bullet.Position()
        if player_bullet.x > Screen_Width or player_bullet.x < 0 or player_bullet.y > Screen_Height or player_bullet.y < 0:
            Player_Bullet_array.remove(player_bullet)

    #The NPCs Bullets
    for bullet in Bullet_array:
        bullet.Position()
        distance_sheild = math.hypot((bullet.x - player_x),(bullet.y - player_y))
        if bullet.x > Screen_Width or bullet.x < 0 or bullet.y > Screen_Height or bullet.y < 0:
            Bullet_array.remove(bullet)
        if mouse_state != False:
            if mouse_state[2] == 1 and distance_sheild < sheild_rad + Bullet_rad: #+ xspeed + yspeed + bullet.Velocity_x + bullet.Velocity_y:
                Bullet_array.remove(bullet)

    ''' Updating Changes to the Screen '''
    pygame.display.flip()
    Clock.tick(fps)
