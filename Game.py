import pygame
import os
import time
import math
import numpy
import random

pygame.init()
pygame.font.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=50)

''' Variables Managment '''
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
shake_screen = pygame.display.set_mode((screen_width, screen_height))

diagonal_multiplyer = 0.65
player_y = screen_height/2
player_x = screen_width/2
sheild_melee_damage = 15
battlemoon_health = 100
angle_increase = 0.025
battlemoon_orbit = 35
sheild_health = 100
player_health = 100
block_number = 60

#Starting Conditions
shotgun_owned = True
homing_owned = False
rifle_owned = True
freezes_owned = 0
player_money = 0
blocks_given = 3
turret_given = 0
weapon = 1

#Shapes
player_bullet_colour = green
bot_health_colour = white
bot_bullet_colour = black
sheild_colour = green
button_size = 120
turret_size = 18
block_size = 40
player_rad = 15
sheild_rad = 30
bullet_size = 5
powerup_rad = 10

#Timing
heart_beat_length = 15000
bullet_exist_time = 7000
freeze_duration = 10000
wave_time_length = 5000
powerup_extent = 15000
powerup_delay = 30000
wave_delay = 15000
dash_time = 300

#Image Libary
image_path = os.path.join(os.getcwd(), 'Image')
money_image = pygame.image.load(os.path.join(image_path, 'money.png'))
player_image = pygame.image.load(os.path.join(image_path, 'player.png'))
enemy_bullet_image = pygame.image.load(os.path.join(image_path, 'enemy_bullet.png'))
powerup_pink_image = pygame.image.load(os.path.join(image_path, 'powerup_pink.png'))
powerup_blue_image = pygame.image.load(os.path.join(image_path, 'powerup_blue.png'))
player_bullet_image = pygame.image.load(os.path.join(image_path, 'player_bullet.png'))
powerup_orange_image = pygame.image.load(os.path.join(image_path, 'powerup_orange.png'))

#Audio Libary
audio_path = os.path.join(os.getcwd(), 'Audio')
smg_sound = pygame.mixer.Sound(os.path.join(audio_path, 'smg.wav'))
shotgun_sound = pygame.mixer.Sound(os.path.join(audio_path, 'shotgun.wav'))
purchase_sound = pygame.mixer.Sound(os.path.join(audio_path, 'purchase.wav'))
sniper_sound = pygame.mixer.Sound(os.path.join(audio_path, 'sniper_rifle.wav'))
shop_entrance = pygame.mixer.Sound(os.path.join(audio_path, 'shop_entrance.wav'))
heart_beat_sound = pygame.mixer.Sound(os.path.join(audio_path, 'human-heartbeat.wav'))
battlemoon_shoot_sound = pygame.mixer.Sound(os.path.join(audio_path, 'battlemoon_shoot.wav'))

#Font Liabry
bot_health_font = pygame.font.SysFont('Comic Sans MS', 10)
shop_button_font = pygame.font.SysFont('Comic Sans MS', 25)
wave_number_font = pygame.font.SysFont('Comic Sans MS', 100)
weapon_selected_font = pygame.font.SysFont('Comic Sans MS', 30)

''' Initializing Random Shite '''
Powerup_array = []
Button_array = []
Bullet_array = []
Turret_array = []
Block_array = []
Money_array = []
Shop_array = []
Bot_array = []

finished = weapon_state = dash = freeze = reason_bot = reason_powerup = shop_collision = block_collision = sheild_n_shoot = False
battlemoon_angle = last_dash = player_speedx = player_speedy = wave_number = powerup_active_time = turret_level = 0
weapon_1_fired = weapon_2_fired = weapon_3_fired = weapon_4_fired = weapon_5_fired = 0
wave_time = -wave_time_length
counter = last_weapon = 1
player_hit_time = -500
heat_beat_time = -heart_beat_length
battlemoon_level = -1
powerup_active = 3

mouse_state = list(pygame.mouse.get_pressed())
key_state = list(pygame.key.get_pressed())

weapon_name = 'SMG'

''' Dictionaries (Well Matrices) '''
Shop = [
    #Name, Cost
    ['Rifle',      200], #0
    ['Shotgun',    150], #1
    ['Turret',     300], #2
    ['Health',     20 ], #3
    ['Armour',     20 ], #4
    ['Battlemoon', 200], #5
    ['Block',      150]] #6

Battlemoon = [
    #Shootrate, Damage, Range, Spray, Colour, Speed
    [30, 4,  300, 0.2,  grey  , 8 ], #Level0
    [30, 8,  400, 0.1,  green , 10], #Level1
    [15, 15, 500, 0.08, yellow, 12], #Level2
    [15, 25, 600, 0.05, orange, 14], #Level3
    [10, 35, 700, 0.01, red   , 16], #Level4
    [10, 50, 800, 0,    black , 18]] #Level5

