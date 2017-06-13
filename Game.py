import pygame
import math
import time
from random import randint, choice

''' Things that need Adding/Fixing '''
#NPC Collosion with the sheild
#Collosion with the BLcoks in Y-Plane
#Being able to shoot diagonally between blocks
#Bots not colliding with each othe
#The Health of each NPC as a number ontop of it
#A Start Screen
#Take you to a death screen where you can reatart after dieing
#Power up where you can sheild and shoot at the same time
#NPC can clip then shoot through blocks
#Have weapon 2 Shot on click
#Stop blocks spawning on top of each other


''' Variable Managment '''
#Colour libary
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
pink = (255,105,180)
orange = (255,165,0)
yellow = (255,255,0)
magenta = (255,0,255)
grey = (128,128,128)
white = (255,255,255)

#Screen display deminsions
(Screen_Width,Screen_Height) = (920,720) #Note this Both need to be Multiples of 60
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
counter = 0
weapon = 1
Block_place = False
key_state = False
Move = False

#Player and NPcs Properties
player_y = Screen_Height/2
player_x = Screen_Width/2
player_rad = 15
sheild_rad = 30
Blocks_given = 5
NPC_Number = 1
Player_Health = 100
Sheild_Health = 100
Diagonal_Speed = 0.7
Start_time = 10000

#Different NPCs *Note that all the Radius must be Integers
npc1 = {'Radius': 15, 'Speed': 6, 'Colour': blue, 'Health': 100, 'Bullet_Damage': 5, 'Sheild_Damage': 1, 'Bullet_rate':10, 'Shoot_range':200, 'Bullet_Speed':8, 'Bullet_Spray':0.5,'Melee_Damage':0,'Block_Damage':0.5} #Default
npc2 = {'Radius': 10, 'Speed': 10, 'Colour': pink, 'Health': 15, 'Bullet_Damage': 5, 'Sheild_Damage': 15, 'Bullet_rate':4, 'Shoot_range':30, 'Bullet_Speed':6, 'Bullet_Spray':1.5,'Melee_Damage':5,'Block_Damage':0.5} #Sheild Breaker
npc3 = {'Radius': 20, 'Speed': 4, 'Colour': magenta, 'Health': 300, 'Bullet_Damage': 7, 'Sheild_Damage': 2, 'Bullet_rate':10, 'Shoot_range':200, 'Bullet_Speed':6, 'Bullet_Spray':0.3,'Melee_Damage':0,'Block_Damage':0.5} #Doc
npc4 = {'Radius': 10, 'Speed': 3, 'Colour': green, 'Health': 200, 'Bullet_Damage': 35, 'Sheild_Damage': 2, 'Bullet_rate':30, 'Shoot_range':800, 'Bullet_Speed':20, 'Bullet_Spray':0,'Melee_Damage':0,'Block_Damage':0.5} #Sniper
npc5 = {'Radius': 15, 'Speed': 3, 'Colour': pink, 'Health': 100, 'Bullet_Damage': 2, 'Sheild_Damage': 1, 'Bullet_rate':10, 'Shoot_range':200, 'Bullet_Speed':8, 'Bullet_Spray':0.5,'Melee_Damage':0,'Block_Damage':2} #Block Breaker

#Bullet Properties
Bullet_rad = 5
Shotgun_Spread_ang = 30
weapon1 = {'Damage':5, 'Speed':8, 'Spray':0.2, 'FireRate':2} #Default
weapon2 = {'Damage':50, 'Speed':30, 'Spray':0.01, 'FireRate':30} #High Power, Low Fire Rate
weapon3 = {'Damage':15, 'Speed':8, 'Spray':0.2, 'FireRate':15} #Shotgun


#Block Properties
Block_size = 40
Block_number = 30
Block_x = [0]*Block_number
Block_y = [0]*Block_number

