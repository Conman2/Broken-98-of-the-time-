import pygame
import math
import time
from random import randint, choice

pygame.init()
pygame.font.init()

''' Things that need Adding/Fixing '''
#Bots not colliding with each other
#Take you to a death screen where you can reatart after dieing
#shotgun triginometery
#Multiplayer
#powerup 2 doesn't work during freezing
#Player Collosion with enemies
#sliding across multiple blocks doesnt work (because the player asctually moves inside the block)
#Collisions with the corners of blocks (Should be taken into account with the new Collisions but isnt)
#wave system kinda in but not happy with it
#Add different levels of Turrets
#enemy with homing bullets
#a function for picking available x and y positions
#make it so you have to win each weapon

''' Variable Managment '''
#Initializing Variables
turret_time = battle_moon_level = lastfired_rifle = lastfired_shotgun = lastfired_smg = xspeed = yspeed = dx = dy = last_dash = Solid = last_powerup = angle = 0
battle_moon = Block_place = Turret_place = key_state = freeze = dash = Overlap = Conflict = Sheild_Shoot = powerup_active1 = powerup_active2 = False
counter = weapon = last_weapon = 1
lastfired_freeze = -30000
Player_Bullet_array = []
NPC_Bullet_array = []
Powerup_array = []
Block_array = []
NPC_1_array = []
Turret_array = []
mouse_state = (0,0,0)

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

#Game Properties
(Screen_Width,Screen_Height) = (1400,1000) #Note this Both need to be Multiples of 60
Screen = pygame.display.set_mode((Screen_Width, Screen_Height))
Clock = pygame.time.Clock()
fps = 30

#General Properties
player_y = Screen_Height/2
player_x = Screen_Width/2
player_rad = 15
player_speed = 8
sheild_rad = 30
Blocks_given = 5
Turret_given = 0
Player_Health = 100
Sheild_Health = 100
Diagonal_Speed = 0.7
Start_time = 15000
dash_time = 250
Block_size = 40
Block_number = 60
battle_moon_radius = 35
battle_moon_shoot = 400
battle_moon_health = 100

#Different NPCs *Note that all the Radius must be Integers
NPC_Number = 1
HealthColour = white
npc1 = {'Radius': 15, 'Speed': 6, 'Colour': blue, 'Health': 100, 'Bullet_Damage': 5, 'Sheild_Damage': 1, 'Bullet_rate':10, 'Shoot_range':200, 'Bullet_Speed':8, 'Bullet_Spray':0.5, 'Melee_Damage':2, 'Block_Damage':0.2} #Default
npc2 = {'Radius': 10, 'Speed': 10, 'Colour': grey, 'Health': 15, 'Bullet_Damage': 5, 'Sheild_Damage': 15, 'Bullet_rate':4, 'Shoot_range':30, 'Bullet_Speed':6, 'Bullet_Spray':1.5, 'Melee_Damage':10, 'Block_Damage':0.4} #Sheild Breaker
npc3 = {'Radius': 19, 'Speed': 4, 'Colour': magenta, 'Health': 300, 'Bullet_Damage': 7, 'Sheild_Damage': 2, 'Bullet_rate':10, 'Shoot_range':200, 'Bullet_Speed':6, 'Bullet_Spray':0.3, 'Melee_Damage':2, 'Block_Damage':0.4} #Doc
npc4 = {'Radius': 10, 'Speed': 3, 'Colour': green, 'Health': 200, 'Bullet_Damage': 35, 'Sheild_Damage': 2, 'Bullet_rate':30, 'Shoot_range':800, 'Bullet_Speed':15, 'Bullet_Spray':0, 'Melee_Damage':2, 'Block_Damage':0.4} #Sniper
npc5 = {'Radius': 15, 'Speed': 3, 'Colour': yellow, 'Health': 100, 'Bullet_Damage': 2, 'Sheild_Damage': 1, 'Bullet_rate':10, 'Shoot_range':200, 'Bullet_Speed':8, 'Bullet_Spray':0.5, 'Melee_Damage':2, 'Block_Damage':3} #Block Breaker

