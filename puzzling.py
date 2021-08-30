import pygame, random, sqlite3, math


pygame.init()

conn = sqlite3.connect('Scores.db')
c = conn.cursor()
# c.execute('''CREATE TABLE scores (
#             score integer)''')

screen = pygame.display.set_mode((500, 500))
running = True
pygame.display.set_caption('Asteroid Blast')
icon = pygame.image.load('C:\\spaceshipicon.png')
pygame.display.set_icon(icon)

background = pygame.image.load('C:\\spacebackground (1).png')

spaceship = pygame.image.load('C:\\spaceshipp.png')
spaceshipx = 185
spaceshipy = 375
spaceshipxchange = 0

playerhealth = 3
playerscore = 0

rocket = pygame.image.load('C:\\rocket.png')
rocketshipx = 0
rocketshipy = 0
rocketx = spaceshipx
rockety = spaceshipy
firing = False

asteroid1 = pygame.image.load('C:\\asteroid1.png')
asteroid1x = random.randint(0, 375)
asteroid1y = 0
asteroid1health = 1
asteroid1destroy = False
asteroid1falling = True
timesfallen = 1

def shootrocket(x, y):
    screen.blit(rocket, (x, y))

def set_pos(x, y):
    screen.blit(spaceship, (x, y))

def hitasteroid1():
    distance = math.sqrt((math.pow(asteroid1x-rocketx, 2)) + (math.pow(asteroid1y-rockety, 2)))
    if distance < 40:
        return True
    else:
        return False

def asteroidpos(x, y):
    screen.blit(asteroid1, (x, y))

while running:
    screen.fill((7, 11, 52))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                spaceshipxchange = -1.55
            if event.key == pygame.K_RIGHT:
                spaceshipxchange = 1.55
            if event.key == pygame.K_SPACE:
                if firing == False:
                    rocketx = spaceshipx
                    rockety = spaceshipy
                    firing = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                spaceshipxchange = 0

    if firing is True:
        shootrocket(rocketx + 36, rockety)
        rockety -= 1.5

    if rockety <= 0:
        firing = False

    spaceshipx += spaceshipxchange
    if spaceshipx < 0:
        spaceshipx = 0
    if spaceshipx > 375:
        spaceshipx = 375
    set_pos(spaceshipx, spaceshipy)

    if asteroid1falling == True:
        asteroid1y += 0.5
        asteroidpos(asteroid1x, asteroid1y)

        iscollided = hitasteroid1()

        if iscollided == True:
            asteroid1x = random.randint(0, 375)
            asteroid1y = 0
            timesfallen += 1
            rocketx = spaceshipx
            firing = False
            rockety = -1
            playerscore += 1
        elif iscollided != True:
            if asteroid1y > 500:
                playerhealth -= 1
                playerscore -= 1
                asteroid1x = random.randint(0, 375)
                asteroid1y = 0
                timesfallen += 1
            #change when timesfallen is 6
        print(playerscore)
        print(playerhealth)
    pygame.display.update()
conn.commit()
conn.close()