''' All the Object Classes '''
class Bullet():
    def __init__(self,x_npc,y_npc,dx,dy,Bullet_rad,Colour,Speed,Damage):
        self.Bullet_rad = Bullet_rad
        self.x = x_npc
        self.y = y_npc
        self.Speed = Speed
        self.Colour = Colour
        self.Damage = Damage
        self.Thickness = 1
        self.Velocity_x = self.Speed*(-dx/(abs(dx)+abs(dy)))
        self.Velocity_y = self.Speed*(-dy/(abs(dx)+abs(dy)))
    def Position(self):
        self.x += self.Velocity_x
        self.y += self.Velocity_y
        pygame.draw.circle(Screen, self.Colour, (int(self.x), int(self.y)), self.Bullet_rad, self.Thickness)

    '''
    def Invisible(self,faster):
        self.x += self.Velocity_x*faster
        self.y += self.Velocity_y*faster
        pygame.draw.circle(Screen, self.Colour, (int(self.x), int(self.y)), self.Bullet_rad, self.Thickness)
    '''

class NPC_1():
    def __init__(self,x_pos,y_pos,npc_rad,Speed,Colour,NPC_Health,Shoot_rate,NPC_Type,Shoot_range,Radius,Sheild_Damage,Melee_Damage,Bullet_speed,Bullet_damage,Bullet_spray,Block_Damage):
        #NPC Properties
        self.Type = NPC_Type
        self.Radius = Radius
        self.Colour = Colour
        self.x = x_pos
        self.y = y_pos
        self.Speed = Speed
        self.Health = NPC_Health

        #Its Shooting Properties
        self.Block_Damage = Block_Damage
        self.Sheild_Damage = Sheild_Damage
        self.Melee_Damage = Melee_Damage
        self.Shoot_rate = Shoot_rate
        self.Shoot_dist = Shoot_range
        self.Bullet_Damage = Bullet_damage
        self.Bullet_speed = Bullet_speed
        self.Bullet_spray = Bullet_spray

    def Movement(self):
        self.Velocity_x = self.Speed*(-(self.x - player_x)/(abs(self.x - player_x)+abs(self.y - player_y)))
        self.Velocity_y = self.Speed*(-(self.y - player_y)/(abs(self.x - player_x)+abs(self.y - player_y)))
        self.x += self.Velocity_x
        self.y += self.Velocity_y
        pygame.draw.circle(Screen, self.Colour, (int(self.x), int(self.y)), self.Radius, 1)

class Block():
    def __init__(self,x_pos,y_pos,Block_size):
        self.x = x_pos
        self.y = y_pos
        self.Colour = orange
        self.Size = Block_size #Note this is the Area of the Rectangle
        self.Health = 200
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

''' Things cus Pygame said so '''
pygame.init()
pygame.font.init()

