import pygame
import math
import time

#The magic function that must be called
pygame.init()

#Colour libary definned through RGB
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
white = (255,255,255)

#Screen display deminsions
(Screen_Width,Screen_Height) = (800,600)
Screen = pygame.display.set_mode((Screen_Width, Screen_Height))

#Positions and stuff
player_x = x_npc = Screen_Width/2
player_y = Screen_Height/2
xspeed = yspeed = xd = xa = ys = yw = dx = dy = 0
player_rad = npc_rad = 20
y_npc = Screen_Height/4
shoot_dist = 100
x_npc_speed = 3
NPC_move = True
size = 3
Bullet_array = []

#Creating Bullets
class Bullet():
    def __init__(self,x_npc,y_npc,dx,dy,size):
        self.size = size
        self.x = x_npc
        self.y = y_npc
        self.speed = 6
        self.thickness = 1
        self.Velocity_x = self.speed*(-dx/(abs(dx)+abs(dy)))
        self.Velocity_y = self.speed*(-dy/(abs(dx)+abs(dy)))
    def Position(self):
        self.x += self.Velocity_x
        self.y += self.Velocity_y
        pygame.draw.circle(Screen, black, (int(self.x), int(self.y)), self.size, self.thickness)

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
    xspeed = 6*(xd - xa)
    yspeed = 6*(ys - yw)

    if abs(xspeed) == abs(yspeed):
        player_x += xspeed*0.5
        player_y += yspeed*0.5
    else:
        player_x += xspeed
        player_y += yspeed

    pygame.draw.circle(Screen,blue,(int(player_x),int(player_y)),player_rad, 1)

    #NPCs movement
    if NPC_move is True:
        if x_npc > Screen_Width/2 + 50:
            x_npc_speed = -3
        elif x_npc < Screen_Width/2 - 50:
            x_npc_speed = 3
        x_npc += x_npc_speed

    pygame.draw.circle(Screen,red,(int(x_npc),int(y_npc)),npc_rad, 1)

    #Difference in Position for PLayer to Enemy
    dx = x_npc-player_x
    dy = y_npc-player_y

    #Collision
    distance = math.hypot(dx, dy)
    if distance < player_rad + npc_rad + shoot_dist + xspeed + x_npc_speed + yspeed:
        NPC_move = False
        bullet = Bullet(x_npc,y_npc,dx,dy,size)
        Bullet_array.append(bullet)
        for bullet in Bullet_array:
            bullet.Position()
            if bullet.x > Screen_Width or bullet.x < 0 or bullet.y > Screen_Height or bullet.y < 0:
                Bullet_array.remove(bullet)
    else:
        NPC_move = True
        for bullet in Bullet_array:
            bullet.Position()
            if bullet.x > Screen_Width or bullet.x < 0 or bullet.y > Screen_Height or bullet.y < 0:
                Bullet_array.remove(bullet)

    #Updates any changes to the screen
    pygame.display.update()
    Screen.fill(white)
    Clock.tick(fps)
