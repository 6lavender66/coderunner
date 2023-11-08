import pygame
import random

pygame.init()

fps = 60
width, height = 800, 600

c_lavender = (105, 79, 150)
c_purple = (65, 35, 158)
c_white = (255, 255, 255)
c_black = (0, 0, 0)

spaceship_width, spaceship_height = 30, 30
bullet_velocity = 15

bullets = []
window = pygame.display.set_mode((width, height))


######################
###    CLASSES     ###
######################


class Rocket:

    color = c_white
    velocity = 6

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))


    def control(self):
        
        keys = pygame.key.get_pressed()

        move_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        move_left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        move_up = keys[pygame.K_UP] or keys[pygame.K_w]
        move_down = keys[pygame.K_DOWN] or keys[pygame.K_s]

        if move_right:
            self.movement("right")
        if move_left:
            self.movement("left")
        if move_up:
            self.movement("up")
        if move_down:
            self.movement("down")


    def movement(self, direction):

        if direction == "right":
            self.x += self.velocity
            if self.x > width:
                self.x = -self.width # Wróć do lewej strony ekranu

        if direction == "left":
            self.x -= self.velocity
            if self.x + self.width < 0:
                self.x = width  # Wróć do prawej strony ekranu

        if direction == "up":
            self.y -= self.velocity
            if self.y  <= 0:
                self.y = 0  # Wróć na dół ekranu

        if direction == "down":
            self.y += self.velocity
            if self.y + self.height >= height:
                self.y = height - self.height # Wróć na górę ekranu)


class Bullets:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self):
        self.y -= bullet_velocity

    def draw(window, rocket, bullets):
        window.fill(c_lavender)
        rocket.draw(window)
        
        for bullet in bullets:
            pygame.draw.rect(window, c_black, (bullet.x, bullet.y, 5, 10))  # Bullet appearance

        pygame.display.update()


class Asteroid:

    color = c_black
    velocity = 3  

    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.width = self.size
        self.height = self.size

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

    def move(self):
        self.y += self.velocity

    @classmethod
    def create_random(cls, size):
        x = random.randint(0, width - size)
        y = random.randint(-size, -size // 2)  # Start above the screen
        return cls(x, y, size)
    

######################
###      DEFS      ###
######################

    
def generate_asteroids(asteroids, num_asteroids, size):
    for _ in range(num_asteroids):
        asteroid = Asteroid.create_random(size)
        asteroids.append(asteroid)


def fire_bullet(spaceship, bullets, cooldown, cooldown_time):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and cooldown == 0:
        bullet = Bullets(spaceship.x + spaceship.width // 2, spaceship.y)
        bullets.append(bullet)
        cooldown = cooldown_time

    for bullet in bullets:
        bullet.move()
        if bullet.y < 0:
            bullets.remove(bullet)

    if cooldown > 0:
        cooldown -= 1

    return cooldown


def check_collisions(rocket, bullets, asteroids):
    # Check for collisions between bullets and asteroids
    bullets_to_remove = []
    asteroids_to_remove = []

    for bullet in bullets:
        for asteroid in asteroids:
            if (bullet.x < asteroid.x + asteroid.size and
                bullet.x + 5 > asteroid.x and
                bullet.y < asteroid.y + asteroid.size and
                bullet.y + 10 > asteroid.y):
                bullets_to_remove.append(bullet)
                asteroids_to_remove.append(asteroid)

    for bullet in bullets_to_remove:
        if bullet in bullets:
            bullets.remove(bullet)

    for asteroid in asteroids_to_remove:
        if asteroid in asteroids:
            asteroids.remove(asteroid)


    # Check for collisions between rocket and asteroids
    for asteroid in asteroids:
        if (rocket.x < asteroid.x + asteroid.size and
            rocket.x + rocket.width > asteroid.x and
            rocket.y < asteroid.y + asteroid.size and
            rocket.y + rocket.height > asteroid.y):
            return True  # Collision with the rocket; game over!

    return False



def draw(window, Rocket, bullets, asteroids):

    window.fill(c_lavender)
    Rocket.draw(window)

    for bullet in bullets:
        pygame.draw.rect(window, c_black, (bullet.x, bullet.y, 5, 10))  # Bullet appearance

    for asteroid in asteroids:
        asteroid.draw(window)

    pygame.display.update()



######################
### MAIN LOOP GAME ###
######################



def main():

    run = True

    clock = pygame.time.Clock()

    spaceship = Rocket(width // 2, height - (height // 10), spaceship_width, spaceship_height)

    cooldown = 0  
    cooldown_time = 15  # Number of frames delay between shots

    asteroids = []  # List to store asteroid objects
    asteroid_counter = 0  
    asteroid_interval = 45  # Set the time interval to generate new asteroids 
    
    while run:
        clock.tick(fps)
        draw(window, spaceship, bullets, asteroids)
        cooldown = fire_bullet(spaceship, bullets, cooldown, cooldown_time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        spaceship.control()

        for asteroid in asteroids:
            asteroid.move()
            if asteroid.y > height:
                asteroids.remove(asteroid)

        # Check for collisions
        if check_collisions(spaceship, bullets, asteroids):
            run = False  # Game over


        # Update the asteroid counter
        asteroid_counter += 1
        if asteroid_counter >= asteroid_interval:
            generate_asteroids(asteroids, 3, 45)  # Generate a new asteroid at the top with size 30
            asteroid_counter = 0  



    pygame.quit()

if __name__ == "__main__":
    main()    