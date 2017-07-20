import pygame
import os

pygame.init()
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
fps = 60
Clock = pygame.time.Clock()
(screen_width,screen_height) = (1400,1000) #Note this Both need to be Multiples of Block_size
screen = pygame.display.set_mode((screen_width, screen_height))
shake_screen = pygame.display.set_mode((screen_width, screen_height))

diagonal_multiplyer = 0.65
player_y = screen_height/2
player_x = screen_width/2
homing_bullet_range = 400
sheild_melee_damage = 15
battlemoon_health = 100
angle_increase = 0.0125
battlemoon_orbit = 40
sheild_health = 90
player_health = 90
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
battlemoon_rad = 8
button_size = 120
turret_size = 18
sheild_type = 1
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
image_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Image')

money_image = pygame.image.load(os.path.join(image_path, 'money.png'))
player_image = pygame.image.load(os.path.join(image_path, 'player.png'))
enemy_bullet_image = pygame.image.load(os.path.join(image_path, 'enemy_bullet.png'))
player_bullet_image = pygame.image.load(os.path.join(image_path, 'player_bullet.png'))

sheild_1_image = pygame.image.load(os.path.join(image_path, 'sheild_1.png'))
sheild_2_image = pygame.image.load(os.path.join(image_path, 'sheild_2.png'))
sheild_3_image = pygame.image.load(os.path.join(image_path, 'sheild_3.png'))

bot_1_image = pygame.image.load(os.path.join(image_path, 'bot_1.png'))
bot_2_image = pygame.image.load(os.path.join(image_path, 'bot_2.png'))
bot_3_image = pygame.image.load(os.path.join(image_path, 'bot_3.png'))
bot_4_image = pygame.image.load(os.path.join(image_path, 'bot_4.png'))
bot_5_image = pygame.image.load(os.path.join(image_path, 'bot_5.png'))

battlemoon_imgs = {
    1:pygame.image.load(os.path.join(image_path, 'battlemoon_1.png')),
    2:pygame.image.load(os.path.join(image_path, 'battlemoon_2.png')),
    3:pygame.image.load(os.path.join(image_path, 'battlemoon_3.png')),
    4:pygame.image.load(os.path.join(image_path, 'battlemoon_4.png')),
    5:pygame.image.load(os.path.join(image_path, 'battlemoon_5.png')),
    6:pygame.image.load(os.path.join(image_path, 'battlemoon_6.png')),
}

sheild_imgs = {
    1:pygame.image.load(os.path.join(image_path, 'sheild_1.png')),
    2:pygame.image.load(os.path.join(image_path, 'sheild_2.png')),
    3:pygame.image.load(os.path.join(image_path, 'sheild_3.png')),
}

powerup_imgs = {
    0:pygame.image.load(os.path.join(image_path, 'powerup_1.png')),
    1:pygame.image.load(os.path.join(image_path, 'powerup_2.png')),
    2:pygame.image.load(os.path.join(image_path, 'powerup_3.png')),
}


#Audio Libary
audio_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Audio')

smg_sound = pygame.mixer.Sound(os.path.join(audio_path, 'smg.wav'))
shotgun_sound = pygame.mixer.Sound(os.path.join(audio_path, 'shotgun.wav'))
purchase_sound = pygame.mixer.Sound(os.path.join(audio_path, 'purchase.wav'))
sniper_sound = pygame.mixer.Sound(os.path.join(audio_path, 'sniper_rifle.wav'))
shop_entrance = pygame.mixer.Sound(os.path.join(audio_path, 'shop_entrance.wav'))
coin_pickup_sound = pygame.mixer.Sound(os.path.join(audio_path, 'coin_pickup.wav'))
heart_beat_sound = pygame.mixer.Sound(os.path.join(audio_path, 'human-heartbeat.wav'))
battlemoon_shoot_sound = pygame.mixer.Sound(os.path.join(audio_path, 'battlemoon_shoot.wav'))

#Font Liabry
bot_health_font = pygame.font.SysFont('Comic Sans MS', 10)
shop_button_font = pygame.font.SysFont('Comic Sans MS', 25)
wave_number_font = pygame.font.SysFont('Comic Sans MS', 100)
weapon_selected_font = pygame.font.SysFont('Comic Sans MS', 30)

