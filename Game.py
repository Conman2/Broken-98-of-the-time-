''' Import '''
import pygame
import math
import numpy
import random
import time

pygame.init()
pygame.font.init()

''' Variables '''
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
fps = 30
Clock = pygame.time.Clock()
(screen_width,screen_height) = (1400,1000) #Note this Both need to be Multiples of Block_size
screen = pygame.display.set_mode((screen_width, screen_height))

diagonal_multiplyer = 0.65
player_y = screen_height/2
player_x = screen_width/2
battlemoon_health = 100
battlemoon_orbit = 35
sheild_health = 100
block_number = 60

#Starting Conditions
rifle_owned = False
blocks_given = 3
turret_given = 1
weapon = 1

#Shapes
sheild_colour = green
block_size = 40
player_rad = 15
sheild_rad = 30
bullet_size = 5

#Timing
bullet_exist_time = 7000
freeze_duration = 10000
powerup_delay = 30000
wave_delay = 20000
dash_time = 300

#Array Shite
Powerup_array = []
Bullet_array = []
Turret_array = []
Block_array = []
Money_array = []
Shop_array = []
Bot_array = []

#Boolean Shite
finished = key_state = weapon_state = dash = freeze = reason_bot = reason_powerup = False

#Number Shite
weapon_1_fired = weapon_2_fired = weapon_3_fired = weapon_4_fired = weapon_5_fired = battlemoon_level = 0
battlemoon_angle = last_dash = player_speedx = player_speedy = powerup_active = wave_number = 0
mouse_state = (0,0,0)
counter = 1


''' Dictionaries '''
Bot = [
    #Radius, Speed, Colour, Health, Bullet Damage, Sheild Damage, Firerate, Range, Bullet Speed, Spray, Melee Damage, Block Damage
    [15, 6,  blue,    100, 5,  1,  10, 200, 8, 0.5, 2, 0.1], #Default        0
    [10, 10, grey,    20,  5,  15, 4,  30,  6, 0.5, 2, 0.1], #Sheild-Breaker 1
    [19, 4,  magenta, 300, 7,  2,  10, 200, 6, 0.5, 2, 0.1], #Doc            2
    [10, 3,  green,   200, 20, 2,  30, 600, 8, 0.5, 2, 0.1], #Sniper         3
    [15, 3,  yellow,  100, 2,  1,  10, 200, 8, 0.5, 2, 0.1]] #Block-Breaker  4

Weapon = [
    #Damage, Speed, Spray, Firerate, Name
    [4,   8,  0.1,  100,   'SMG'    ], #SMG     0
    [100, 25, 0.01, 1000,  'Sniper' ], #Sniper  1
    [25,  15, 0.1,  1000,  'Shotgun'], #Shotgun 2
    [50,  15, 0,    2000,  'Homing' ], #Homing  3
    [0,   0,  0,    30000, 'Freeze' ]] #Freeze  4

Powerup = [
    #Colour, Radius, Active, Draw
    [orange, 7], #Sheild and Shoot 0
    [yellow, 7], #Sheild Melee     1
    [blue,   7]] #Battlemoon       2

Shop = [
    #Name, Cost
    ['Rifle',      200], #0
    ['Shotgun',    150], #1
    ['Turret',     300], #2
    ['Health',     20 ], #3
    ['Armour',     20 ], #4
    ['Battlemoon', 200], #5
    ['Block',      150]] #6

Turret = [
    #Shootrate, Damage, Range, Spray, Speed, Colour
    [30,  5,  400,  0.2,  8 , grey  ], #Turret0
    [15,  18, 600,  0.01, 14, orange], #Turret1
    [15,  35, 800,  0,    18, red   ], #Turret2
    [10,  80, 1000, 0,    25, black ]] #Turret3

Battlemoon = [
    #Shootrate, Damage, Radius, Spray, Colour, Speed
    [30, 4,  300, 0.2,  grey  , 8 ], #Level0
    [30, 8,  400, 0.1,  green , 10], #Level1
    [15, 15, 500, 0.08, yellow, 12], #Level2
    [15, 25, 600, 0.05, orange, 14], #Level3
    [10, 35, 700, 0.01, red   , 16], #Level4
    [10, 50, 800, 0,    black , 18]] #Level5