Turret = [
    #Shootrate, Damage, Range, Spray, Speed, Colour
    [30,  5,  400,  0.2,  8 , grey  ], #Turret0
    [15,  18, 600,  0.01, 14, orange], #Turret1
    [15,  35, 800,  0,    18, red   ], #Turret2
    [10,  80, 1000, 0,    25, black ]] #Turret3

Weapon = [
    #Damage, Speed, Spray, Firerate, Name
    [8,   8,  0.1,  400,   'SMG'    ], #SMG     0
    [100, 25, 0.01, 2700,  'Sniper' ], #Sniper  1
    [25,  15, 0.1,  1300,  'Shotgun'], #Shotgun 2
    [50,  15, 0,    1000,  'Homing' ], #Homing  3
    [0,   0,  0,    30000, 'Freeze' ]] #Freeze  4

Item = [
    #x, y, colour, name, cost
    [60,  60,  red,     'Rifle'  ,      150], #0
    [240, 60,  yellow,  'Shotgun',      100], #1
    [420, 60,  pink,    'Turrets',      200], #2
    [600, 60,  green ,  'Health' ,      20 ], #3
    [780, 60,  magenta, 'Armour' ,      20 ], #4
    [60,  240, red,     'Battlemoon',   800], #5
    [240, 240, yellow,  'Block',        60 ], #6
    [420, 240, pink,    'Turret Level', 100], #7
    [600, 240, green,   'Homing',       200 ], #8
    [780, 240, magenta, 'Freezes',      40 ]] #9

Bot = [
    #Radius, Speed, Colour, Health, Bullet Damage, Sheild Damage, Firerate, Range, Bullet Speed, Spray, Melee Damage, Block Damage
    [15, 6,  blue,    100, 5,  1,  15, 400, 12, 0.5, 2, 0.1], #Default        0
    [10, 10, grey,    20,  5,  15, 30, 0,   0,  0.5, 8, 0.1], #Sheild-Breaker 1
    [19, 4,  magenta, 300, 7,  2,  15, 400, 12, 0.5, 2, 0.1], #Doc            2
    [10, 3,  green,   200, 20, 2,  30, 800, 25, 0.5, 2, 0.1], #Sniper         3
    [15, 3,  yellow,  100, 2,  1,  15, 400, 12, 0.5, 2, 0.1]] #Block-Breaker  4

''' Collision Functions '''
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
class NPC():
    def __init__(self, bot_type, health):
        self.type = bot_type
        self.health = health
        #Spawn Location
        position = random.choice([1,2])
        if position == 1:
            self.x = random.choice([-50, screen_width + 50])
            self.y = random.randint(0, screen_height)
        elif position == 2:
            self.x = random.randint(0, screen_width)
            self.y = random.choice([-50, screen_width + 50])
        self.velocity_x = self.velocity_y = 0
    def Move(self, Bot):
        self.velocity_x = Bot[self.type][1]*(-(self.x - player_x)/(abs(self.x - player_x)+abs(self.y - player_y)))
        self.velocity_y = Bot[self.type][1]*(-(self.y - player_y)/(abs(self.x - player_x)+abs(self.y - player_y)))
        self.x += self.velocity_x
        self.y += self.velocity_y
        pygame.draw.circle(screen, Bot[self.type][2], (int(self.x), int(self.y)), Bot[self.type][0], 0)
        pygame.draw.circle(screen, black, (int(self.x), int(self.y)), Bot[self.type][0], 2)
    def Still(self, Bot):
        pygame.draw.circle(screen, Bot[self.type][2], (int(self.x), int(self.y)), Bot[self.type][0], 0)
        pygame.draw.circle(screen, black, (int(self.x), int(self.y)), self.Radius, 2)

class Bullet():
    def __init__(self, speed, size, colour, x, y, dx, dy, bullet_type, damage_type):
        self.exist_time = pygame.time.get_ticks()
        self.damage_type = damage_type
        self.type = bullet_type
        self.colour = colour
        self.size = size
        self.speed = speed
        self.x = x
        self.y = y
        self.velocity_x = self.speed*(-dx/(abs(dx)+abs(dy)))
        self.velocity_y = self.speed*(-dy/(abs(dx)+abs(dy)))
    def Move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        if self.type == 1:
            screen.blit(player_bullet_image, (self.x - bullet_size, self.y - bullet_size))
        else:
            screen.blit(enemy_bullet_image, (self.x - bullet_size, self.y - bullet_size))