#Bullet Properties
Bullet_rad = 5
Exist_time = 7000
Freeze_Space = 15000
Shotgun_Spread_ang = 0.1
weapon1 = {'Damage':4, 'Speed':8, 'Spray':0.2, 'FireRate':100} #SMG
weapon2 = {'Damage':100, 'Speed':25, 'Spray':0.01, 'FireRate':1000} #High Power, Low Fire Rate
weapon3 = {'Damage':25, 'Speed':15, 'Spray':0.2, 'FireRate':1000} #Shotgun
weapon4 = {'Damage':0, 'Speed':0, 'Spray':0, 'FireRate':30000}#Freeze Gun

#Power Ups
powerup_extent = 10000
powerup_spacing = 30000
powerup_sheild_melee = 30
power1 = {'Colour':orange, 'Size':7, 'Active':False, 'Draw':False}#Sheild and Shoot
power2 = {'Colour':yellow, 'Size':7, 'Active':False, 'Draw':False}#Sheild Melee
power3 = {'Colour':blue, 'Size':7, 'Active':False,' Draw':False}#Spinning Ball

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
        self.Velocity_x = self.Velocity_y = 0
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

class Objects():
    def __init__(self, x_pos, y_pos, size, poweruptype, colour):
        self.x = x_pos
        self.y = y_pos
        self.colour = colour
        self.Size = size
        self.type = poweruptype
        self.Health = 100
        self.range = 400
        self.shootrate = 5
    def Block(self):
        pygame.draw.rect(Screen, self.colour, (self.x, self.y, self.Size, self.Size), Solid)
        pygame.draw.rect(Screen, black, (self.x, self.y, self.Size, self.Size), 2)
    def Powerup(self):
        pygame.draw.circle(Screen, self.colour, (int(self.x + Block_size/2), int(self.y + Block_size/2)), self.Size, Solid)
        pygame.draw.circle(Screen, black, (int(self.x + Block_size/2), int(self.y + Block_size/2)), self.Size, 2)
    def Turret(self):
        pygame.draw.circle(Screen, self.colour, (int(self.x + Block_size/2), int(self.y + Block_size/2)), self.Size, Solid)
        pygame.draw.circle(Screen, black, (int(self.x + Block_size/2), int(self.y + Block_size/2)), self.Size, 2)

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
        return x, y, xspeed, yspeed, True
    return x, y, xspeed, yspeed, False

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
    Overlap = False
    for block in Block_array:
        if X_value == block.x and Y_value == block.y:
            Block_number += 1
            Overlap = True
            break
        elif X_value == Screen_Width/2 and Y_value == Screen_Height/2:
            Block_number += 1
            Overlap = True
            break

    if Overlap is False:
        block = Objects(X_value, Y_value, Block_size, 0, grey)
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

    if NPC_Number%5 == 0:
        Start_time = pygame.time.get_ticks() + 60000

    if pygame.time.get_ticks() - turret_time > 45000:
        Turret_given += 1
        turret_time = pygame.time.get_ticks()

    ''' Creating NPCs '''
    if len(NPC_1_array) < NPC_Number and pygame.time.get_ticks() > Start_time:
        x_y = choice([1,2])
        if x_y == 1:
            x = choice([-50, Screen_Width + 50])
            y = randint(0,Screen_Height)
        elif x_y == 2:
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
            key_state = pygame.key.get_pressed()
            if event.key == pygame.K_1:
                weapon = 1
                last_weapon = 1
            elif event.key == pygame.K_2:
                weapon = 2
                last_weapon = 2
            elif event.key == pygame.K_3:
                weapon = 3
                last_weapon = 3
            elif event.key == pygame.K_4 and Blocks_given > 0:
                weapon = 4
            elif event.key == pygame.K_5 and Turret_given > 0:
                weapon = 5

        if event.type == pygame.KEYDOWN:
            key_state = pygame.key.get_pressed()
            if event.key == pygame.K_LSHIFT and key_state != False:
                xspeed = 3*player_speed*(key_state[100] - key_state[97])
                yspeed = 3*player_speed*(key_state[115] - key_state[119])
                last_dash = pygame.time.get_ticks()
                dash = True

        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            mouse_state = pygame.mouse.get_pressed()

        if event.type == pygame.MOUSEBUTTONUP:
            Block_place = False
            Turret_place = False

    ''' Managing Key Inputs '''
    if key_state != False and dash is False:
        xspeed = player_speed*(key_state[100] - key_state[97])
        yspeed = player_speed*(key_state[115] - key_state[119])
    if abs(xspeed) == abs(yspeed):
        player_x += xspeed*Diagonal_Speed
        player_y += yspeed*Diagonal_Speed
    else:
        player_x += xspeed
        player_y += yspeed

    ''' Placing Blocks '''
    if mouse_state[1] == 1 and Blocks_given > 0 and Block_place is False and weapon != 5:
        Conflict = False
        for thing1 in X_range:
            if mouse_pos[0] > thing1:
                Block_x = thing1

        for thing2 in Y_range:
            if mouse_pos[1] > thing2:
                Block_y = thing2

        for npc_1 in NPC_1_array:
            if Block_x < npc_1.x < Block_x + Block_size and Block_y < npc_1.y < Block_y + Block_size :
                NPC_1_array.remove(npc_1)
                NPC_Number += 1
                Player_Health += 10
                Sheild_Health += 10

        for block in Block_array:
            if Block_x == block.x and Block_y == block.y:
                Conflict = True
                break

        for turret in Turret_array:
            if turret.x == Block_x and turret.y == Block_y:
                Conflict = True
                break

        if Conflict is False:
            block = Objects(Block_x, Block_y, Block_size, 0, grey)
            Block_array.append(block)
            Block_place = True
            Blocks_given += -1

    ''' Placing Turret '''
    if mouse_state[1] == 1 and Turret_given > 0 and Turret_place is False and weapon == 5:
        Conflict_t = False
        for thing3 in X_range:
            if mouse_pos[0] > thing3:
                turret_x = thing3

        for thing4 in Y_range:
            if mouse_pos[1] > thing4:
                turret_y = thing4

        for block in Block_array:
            if turret_x == block.x and turret_y == block.y:
                Conflict_t = True
                break

        for turret in Turret_array:
            if turret.x == turret_x and turret.y == turret_y:
                Conflict_t = True
                break

        if Conflict_t is False:
            turret = Objects(turret_x, turret_y, 15, 0, magenta)
            Turret_array.append(turret)
            Turret_place = True
            Turret_given += -1
            weapon = last_weapon

    ''' Player Bullets '''
    for player_bullet in Player_Bullet_array:
        Player_Bullet_Deleted = False

        for block in Block_array:
            player_bullet.x, player_bullet.y, player_bullet.Velocity_x, player_bullet.Velocity_y, NaN = Collosion(Block_size, player_bullet.Bullet_rad, player_bullet.x, player_bullet.y, block.x, block.y, player_bullet.Velocity_x, player_bullet.Velocity_y)

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
            npc_bullet.x, npc_bullet.y, npc_bullet.Velocity_x, npc_bullet.Velocity_y, NaN = Collosion(Block_size, npc_bullet.Bullet_rad, npc_bullet.x, npc_bullet.y, block.x, block.y, npc_bullet.Velocity_x, npc_bullet.Velocity_y)

        if mouse_state[2] == 1 and BallCollosion(sheild_rad, npc_bullet.Bullet_rad, npc_bullet.x, npc_bullet.y, player_x, player_y) is True and mouse_state != False:
            NPC_Bullet_array.remove(npc_bullet)
            NPC_Bullet_Deleted = True

        if npc_bullet.x > Screen_Width or npc_bullet.x < 0 or npc_bullet.y > Screen_Height or npc_bullet.y < 0 and NPC_Bullet_Deleted is False:
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
            if BallCollosion(player_rad, npc_1.Shoot_dist, npc_1.x, npc_1.y, player_x, player_y) is True and counter%npc_1.Shoot_rate == 0:
                diffx_npc = npc_1.x - player_x
                diffy_npc = npc_1.y - player_y
                npc_bullet = Bullet(npc_1.x, npc_1.y, diffx_npc + randint(-abs(int(npc_1.Bullet_spray*diffx_npc)),abs(int(npc_1.Bullet_spray*diffx_npc))), diffy_npc + randint(-abs(int(npc_1.Bullet_spray*diffy_npc)), abs(int(npc_1.Bullet_spray*diffy_npc))), 5, black, npc_1.Bullet_speed, npc_1.Bullet_Damage, pygame.time.get_ticks(), 0, 0)
                NPC_Bullet_array.append(npc_bullet)

            if mouse_state[2] == 1 and Sheild is True and BallCollosion(sheild_rad, npc_1.Radius, npc_1.x, npc_1.y, player_x, player_y) is True and  mouse_state != False:
                npc_1.x += (-player_x + sheild_rad + npc_1.x - npc_1.Radius)
                npc_1.y += (-player_y + sheild_rad + npc_1.y - npc_1.Radius)
                if powerup_active2 is False:
                    Sheild_Health += -npc_1.Sheild_Damage
                else:
                    npc_1.Health += -powerup_sheild_melee

            if BallCollosion(player_rad, npc_1.Radius, npc_1.x-5, npc_1.y-10, player_x, player_y) is True:
                Player_Health += -npc_1.Melee_Damage

            for block in Block_array:
                npc_1.x, npc_1.y, npc_1.Velocity_x, npc_1.Velocity_y, Hit = Collosion(Block_size, npc_1.Radius, npc_1.x, npc_1.y, block.x, block.y, npc_1.Velocity_x, npc_1.Velocity_y)
                if Hit is True:
                    block.Health += -npc_1.Block_Damage
            npc_1.Movement()
        else:
            npc_1.Still()

        myfont = pygame.font.SysFont('Comic Sans MS', 10)
        textsurface = myfont.render(str(int(npc_1.Health)), False, HealthColour)
        Screen.blit(textsurface,(npc_1.x-10, npc_1.y-5))

        #Collosions with PLayer_Bullet
        for player_bullet in Player_Bullet_array:
            if BallCollosion(npc_1.Radius, Bullet_rad, npc_1.x, npc_1.y, player_bullet.x, player_bullet.y) is True:
                Player_Bullet_array.remove(player_bullet)
                npc_1.Health += -player_bullet.Damage

        #Checking if the NPC should die
        if npc_1.Health <= 0:
            NPC_1_array.remove(npc_1)
            NPC_Number += 1
            Player_Health += 10
            Sheild_Health += 10
            Blocks_given += 1

    ''' Power Ups '''
    if pygame.time.get_ticks() - last_powerup > powerup_extent:
        powerup_active1 = powerup_active2 = False

    if powerup_active1 is False and powerup_active2 is False and pygame.time.get_ticks() - last_powerup > powerup_spacing and len(Powerup_array) == 0:
        while True:
            Conflict_p = False
            power_x = choice(X_range)
            power_y = choice(Y_range)

            for block in Block_array:
                if power_x == block.x and power_y == block.y:
                    Conflict_p = True
                    break

            for turret in Turret_array:
                if turret.x == power_x and turret.y == power_x:
                    Conflict_p = True
                    break

            if Conflict_p is False:
                break

        pickone = randint(1,3)
        if pickone == 1:
            powerup = Objects(power_x, power_y, power1['Size'], 1, yellow)
            Powerup_array.append(powerup)
        if pickone == 2:
            powerup = Objects(power_x, power_y, power2['Size'], 2, orange)
            Powerup_array.append(powerup)
        if pickone == 3:
            powerup = Objects(power_x, power_y, power3['Size'], 3, blue)
            Powerup_array.append(powerup)

    for powerup in Powerup_array:
        powerup.Powerup()
        if powerup.type == 1 and player_x - player_rad < powerup.x + Block_size/2 < player_x + player_rad and player_y - player_rad < powerup.y + Block_size/2 < player_y + player_rad:
            powerup_active1 = True
            last_powerup = pygame.time.get_ticks()
            Powerup_array.remove(powerup)
        if powerup.type == 2 and player_x - player_rad < powerup.x + Block_size/2 < player_x + player_rad and player_y - player_rad < powerup.y + Block_size/2 < player_y + player_rad:
            powerup_active2 = True
            last_powerup = pygame.time.get_ticks()
            Powerup_array.remove(powerup)
        if powerup.type == 3 and player_x - player_rad < powerup.x + Block_size/2 < player_x + player_rad and player_y - player_rad < powerup.y + Block_size/2 < player_y + player_rad:
            last_powerup = pygame.time.get_ticks()
            battle_moon = True
            battle_moon_level += 1
            battle_moon_health += 100
            Powerup_array.remove(powerup)

    ''' Turrets '''
    for turret in Turret_array:
        turret.Turret()
        turret_diffx = turret_diffy = 2000
        for npc_1 in NPC_1_array:
            temp_turret_diffx = turret.x - npc_1.x
            temp_turret_diffy = turret.y - npc_1.y
            if math.hypot(temp_turret_diffx, temp_turret_diffy) < math.hypot(turret_diffx, turret_diffy):
                turret_diffx = temp_turret_diffx
                turret_diffy = temp_turret_diffy
            if BallCollosion(turret.size, npc_1.Radius, npc_1.x, npc_1.y, turret.x + Block_size/2, turret.y + Block_size/2) is True:
                npc_1.x += (-turret.x + turret.radius + npc_1.x - npc_1.Radius)
                npc_1.y += (-turret.y + turret.radius + npc_1.y - npc_1.Radius)
                turret.health += -npc_1.Melee_Damage

        if math.hypot(turret_diffx, turret_diffy) < 400 and counter%turret.shootrate == 0:
            player_bullet = Bullet(turret.x, turret.y, turret_diffx + randint(-abs(int(weapon1['Spray']*turret_diffx)),abs(int(weapon1['Spray']*turret_diffx))), turret_diffy + randint(-abs(int(weapon1['Spray']*turret_diffy)),abs(int(weapon1['Spray']*turret_diffy))), Bullet_rad, green, 1.3*weapon1['Speed'], 2*weapon1['Damage'], pygame.time.get_ticks(), xspeed, yspeed)
            Player_Bullet_array.append(player_bullet)

        if turret.health <= 0:
            Turret_array.remove(turret)

    ''' Blocks '''
    for block in Block_array:
        block.Block()
        if block.Health < 0:
            Block_array.remove(block)
        elif mouse_state[2] == 1:
            player_x, player_y, xspeed, yspeed, NaN = Collosion(Block_size, sheild_rad, player_x, player_y, block.x, block.y, xspeed, yspeed)
        else:
            player_x, player_y, xspeed, yspeed, NaN = Collosion(Block_size, player_rad, player_x, player_y, block.x, block.y, xspeed, yspeed)

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

    Sheild = False
    mouse_pos = pygame.mouse.get_pos()
    mouse_x = player_x - mouse_pos[0]
    mouse_y = player_y - mouse_pos[1]

    if mouse_state != False and mouse_state[2] == 1:
        if Sheild_Health > 0:
            if powerup_active2 is False:
                pygame.draw.circle(Screen,green,(int(player_x),int(player_y)),sheild_rad, 3)
            else:
                pygame.draw.circle(Screen,pink,(int(player_x),int(player_y)),sheild_rad, 2)
                pygame.draw.circle(Screen,orange,(int(player_x),int(player_y)),sheild_rad+3, 2)
                pygame.draw.circle(Screen,red,(int(player_x),int(player_y)),sheild_rad+3, 2)
            Sheild = True
            Melee_Damage = 0
        elif Sheild_Health < 0:
            Sheild = False
            Melee_Damage = 30

    Sheild_Shoot = Sheild
    if powerup_active1 is True:
        Sheild_Shoot = False

    if mouse_state[0] == 1 and mouse_x != 0 and mouse_y != 0 and Sheild_Shoot is False:
        #SMG
        if weapon == 1 and pygame.time.get_ticks() - lastfired_smg > weapon1['FireRate']:
            lastfired_smg = pygame.time.get_ticks()
            player_bullet = Bullet(player_x, player_y, mouse_x + randint(-abs(int(weapon1['Spray']*mouse_x)),abs(int(weapon1['Spray']*mouse_x))), mouse_y + randint(-abs(int(weapon1['Spray']*mouse_y)),abs(int(weapon1['Spray']*mouse_y))), Bullet_rad, green, weapon1['Speed'], weapon1['Damage'], pygame.time.get_ticks(), xspeed, yspeed)
            Player_Bullet_array.append(player_bullet)
        #Rifle
        if weapon == 2 and pygame.time.get_ticks() - lastfired_rifle > weapon2['FireRate']:
            lastfired_rifle = pygame.time.get_ticks()
            player_bullet = Bullet(player_x, player_y, mouse_x + randint(-abs(int(weapon2['Spray']*mouse_x)),abs(int(weapon2['Spray']*mouse_x))), mouse_y + randint(-abs(int(weapon2['Spray']*mouse_y)),abs(int(weapon2['Spray']*mouse_y))), Bullet_rad, green, weapon2['Speed'], weapon2['Damage'], pygame.time.get_ticks(), xspeed, yspeed)
            Player_Bullet_array.append(player_bullet)
        #Shotgun
        if weapon == 3 and pygame.time.get_ticks() - lastfired_shotgun > weapon3['FireRate']:
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
        if weapon == 4 and pygame.time.get_ticks() - lastfired_freeze > weapon4['FireRate']:
            lastfired_freeze = pygame.time.get_ticks()
            freeze = True
            weapon = last_weapon

    ''' Experimental Battle moon '''
    if battle_moon_health > 0 and battle_moon is True:
        diffx = diffy = 2000
        angle += 7
        if angle >= 360:
            angle = 0

        orb_x = player_x + battle_moon_radius*math.cos(math.radians(angle))
        orb_y = player_y + battle_moon_radius*math.sin(math.radians(angle))

        if battle_moon_level == 1:
            pygame.draw.circle(Screen, grey, (int(orb_x), int(orb_y)), 7, 0)
            pygame.draw.circle(Screen, black, (int(orb_x), int(orb_y)), 7, 2)
        if battle_moon_level == 2:
            pygame.draw.circle(Screen, green, (int(orb_x), int(orb_y)), 7, 0)
            pygame.draw.circle(Screen, black, (int(orb_x), int(orb_y)), 7, 2)
        if battle_moon_level == 3:
            pygame.draw.circle(Screen, yellow, (int(orb_x), int(orb_y)), 7, 0)
            pygame.draw.circle(Screen, black, (int(orb_x), int(orb_y)), 7, 2)
        if battle_moon_level == 4:
            pygame.draw.circle(Screen, orange, (int(orb_x), int(orb_y)), 7, 0)
            pygame.draw.circle(Screen, black, (int(orb_x), int(orb_y)), 7, 2)
        if battle_moon_level == 5:
            pygame.draw.circle(Screen, red, (int(orb_x), int(orb_y)), 7, 0)
            pygame.draw.circle(Screen, black, (int(orb_x), int(orb_y)), 7, 2)
        if battle_moon_level >= 6:
            pygame.draw.circle(Screen, black, (int(orb_x), int(orb_y)), 7, 0)
            pygame.draw.circle(Screen, black, (int(orb_x), int(orb_y)), 7, 2)

        for npc_1 in NPC_1_array:
            temp_diffx = orb_x - npc_1.x
            temp_diffy = orb_y - npc_1.y

            if BallCollosion(battle_moon_radius, npc_1.Radius, int(orb_x), int(orb_y), npc_1.x, npc_1.y) is True:
                battle_moon_health += -npc_1.Melee_Damage/2

            if math.hypot(temp_diffx, temp_diffy) < math.hypot(diffx, diffy):
                diffx = temp_diffx
                diffy = temp_diffy

        if math.hypot(diffx, diffy) < battle_moon_shoot:
            if battle_moon_level == 1 and counter%30 == 0: #SMG
                player_bullet = Bullet(orb_x, orb_y, diffx + randint(-abs(int(weapon1['Spray']*diffx)),abs(int(weapon1['Spray']*diffx))), diffy + randint(-abs(int(weapon1['Spray']*diffy)),abs(int(weapon2['Spray']*diffy))), Bullet_rad, green, weapon1['Speed'], weapon1['Damage']/3, pygame.time.get_ticks(), xspeed, yspeed)
                Player_Bullet_array.append(player_bullet)
            if battle_moon_level == 2 and counter%15 == 0: #SMG
                player_bullet = Bullet(orb_x, orb_y, diffx + randint(-abs(int(weapon1['Spray']*diffx)),abs(int(weapon1['Spray']*diffx))), diffy + randint(-abs(int(weapon1['Spray']*diffy)),abs(int(weapon2['Spray']*diffy))), Bullet_rad, green, weapon1['Speed'], weapon1['Damage']/2, pygame.time.get_ticks(), xspeed, yspeed)
                Player_Bullet_array.append(player_bullet)
            if battle_moon_level == 3 and counter%30 == 0: #Shotgun
                player_bullet = Bullet(orb_x, orb_y, diffx, diffy, Bullet_rad, green, weapon3['Speed'], weapon3['Damage'], pygame.time.get_ticks(), xspeed, yspeed)
                Player_Bullet_array.append(player_bullet)
                player_bullet = Bullet(orb_x, orb_y, diffx - abs(diffy*Shotgun_Spread_ang), diffy - abs(diffx*Shotgun_Spread_ang), Bullet_rad, green, weapon3['Speed'], weapon3['Damage']/1.5, pygame.time.get_ticks(), xspeed, yspeed)
                Player_Bullet_array.append(player_bullet)
                player_bullet = Bullet(orb_x, orb_y, diffx + abs(diffy*Shotgun_Spread_ang), diffy + abs(diffx*Shotgun_Spread_ang), Bullet_rad, green, weapon3['Speed'], weapon3['Damage']/1.5, pygame.time.get_ticks(), xspeed, yspeed)
                Player_Bullet_array.append(player_bullet)
            if battle_moon_level == 4 and counter%15 == 0: #Shotgun
                player_bullet = Bullet(orb_x, orb_y, diffx, diffy, Bullet_rad, green, weapon3['Speed'], weapon3['Damage'],pygame.time.get_ticks(), xspeed, yspeed)
                Player_Bullet_array.append(player_bullet)
                player_bullet = Bullet(orb_x, orb_y, diffx - abs(diffy*Shotgun_Spread_ang), diffy - abs(diffx*Shotgun_Spread_ang), Bullet_rad, green, weapon3['Speed'], weapon3['Damage'], pygame.time.get_ticks(), xspeed, yspeed)
                Player_Bullet_array.append(player_bullet)
                player_bullet = Bullet(orb_x, orb_y, diffx + abs(diffy*Shotgun_Spread_ang), diffy + abs(diffx*Shotgun_Spread_ang), Bullet_rad, green, weapon3['Speed'], weapon3['Damage'], pygame.time.get_ticks(), xspeed, yspeed)
                Player_Bullet_array.append(player_bullet)
                player_bullet = Bullet(orb_x, orb_y, diffx - 2*abs(diffy*Shotgun_Spread_ang), diffy - 2*abs(diffx*Shotgun_Spread_ang), Bullet_rad, green, weapon3['Speed'], weapon3['Damage'], pygame.time.get_ticks(), xspeed, yspeed)
                Player_Bullet_array.append(player_bullet)
                player_bullet = Bullet(orb_x, orb_y, diffx + 2*abs(diffy*Shotgun_Spread_ang), diffy + 2*abs(diffx*Shotgun_Spread_ang), Bullet_rad, green, weapon3['Speed'], weapon3['Damage'], pygame.time.get_ticks(), xspeed, yspeed)
                Player_Bullet_array.append(player_bullet)
            if battle_moon_level == 5 and counter%30 == 0: #Rifle
                player_bullet = Bullet(orb_x, orb_y, diffx + randint(-abs(int(weapon2['Spray']*diffx)),abs(int(weapon2['Spray']*diffx))), diffy + randint(-abs(int(weapon2['Spray']*diffy)),abs(int(weapon2['Spray']*diffy))), Bullet_rad, green, weapon2['Speed'], weapon2['Damage']/2, pygame.time.get_ticks(), xspeed, yspeed)
                Player_Bullet_array.append(player_bullet)
            if battle_moon_level >= 6 and counter%15 == 0: #Rifle
                player_bullet = Bullet(orb_x, orb_y, diffx + randint(-abs(int(weapon2['Spray']*diffx)),abs(int(weapon2['Spray']*diffx))), diffy + randint(-abs(int(weapon2['Spray']*diffy)),abs(int(weapon2['Spray']*diffy))), Bullet_rad, green, weapon2['Speed'], weapon2['Damage'], pygame.time.get_ticks(), xspeed, yspeed)
                Player_Bullet_array.append(player_bullet)

        if battle_moon_health <= 0:
            battle_moon_level = 0
            battle_moon = False

    ''' Writing the Stats '''
    if weapon4['FireRate'] - pygame.time.get_ticks() + lastfired_freeze > 0:
        freeze_left = int((weapon4['FireRate'] - pygame.time.get_ticks() + lastfired_freeze)/1000)
    else:
        freeze_left = 0

    myfont = pygame.font.SysFont('Comic Sans MS', 25)
    textsurface = myfont.render(' Players Health:'+str(Player_Health)+'  Sheilds Health:'+str(Sheild_Health)+'  NPC Number:'+str(len(NPC_1_array))+'  Blocks Available:'+str(Blocks_given)+'  Freeze:'+str(freeze_left)+'  Turrets Available:'+str(Turret_given), False, black)
    Screen.blit(textsurface,(0,0))

    ''' Updating Changes to the Screen '''
    pygame.display.flip()
    Screen.fill(white)
    Clock.tick(fps)