''' Initializing Random Shite '''
finished = weapon_state = dash = freeze = reason_bot = reason_powerup = False
shop_collision = block_collision = sheild_n_shoot = False
wave_number = powerup_active_time = turret_level = 0
weapon_1_fired = weapon_2_fired = weapon_3_fired = 0
player_speedy = weapon_4_fired = weapon_5_fired = 0
battlemoon_angle = last_dash = player_speedx = 0
heat_beat_time = -heart_beat_length
wave_time = -wave_time_length
counter = last_weapon = 1
player_hit_time = -500
battlemoon_level = 0
powerup_active = 3

Powerup_array = []
Button_array = []
Bullet_array = []
Turret_array = []
Block_array = []
Money_array = []
Shop_array = []
Bot_array = []

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
    [30, 4,  300, 0.2,  grey  , 5 ], #Level0
    [30, 8,  400, 0.1,  green , 6 ], #Level1
    [15, 15, 500, 0.08, yellow, 7 ], #Level2
    [15, 25, 600, 0.05, orange, 8 ], #Level3
    [10, 35, 700, 0.01, red   , 9 ], #Level4
    [10, 50, 800, 0,    black , 10]] #Level5

Turret = [
    #Shootrate, Damage, Range, Spray, Speed, Colour
    [30,  5,  400,  0.2,  5 , grey  ], #Turret0
    [15,  18, 600,  0.01, 8 , orange], #Turret1
    [15,  35, 800,  0,    10, red   ], #Turret2
    [10,  80, 1000, 0,    14, black ]] #Turret3

Weapon = [
    #Damage, Speed, Spray, Firerate, Name
    [8,   5,  0.1,  300,   'SMG'    ], #SMG     0
    [100, 14, 0.01, 2700,  'Sniper' ], #Sniper  1
    [25,  8,  0.1,  1300,  'Shotgun'], #Shotgun 2
    [50,  8,  0,    1000,  'Homing' ], #Homing  3
    [0,   0,  0,    30000, 'Freeze' ]] #Freeze  4

Item = [
    #x, y, colour, name, cost
    [60,  60,  red,     'Rifle'  ,      150], #0
    [240, 60,  yellow,  'Shotgun',      100], #1
    [420, 60,  pink,    'Turrets',      200], #2
    [600, 60,  green ,  'Health' ,      20 ], #3
    [780, 60,  magenta, 'Armour' ,      20 ], #4
    [60,  240, red,     'Battlemoon',   80 ], #5
    [240, 240, yellow,  'Block',        60 ], #6
    [420, 240, pink,    'Turret Level', 100], #7
    [600, 240, green,   'Homing',       200], #8
    [780, 240, magenta, 'Freezes',      40 ]] #9

Bot = [
    #Radius, Speed, Colour, Health, Bullet Damage, Sheild Damage, Firerate, Range, Bullet Speed, Spray, Melee Damage, Block Damage
    [15, 4,  blue,    100, 5,  1,  15, 400, 7,  0.5, 2, 0.1], #Default        0
    [10, 6,  grey,    20,  5,  15, 30, 0,   0,  0.5, 8, 0.1], #Sheild-Breaker 1
    [19, 3,  magenta, 300, 7,  2,  15, 400, 7,  0.5, 2, 0.1], #Doc            2
    [10, 2,  green,   200, 20, 2,  30, 800, 14, 0.5, 2, 0.1], #Sniper         3
    [15, 2,  yellow,  100, 2,  1,  15, 400, 7,  0.5, 2, 0.1]] #Block-Breaker  4

''' Credit '''
#smg_sound - Recorded by Kibblesbob - sourced at http://soundbible.com/1804-M4A1-Single.html - Shortened and Volume Reduced - Attribution 3.0
#shotgun_sound - Recorded by RA The Sun God - sourced at http://soundbible.com/2101-12-Ga-Winchester-Shotgun.html - Shortened and Volume Reduced - Attribution 3.0
#sniper_sound - Recorded by Kibblesbob - sourced at http://soundbible.com/1788-Sniper-Rifle.html - Public Domain
#heart_beat_sound - Recorded by Daniel Simion - sourced at http://soundbible.com/2162-Human-Heartbeat.html - Attribution 3.0
#battlemoon_shoot_sound - Recorded by Mike Koenig - sourced at http://soundbible.com/1087-Laser.html - Attribution 3.0
#purchase_sound - Recorded by Muska666 - sourced at http://soundbible.com/1997-Cha-Ching-Register.html - Attribution 3.0
#shop_entrance - Recorded by Daniel Simion - sourced at http://soundbible.com/2160-Old-Fashion-Door-Bell.html - Attribution 3.0
#money_sound - Recorded by Willem Hunt - sourced at http://soundbible.com/2081-Coin-Drop.html - Shortened - Public Domain
