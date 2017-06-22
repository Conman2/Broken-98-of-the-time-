import pygame
import math
import time
from random import randint, choice

pygame.init()
pygame.font.init()

''' Things that need Adding/Fixing '''
#NPC Collosion with the sheild
#Bots not colliding with each other
#Take you to a death screen where you can reatart after dieing
#Power up where yuo sheild does melee
#POwer up where you can move on blocks
#NPCs can still morph through blocks, problem known need fix - The bot movement is after the collision
#try adding some basic NPC Ai for transversing blocks, eg if stuck change y velocity
#add a new way of spawning enemies in a wave style system
#shotgun triginometery
#friction for the dash function
#Multiplayer
#Create big map with following camera (and spawn structers and stuff)
#powerups lasting longer than they should
#Adding a timer for the freezeray cooldown
#Balancing the wepaons

''' Variable Managment '''
#Colour libary
black = (0,0,0)
red = (255,0,0)
green = (0,220,0)
blue = (0,0,255)
pink = (255,105,180)
yellow = (255,255,0)
magenta = (255,0,255)
grey = (128,128,128)
orange = (255,69,0)
white = (255,255,255)

#Setting up Pygame
(Screen_Width,Screen_Height) = (920,720) #Note this Both need to be Multiples of 60
Screen = pygame.display.set_mode((Screen_Width, Screen_Height))
Clock = pygame.time.Clock()
fps = 30

#Initializing Variables
lastfired_rifle = lastfired_shotgun = lastfired_smg = 0
xspeed = yspeed = dx = dy = 0
lastfired_freeze = -20000
last_dash = 0
Player_Bullet_array = []
NPC_Bullet_array = []
Block_array = []
NPC_1_array = []
Powerup_array = []
mouse_state = (0,0,0)
counter = 1
weapon = 1
Block_place = False
key_state = False
freeze = False
dash = False
Overlap = False
Conflict = False
Sheild_Shoot = False
Solid = 0
HealthColour = white

last_powerup = 0
powerup_active = False
powerup_extent = 10000
powerup_spacing = 30000

#Player Properties
player_y = Screen_Height/2
player_x = Screen_Width/2
player_rad = 15
player_speed = 8
sheild_rad = 30
Blocks_given = 5
Player_Health = 100
Sheild_Health = 100
Diagonal_Speed = 0.7
Start_time = 15000
dash_time = 250

#Block Properties
Block_size = 40
Block_number = 40

#Different NPCs *Note that all the Radius must be Integers
NPC_Number = 1
npc1 = {'Radius': 15, 'Speed': 6, 'Colour': blue, 'Health': 100, 'Bullet_Damage': 5, 'Sheild_Damage': 1, 'Bullet_rate':10, 'Shoot_range':200, 'Bullet_Speed':8, 'Bullet_Spray':0.5, 'Melee_Damage':2, 'Block_Damage':0.5} #Default
npc2 = {'Radius': 10, 'Speed': 10, 'Colour': grey, 'Health': 15, 'Bullet_Damage': 5, 'Sheild_Damage': 15, 'Bullet_rate':4, 'Shoot_range':30, 'Bullet_Speed':6, 'Bullet_Spray':1.5, 'Melee_Damage':10, 'Block_Damage':0.5} #Sheild Breaker
npc3 = {'Radius': 19, 'Speed': 4, 'Colour': magenta, 'Health': 300, 'Bullet_Damage': 7, 'Sheild_Damage': 2, 'Bullet_rate':10, 'Shoot_range':200, 'Bullet_Speed':6, 'Bullet_Spray':0.3, 'Melee_Damage':2, 'Block_Damage':0.5} #Doc
npc4 = {'Radius': 10, 'Speed': 3, 'Colour': green, 'Health': 200, 'Bullet_Damage': 35, 'Sheild_Damage': 2, 'Bullet_rate':30, 'Shoot_range':800, 'Bullet_Speed':20, 'Bullet_Spray':0, 'Melee_Damage':2, 'Block_Damage':0.5} #Sniper
npc5 = {'Radius': 15, 'Speed': 3, 'Colour': yellow, 'Health': 100, 'Bullet_Damage': 2, 'Sheild_Damage': 1, 'Bullet_rate':10, 'Shoot_range':200, 'Bullet_Speed':8, 'Bullet_Spray':0.5, 'Melee_Damage':2, 'Block_Damage':2} #Block Breaker