''' Functions '''
def Blocks(Block_size, Radius, x, y, block_x, block_y, xspeed, yspeed):
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

def Balls(Radius1,Radius2,x1,y1,x2,y2):
    diffx = x1 - x2
    diffy = y1 - y2
    distance = math.hypot(diffx, diffy)
    if distance < Radius1 + Radius2:
        return True
    else:
        return False

''' Classes '''
class Bot():
    def __init__(self, bot_type):
        self.type = bot_type
        #Spawn Location
        position = random.choice([1,2])
        if position == 1:
            self.x = random.choice([-50, screen_width + 50])
            self.y = random.randint(0, screen_height)
        elif position == 2:
            self.x = random.randint(0, screen_width)
            self.y = random.choice([-50, screen_width + 50])
    def Move(self, Bot):
        self.velocity_x = Bot[self.type][1]*(-(self.x - player_x)/(abs(self.x - player_x)+abs(self.y - player_y)))
        self.velocity_y = Bot[self.type][1]*(-(self.y - player_y)/(abs(self.x - player_x)+abs(self.y - player_y)))
        self.x += self.Velocity_x
        self.y += self.Velocity_y
        pygame.draw.circle(screen, Bot[self.type][2], (int(self.x), int(self.y)), Bot[self.type][0], 0)
        pygame.draw.circle(screen, black, (int(self.x), int(self.y)), Bot[self.type][0], 2)
    def Still(self, Bot):
        pygame.draw.circle(screen, Bot[self.type][2], (int(self.x), int(self.y)), Bot[self.type][0], 0)
        pygame.draw.circle(screen, black, (int(self.x), int(self.y)), self.Radius, 2)

class Bullet():
    def __init__(self, speed, size, colour, x, y, dx, dy, bullet_type):
        self.type = bullet_type
        self.x = x
        self.y = y
        self.size = size
        self.colour = colour
        self.exist_time = pygame.time.get_ticks()
        self.velocity_x = speed*(-dx/(abs(dx)+abs(dy)))
        self.velocity_y = speed*(-dy/(abs(dx)+abs(dy)))
    def Move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, 0)
        pygame.draw.circle(screen, black, (int(self.x), int(self.y)), self.size, 2)

class Object():
    def __init__(self, x, y, size, colour, object_type):
        self.type = object_type
        self.x = x
        self.y = y
        self.size = size
        self.health = 100
        self.colour = colour
    def Block(self):
        pygame.draw.rect(screen, grey, (self.x, self.y, self.size, self.size), 0)
        pygame.draw.rect(screen, black, (self.x, self.y, self.size, self.size), 2)
    def Turret(self, Turret):
        pygame.draw.circle(screen, Turret[self.type][6], (int(self.x + block_size/2), int(self.y + block_size/2)), self.size, 0)
        pygame.draw.circle(screen, black, (int(self.x + block_size/2), int(self.y + block_size/2)), self.size, 2)
    def Powerup(self, Powerup):
        pygame.draw.circle(screen, Powerup[self.type][1], (int(self.x + block_size/2), int(self.y + block_size/2)), self.size, 0)
        pygame.draw.circle(screen, black, (int(self.x + block_size/2), int(self.y + block_size/2)), self.size, 2)
    def Money(self):
        dist_x = player_x - self.x
        dist_y = player_y - self.y
        if math.hypot(dist_x, dist_y) < 300:
            Speed = 500/math.hypot(dist_x, dist_y)
            self.Velocity_x = Speed*(-(self.x - player_x)/(abs(self.x - player_x)+abs(self.y - player_y)))
            self.Velocity_y = Speed*(-(self.y - player_y)/(abs(self.x - player_x)+abs(self.y - player_y)))
            self.x += self.Velocity_x
            self.y += self.Velocity_y
        pygame.draw.circle(screen, yellow, (int(self.x), int(self.y)), self.size, 0)
        pygame.draw.circle(screen, black, (int(self.x), int(self.y)), self.Size, 2)

''' Map Generation '''
x_range = range(0, screen_width,  block_size)
y_range = range(0, screen_height, block_size)
position = numpy.zeros((len(x_range), len(y_range)))
for i in range(0, block_number):
    while True:
        x_value = random.choice(x_range)
        y_value = random.choice(y_range)
        if position[int(x_value/block_size)][int(y_value/block_size)] ==  0:
            position[int(x_value/block_size)][int(y_value/block_size)] = 1
            block = Object(x_value, y_value, block_size, grey, 1)
            Block_array.append(block)
            break