''' Start Screen '''
end_the_start = False
while end_the_start is False:
    Screen.fill(white)
    myfont = pygame.font.SysFont("Britannic Bold", 40)
    nlabel = myfont.render("WASD does stuff and All Mouse Buttons do Things", 1, (255, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            end_the_start=True
    Screen.blit(nlabel,(110,Screen_Height/2))
    pygame.display.flip()

''' Running the Game '''
while True:
    #Used for tracking the loop (Used for Limiting Bullets)
    counter += 1
    if counter > fps:
        counter = 0

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

        if NPC_Number%1 == 0:
            npc_1 = NPC_1(x,y,npc1['Radius'],npc1['Speed'],npc1['Colour'],npc1['Health'],npc1['Bullet_rate'],1,npc1['Shoot_range'],npc1['Radius'],npc1['Sheild_Damage'],npc1['Melee_Damage'],npc1['Bullet_Speed'],npc1['Bullet_Damage'],npc1['Bullet_Spray'],npc1['Block_Damage'])
            NPC_1_array.append(npc_1)
        if NPC_Number%6 == 0:
            npc_1 = NPC_1(x,y,npc2['Radius'],npc2['Speed'],npc2['Colour'],npc2['Health'],npc2['Bullet_rate'],2,npc2['Shoot_range'],npc2['Radius'],npc2['Sheild_Damage'],npc2['Melee_Damage'],npc2['Bullet_Speed'],npc2['Bullet_Damage'],npc2['Bullet_Spray'],npc2['Block_Damage'])
            NPC_1_array.append(npc_1)
        if NPC_Number%4 == 0:
            npc_1 = NPC_1(x,y,npc3['Radius'],npc3['Speed'],npc3['Colour'],npc3['Health'],npc3['Bullet_rate'],3,npc3['Shoot_range'],npc3['Radius'],npc3['Sheild_Damage'],npc3['Melee_Damage'],npc3['Bullet_Speed'],npc3['Bullet_Damage'],npc3['Bullet_Spray'],npc3['Block_Damage'])
            NPC_1_array.append(npc_1)
        if NPC_Number%3 == 0:
            npc_1 = NPC_1(x,y,npc4['Radius'],npc4['Speed'],npc4['Colour'],npc4['Health'],npc4['Bullet_rate'],4,npc4['Shoot_range'],npc4['Radius'],npc4['Sheild_Damage'],npc4['Melee_Damage'],npc4['Bullet_Speed'],npc4['Bullet_Damage'],npc4['Bullet_Spray'],npc4['Block_Damage'])
            NPC_1_array.append(npc_1)
        if NPC_Number%2 == 0:
            npc_1 = NPC_1(x,y,npc5['Radius'],npc5['Speed'],npc5['Colour'],npc5['Health'],npc5['Bullet_rate'],4,npc5['Shoot_range'],npc5['Radius'],npc5['Sheild_Damage'],npc5['Melee_Damage'],npc5['Bullet_Speed'],npc5['Bullet_Damage'],npc5['Bullet_Spray'],npc5['Block_Damage'])
            NPC_1_array.append(npc_1)

    ''' Receiving any Player Inputs '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            break

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_1:
                weapon = 1
            if event.key == pygame.K_2:
                weapon = 2
            if event.key == pygame.K_3:
                weapon = 3

        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            key_state = pygame.key.get_pressed()
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            mouse_state = pygame.mouse.get_pressed()
        if event.type == pygame.MOUSEBUTTONUP:
            Block_place = False


    ''' Managing Key Inputs '''
    if key_state != False:
        xspeed = 6*(key_state[100] - key_state[97])
        yspeed = 6*(key_state[115] - key_state[119])
        if abs(xspeed) == abs(yspeed):
            player_x += xspeed*Diagonal_Speed
            player_y += yspeed*Diagonal_Speed
        else:
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
                Sheilf = False
                Melee_Damage = 30

        elif mouse_state[0] == 1:
            #Default Weapon
            if weapon == 1:
                if counter%weapon1['FireRate'] == 0:
                    player_bullet = Bullet(player_x, player_y, mouse_x + randint(-abs(int(weapon1['Spray']*mouse_x)),abs(int(weapon1['Spray']*mouse_x))), mouse_y + randint(-abs(int(weapon1['Spray']*mouse_y)),abs(int(weapon1['Spray']*mouse_y))), Bullet_rad, green, weapon1['Speed'], weapon1['Damage'])
                    Player_Bullet_array.append(player_bullet)
            #High Power, Low Fire Rate
            if weapon == 2:
                if counter%weapon2['FireRate'] == 0:
                    player_bullet = Bullet(player_x, player_y, mouse_x + randint(-abs(int(weapon2['Spray']*mouse_x)),abs(int(weapon2['Spray']*mouse_x))), mouse_y + randint(-abs(int(weapon2['Spray']*mouse_y)),abs(int(weapon2['Spray']*mouse_y))), Bullet_rad, green, weapon2['Speed'], weapon2['Damage'])
                    Player_Bullet_array.append(player_bullet)
            #Shootgun
            if weapon == 3:
                if counter%weapon3['FireRate'] == 0:
                    player_bullet = Bullet(player_x, player_y, mouse_x, mouse_y, Bullet_rad, green, weapon3['Speed'], weapon3['Damage'])
                    Player_Bullet_array.append(player_bullet)
                    player_bullet = Bullet(player_x, player_y, mouse_x - mouse_y*math.cos(math.radians(Shotgun_Spread_ang)), mouse_y - mouse_x*math.sin(math.radians(Shotgun_Spread_ang)), Bullet_rad, green, weapon3['Speed'], weapon3['Damage'])
                    Player_Bullet_array.append(player_bullet)
                    player_bullet = Bullet(player_x, player_y, mouse_x + mouse_y*math.sin(math.radians(Shotgun_Spread_ang)), mouse_y + mouse_x*math.sin(math.radians(Shotgun_Spread_ang)), Bullet_rad, green, weapon3['Speed'], weapon3['Damage'])
                    Player_Bullet_array.append(player_bullet)

    ''' Placing Blocks '''
    if mouse_state[1] == 1 and Blocks_given > 0 and Block_place is False:
        mouse_pos[0] #X_mouse
        mouse_pos[1] #Y_mouse
        for thing1 in X_range:
            if mouse_pos[0] > thing1:
                Block_x = thing1
        for thing2 in Y_range:
            if mouse_pos[1] > thing2:
                Block_y = thing2
        block = Block(Block_x, Block_y, Block_size)
        Block_array.append(block)
        Block_place = True
        Blocks_given += -1


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
        diffx_npc = npc_1.x - player_x
        diffy_npc = npc_1.y - player_y
        distance_player = math.hypot(diffx_npc, diffy_npc)

        '''
        #Shooting the tracker_bullet
        tracker_bullet = Bullet(npc_1.x, npc_1.y, diffx_npc, diffy_npc, 3, red, 8,0)
        Tracker_Bullet_array.append(tracker_bullet)
        '''

        #Shooting Real Bullets
        if distance_player < player_rad + npc_1.Radius + npc_1.Shoot_dist and counter%npc_1.Shoot_rate == 0:
            npc_bullet = Bullet(npc_1.x, npc_1.y, diffx_npc + randint(-abs(int(npc_1.Bullet_spray*diffx_npc)),abs(int(npc_1.Bullet_spray*diffx_npc))), diffy_npc + randint(-abs(int(npc_1.Bullet_spray*diffy_npc)), abs(int(npc_1.Bullet_spray*diffy_npc))), 5, black, npc_1.Bullet_speed, npc_1.Bullet_Damage)
            NPC_Bullet_array.append(npc_bullet)

        #Collosion with Player
        '''
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
        '''

        #Update the NPC Position
        npc_1.Movement()

        #Collosions with Blocks
        for block in Block_array:
            if (block.x - npc_1.Radius + 1 <= npc_1.x <= block.x + Block_size + npc_1.Radius - 1) and (block.y - npc_1.Radius + 1 <= npc_1.y <= block.y + Block_size + npc_1.Radius - 1):
                if npc_1.Velocity_x > 0:
                    npc_1.x = block.x - npc_1.Radius
                elif npc_1.Velocity_x < 0:
                    npc_1.x = block.x + Block_size + npc_1.Radius
                elif npc_1.Velocity_y > 0:
                    npc_1.y = block.y - npc_1.Radius
                elif npc_1.Velocity_y < 0:
                    npc_1.y = block.y + Block_size + npc_1.Radius
                block.Health += -npc_1.Block_Damage


        #Collosions with Sheild
        if mouse_state != False:
            if mouse_state[2] == 1 and Sheild is True and distance_player < sheild_rad + npc_1.Radius:
                npc_1.x = player_x + sheild_rad + npc_1.Radius
                npc_1.y = player_y + sheild_rad + npc_1.Radius
                Sheild_Health += -npc_1.Sheild_Damage

        #Collosions with Player
        if distance_player < player_rad + npc_1.Radius:
            Player_Health += -npc_1.Melee_Damage

        #Collosions with PLayer_Bullet
        for player_bullet in Player_Bullet_array:
            diffx_playerbullet = player_bullet.x - npc_1.x
            diffy_playerbullet = player_bullet.y - npc_1.y
            distance_playerbullet = math.hypot(diffx_playerbullet,diffy_playerbullet)
            if distance_playerbullet < npc_1.Radius + Bullet_rad:
                Player_Bullet_array.remove(player_bullet)
                npc_1.Health += -player_bullet.Damage

        #Checking if the NPC should die
        if npc_1.Health < 0:
            NPC_1_array.remove(npc_1)
            NPC_Number += 1
            Player_Health += 10
            Sheild_Health += 10
            Blocks_given += 1

        #Collosion wih each other

    ''' Tracker Bullet
    for tracker_bullet in Tracker_Bullet_array:
        tracker_bullet.Invisible(5)

        #To check if a Bullet needs Deleting
        Tracker_Deleted = False

        #Collosions with Blocks
        for block in Block_array:
            #Note the Velocities are here becasue these bullets move so godamn fast that the could partially morph through blocks in one frame
            if (block.x - tracker_bullet.Velocity_x <= tracker_bullet.x <= block.x + Block_size + tracker_bullet.Velocity_x) and (block.y - tracker_bullet.Velocity_y <= tracker_bullet.y <= block.y + Block_size + tracker_bullet.Velocity_y):
                Tracker_Bullet_array.remove(tracker_bullet)
                Tracker_Deleted = True
                break

        #Collosions with Boundary
        if Tracker_Deleted is False:
            if tracker_bullet.x > Screen_Width or tracker_bullet.x < 0 or tracker_bullet.y > Screen_Height or tracker_bullet.y < 0:
                Tracker_Bullet_array.remove(tracker_bullet)
                Tracker_Deleted = True
    '''



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
            if (block.x - npc_bullet.Bullet_rad <= npc_bullet.x <= block.x + Block_size + npc_bullet.Bullet_rad) and (block.y - npc_bullet.Bullet_rad <= npc_bullet.y <= block.y + Block_size + npc_bullet.Bullet_rad):
                if npc_bullet.Velocity_x > 0:
                    npc_bullet.x = block.x - npc_bullet.Bullet_rad
                    npc_bullet.Velocity_x = -npc_bullet.Velocity_x
                elif npc_bullet.Velocity_x < 0:
                    npc_bullet.x = block.x + Block_size + npc_bullet.Bullet_rad
                    npc_bullet.Velocity_x = -npc_bullet.Velocity_x
                elif npc_bullet.Velocity_y > 0:
                    npc_bullet.y = block.y - npc_bullet.Bullet_rad
                    npc_bullet.Velocity_y = -npc_bullet.Velocity_y
                elif npc_bullet.Velocity_y < 0:
                    npc_bullet.y = block.y + Block_size + npc_bullet.Bullet_rad
                    npc_bullet.Velocity_y = -npc_bullet.Velocity_y

        #Collosion with the Sheild
        if mouse_state != False:
            if mouse_state[2] == 1 and distance_npc_bullet < sheild_rad + npc_bullet.Bullet_rad:
                NPC_Bullet_array.remove(npc_bullet)
                NPC_Bullet_Deleted = True

        #Collosions with Boundary
        if NPC_Bullet_Deleted is False:
            if npc_bullet.x > Screen_Width or npc_bullet.x < 0 or npc_bullet.y > Screen_Height or npc_bullet.y < 0:
                NPC_Bullet_array.remove(npc_bullet)

        #Collosion with Player
        if distance_npc_bullet < player_rad + npc_bullet.Bullet_rad and NPC_Bullet_Deleted is False:
            NPC_Bullet_array.remove(npc_bullet)
            Player_Health += -npc_bullet.Damage


    ''' Blocks '''
    for block in Block_array:
        block.Draw()

        #Checking if Block Should be Broken
        if block.Health < 0:
            Block_array.remove(block)

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
    if Player_Health > 0:
        pygame.draw.circle(Screen,red,(int(player_x),int(player_y)),player_rad, 1)
    else:
        print('You only killed '+str(NPC_Number - 1)+' Bots, Pls Git Gud')
        break


    ''' Writing the Player Stats '''
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    textsurface = myfont.render('  Players Health: '+str(Player_Health)+'     Sheilds Health: '+str(Sheild_Health)+'     NPC Number: '+str(NPC_Number), False, black)
    Screen.blit(textsurface,(0,0))


    ''' Updating Changes to the Screen '''
    pygame.display.flip()
    Screen.fill(white)
    Clock.tick(fps)