class Object():
    def __init__(self, x, y, size, colour, object_type):
        self.type = object_type
        self.x = x
        self.y = y
        self.size = size
        self.health = 100
        self.colour = colour
    def Block(self):
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.size, self.size), 0)
        pygame.draw.rect(screen, black, (self.x, self.y, self.size, self.size), 2)
    def Turret(self, Turret):
        pygame.draw.circle(screen, Turret[self.type][5], (int(self.x + block_size/2), int(self.y + block_size/2)), self.size, 0)
        pygame.draw.circle(screen, black, (int(self.x + block_size/2), int(self.y + block_size/2)), self.size, 2)
    def Powerup(self):
        if self.type == 0:
            screen.blit(powerup_pink_image, (self.x - powerup_rad, self.y - powerup_rad))
        elif self.type == 1:
            screen.blit(powerup_orange_image, (self.x - powerup_rad, self.y - powerup_rad))
        elif self.type == 2:
            screen.blit(powerup_blue_image, (self.x - powerup_rad, self.y - powerup_rad))

    def Money(self, player_x, player_y):
        dist_x = player_x - self.x
        dist_y = player_y - self.y
        if math.hypot(dist_x, dist_y) < 300:
            Speed = 500/math.hypot(dist_x, dist_y)
            self.Velocity_x = Speed*(-(self.x - player_x)/(abs(self.x - player_x)+abs(self.y - player_y)))
            self.Velocity_y = Speed*(-(self.y - player_y)/(abs(self.x - player_x)+abs(self.y - player_y)))
            self.x += self.Velocity_x
            self.y += self.Velocity_y
            screen.blit(money_image, (self.x - self.size, self.y - self.size))


class Button():
    def __init__(self, x, y, size, colour, name, cost, imshit):
        self.cus = imshit
        self.x = x
        self.y = y
        self.cost = cost
        self.size = size
        self.colour = colour
        self.name = shop_button_font.render(name, False, black)
        self.cost_text = shop_button_font.render('$'+str(cost), False, black)
    def Draw(self):
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.size, self.size), 0)
        pygame.draw.rect(screen, black, (self.x, self.y, self.size, self.size), 2)
        screen.blit(self.name, (self.x + 5, self.y))
        screen.blit(self.cost_text, (self.x + 5, self.y + 30))
    def Click(self, mouse_x, mouse_y):
        if self.x < mouse_x < self.x + self.size and self.y < mouse_y < self.y + self.y + self.size:
            return True
        else:
            return False

