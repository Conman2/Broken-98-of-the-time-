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

#Screen display deminsions
(Screen_Width,Screen_Height) = (900,720) #Note this Both need to be Multiples of 60
Screen = pygame.display.set_mode((Screen_Width, Screen_Height))

#Used to control game speed linking it to FPS
Clock = pygame.time.Clock()
fps = 30

#Initializing Variables
xspeed = yspeed = xd = xa = ys = yw = dx = dy = 0
Player_Bullet_array = []
Tracker_Bullet_array = []
NPC_Bullet_array = []
Block_array = []
NPC_1_array = []
mouse_state = (0,0,0)
key_state = False
Move = False

#Positions and Other Variables
player_y = Screen_Height/2
player_x = Screen_Width/2
player_rad = npc_rad = 20
shoot_dist = 150
sheild_rad = 30
NPC_Number = 2
Bullet_rad = 3
Bullet_spray = 0.5
Block_size = 60
Block_number = 0
Block_x = [0]*Block_number
Block_y = [0]*Block_number

for i in range(0,NPC_Number)


''' All the Object Classes '''
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

class NPC_1():
    def __init__(self,x_pos,y_pos,npc_rad,Speed,Colour):
        self.Move = False
        self.Radius = npc_rad
        self.Colour = Colour
        self.x = x_pos
        self.y = y_pos
        self.last_seen_x = x_pos
        self.last_seen_y = y_pos
        self.Speed = Speed
        self.Thickness = 1
    def Movement(self):
        self.Velocity_x = self.Speed*(-(self.x - self.last_seen_x)/(abs(self.x - self.last_seen_x)+abs(self.y - self.last_seen_y)))
        self.Velocity_y = self.Speed*(-(self.y - self.last_seen_y)/(abs(self.x - self.last_seen_x)+abs(self.y - self.last_seen_y)))
        self.x += self.Velocity_x
        self.y += self.Velocity_y
        pygame.draw.circle(Screen, self.Colour, (int(self.x), int(self.y)), self.Radius, self.Thickness)
    def Still(self):
        pygame.draw.circle(Screen, self.Colour, (int(self.x), int(self.y)), self.Radius, self.Thickness)

class Block():
    def __init__(self,x_pos,y_pos,Block_size):
        self.x = x_pos
        self.y = y_pos
        self.Colour = orange
        self.Size = Block_size #Note this is the Area of the Rectangle

    def Draw(self):
        pygame.draw.rect(Screen, self.Colour, (self.x, self.y, self.Size, self.Size), 1)


''' Generating the Block Spawns '''
X_range = range(0, Screen_Width, Block_size)
Y_range = range(0, Screen_Height, Block_size)

#Creating the Spawn Locations in an Array
for i in range(0,Block_number):
    X_value = choice(X_range)
    Y_value = choice(Y_range)
    block = Block(X_value, Y_value, Block_size)
    Block_array.append(block)


