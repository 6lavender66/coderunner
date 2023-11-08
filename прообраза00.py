import pygame
import random

pygame.init() 


################################
###     GLOBAL VARIABLES    ####
################################


szerokosc = 800
wysokosc = 600

window = pygame.display.set_mode((szerokosc, wysokosc))

player_x = szerokosc // 2
player_y = wysokosc - 100
player = pygame.Rect(player_x, player_y, 30, 30)

asteroid_x = random.randint(-10, szerokosc)
asteroid_y = random.randint(5, 10)
asteroid = pygame.Rect(asteroid_x, asteroid_y, 60, 60)

speed = 7
cooldown = 0
cooldown_time = 15 

bullets = []
asteroids = []


##########################
###      FUNCTIONS    ####
##########################


def sterowanie():

    global player_x  
    global player_y  
    
    keys = pygame.key.get_pressed()

    ruch_prawo = keys[pygame.K_RIGHT]
    ruch_lewo = keys[pygame.K_LEFT]
    ruch_gora = keys[pygame.K_UP]
    ruch_dol = keys[pygame.K_DOWN]

    if ruch_prawo:
        player_x += speed
    if ruch_lewo:
        player_x -= speed
    if ruch_gora:
        player_y -= speed
    if ruch_dol:
        player_y += speed


    if player_x <= 0:
        player_x = szerokosc
    if player_x >= szerokosc:
        player_x = -5
    if player_y <= 0:
        player_y = wysokosc
    if player_y >= wysokosc:
        player_y = -5



def strzelanie():
    
    global cooldown

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and cooldown <= 0:                                    
        bullet_x = player_x + player.width // 2
        bullet_y = player_y
        bullets.append([bullet_x, bullet_y])
        cooldown = cooldown_time  


    for bullet in bullets:
        bullet[1] -= 15
        if bullet[1] < 0:
            bullets.remove(bullet)

    if cooldown > 0:
        cooldown -= 1  

def kolidowanie():

    global bullets, asteroids, player, run

    bullets_to_remove = []  

    for bullet in bullets:
        bullet = pygame.Rect(bullet[0], bullet[1], 5, 10)
        for asteroid in asteroids:
            asteroid = pygame.Rect(asteroid[0], asteroid[1], 60, 60)
            if bullet.colliderect(asteroid): 
                bullets_to_remove.append(bullet)
                asteroids.remove(asteroid)


    for bullet in bullets_to_remove:
        bullets.remove(bullet)

    
    for asteroid in asteroids:
        asteroid = pygame.Rect(asteroid[0], asteroid[1], 60, 60)
        if player.colliderect(asteroid):
            run = False


def kolidowanie2():
    global bullets, asteroids, player, run

    bullets_to_remove = []  

    for bullet in bullets[:]:
        bullet_rect = pygame.Rect(bullet[0], bullet[1], 5, 10)
        for asteroid in asteroids[:]:
            asteroid_rect = pygame.Rect(asteroid[0], asteroid[1], 60, 60)
            if bullet_rect.colliderect(asteroid_rect):
                bullets_to_remove.append(bullet)
                asteroids.remove(asteroid)

    for bullet in bullets_to_remove:
        bullets.remove(bullet)

    player_rect = pygame.Rect(player_x, player_y, 30, 30)
    for asteroid in asteroids[:]:
        asteroid_rect = pygame.Rect(asteroid[0], asteroid[1], 60, 60)
        if player_rect.colliderect(asteroid_rect):
            run = False



def asteroidy():
    global asteroid_x, asteroid_y, asteroid

    asteroid_y += 5

    if asteroid_y > wysokosc: 
        asteroid_y = -60 
        asteroid_x = random.randint(0, szerokosc - 60)
        
    asteroid = pygame.Rect(asteroid_x, asteroid_y, 60, 60) 


run = True
while run:
    pygame.time.Clock().tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    sterowanie()  
    strzelanie() 
   
    
          
    window.fill((105, 79, 150))

    asteroidy()
    kolidowanie2()

    player = pygame.Rect(player_x, player_y, 30, 30)  
    pygame.draw.rect(window, (255, 255, 255), player)  
    for bullet in bullets:
        pygame.draw.rect(window, (255, 255, 255), pygame.Rect(bullet[0], bullet[1], 5, 10))

    pygame.draw.rect(window, (255, 255, 255), asteroid)

    pygame.display.update() 