#Bullet Properties
Bullet_rad = 5
Exist_time = 10000
Freeze_Space = 15000
Shotgun_Spread_ang = 0.1
weapon1 = {'Damage':5, 'Speed':8, 'Spray':0.2, 'FireRate':50} #SMG
weapon2 = {'Damage':100, 'Speed':25, 'Spray':0.01, 'FireRate':1000} #High Power, Low Fire Rate
weapon3 = {'Damage':20, 'Speed':15, 'Spray':0.2, 'FireRate':1000} #Shotgun
weapon4 = {'Damage':0, 'Speed':0, 'Spray':0, 'FireRate':30000}#Freeze Gun

#Power Ups
power1 = {'Colour':orange, 'Size':7, 'Active':False, 'Draw':False}#Sheild and Shoot
power2 = {'Colour':yellow, 'Size':7, 'Active':False, 'Draw':False}
power3 = {'Colour':blue, 'Size':7, 'Active':False,' Draw':False}

''' Object Classes '''
class NPC_1():
    def __init__(self, x_pos, y_pos, npc_rad, Speed, Colour, NPC_Health, Shoot_rate, NPC_Type, Shoot_range, Radius, Sheild_Damage, Melee_Damage, Bullet_speed, Bullet_damage, Bullet_spray, Block_Damage):
        self.Type = NPC_Type
        self.Radius = Radius
        self.Colour = Colour
        self.x = x_pos
        self.y = y_pos
        self.Speed = Speed
        self.Health = NPC_Health
        self.Block_Damage = Block_Damage
        self.Sheild_Damage = Sheild_Damage
        self.Melee_Damage = Melee_Damage
        self.Shoot_rate = Shoot_rate
        self.Shoot_dist = Shoot_range
        self.Bullet_Damage = Bullet_damage
        self.Bullet_speed = Bullet_speed
        self.Bullet_spray = Bullet_spray
        self.Velocity_x = 0
        self.Velocity_y = 0
    def Movement(self):
        if (self.x - player_x != 0) and (self.y - player_y != 0):
            self.Velocity_x = self.Speed*(-(self.x - player_x)/(abs(self.x - player_x)+abs(self.y - player_y)))
            self.Velocity_y = self.Speed*(-(self.y - player_y)/(abs(self.x - player_x)+abs(self.y - player_y)))
        else:
            self.Velocity_x = 0
            self.Velocity_y = 0
        self.x += self.Velocity_x
        self.y += self.Velocity_y
        pygame.draw.circle(Screen, self.Colour, (int(self.x), int(self.y)), self.Radius, Solid)
        pygame.draw.circle(Screen, black, (int(self.x), int(self.y)), self.Radius, 2)
    def Dodge(self):
        self.x += self.Velocity_x
        self.y += self.Velocity_y
        pygame.draw.circle(Screen, self.Colour, (int(self.x), int(self.y)), self.Radius, Solid)
        pygame.draw.circle(Screen, black, (int(self.x), int(self.y)), self.Radius, 2)
    def Still(self):
        pygame.draw.circle(Screen, self.Colour, (int(self.x), int(self.y)), self.Radius, Solid)
        pygame.draw.circle(Screen, black, (int(self.x), int(self.y)), self.Radius, 2)

class Bullet():
    def __init__(self,x_npc,y_npc,dx,dy,Bullet_rad,Colour,Speed,Damage,Exist_time,xspeed,yspeed):
        self.Bullet_rad = Bullet_rad
        self.x = x_npc
        self.y = y_npc
        self.Speed = Speed
        self.Colour = Colour
        self.Damage = Damage
        self.Velocity_x = self.Speed*(-dx/(abs(dx)+abs(dy)))
        self.Velocity_y = self.Speed*(-dy/(abs(dx)+abs(dy)))
        self.Exist_time = Exist_time
    def Position(self):
        self.x += self.Velocity_x
        self.y += self.Velocity_y
        pygame.draw.circle(Screen, self.Colour, (int(self.x), int(self.y)), self.Bullet_rad, Solid)
        pygame.draw.circle(Screen, black, (int(self.x), int(self.y)), self.Bullet_rad, 2)

class Block():
    def __init__(self,x_pos,y_pos,Block_size):
        self.x = x_pos
        self.y = y_pos
        self.Colour = grey
        self.Size = Block_size
        self.Health = 200
    def Draw(self):
        pygame.draw.rect(Screen, self.Colour, (self.x, self.y, self.Size, self.Size), Solid)
        pygame.draw.rect(Screen, black, (self.x, self.y, self.Size, self.Size), 2)

