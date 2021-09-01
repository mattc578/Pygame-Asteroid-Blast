import pygame, random, sqlite3, math
from pygame import mixer

pygame.init()

conn = sqlite3.connect('Scores.db')
c = conn.cursor()
c.execute('''CREATE TABLE scores (
           score integer)''')

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

mixer.music.load('C:\\sci-fi-spaceship-computer-sound-effect.mp3')
mixer.music.play(-1)

playerhealth = 3
playerscore = 0
font = pygame.font.Font('freesansbold.ttf', 28)

textx = 376
texty = 0
healthx = 375
healthy = 30
highx = 0
highy = 0

def showscore(x, y):
    score = font.render('Score: '+str(playerscore), True, (0, 0, 0))
    screen.blit(score, (x, y))

def showhealth(x, y):
    health = font.render('Health: '+str(playerhealth), True, (0, 0, 0))
    screen.blit(health, (x,y))

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


bigfont = pygame.font.SysFont('calibri.', 35)

def gameoverscreen():
    gameover = bigfont.render(f'GAME OVER', True, (255, 0, 0))
    screen.blit(gameover, (160, 235))

def shootrocket(x, y):
    screen.blit(rocket, (x, y))

def highscore():
    conn = sqlite3.connect('Scores.db')
    c = conn.cursor()
    c.execute('SELECT score FROM scores')
    allscores = c.fetchall()
    greatest2least = sorted(allscores, reverse=True)
    highscore = font.render('High Score: '+str(greatest2least[0][0]), True, (0,0,0))
    screen.blit(highscore, (300, 60))

def set_pos(x, y):
    screen.blit(spaceship, (x, y))

def hitasteroid1():
    distance = math.sqrt((math.pow(asteroid1x-rocketx, 2)) + (math.pow(asteroid1y-rockety, 2)))
    if distance < 40:
        collidesound = mixer.Sound('C:\\small-explosion-sound-effect.mp3')
        collidesound.play()
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
                spaceshipxchange = -4.5
            if event.key == pygame.K_RIGHT:
                spaceshipxchange = 4.5
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
        rockety -= 5

    if rockety <= 0:
        firing = False

    spaceshipx += spaceshipxchange
    if spaceshipx < 0:
        spaceshipx = 0
    if spaceshipx > 375:
        spaceshipx = 375
    set_pos(spaceshipx, spaceshipy)

    if asteroid1falling == True:
        if timesfallen < 6:
            asteroid1y += 2.5
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

        if timesfallen >= 6 and timesfallen < 10:
            asteroid1 = pygame.image.load('C:\\asteroid2.png')
            asteroid1y += 4.5
            asteroidpos(asteroid1x, asteroid1y)

        if timesfallen >= 10 and timesfallen < 16:
            asteroid1 = pygame.image.load('C:\\asteroid3.png')
            asteroid1y += 6
            asteroidpos(asteroid1x, asteroid1y)

        if timesfallen >= 16:
            gameoverscreen()

        if playerhealth <= 0:
            asteroid1x = 2000
            asteroid1y -= 6
            gameoverscreen()

        showscore(textx, texty)
        showhealth(healthx, healthy)

        conn = sqlite3.connect('Scores.db')
        c = conn.cursor()

        c.execute('INSERT INTO scores VALUES (:score)', {
            'score' : playerscore
        })
        conn.commit()
        conn.close()

        highscore()

    pygame.display.update()