''' Shop Generation '''
for thingo in range(0, len(Item)):
    button = Button(Item[thingo][0], Item[thingo][1], button_size, Item[thingo][2], Item[thingo][3], Item[thingo][4], thingo)
    Button_array.append(button)

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
        #Keyboard Press
        if event.type == pygame.KEYUP or event.type == pygame.KEYDOWN:
            key_state = list(pygame.key.get_pressed())

        #Mouse Press
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            mouse_state = list(pygame.mouse.get_pressed())

        #Scroll Wheel
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                weapon += -1
                if weapon < 1:
                    weapon = 6
            elif event.button == 5:
                weapon += 1
                if weapon > 6:
                    weapon = 1

    if key_state[pygame.K_1] == 1: weapon = 1
    elif key_state[pygame.K_2] == 1: weapon = 2
    elif key_state[pygame.K_3] == 1: weapon = 3
    elif key_state[pygame.K_4] == 1: weapon = 4
    elif key_state[pygame.K_5] == 1: weapon = 5
    elif key_state[pygame.K_6] == 1: weapon = 6

    #Weapon Selecting
    if weapon == 1:
        weapon = last_weapon = 1
        weapon_name = 'SMG'
    elif rifle_owned is True and weapon == 2:
        weapon = last_weapon = 2
        weapon_name = 'Sniper rifle'
    elif shotgun_owned is True and weapon == 3:
        weapon = last_weapon = 3
        weapon_name = 'Shotgun'
    elif homing_owned is True and weapon == 4:
        weapon = last_weapon = 4
        weapon_name = 'Homing gun'
    elif freezes_owned > 0 and weapon == 5:
        weapon_name = 'Freeze ray'
        weapon = 5
    elif turret_given > 0 and weapon == 6:
        weapon_name = 'Turrets'
        weapon = 6

    ''' Player '''
    mouse_pos = pygame.mouse.get_pos()
    mouse_pos_x = player_x - mouse_pos[0]
    mouse_pos_y = player_y - mouse_pos[1]

    #Movement
    if dash is False:
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
        sheild_active = True
        pygame.draw.circle(screen, sheild_colour, (int(player_x),int(player_y)), sheild_rad, 3)
        if powerup_active == 0:
            sheild_n_shoot = True
        else:
            sheild_n_shoot = False
    else:
        sheild_active = False

    #Weapons
    if mouse_state[0] == 1 and (sheild_n_shoot is True or sheild_active is False):
        #SMG
        if weapon == 1 and pygame.time.get_ticks() - weapon_1_fired > Weapon[0][3]:
            weapon_1_fired = pygame.time.get_ticks()
            bullet = Bullet(Weapon[0][1], bullet_size, player_bullet_colour, player_x, player_y, mouse_pos_x + random.randint(-abs(int(Weapon[0][2]*mouse_pos_y)), abs(int(Weapon[0][2]*mouse_pos_y))), mouse_pos_y + random.randint(-abs(int(Weapon[0][2]*mouse_pos_x)), abs(int(Weapon[0][2]*mouse_pos_x))), 1, 0)
            Bullet_array.append(bullet)
            smg_sound.play()
        #Sniper-rifle
        elif weapon == 2 and rifle_owned is True and pygame.time.get_ticks() - weapon_2_fired > Weapon[1][3]:
            weapon_2_fired = pygame.time.get_ticks()
            bullet = Bullet(Weapon[1][1], bullet_size, player_bullet_colour, player_x, player_y, mouse_pos_x + random.randint(-abs(int(Weapon[1][2]*mouse_pos_y)), abs(int(Weapon[1][2]*mouse_pos_y))), mouse_pos_y + random.randint(-abs(int(Weapon[1][2]*mouse_pos_x)), abs(int(Weapon[1][2]*mouse_pos_x))), 1, 1)
            Bullet_array.append(bullet)
            sniper_sound.play()
        #Shotgun
        elif weapon == 3 and shotgun_owned is True and pygame.time.get_ticks() - weapon_3_fired > Weapon[2][3]:
            weapon_3_fired = pygame.time.get_ticks()
            bullet = Bullet(Weapon[2][1], bullet_size, player_bullet_colour, player_x, player_y, mouse_pos_x + random.randint(-abs(int(Weapon[2][2]*mouse_pos_y)), abs(int(Weapon[2][2]*mouse_pos_y))), mouse_pos_y + random.randint(-abs(int(Weapon[2][2]*mouse_pos_x)), abs(int(Weapon[2][2]*mouse_pos_x))), 1, 2)
            Bullet_array.append(bullet)
            shotgun_sound.play()
        #Homing
        elif weapon == 4 and homing_owned is True and pygame.time.get_ticks() - weapon_4_fired > Weapon[3][3]:
            weapon_4_fired = pygame.time.get_ticks()
            bullet = Bullet(Weapon[3][1], bullet_size, player_bullet_colour, player_x, player_y, mouse_pos_x + random.randint(-abs(int(Weapon[4][3]*mouse_pos_y)), abs(int(Weapon[4][3]*mouse_pos_y))), mouse_pos_y + random.randint(-abs(int(Weapon[3][2]*mouse_pos_x)), abs(int(Weapon[3][2]*mouse_pos_x))), 3, 3)
            Bullet_array.append(bullet)
        #Freeze
        elif weapon == 5 and freezes_owned > 0 and pygame.time.get_ticks() - weapon_5_fired > Weapon[4][3]:
            weapon_5_fired = pygame.time.get_ticks()
            freeze = True
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
            block = Object(block_x, block_y, block_size, grey, 0)
            Block_array.append(block)
            blocks_given += -1
            mouse_state[1] = 0
            for bot in Bot_array:
                if block_x < bot.x < block_x + block_size and block_y < bot.y < block_y + block_size:
                    Bot_array.remove(bot)

    #Turrets
    elif mouse_state[0] == 1 and turret_given > 0 and weapon == 6:
        for thing3 in x_range:
            if mouse_pos[0] > thing3:
                turret_x = thing3

        for thing4 in y_range:
            if mouse_pos[1] > thing4:
                turret_y = thing4

        if position[int(turret_x/block_size)][int(turret_y/block_size)] == 0:
            position[int(turret_x/block_size)][int(turret_y/block_size)] = 3
            turret = Object(turret_x, turret_y, turret_size, Turret[turret_level][5], turret_level)
            Turret_array.append(turret)
            weapon = last_weapon
            turret_given += -1

    ''' Bullets '''
    for bullet in Bullet_array:
        #Block Collision
        for block in Block_array:
            bullet.x, bullet.y, bullet.velocity_x, bullet.velocity_y, block_collision = Blocks(block_size, bullet_size, bullet.x, bullet.y, block.x, block.y, bullet.velocity_x, bullet.velocity_y)
            if block_collision is True:
                break

        #Shop Collision
        for shop in Shop_array:
            bullet.x, bullet.y, bullet.velocity_x, bullet.velocity_y, shop_collision = Blocks(block_size, bullet_size, bullet.x, bullet.y, shop.x, shop.y, bullet.velocity_x, bullet.velocity_y)
            if shop_collision is True:
                break

        #Edge of map despawn
        if bullet.x > screen_width or bullet.x < 0 or bullet.y > screen_height or bullet.y < 0:
            Bullet_array.remove(bullet)
            continue

        #Maximium life reached
        if pygame.time.get_ticks() - bullet.exist_time > bullet_exist_time:
            Bullet_array.remove(bullet)
            continue

        #Player Bullets
        if bullet.type == 1 or bullet.type == 3:
            for bot in Bot_array:
                if Balls(Bot[bot.type][0], bullet_size, bot.x, bot.y, bullet.x, bullet.y) is True:
                    bot.health += -Weapon[bullet.damage_type][0]
                    Bullet_array.remove(bullet)
                    break

            #Homing Bullets
            if bullet.type == 3 and pygame.time.get_ticks() - bullet.exist_time > 500:
                #Closest Bot
                angle_change = False
                distance_turn = 400
                for bot in Bot_array:
                    temp_distance_x = bullet.x - bot.x
                    temp_distance_y = bullet.y - bot.y
                    temp_distance_turn = math.hypot(temp_distance_x, temp_distance_y)
                    if temp_distance_turn < distance_turn:
                        angle_change = True
                        distance = temp_distance_turn
                        distance_x = bot.x
                        distance_y = bot.y

                if angle_change is True:
                    #Turn Left or Right
                    (Ax, Ay) = (bullet.x, bullet.y)
                    (Bx, By) = (bullet.x + (bullet.velocity_x), bullet.y + (bullet.velocity_y))
                    (Cx, Cy) = (distance_x, distance_y)
                    direction = numpy.sign((Bx - Ax)*(Cy - Ay) - (By - Ay)*(Cx - Ax))

                    #How to Adjust its past (Dont ask about the Maths)
                    if numpy.sign(bullet.velocity_x) == numpy.sign(bullet.velocity_y):
                        if direction > 0:
                            alpha = math.atan(bullet.velocity_y/bullet.velocity_x)
                            dx = bullet.velocity_x
                            dy = bullet.velocity_x*math.tan(alpha + angle_increase)

                            bullet.velocity_x = bullet.speed*(dx/(abs(dx)+abs(dy)))
                            bullet.velocity_y = bullet.speed*(dy/(abs(dx)+abs(dy)))

                        elif direction <  0:
                            alpha = math.atan(bullet.velocity_y/bullet.velocity_x)
                            dx = bullet.velocity_x
                            dy = bullet.velocity_x*math.tan(alpha - angle_increase)

                            bullet.velocity_x = bullet.speed*(dx/(abs(dx)+abs(dy)))
                            bullet.velocity_y = bullet.speed*(dy/(abs(dx)+abs(dy)))

                    else:
                        if direction > 0:
                            alpha = math.atan(bullet.velocity_y/bullet.velocity_x)
                            dx = bullet.velocity_x
                            dy = bullet.velocity_x*math.tan(alpha + angle_increase)

                            bullet.velocity_x = bullet.speed*(dx/(abs(dx)+abs(dy)))
                            bullet.velocity_y = bullet.speed*(dy/(abs(dx)+abs(dy)))

                        elif direction <  0:
                            alpha = math.atan(bullet.velocity_y/bullet.velocity_x)
                            dx = bullet.velocity_x
                            dy = bullet.velocity_x*math.tan(alpha - angle_increase)

                            bullet.velocity_x = bullet.speed*(dx/(abs(dx)+abs(dy)))
                            bullet.velocity_y = bullet.speed*(dy/(abs(dx)+abs(dy)))

        #Bot Bullets
        elif bullet.type == 2:
            #Collision with sheild
            if sheild_active is True and Balls(sheild_rad, bullet_size, bullet.x, bullet.y, player_x, player_y) is True:
                Bullet_array.remove(bullet)

            #Collision with player
            elif Balls(player_rad, bullet_size, bullet.x, bullet.y, player_x, player_y) is True:
                player_hit_time = pygame.time.get_ticks()
                player_health += - Bot[bot.type][4]
                Bullet_array.remove(bullet)

        bullet.Move()

    ''' Bots '''
    #Wave Spawning
    if len(Bot_array) == 0 and reason_bot is False:
        reason_bot = True
        delay_bot = pygame.time.get_ticks()

        #The Player Wave-Bonus
        block_number += 1
        player_health += 10
        sheild_health += 10
        player_money += 20

        #Spawning Shop
        if len(Shop_array) < 1 and wave_number > 0:
            while True:
                shop_x = random.choice(x_range)
                shop_y = random.choice(y_range)
                if position[int(shop_x/block_size)][int(shop_y/block_size)] == 0:
                    position[int(shop_x/block_size)][int(shop_y/block_size)] = 1
                    shop = Object(shop_x, shop_y, block_size, blue, 1)
                    Shop_array.append(shop)
                    break

    elif len(Bot_array) == 0 and pygame.time.get_ticks() - delay_bot > wave_delay:
        wave_time = pygame.time.get_ticks()
        reason_bot = False
        wave_number += 1

        for thing in range(0, wave_number):
            #Bot 1
            bot = NPC(0, Bot[0][3])
            Bot_array.append(bot)

            #Bot 2
            if thing%3 == 0:
                bot = NPC(1, Bot[1][3])
                Bot_array.append(bot)

            #Bot 3
            if thing%4 == 0:
                bot = NPC(2, Bot[2][3])
                Bot_array.append(bot)

            #Bot 4
            if thing > 5 and thing%5 == 0:
                bot = NPC(3, Bot[3][3])
                Bot_array.append(bot)

            #Bot 5
            if thing > 6 and thing%6 == 0:
                bot = NPC(4, Bot[4][3])
                Bot_array.append(bot)

    #Updating them
    for bot in Bot_array:
        if bot.health <= 0:
            money = Object(bot.x, bot.y, 5, yellow, 0)
            Money_array.append(money)
            Bot_array.remove(bot)

        elif freeze is True:
            bot.Still(Bot)

        elif freeze is False:
            #Should the bot Shoot
            if Balls(player_rad, Bot[bot.type][7], bot.x, bot.y, player_x, player_y) is True and counter%Bot[bot.type][6] == 0:
                bullet = Bullet(Bot[bot.type][8], bullet_size, bot_bullet_colour, bot.x, bot.y, (bot.x - player_x), (bot.y - player_y), 2, 0)
                Bullet_array.append(bullet)

            #Collosion with Sheild
            if Balls(sheild_rad, Bot[bot.type][0], bot.x, bot.y, player_x, player_y) is True and sheild_active is True:
                bot.x += (-player_x + sheild_rad + bot.x - Bot[bot.type][0])
                bot.y += (-player_y + sheild_rad + bot.y - Bot[bot.type][0])
                if powerup_active == 1:
                    bot.health += -sheild_melee_damage
                else:
                    sheild_health += -Bot[bot.type][5]

            #Collosion with Player
            elif Balls(player_rad, Bot[bot.type][0], bot.x, bot.y, player_x, player_y) is True:
                bot.x += (-player_x + player_rad + bot.x - Bot[bot.type][0])
                bot.y += (-player_y + player_rad + bot.y - Bot[bot.type][0])
                player_hit_time = pygame.time.get_ticks()
                player_health += -Bot[bot.type][10]

            #Block Collision
            for block in Block_array:
                bot.x, bot.y, bot.velocity_x, bot.velocity_y, Hit = Blocks(block_size, Bot[bot.type][0], bot.x, bot.y, block.x, block.y, bot.velocity_x, bot.velocity_y)
                if Hit is True:
                    block.health += -Bot[bot.type][11]
                    if block.health <= 0:
                        position[int(block.x/block_size)][int(block.y/block_size)] = 0
                        Block_array.remove(block)

            #Shop Collision
            for shop in Shop_array:
                bot.x, bot.y, bot.velocity_x, bot.velocity_y, _ = Blocks(block_size, Bot[bot.type][0], bot.x, bot.y, block.x, block.y, bot.velocity_x, bot.velocity_y)

            bot.Move(Bot)

            #Printing Bot Health
            textsurface = bot_health_font.render(str(int(bot.health)), False, bot_health_colour)
            screen.blit(textsurface, (bot.x - 8, bot.y - 8))

    ''' PowerUps '''
    #Spawning the Powerups
    if len(Powerup_array) == 0 and reason_powerup is False:
        delay_powerup = pygame.time.get_ticks()
        reason_powerup = True

    elif len(Powerup_array) == 0 and pygame.time.get_ticks() - delay_powerup > powerup_delay:
        reason_powerup = False
        while True:
            powerup_x = random.choice(x_range)
            powerup_y = random.choice(y_range)
            if position[int(powerup_x/block_size)][int(powerup_y/block_size)] == 0:
                position[int(powerup_x/block_size)][int(powerup_y/block_size)] = 1
                pickone = random.randint(0,2)
                powerup = Object(powerup_x, powerup_y, powerup_rad, _, pickone)
                Powerup_array.append(powerup)
                break

    #Activating Powerups
    for powerup in Powerup_array:
        if Balls(player_rad, powerup_rad, powerup.x + block_size/2, powerup.y + block_size/2, player_x, player_y) is True:
            position[int(powerup.x/block_size)][int(powerup.y/block_size)] = 0
            powerup_active_time = pygame.time.get_ticks()
            powerup_active = powerup.type
            Powerup_array.remove(powerup)
            if powerup_active == 0:
                sheild_colour = magenta
            elif powerup_active == 1:
                sheild_colour = orange
            elif powerup_active == 2:
                battlemoon_health += 50
                battlemoon_level += 1
                powerup_active = 0

        if powerup_active != 3 and pygame.time.get_ticks() - powerup_active_time > powerup_extent:
            sheild_colour = green
            powerup_active = 3

        powerup.Powerup()

    #Battlemoon
    if battlemoon_level > -1:
        #Moving the Moon
        battlemoon_angle += 7
        if battlemoon_angle >= 360:
            battlemoon_angle = 0
        if battlemoon_level > 5:
            battlemoon_health += 50
            battlemoon_level = 5

        battlemoon_x = player_x + battlemoon_orbit*math.cos(math.radians(battlemoon_angle))
        battlemoon_y = player_y + battlemoon_orbit*math.sin(math.radians(battlemoon_angle))

        #Drawing
        pygame.draw.circle(screen, Battlemoon[battlemoon_level][4], (int(battlemoon_x), int(battlemoon_y)), 7, 0)
        pygame.draw.circle(screen, black, (int(battlemoon_x), int(battlemoon_y)), 7, 2)

        #Finding the Closest Bot
        battlemoon_shoot = False
        distance = Battlemoon[battlemoon_level][2]
        for bot in Bot_array:
            temp_distance_x = battlemoon_x - bot.x
            temp_distance_y = battlemoon_y - bot.y
            temp_distance = math.hypot(temp_distance_x, temp_distance_y)
            if temp_distance < distance:
                battlemoon_shoot = True
                distance = temp_distance
                distance_x = temp_distance_x
                distance_y = temp_distance_y

        #Shooting
        if battlemoon_shoot is True and counter%Battlemoon[battlemoon_level][0] == 0:
            bullet = Bullet(Battlemoon[battlemoon_level][5], bullet_size, green, battlemoon_x, battlemoon_y, distance_x, distance_y, 1, 0)
            Bullet_array.append(bullet)
            battlemoon_shoot_sound.play()

        #Health
        if battlemoon_health <= 0:
            battlemoon_level = -1

    ''' Shop '''
    #Updating
    for shop in Shop_array:
        shop.Block()

        #Running the Shop
        player_x, player_y, _, _, shop_collision = Blocks(block_size, player_rad, player_x, player_y, shop.x, shop.y, player_speedx, player_speedy)
        if shop_collision is True:
            heart_beat_sound.stop()
            shop_entrance.play()
            end_shop = False
            while end_shop is False:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            Shop_array.remove(shop)
                            end_shop = True
                    if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                        mouse_state = list(pygame.mouse.get_pressed())

                mouse_pos = pygame.mouse.get_pos()

                myfont = pygame.font.SysFont('Comic Sans MS', 25)
                text = myfont.render(' Money:$'+str(player_money)+' Players Health:'+str(player_health)+' Sheilds Health:'+str(sheild_health)+' Freezes Owned:'+str(freezes_owned)+' Turrets Owned:'+str(turret_given)+' Rifle Owned:'+str(rifle_owned)+' Shotgun Owned:'+str(shotgun_owned), False, black)
                screen.blit(text,(0,0))

                for button in Button_array:
                    button.Draw()
                    if mouse_state[0] == 1 and button.Click(mouse_pos[0], mouse_pos[1]) is True:
                        mouse_state[0] = 0
                        if button.cus == 0 and rifle_owned is False and player_money >= int(button.cost):
                            purchase_sound.play()
                            player_money += -button.cost
                            rifle_owned = True
                        elif button.cus == 1 and shotgun_owned is False and player_money >= int(button.cost):
                            purchase_sound.play()
                            player_money += -button.cost
                            shotgun_owned = True
                        elif button.cus == 2 and player_money >= button.cost:
                            purchase_sound.play()
                            player_money += -button.cost
                            turret_given += 1
                        elif button.cus == 3 and player_money >= button.cost:
                            purchase_sound.play()
                            player_money += -button.cost
                            player_health += 15
                        elif button.cus == 4 and player_money >= button.cost:
                            purchase_sound.play()
                            player_money += -button.cost
                            sheild_health += 15
                        elif button.cus == 5 and player_money >= button.cost:
                            purchase_sound.play()
                            player_money += -button.cost
                            battlemoon_level += 1
                        elif button.cus == 6 and player_money >= button.cost:
                            purchase_sound.play()
                            player_money += -button.cost
                            block_number += 1
                        elif button.cus == 7 and player_money >= button.cost:
                            purchase_sound.play()
                            player_money += -button.cost
                            turret_level += 1
                        elif button.cus == 8 and homing_owned is False and player_money >= button.cost:
                            purchase_sound.play()
                            player_money += -button.cost
                            homing_owned = True
                        elif button.cus == 9 and player_money >= button.cost:
                            purchase_sound.play()
                            player_money += -button.cost
                            freezes_owned += 1

                pygame.display.flip()
                pygame.display.set_caption('The Shop')
                screen.fill(white)

    ''' Turret '''
    for turret in Turret_array:
        #Finding the Closest Bot
        turret_shoot = False
        distance = Turret[turret.type][2]
        for bot in Bot_array:
            temp_distance_x = turret.x - bot.x
            temp_distance_y = turret.y - bot.y
            temp_distance = math.hypot(temp_distance_x, temp_distance_y)
            if temp_distance < distance:
                turret_shoot = True
                distance = temp_distance
                distance_x = temp_distance_x
                distance_y = temp_distance_y

        #Shooting
        if turret_shoot is True and counter%Turret[turret.type][0] == 0:
            bullet = Bullet(Turret[turret.type][4], bullet_size, player_bullet_colour, turret.x, turret.y, distance_x, distance_y, 1, 0)
            Bullet_array.append(bullet)

        #Collisions
        for bot in Bot_array:
            if Balls(turret.size, Bot[bot.type][0], bot.x, bot.y, turret.x, turret.y):
                turret.health +=  -Bot[bot.type][10]
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

    ''' More Player Stuff '''
    if player_x < player_rad:
        player_x = player_rad
    elif  player_y < player_rad:
        player_y = player_rad
    elif player_x > screen_width - player_rad:
        player_x = screen_width - player_rad
    elif  player_y > screen_height - player_rad:
        player_y = screen_height - player_rad

    if player_health > 0:
        #Heart Beat effect
        if player_health < 30 and pygame.time.get_ticks() - heat_beat_time > heart_beat_length:
            heart_beat_sound.play()
        else:
            heart_beat_sound.stop()

        #Drawing Player
        #pygame.draw.circle(screen, red, (int(player_x), int(player_y)), player_rad, 0)
        #pygame.draw.circle(screen, black ,(int(player_x), int(player_y)), player_rad, 2)
        screen.blit(player_image, (player_x - player_rad, player_y - player_rad))

        #Writing Health
        textsurface = bot_health_font.render(str(player_health), False, black)
        screen.blit(textsurface, (player_x - 8, player_y - 7))
    else:
        print('ur so shit')
        pygame.quit()

    ''' Writing Stats '''
    if pygame.time.get_ticks() - wave_time < wave_time_length:
        textsurface = wave_number_font.render('Wave Number is '+str(wave_number), False, black)
        screen.blit(textsurface, (screen_width/2 - 400, screen_height/2))

    textsurface = weapon_selected_font.render('Weapon Selected: ' + weapon_name, False, black)
    screen.blit(textsurface, (10, 0))

    if freeze_duration - pygame.time.get_ticks() + weapon_5_fired > 0:
        freeze_left = int((freeze_duration - pygame.time.get_ticks() + weapon_5_fired)/1000)
    else:
        freeze_left = 0

    textsurface = weapon_selected_font.render('Freeze Time: ' + str(freeze_left), False, black)
    screen.blit(textsurface, (10, 40))

    ''' Updating Changes to the Screen '''
    if pygame.time.get_ticks() - player_hit_time < 500:
        x_shake = random.randint(-10, 10)
        y_shake = random.randint(-10, 10)
        shake_screen.blit(screen, (0,0), pygame.Rect(0 + x_shake, 0 + y_shake, screen_width + x_shake, screen_height + y_shake))

    pygame.display.set_caption('The Battleground')
    pygame.display.flip()
    screen.fill(white)
    Clock.tick(fps)

    ''' Credit '''
    #smg_sound - Recorded by Kibblesbob - sourced at http://soundbible.com/1804-M4A1-Single.html - Shortened and Volume Reduced - Attribution 3.0
    #shotgun_sound - Recorded by RA The Sun God - sourced at http://soundbible.com/2101-12-Ga-Winchester-Shotgun.html - Shortened and Volume Reduced - Attribution 3.0
    #sniper_sound - Recorded by Kibblesbob - sourced at http://soundbible.com/1788-Sniper-Rifle.html - Public Domain
    #heart_beat_sound - Recorded by Daniel Simion - sourced at http://soundbible.com/2162-Human-Heartbeat.html - Attribution 3.0
    #battlemoon_shoot_sound - Recorded by Mike Koenig - sourced at http://soundbible.com/1087-Laser.html - Attribution 3.0
    #purchase_sound - Recorded by Muska666 - sourced at http://soundbible.com/1997-Cha-Ching-Register.html - Attribution 3.0
    #shop entrance - Recorded by Daniel Simion - sourced at http://soundbible.com/2160-Old-Fashion-Door-Bell.html - Attribution 3.0