''' Running the Game '''
pygame.init()
while True:
    ''' Creating NPCs '''
    if len(NPC_1_array) < NPC_Number:
        npc_1 = NPC_1(randint(2*npc_rad, Screen_Width-2*npc_rad),randint(2*npc_rad, Screen_Height-2*npc_rad),npc_rad,4,blue)
        NPC_1_array.append(npc_1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            break

        ''' Managing Key Inputs '''
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            key_state = pygame.key.get_pressed()
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            mouse_state = pygame.mouse.get_pressed()

    if key_state != False:
        xspeed = 6*(key_state[100] - key_state[97])
        yspeed = 6*(key_state[115] - key_state[119])
        if abs(xspeed) == abs(yspeed):
            player_x += xspeed*0.5
            player_y += yspeed*0.5
        else:
            player_x += xspeed
            player_y += yspeed

    ''' Managing Mouse Inputs '''
    mouse_pos = pygame.mouse.get_pos()
    mouse_x = player_x - mouse_pos[0]
    mouse_y = player_y - mouse_pos[1]

    if mouse_state != False:
        if mouse_state[2] == 1:
            pygame.draw.circle(Screen,green,(int(player_x),int(player_y)),sheild_rad, 1)
        elif mouse_state[0] == 1:
            player_bullet = Bullet(player_x,player_y, mouse_x + randint(-abs(int(Bullet_spray*mouse_x)),abs(int(Bullet_spray*mouse_x))), mouse_y + randint(-abs(int(Bullet_spray*mouse_y)),abs(int(Bullet_spray*mouse_y))), Bullet_rad,green)
            Player_Bullet_array.append(player_bullet)


    ''' Player Bullets '''
    for player_bullet in Player_Bullet_array:
        player_bullet.Position()

        #Rebounds with Blocks
        for block in Block_array:
            if (block.x - Bullet_rad <= player_bullet.x <= block.x + Block_size + Bullet_rad) and (block.y - Bullet_rad <= player_bullet.y <= block.y + Block_size + Bullet_rad):
                if (block.x - Bullet_rad <= player_bullet.x <= block.x + Block_size + Bullet_rad):
                    if player_bullet.Velocity_x > 0:
                        player_bullet.x = block.x - Bullet_rad
                        player_bullet.Velocity_x = -player_bullet.Velocity_x
                    elif player_bullet.Velocity_x < 0:
                        player_bullet.x = block.x + Block_size + Bullet_rad
                        player_bullet.Velocity_x = -player_bullet.Velocity_x
                elif (block.y - Bullet_rad <= player_bullet.y <= block.y + Block_size + Bullet_rad):
                    if player_bullet.Velocity_y > 0:
                        player_bullet.y = block.y - Bullet_rad
                        player_bullet.Velocity_y = -player_bullet.Velocity_y
                    elif player_bullet.Velocity_y < 0:
                        player_bullet.y = block.y + Block_size + Bullet_rad
                        player_bullet.Velocity_y = -player_bullet.Velocity_y

        #Collosions with Boundary
        if player_bullet.x > Screen_Width or player_bullet.x < 0 or player_bullet.y > Screen_Height or player_bullet.y < 0:
            Player_Bullet_array.remove(player_bullet)


    ''' NPCs '''
    for npc_1 in NPC_1_array:
        #Distance from Player
        diffx_bullets = npc_1.x - player_x
        diffy_bullets = npc_1.y - player_y
        distance_player = math.hypot(diffx_bullets, diffy_bullets)

        #Shooting the tracker_bullet
        tracker_bullet = Bullet(npc_1.x, npc_1.y, diffx_bullets, diffy_bullets, 1, red)
        Tracker_Bullet_array.append(tracker_bullet)

        #Shooting Real Bullets
        if distance_player < player_rad + npc_rad + shoot_dist:
            npc_bullet = Bullet(npc_1.x, npc_1.y, diffx_bullets + randint(-abs(int(Bullet_spray*diffx_bullets)),abs(int(Bullet_spray*diffx_bullets))), diffy_bullets + randint(-abs(int(Bullet_spray*diffy_bullets)), abs(int(Bullet_spray*diffy_bullets))), Bullet_rad,black)
            NPC_Bullet_array.append(npc_bullet)

        #Collosion with Player
        for tracker_bullet in Tracker_Bullet_array:
            #Distance from Player
            diffx_tracker = tracker_bullet.x - player_x
            diffy_tracker = tracker_bullet.y - player_y
            distance_tracker = math.hypot(diffx_tracker,diffy_tracker)

            #If it hits the Player
            if distance_tracker < player_rad:
                Tracker_Bullet_array.remove(tracker_bullet)
                npc_1.last_seen_x = player_x
                npc_1.last_seen_y = player_y
                npc_1.Move = True
                break

        #Moving the NPC
        if npc_1.Move is True:
            if npc_1.last_seen_x == npc_1.x or npc_1.last_seen_y == npc_1.y:
                npc_1.Move = False

        if npc_1.Move is False:
            npc_1.Still()

        elif npc_1.Move is True:
            #Update the NPC Position
            npc_1.Movement()

            #Collosions with Blocks
            for block in Block_array:
                if (block.x - npc_rad + 1 <= npc_1.x <= block.x + Block_size + npc_rad - 1) and (block.y - npc_rad + 1 <= npc_1.y <= block.y + Block_size + npc_rad - 1):
                    if npc_1.Velocity_x > 0:
                        npc_1.x = block.x - npc_rad
                    elif npc_1.Velocity_x < 0:
                        npc_1.x = block.x + Block_size + npc_rad
                    elif npc_1.Velocity_y > 0:
                        npc_1.y = block.y - npc_rad
                    elif npc_1.Velocity_y < 0:
                        npc_1.y = block.y + Block_size + npc_rad

            #Collosions with Boundary
            if npc_1.x < npc_rad:
                npc_1.x = player_rad + 1
            elif  npc_1.y < npc_rad:
                npc_1.y = player_rad + 1
            elif npc_1.x > Screen_Width - npc_rad:
                npc_1.x = Screen_Width - npc_rad - 1
            elif  npc_1.y > Screen_Height - npc_rad:
                npc_1.y = Screen_Height - npc_rad - 1

    ''' Tracker Bullet '''
    for tracker_bullet in Tracker_Bullet_array:
        #tracker_bullet.Invisible(0.1)
        tracker_bullet.Position()

        #To check if a Bullet needs Deleting
        Tracker_Deleted = False

        #Collosions with Blocks
        for block in Block_array:
            if (block.x <= tracker_bullet.x <= block.x + Block_size) and (block.y <= tracker_bullet.y <= block.y + Block_size):
                Tracker_Bullet_array.remove(tracker_bullet)
                Tracker_Deleted = True
                break

        #Collosions with Boundary
        if Tracker_Deleted is False:
            if tracker_bullet.x > Screen_Width or tracker_bullet.x < 0 or tracker_bullet.y > Screen_Height or tracker_bullet.y < 0:
                Tracker_Bullet_array.remove(tracker_bullet)
                Tracker_Deleted = True


    ''' NPCs bullet '''
    for npc_bullet in NPC_Bullet_array:
        npc_bullet.Position()

        #Distance from Player
        diffx_npc_bullet = npc_bullet.x - player_x
        diffy_npc_bullet = npc_bullet.y - player_y
        distance_npc_bullet = math.hypot(diffx_npc_bullet,diffy_npc_bullet)

        #To check if a Bullet needs Deleting
        NPC_Bullet_Deleted = False

        #Rebounds with Blocks
        for block in Block_array:
            if (block.x - Bullet_rad <= npc_bullet.x <= block.x + Block_size + Bullet_rad) and (block.y - Bullet_rad <= npc_bullet.y <= block.y + Block_size + Bullet_rad):
                if (block.x - Bullet_rad <= npc_bullet.x <= block.x + Block_size + Bullet_rad):
                    if npc_bullet.Velocity_x > 0:
                        npc_bullet.x = block.x - Bullet_rad
                        npc_bullet.Velocity_x = -npc_bullet.Velocity_x
                    elif npc_bullet.Velocity_x < 0:
                        npc_bullet.x = block.x + Block_size + Bullet_rad
                        npc_bullet.Velocity_x = -npc_bullet.Velocity_x
                elif (block.y - Bullet_rad <= npc_bullet.y <= block.y + Block_size + Bullet_rad):
                    if npc_bullet.Velocity_y > 0:
                        npc_bullet.y = block.y - Bullet_rad
                        npc_bullet.Velocity_y = -npc_bullet.Velocity_y
                    elif npc_bullet.Velocity_y < 0:
                        npc_bullet.y = block.y + Block_size + Bullet_rad
                        npc_bullet.Velocity_y = -npc_bullet.Velocity_y

        #Collosion with the Sheild
        if mouse_state != False:
            if mouse_state[2] == 1 and distance_npc_bullet < sheild_rad + Bullet_rad:
                NPC_Bullet_array.remove(npc_bullet)
                NPC_Bullet_Deleted = True

        #Collosions with Boundary
        if NPC_Bullet_Deleted is False:
            if npc_bullet.x > Screen_Width or npc_bullet.x < 0 or npc_bullet.y > Screen_Height or npc_bullet.y < 0:
                NPC_Bullet_array.remove(npc_bullet)


    ''' Blocks '''
    for block in Block_array:
        block.Draw()

        #Collosion with Player
        if (block.x - player_rad + 1 <= player_x <= block.x + Block_size + player_rad - 1) and (block.y - player_rad + 1 <= player_y <= block.y + Block_size + player_rad - 1):
            if xspeed > 0:
                player_x = block.x - player_rad
            elif xspeed < 0:
                player_x = block.x + Block_size + player_rad
            elif yspeed > 0:
                player_y = block.y - player_rad
            elif yspeed < 0:
                player_y = block.y + Block_size + player_rad


    ''' Player Collosion with Boundary '''
    if player_x < player_rad:
        player_x = player_rad
    elif  player_y < player_rad:
        player_y = player_rad
    elif player_x > Screen_Width - player_rad:
        player_x = Screen_Width - player_rad
    elif  player_y > Screen_Height - player_rad:
        player_y = Screen_Height - player_rad


    ''' Drawing the character '''
    pygame.draw.circle(Screen,red,(int(player_x),int(player_y)),player_rad, 1)


    ''' Updating Changes to the Screen '''
    pygame.display.flip()
    Screen.fill(white)
    Clock.tick(fps)
