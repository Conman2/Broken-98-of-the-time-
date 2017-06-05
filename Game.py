import pygame
import math
import time

#the magic function that must be called
pygame.init()

#colour libary definned through RGB
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

#Screen display deminsions
(Screen_Width,Screen_Height) = (800,600)
Screen = pygame.display.set_mode((Screen_Width, Screen_Height))

#Positions and stuff
x = x_npc = Screen_Width/2
y = Screen_Height/2
xspeed = yspeed = 0
xd = xa = ys = yw = 0
x_npc = x
x_npc_speed = 3
y_npc = Screen_Height/3
player_rad = npc_rad = 20
shoot_dist = 150
NPC_move = True

#Used to control game speed linking it to FPS
Clock = pygame.time.Clock()
fps = 30

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            break

        #Taking the User Inputs
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                xa = True
            elif event.key == pygame.K_d:
                xd = True
            if event.key == pygame.K_s:
                ys = True
            elif event.key == pygame.K_w:
                yw= True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                xa = False
            elif event.key == pygame.K_d:
                xd = False
            elif event.key == pygame.K_w:
                yw = False
            elif  event.key == pygame.K_s:
                ys = False

    #Players Movement
    xspeed = 4*(xd - xa)
    yspeed = 4*(ys - yw)

    if abs(xspeed) == abs(yspeed):
        x += xspeed*0.5
        y += yspeed*0.5
    else:
        x += xspeed
        y += yspeed

    pygame.draw.circle(Screen,blue,(int(x),int(y)),player_rad, 1)

    #NPCs movement
    if x_npc > Screen_Width/2 + 50:
        x_npc_speed = -3
    elif x_npc < Screen_Width/2 - 50:
        x_npc_speed = 3

    x_npc += x_npc_speed

    if NPC_move is True:
        pygame.draw.circle(Screen,red,(int(x_npc),int(y_npc)),npc_rad, 1)

    #Collision
    distance = math.hypot(x_npc-x, y_npc-y)
    if distance < player_rad + npc_rad + shoot_dist #+ xspeed + x_npc_speed + yspeed:
        NPC_move = False
        x_bullet = x_npc
        y_bullet = y_npc

        pygame.draw.circle(Screen,black,(int(x_bullet),int(y_bullet)),3, 1)
    else:
        NPC_move = True

    #Updates any changes to the screen
    pygame.display.update()
    Screen.fill(white)
    Clock.tick(30)