class Powerup():
    def __init__(self, radius, colour, poweruptype):
        xpos = randint(5, Screen_Width-5)
        ypos = randint(5, Screen_Height-5)
        self.x = int(xpos)
        self.y = int(ypos)
        self.radius = radius
        self.colour = colour
        self.type = poweruptype
    def Draw(self):
        pygame.draw.circle(Screen, self.colour, (self.x ,self.y), self.radius, Solid)
        pygame.draw.circle(Screen, black, (self.x ,self.y), self.radius, 2)

''' Collosions '''
def Collosion(Block_size, Radius, x, y, block_x, block_y, xspeed, yspeed):
    diffx = x - max(block_x - abs(xspeed), min(x, block_x + Block_size + abs(xspeed)))
    diffy = y - max(block_y - abs(yspeed), min(y, block_y + Block_size + abs(yspeed)))
    if (diffx*diffx + diffy*diffy) < Radius*Radius:
        if x < block_x and xspeed > 0:
            xspeed = -xspeed
            x = block_x - Radius
        elif x > block_x + Block_size and xspeed < 0:
            xspeed = -xspeed
            x = block_x + Block_size + Radius
        if y < block_y and yspeed > 0:
            yspeed = -yspeed
            y = block_y - Radius
        elif y > block_y + Block_size and yspeed < 0:
            yspeed = -yspeed
            y = block_y + Block_size + Radius
        return x, y, xspeed, yspeed
    return x, y, xspeed, yspeed

def BallCollosion(Radius1,Radius2,x1,y1,x2,y2):
    diffx = x1 - x2
    diffy = y1 - y2
    distance = math.hypot(diffx, diffy)
    if distance < Radius1 + Radius2:
        return True
    else:
        return False

''' Generating the Block Spawns '''
X_range = range(0, Screen_Width, Block_size)
Y_range = range(0, Screen_Height, Block_size)
for i in range(0,Block_number):
    X_value = choice(X_range)
    Y_value = choice(Y_range)
    for block in Block_array:
        if X_value == block.x and Y_value == block.y:
            Block_number += 1
            Overlap = True
            break
        else:
            Overlap = False

    if Overlap is False:
        block = Block(X_value, Y_value, Block_size)
        Block_array.append(block)