''' Game '''
while True:
    counter += 1
    if counter > fps:
        counter = 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        ''' User Inputs '''
        if event.type == pygame.KEYUP or event.type == pygame.KEYDOWN:
            key_state = list(pygame.key.get_pressed())

        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            mouse_state = list(pygame.mouse.get_pressed())

    if key_state is not False:
        if key_state[pygame.K_1] == 1:
            weapon = last_weapon = 1
        elif key_state[pygame.K_2] == 1:
            weapon = last_weapon = 2
        elif key_state[pygame.K_3] == 1:
            weapon = last_weapon = 3
        elif key_state[pygame.K_4] == 1:
            weapon = last_weapon = 4
        elif key_state[pygame.K_5] == 1:
            weapon = 5
        elif key_state[pygame.K_6] == 1:
            weapon = 6

    ''' Player '''
    #Movement
    if dash is False and key_state != False:
        player_speedx = 7*(key_state[pygame.K_d] - key_state[pygame.K_a])
        player_speedy = 7*(key_state[pygame.K_s] - key_state[pygame.K_w])
        if key_state[pygame.K_SPACE] == 1:
            player_speedx = player_speedx*3
            player_speedy = player_speedy*3
            last_dash = pygame.time.get_ticks()
            key_state[pygame.K_SPACE] = 0
            dash = True
    elif pygame.time.get_ticks() - last_dash > dash_time:
        dash = False

    if abs(player_speedx) == abs(player_speedy):
        player_x += player_speedx*diagonal_multiplyer
        player_y += player_speedy*diagonal_multiplyer
    else:
        player_x += player_speedx
        player_y += player_speedy

    #Sheild
    if mouse_state[2] == 1 and sheild_health >= 0:
        pygame.draw.circle(screen, sheild_colour, (int(player_x),int(player_y)), sheild_rad, 3)
        if powerup_active != 1:
            sheild_active = True
    else:
        sheild_active = False

    #Weapons
    mouse_pos = pygame.mouse.get_pos()
    mouse_pos_x = player_x - mouse_pos[0]
    mouse_pos_y = player_y - mouse_pos[1]
    if mouse_state[0] == 1 and sheild_active is False:
        #SMG
        if weapon == 1 and pygame.time.get_ticks() - weapon_1_fired > Weapon[0][3]:
            weapon_1_fired = pygame.time.get_ticks()
            bullet = Bullet(Weapon[0][1], bullet_size, green, player_x, player_y, mouse_pos_x + random.randint(-abs(int(Weapon[0][2]*mouse_pos_y)), abs(int(Weapon[0][2]*mouse_pos_y))), mouse_pos_y + random.randint(-abs(int(Weapon[0][2]*mouse_pos_x)), abs(int(Weapon[0][2]*mouse_pos_x))), 1)
            Bullet_array.append(bullet)
        #Sniper-rifle
        elif weapon == 2 and rifle_owned is True and pygame.time.get_ticks() - weapon_2_fired > Weapon[1][3]:
            weapon_2_fired = pygame.time.get_ticks()
            bullet = Bullet(Weapon[1][1], bullet_size, green, player_x, player_y, mouse_pos_x + random.randint(-abs(int(Weapon[1][2]*mouse_pos_y)), abs(int(Weapon[1][2]*mouse_pos_y))), mouse_pos_y + random.randint(-abs(int(Weapon[1][2]*mouse_pos_x)), abs(int(Weapon[1][2]*mouse_pos_x))), 1)
            Bullet_array.append(bullet)
        #Shotgun
        elif weapon == 3 and shotgun_owned is False and pygame.time.get_ticks() - weapon_3_fired > Weapon[2][3]:
            weapon_3_fired = pygame.time.get_ticks()
            bullet = Bullet(Weapon[2][1], bullet_size, green, player_x, player_y, mouse_pos_x + random.randint(-abs(int(Weapon[2][2]*mouse_pos_y)), abs(int(Weapon[2][2]*mouse_pos_y))), mouse_pos_y + random.randint(-abs(int(Weapon[2][2]*mouse_pos_x)), abs(int(Weapon[2][2]*mouse_pos_x))), 1)
            Bullet_array.append(bullet)
        #Homing
        elif weapon == 4 and homing is True and pygame.time.get_ticks() - weapon_4_fired > Weapon[3][3]:
            weapon_4_fired = pygame.time.get_ticks()
            bullet = Bullet(Weapon[3][1], bullet_size, green, player_x, player_y, mouse_pos_x + random.randint(-abs(int(Weapon[4][3]*mouse_pos_y)), abs(int(Weapon[4][3]*mouse_pos_y))), mouse_pos_y + random.randint(-abs(int(Weapon[3][2]*mouse_pos_x)), abs(int(Weapon[3][2]*mouse_pos_x))), 1)
            Bullet_array.append(bullet)
        #Freeze
        elif weapon == 5 and freezes_owned > 0 and pygame.time.get_ticks() - weapon_5_fired > Weapon[4][3]:
            freeze = True
            weapon_5_fired = pygame.time.get_ticks()

        #Ending the Freeze
        if pygame.time.get_ticks() - weapon_5_fired > freeze_duration:
            freeze = False

    ''' Placing '''
    #Blocks
    if mouse_state[1] == 1 and blocks_given > 0:
        for thing1 in x_range:
            if mouse_pos[0] > thing1:
                block_x = thing1

        for thing2 in y_range:
            if mouse_pos[1] > thing2:
                block_y = thing2

        if position[int(block_x/block_size)][int(block_y/block_size)] == 0:
            position[int(block_x/block_size)][int(block_y/block_size)] = 1
            block = Object(block_x, block_y, block_size, 0, grey)
            Block_array.append(block)
            mouse_state[1] = 0

            for bot in Bot_array:
                if block_x < bot.x < block_x + block_size and block_y < bot.y < block_y + block_size :
                    Bot_array.remove(bot)

    #Turrets
    elif mouse_state[0] == 1 and turret_given > 0 and weapon == 6 is True:
        for thing3 in x_range:
            if mouse_pos[0] > thing3:
                turret_x = thing3

        for thing4 in y_range:
            if mouse_pos[1] > thing4:
                turret_y = thing4

        if positions[int(turret_x/Block_size)][int(turret_y/Block_size)] == 0:
            positions[int(turret_x/Block_size)][int(turret_y/Block_size)] = 3
            weapon = last_weapon
            turret = Object()
            Turret_array.append(turret)
            Turret_given += -1

    ''' Bullets '''
    for bullet in Bullet_array:
        #Block Collision
        for block in Block_array:
            bullet.x, bullet.y, bullet.velocity_x, bullet.velocity_y, _ = Blocks(block_size, bullet.size, bullet.x, bullet.y, block.x, block.y, bullet.velocity_x, bullet.velocity_y)

        #Shop Collision
        for shop in Shop_array:
            bullet.x, bullet.y, bullet.velocity_x, bullet.velocity_y, _ = Blocks(block_size, bullet.size, bullet.x, bullet.y, block.x, block.y, bullet.velocity_x, bullet.velocity_y)

        #Edge of map despawn
        if bullet.x > screen_width or bullet.x < 0 or bullet.y > screen_height or bullet.y < 0:
            Bullet_array.remove(bullet)

        #Maximium life reached
        if pygame.time.get_ticks() - bullet.exist_time > bullet_exist_time:
            Bullet_array.remove(bullet)

        #Bot Bullets only
        if bullet.type == 2:
            #Collision with sheild
            if mouse_state[2] is True and Balls(sheild_rad, npc_bullet.Bullet_rad, npc_bullet.x, npc_bullet.y, player_x, player_y) is True:
                Bullet_array.remove(bullet)

            #Collision with player
            elif Balls(player_rad, npc_bullet.Bullet_rad, npc_bullet.x, npc_bullet.y, player_x, player_y) is True:
                Bullet_array.remove(bullet)

        bullet.Move()

    ''' NPCs '''
    #Wave Spawning
    if len(Bot_array) == 0 and reason_bot is False:
        reason_bot = True
        delay_bot = pygame.time.get_ticks()

    if len(Bot_array) == 0 and pygame.time.get_ticks() - delay_bot > wave_delay:
        reason_bot = False
        wave_number += 1
        for thing in range(0, wave_number):
            #Bot 1
            bot = Bot(0)
            Bot_array.append(bot)

            #Bot 2
            if thing%2 == 0:
                bot = Bot(1)
                Bot_array.append(bot)

            #Bot 3
            if thing%3 == 0:
                bot = Bot(2)
                Bot_array.append(bot)

            #Bot 4
            if thing > 4 and thing%4 == 0:
                bot = Bot(3)
                Bot_array.append(bot)

            #Bot 5
            if thing > 5 and thing%5 == 0:
                bot = Bot(4)
                Bot_array.append(bot)

    #Updating them
    for bot in Bot_array:
        if freeze is False:
            bot.Move(Bot)
            #Should the bot Shoot
            if Balls(player_rad, Bot[bot.type][0], bot.x, bot.y, player_x, player_y) is True and counter%Bot[bot.type][6] == 0:
                bullet = (Bot[bot.type][8], bullet_size, bot_bullet_colour, bot.x, bot.y, (bot.x - player_x), (bot.y - player_y), 2)
                Bullet_array.append(bullet)

            #Collosion with Sheild
            if Balls(sheild_rad, Bot[bot.type][0], bot.x, bot.y, player_x, player_y) is True and sheild_active is True:
                #Create a function for deflections of ball on ball
                sheild_health += -Bot[bot.type][5]

            #Collosion with Player
            elif Balls(player_rad, Bot[bot.type][0], bot.x, bot.y, player_x, player_y) is True:
                 #Create a function for deflections of ball on ball
                 player_health += -Bot[bot_type][10]

            for block in Block_array:
                bot.x, bot.y, bot.velocity_x, bot.velocity_y, Hit = Blocks(block_size, Bot[bot.type][0], bot.x, bot.y, block.x, block.y, bot.velocity_x, bot.velocity_y)
                if Hit is True:
                    block.health += -bot[bot.type][11]
                    if block.Health <= 0:
                        position[int(block.x/block_size)][int(block.y/block_size)] = 0
                        Block_array.remove(block)

            for shop in Shop_array:
                bot.x, bot.y, bot.velocity_x, bot.velocity_y, _ = Blocks(block_size, Bot[bot.type][0], bot.x, bot.y, block.x, block.y, bot.velocity_x, bot.velocity_y)
        else:
            bot.Still(Bot)

    ''' PowerUps '''
    #Spawning the Powerups
    if len(Powerup_array) == 0 and reason_powerup is False:
        reason_powerup = True
        delay_powerup = pygame.time.get_ticks()

    if len(Powerup_array) == 0 and pygame.time.get_ticks() - delay_powerup > powerup_delay:
        reason_powerup = False
        while True:
            powerup_x = random.choice(x_range)
            powerup_y = random.choice(y_range)
            if position[int(powerup_x/block_size)][int(powerup_y/block_size)] == 0:
                position[int(powerup_x/block_size)][int(powerup_y/block_size)] = 1
                pickone = random.randint(0,2)
                powerup = Object(power_x, power_y, Powerup[pickone][1], 1, Powerup[pickone][0])
                Powerup_array.append(powerup)
                break

    #Activating Powerups
    for powerup in Powerup_array:
        if Balls(player_rad, Powerup[powerup.type][2], powerup.x, powerup.y, player_x, player_y) is True:
            position[int(powerup.x/block_size)][int(powerup.y/block_size)] = 0
            powerup_active_time = pygame.time.get_ticks()
            powerup_active = powerup.type
            Powerup_array.remove(powerup)
            if powerup_active == 1:
                sheild_colour = magenta
            elif powerup_active == 2:
                sheild_colour = oragne

        if pygame.time.get_ticks() - powerup_active_time > powerup_extent:
            sheild_colour = green
            powerup_active = 0

        powerup.Powerup(Powerup)

    #Battlemoon level
    if powerup_active == 3:
        battlemoon_health += 50
        battlemoon_level += 1
        powerup_active = 0

    if battlemoon_level > 0:
        #Moving the Moon
        battlemoon_angle += 7
        if battlemoon_angle >= 360:
            battlemoon_active = 0
        if battlemoon_level > 6:
            battlemoon_health += 50
            battlemoon_level = 6
        battlemoon_x = player_x + battlemoon_orbit*math.cos(math.radians(battlemoon_angle))
        battlemoon_y = player_y + battlemoon_orbit*math.sin(math.radians(battlemoon_angle))

        #Drawing
        pygame.draw.circle(screen, Battlemoon[battlemoon_level][5], (int(battlemoon_x), int(battlemoon_y)), 7, 0)
        pygame.draw.circle(screen, black, (int(battlemoon_x), int(battlemoon_y)), 7, 2)

        #Finding the Closest Bot
        distance = Battlemoon[battlemoon_level][2]
        battlemoon_shoot = False
        for bot in Bot_array:
            temp_distance_x = battlemoon_x - bot.x
            temp_distance_y = battlemoon_y - bot.y
            temp_distance = math.hypot(distance_x, distance_y)
            if temp_distance < distance:
                battlemoon_shoot = True
                distance_x = temp_distance_x
                distance_y = temp_distance_y

        #Shooting
        if battlemoon_shoot is True and counter%Battlemoon[battlemoon_level][1] is False:
                bullet = Bullet(Battlemoon[battlemoon_level][6], bullet_size, green, battlemoon_x, battlemoon_y, distance_x, distance_y, 1)
                Bullet_array.append(bullet)

        #Health
        if battlemoon_health <= 0:
            battlemoon_level = 0

    ''' Shop '''
    #Spawning
    if len(Shop_array) == 0:
        while True:
            shop_x = random.choice(x_range)
            shop_y = random.choice(y_range)
            if position[int(shop_x/block_size)][int(shop_y/block_size)] == 0:
                position[int(shop_x/block_size)][int(shop_y/block_size)] = 1
                shop = Object(shop_x, shop_y, block_size, blue, 1)
                Shop_array.append(shop)
                break

    #Updating
    for shop in Shop_array:
        shop.Block()

        if Blocks()
            position[int(shop.x/block_size)][int(shop.y/block_size)] = 0
            Shop_array.remove(shop)

    ''' Turret '''
    for turret in Turret_array:
        #Finding the Closest Bot
        turret_shoot = False
        distance = Turret[turret.type][3]
        for bot in Bot_array:
            temp_distance_x = battlemoon_x - bot.x
            temp_distance_y = battlemoon_y - bot.y
            temp_distance = math.hypot(distance_x, distance_y)
            if temp_distance < distance:
                turret_shoot = True
                distance_x = temp_distance_x
                distance_y = temp_distance_y

        #Shooting
        if turret_shoot is True and counter%Turret[turret.type][1] == 0:
            bullet = Bullet(Turret[turret.type][5], player_bullet_colour, turret.x, turret.y, distance_x, distance_y, 1)
            Bullet_array.append(bullet)

        #Collisions
        for bot in Bot_array:
            if Balls(turret.size, Bot[bot.type][1], bot.x, bot.y, turret.x, turret.y):
                turret.health +=  -Bot[bot.type][11]
                if turret.health <= 0:
                    position[int(turret.x/block_size)][int(turret.x/block_size)] = 0
                    Turret_array.remove(remove)

        turret.Turret(Turret)

    ''' Money '''
    for money in Money_array:
        money.Money(player_x, player_y)
        if Balls(money.size, player_rad, player_x, player_y, money.x, money.y) is True:
            player_money += 10
            Money_array.remove(money)

    ''' Block '''
    for block in Block_array:
        block.Block()
        if mouse_state[2] == 1:
            player_x, player_y, player_speedx, player_speedy, _ = Blocks(block_size, sheild_rad, player_x, player_y, block.x, block.y, player_speedx, player_speedy)
        else:
            player_x, player_y, player_speedx, player_speedy, _ = Blocks(block_size, player_rad, player_x, player_y, block.x, block.y, player_speedx, player_speedy)

    #Collosion with Boundary
    if player_x < player_rad:
        player_x = player_rad
    elif  player_y < player_rad:
        player_y = player_rad
    elif player_x > screen_width - player_rad:
        player_x = screen_width - player_rad
    elif  player_y > screen_height - player_rad:
        player_y = screen_height - player_rad

    pygame.draw.circle(screen, red, (int(player_x), int(player_y)), player_rad, 0)
    pygame.draw.circle(screen, black ,(int(player_x), int(player_y)), player_rad, 2)

    ''' Updating Changes to the Screen '''
    pygame.display.flip()
    pygame.display.set_caption('The Battleground')
    screen.fill(white)
    Clock.tick(fps)
