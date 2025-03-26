import pygame, random
import os

# TAMAÑO DEL LIENZO
WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ROOT_DIR = os.path.dirname(__file__)
IMAGE_DIR = os.path.join(ROOT_DIR, 'assets')


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('GALAGA')
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(IMAGE_DIR, 'player.png')).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0

    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0


class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(IMAGE_DIR, 'meteorGrey_big1.png'))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-5, 5)

    def update(self):
        # Movimiento de los meteoros
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        # Si un meteorito se sale de la pantalla por abajo, lo reposicionamos en la parte superior
        if self.rect.top > HEIGHT:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)


class Disparo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(os.path.join(IMAGE_DIR, 'laser1.png'))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10  # Velocidad de disparo hacia arriba

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:  # El disparo sale de la pantalla
            self.kill()


background = pygame.image.load(os.path.join(IMAGE_DIR, 'espacio.jpg')).convert()

# Grupos de sprites
all_sprites = pygame.sprite.Group()
meteor_list = pygame.sprite.Group()
disparos_list = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# Crear meteoros y agregarlos a los grupos
for i in range(8):
    meteor = Meteor()
    all_sprites.add(meteor)
    meteor_list.add(meteor)

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Detectamos cuando se presiona la tecla espacio
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                disparo = Disparo(player.rect.centerx, player.rect.top)
                all_sprites.add(disparo)
                disparos_list.add(disparo)

    all_sprites.update()

    # Detectamos las colisiones entre los meteoros y los disparos
    
    colisionM = pygame.sprite.groupcollide(meteor_list, disparos_list, True, True)
    
    for meteor in colisionM:
        nuevo_meteor = Meteor()
        all_sprites.add(nuevo_meteor)
        meteor_list.add(nuevo_meteor)

    # Detectamos las colisiones entre los meteoros y el jugador
    colisionJ = pygame.sprite.spritecollide(player, meteor_list, True)

    if colisionJ:   
       print("Game Over")
        
    screen.blit(background, [0, 0])

    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()