''' Start Screen '''
end_the_start = False
while end_the_start is False:
    Screen.fill(white)
    myfont = pygame.font.SysFont("Britannic Bold", 40)
    nlabel = myfont.render("WASD and 1234 does stuff and All Mouse Buttons do Things", 1, (255, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            end_the_start=True
    Screen.blit(nlabel,(50,Screen_Height/2))
    pygame.display.flip()

''' Running the Game '''
while True:
    counter += 1
    if counter > fps + 1:
        counter = 1

    if pygame.time.get_ticks() - lastfired_freeze > Freeze_Space:
        freeze = False

    if pygame.time.get_ticks() - last_dash > dash_time:
        dash = False

    ''' Creating NPCs '''
    if len(NPC_1_array) < NPC_Number and pygame.time.get_ticks() > Start_time:
        #Calculating the Random Starting Position
        x_y = choice([1,2])
        if x_y == 1: #This is for x_sides
            x = choice([-50, Screen_Width + 50])
            y = randint(0,Screen_Height)
        elif x_y == 2: #This is for y_sides
            y = choice([-50, Screen_Width + 50])
            x = randint(0,Screen_Width)

        if NPC_Number%6 == 0:
            npc_1 = NPC_1(x,y,npc2['Radius'],npc2['Speed'],npc2['Colour'],npc2['Health'],npc2['Bullet_rate'],2,npc2['Shoot_range'],npc2['Radius'],npc2['Sheild_Damage'],npc2['Melee_Damage'],npc2['Bullet_Speed'],npc2['Bullet_Damage'],npc2['Bullet_Spray'],npc2['Block_Damage'])
            NPC_1_array.append(npc_1)
        elif NPC_Number%3 == 0:
            npc_1 = NPC_1(x,y,npc3['Radius'],npc3['Speed'],npc3['Colour'],npc3['Health'],npc3['Bullet_rate'],3,npc3['Shoot_range'],npc3['Radius'],npc3['Sheild_Damage'],npc3['Melee_Damage'],npc3['Bullet_Speed'],npc3['Bullet_Damage'],npc3['Bullet_Spray'],npc3['Block_Damage'])
            NPC_1_array.append(npc_1)
        elif NPC_Number%4 == 0:
            npc_1 = NPC_1(x,y,npc4['Radius'],npc4['Speed'],npc4['Colour'],npc4['Health'],npc4['Bullet_rate'],4,npc4['Shoot_range'],npc4['Radius'],npc4['Sheild_Damage'],npc4['Melee_Damage'],npc4['Bullet_Speed'],npc4['Bullet_Damage'],npc4['Bullet_Spray'],npc4['Block_Damage'])
            NPC_1_array.append(npc_1)
        elif NPC_Number%5 == 0:
            npc_1 = NPC_1(x,y,npc5['Radius'],npc5['Speed'],npc5['Colour'],npc5['Health'],npc5['Bullet_rate'],5,npc5['Shoot_range'],npc5['Radius'],npc5['Sheild_Damage'],npc5['Melee_Damage'],npc5['Bullet_Speed'],npc5['Bullet_Damage'],npc5['Bullet_Spray'],npc5['Block_Damage'])
            NPC_1_array.append(npc_1)
        else:
            npc_1 = NPC_1(x,y,npc1['Radius'],npc1['Speed'],npc1['Colour'],npc1['Health'],npc1['Bullet_rate'],1,npc1['Shoot_range'],npc1['Radius'],npc1['Sheild_Damage'],npc1['Melee_Damage'],npc1['Bullet_Speed'],npc1['Bullet_Damage'],npc1['Bullet_Spray'],npc1['Block_Damage'])
            NPC_1_array.append(npc_1)

    ''' Receiving any Player Inputs '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_1:
                weapon = 1
            if event.key == pygame.K_2:
                weapon = 2
            if event.key == pygame.K_3:
                weapon = 3
            if event.key == pygame.K_4:
                weapon = 4

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                last_dash = pygame.time.get_ticks()
                dash = True
                xspeed = 4*player_speed*(-mouse_x/(abs(mouse_x)+abs(mouse_y)))
                yspeed = 4*player_speed*(-mouse_y/(abs(mouse_x)+abs(mouse_y)))

        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            key_state = pygame.key.get_pressed()

        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            mouse_state = pygame.mouse.get_pressed()

        if event.type == pygame.MOUSEBUTTONUP:
            Block_place = False

    ''' Managing Key Inputs '''
    if dash is False:
        if key_state != False:
            xspeed = player_speed*(key_state[100] - key_state[97])
            yspeed = player_speed*(key_state[115] - key_state[119])
            if abs(xspeed) == abs(yspeed):
                player_x += xspeed*Diagonal_Speed
                player_y += yspeed*Diagonal_Speed
            else:
                player_x += xspeed
                player_y += yspeed
    elif dash is True:
        player_x += xspeed
        player_y += yspeed

    ''' Managing Mouse Inputs '''
    Sheild = False
    mouse_pos = pygame.mouse.get_pos()
    mouse_x = player_x - mouse_pos[0]
    mouse_y = player_y - mouse_pos[1]

    #Note this is where the NPC Melee_Damage is Defined
    if mouse_state != False:
        if mouse_state[2] == 1:
            if Sheild_Health > 0:
                pygame.draw.circle(Screen,green,(int(player_x),int(player_y)),sheild_rad, 1)
                Sheild = True
                Melee_Damage = 0
            elif Sheild_Health < 0:
                Sheild = False
                Melee_Damage = 30

        for powerup in Powerup_array:
            if powerup_active is True:
                Sheild_Shoot = False
            elif Sheild is True:
                Sheild_Shoot = True
            elif Sheild is False:
                Sheild_Shoot = False

        if mouse_state[0] == 1 and mouse_x != 0 and mouse_y != 0 and Sheild_Shoot is False:
            #SMG
            if weapon == 1:
                if pygame.time.get_ticks() - lastfired_smg > weapon1['FireRate']:
                    lastfired_smg = pygame.time.get_ticks()
                    player_bullet = Bullet(player_x, player_y, mouse_x + randint(-abs(int(weapon1['Spray']*mouse_x)),abs(int(weapon1['Spray']*mouse_x))), mouse_y + randint(-abs(int(weapon1['Spray']*mouse_y)),abs(int(weapon1['Spray']*mouse_y))), Bullet_rad, green, weapon1['Speed'], weapon1['Damage'], pygame.time.get_ticks(), xspeed, yspeed)
                    Player_Bullet_array.append(player_bullet)
            #Rifle
            if weapon == 2:
                if pygame.time.get_ticks() - lastfired_rifle > weapon2['FireRate']:
                    lastfired_rifle = pygame.time.get_ticks()
                    player_bullet = Bullet(player_x, player_y, mouse_x + randint(-abs(int(weapon2['Spray']*mouse_x)),abs(int(weapon2['Spray']*mouse_x))), mouse_y + randint(-abs(int(weapon2['Spray']*mouse_y)),abs(int(weapon2['Spray']*mouse_y))), Bullet_rad, green, weapon2['Speed'], weapon2['Damage'], pygame.time.get_ticks(), xspeed, yspeed)
                    Player_Bullet_array.append(player_bullet)
            #Shotgun
            if weapon == 3:
                if pygame.time.get_ticks() - lastfired_shotgun > weapon3['FireRate']:
                    lastfired_shotgun = pygame.time.get_ticks()
                    player_bullet = Bullet(player_x, player_y, mouse_x, mouse_y, Bullet_rad, green, weapon3['Speed'], weapon3['Damage'],pygame.time.get_ticks(), xspeed, yspeed)
                    Player_Bullet_array.append(player_bullet)
                    player_bullet = Bullet(player_x, player_y, mouse_x - abs(mouse_y*Shotgun_Spread_ang), mouse_y - abs(mouse_x*Shotgun_Spread_ang), Bullet_rad, green, weapon3['Speed'], weapon3['Damage'], pygame.time.get_ticks(), xspeed, yspeed)
                    Player_Bullet_array.append(player_bullet)
                    player_bullet = Bullet(player_x, player_y, mouse_x - 2*abs(mouse_y*Shotgun_Spread_ang), mouse_y - 2*abs(mouse_x*Shotgun_Spread_ang), Bullet_rad, green, weapon3['Speed'], weapon3['Damage'], pygame.time.get_ticks(), xspeed, yspeed)
                    Player_Bullet_array.append(player_bullet)
                    player_bullet = Bullet(player_x, player_y, mouse_x + abs(mouse_y*Shotgun_Spread_ang), mouse_y + abs(mouse_x*Shotgun_Spread_ang), Bullet_rad, green, weapon3['Speed'], weapon3['Damage'], pygame.time.get_ticks(), xspeed, yspeed)
                    Player_Bullet_array.append(player_bullet)
                    player_bullet = Bullet(player_x, player_y, mouse_x + 2*abs(mouse_y*Shotgun_Spread_ang), mouse_y + 2*abs(mouse_x*Shotgun_Spread_ang), Bullet_rad, green, weapon3['Speed'], weapon3['Damage'], pygame.time.get_ticks(), xspeed, yspeed)
                    Player_Bullet_array.append(player_bullet)
            #Freeze
            if weapon == 4:
                if pygame.time.get_ticks() - lastfired_freeze > weapon4['FireRate']:
                    lastfired_freeze = pygame.time.get_ticks()
                    freeze = True

    ''' Placing Blocks '''
    if mouse_state[1] == 1 and Blocks_given > 0 and Block_place is False:
        for thing1 in X_range:
            if mouse_pos[0] > thing1:
                Block_x = thing1

        for thing2 in Y_range:
            if mouse_pos[1] > thing2:
                Block_y = thing2

        for npc_1 in NPC_1_array:
            if Block_x < npc_1.x< Block_x + Block_size and Block_y < npc_1.y < Block_y + Block_size :
                NPC_1_array.remove(npc_1)
                NPC_Number += 1
                Player_Health += 10
                Sheild_Health += 10

        for block in Block_array:
            if Block_x == block.x and Block_y == block.y:
                Conflict = True
                break
            else:
                Conflict = False

        if Conflict is False:
            block = Block(Block_x, Block_y, Block_size)
            Block_array.append(block)
            Block_place = True
            Blocks_given += -1

    ''' Player Bullets '''
    for player_bullet in Player_Bullet_array:
        Player_Bullet_Deleted = False

        for block in Block_array:
            player_bullet.x, player_bullet.y, player_bullet.Velocity_x, player_bullet.Velocity_y = Collosion(Block_size, player_bullet.Bullet_rad, player_bullet.x, player_bullet.y, block.x, block.y, player_bullet.Velocity_x, player_bullet.Velocity_y)

        if player_bullet.x > Screen_Width or player_bullet.x < 0 or player_bullet.y > Screen_Height or player_bullet.y < 0:
            Player_Bullet_array.remove(player_bullet)
            Player_Bullet_Deleted = True

        if pygame.time.get_ticks() - player_bullet.Exist_time > Exist_time and Player_Bullet_Deleted is False:
            Player_Bullet_array.remove(player_bullet)

        player_bullet.Position()

    ''' NPCs bullet '''
    for npc_bullet in NPC_Bullet_array:
        NPC_Bullet_Deleted = False

        for block in Block_array:
            npc_bullet.x, npc_bullet.y, npc_bullet.Velocity_x, npc_bullet.Velocity_y = Collosion(Block_size, npc_bullet.Bullet_rad, npc_bullet.x, npc_bullet.y, block.x, block.y, npc_bullet.Velocity_x, npc_bullet.Velocity_y)

        if mouse_state != False:
            if mouse_state[2] == 1 and BallCollosion(sheild_rad, npc_bullet.Bullet_rad, npc_bullet.x, npc_bullet.y, player_x, player_y) is True:
                NPC_Bullet_array.remove(npc_bullet)
                NPC_Bullet_Deleted = True

        if NPC_Bullet_Deleted is False:
            if npc_bullet.x > Screen_Width or npc_bullet.x < 0 or npc_bullet.y > Screen_Height or npc_bullet.y < 0:
                NPC_Bullet_array.remove(npc_bullet)
                NPC_Bullet_Deleted = True

        if BallCollosion(player_rad, npc_bullet.Bullet_rad, npc_bullet.x, npc_bullet.y, player_x, player_y) and NPC_Bullet_Deleted is False:
            NPC_Bullet_array.remove(npc_bullet)
            Player_Health += -npc_bullet.Damage
            NPC_Bullet_Deleted = True

        if pygame.time.get_ticks() - npc_bullet.Exist_time > Exist_time and NPC_Bullet_Deleted is False:
            NPC_Bullet_array.remove(npc_bullet)

        npc_bullet.Position()

    ''' NPCs '''
    for npc_1 in NPC_1_array:
        if freeze is False:
            Dodge = False
            orginalx = npc_1.Velocity_x
            orginaly = npc_1.Velocity_y

            if BallCollosion(player_rad, npc_1.Shoot_dist, npc_1.x, npc_1.y, player_x, player_y) is True and counter%npc_1.Shoot_rate == 0:
                diffx_npc = npc_1.x - player_x
                diffy_npc = npc_1.y - player_y
                npc_bullet = Bullet(npc_1.x, npc_1.y, diffx_npc + randint(-abs(int(npc_1.Bullet_spray*diffx_npc)),abs(int(npc_1.Bullet_spray*diffx_npc))), diffy_npc + randint(-abs(int(npc_1.Bullet_spray*diffy_npc)), abs(int(npc_1.Bullet_spray*diffy_npc))), 5, black, npc_1.Bullet_speed, npc_1.Bullet_Damage, pygame.time.get_ticks(), 0, 0)
                NPC_Bullet_array.append(npc_bullet)

            if mouse_state != False:
                if mouse_state[2] == 1 and Sheild is True and BallCollosion(sheild_rad, npc_1.Radius, npc_1.x, npc_1.y, player_x, player_y) is True:
                    inside_x = -player_x + sheild_rad + npc_1.x - npc_1.Radius
                    inside_y = -player_y + sheild_rad + npc_1.y - npc_1.Radius
                    npc_1.x += inside_x
                    npc_1.y += inside_y
                    Sheild_Health += -npc_1.Sheild_Damage

            if BallCollosion(player_rad, npc_1.Radius, npc_1.x-5, npc_1.y-10, player_x, player_y) is True:
                Player_Health += -npc_1.Melee_Damage

            for block in Block_array:
                npc_1.x, npc_1.y, npc_1.Velocity_x, npc_1.Velocity_y = Collosion(Block_size, npc_1.Radius, npc_1.x, npc_1.y, block.x, block.y, npc_1.Velocity_x, npc_1.Velocity_y)
            '''
            print(Dodge)
            if npc_1.Velocity_x + orginalx == 0:
                npc_1.Velocity_y = npc_1.Speed
                Dodge = True
                print('x')
            if npc_1.Velocity_y + orginaly == 0:
                npc_1.Velocity_x = npc_1.Speed
                Dodge = True
                print('y')
            print(Dodge)

            if Dodge is True:
                npc_1.Dodge()
            else:
                '''
            npc_1.Movement()
        else:
            npc_1.Still()

        myfont = pygame.font.SysFont('Comic Sans MS', 10)
        textsurface = myfont.render(str(npc_1.Health), False, HealthColour)
        Screen.blit(textsurface,(npc_1.x-5, npc_1.y))

        #Collosions with PLayer_Bullet
        for player_bullet in Player_Bullet_array:
            if BallCollosion(npc_1.Radius, Bullet_rad, npc_1.x, npc_1.y, player_bullet.x, player_bullet.y) is True:
                Player_Bullet_array.remove(player_bullet)
                npc_1.Health += -player_bullet.Damage

        #Checking if the NPC should die
        if npc_1.Health < 0:
            NPC_1_array.remove(npc_1)
            NPC_Number += 1
            Player_Health += 10
            Sheild_Health += 10
            Blocks_given += 1

    ''' Blocks '''
    for block in Block_array:
        block.Draw()
        #Block Health
        if block.Health < 0:
            Block_array.remove(block)
        #Checking for player Collosion
        if mouse_state[2] == 1:
            player_x, player_y, xspeed, yspeed = Collosion(Block_size, sheild_rad, player_x, player_y, block.x, block.y, xspeed, yspeed)
        else:
            player_x, player_y, xspeed, yspeed = Collosion(Block_size, player_rad, player_x, player_y, block.x, block.y, xspeed, yspeed)

    ''' Power Ups '''
    if pygame.time.get_ticks() - last_powerup > powerup_extent:
        powerup_active = False

    if powerup_active == False and pygame.time.get_ticks() - last_powerup > powerup_spacing and len(Powerup_array) == 0:
        pickone = randint(1,3)
        pickone = 1
        if pickone == 1:
            powerup = Powerup(power1['Size'], power1['Colour'], 1)
            Powerup_array.append(powerup)
        if pickone == 2:
            powerup = Powerup(power2['Size'], power2['Colour'], 2)
            Powerup_array.append(powerup)
        if pickone == 3:
            powerup = Powerup(power3['Size'], power3['Colour'], 3)
            Powerup_array.append(powerup)

    for powerup in Powerup_array:
        powerup.Draw()
        if powerup.type == 1:
            if player_x - player_rad < powerup.x < player_x + player_rad and player_y - player_rad < powerup.y < player_y + player_rad:
                powerup_active = True
                last_powerup = pygame.time.get_ticks()
                Powerup_array.remove(powerup)
        elif powerup.type == 2:
            if player_x - player_rad < powerup.x < player_x + player_rad and player_y - player_rad < powerup.y < player_y + player_rad:
                powerup_active = True
                last_powerup = pygame.time.get_ticks()
                Powerup_array.remove(powerup)
        elif powerup.type == 3:
            if player_x - player_rad < powerup.x < player_x + player_rad and player_y - player_rad < powerup.y < player_y + player_rad:
                powerup_active = True
                last_powerup = pygame.time.get_ticks()
                Powerup_array.remove(powerup)

    ''' Player '''
    #Collosion with Boundary
    if player_x < player_rad:
        player_x = player_rad
    elif  player_y < player_rad:
        player_y = player_rad
    elif player_x > Screen_Width - player_rad:
        player_x = Screen_Width - player_rad
    elif  player_y > Screen_Height - player_rad:
        player_y = Screen_Height - player_rad

    if Player_Health > 0:
        pygame.draw.circle(Screen,red,(int(player_x),int(player_y)),player_rad, Solid)
        pygame.draw.circle(Screen,black,(int(player_x),int(player_y)),player_rad, 2)
    else:
        print('You only killed '+str(NPC_Number - 1)+' Bots, Pls Git Gud')
        break

    ''' Writing the Stats '''
    myfont = pygame.font.SysFont('Comic Sans MS', 25)
    textsurface = myfont.render('  Players Health:'+str(Player_Health)+'   Sheilds Health:'+str(Sheild_Health)+'   NPC Number:'+str(len(NPC_1_array))+'   Blocks Available:'+str(Blocks_given), False, black)
    Screen.blit(textsurface,(0,0))

    ''' Updating Changes to the Screen '''
    pygame.display.flip()
    Screen.fill(white)
    Clock.tick(fps)
