import sys
import pygame, random
from pygame.locals import *

STARTING_FPS = 4
FPS_INCREMENT_FREQUENCY = 80

IMG = pygame.image.load('fon.jpg')
DIRECTION_UP = 1
DIRECTON_DOWN = 2
DIRECTION_LEFT = 3
DIRECTION_RIGHT = 4

WORLD_SIZE_X = 20
WORLD_SIZE_Y = 20

SNAKE_START_LENGTH = 4
SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 0, 0)


class Snake:
    def __init__(self, x, y, startLength):
        self.startLength = startLength
        self.startX = x
        self.startY = y
        self.reset()

    def reset(self):
        self.pieces = []
        self.direction = 1

        for n in range(0, self.startLength):
            self.pieces.append((self.startX, self.startY + n))

    def changeDirection(self, direction):
        if self.direction == 1 and direction == 2:
            return
        if self.direction == 2 and direction == 1:
            return
        if self.direction == 3 and direction == 4:
            return
        if self.direction == 4 and direction == 3:
            return

        self.direction = direction

    def getHead(self):
        return self.pieces[0]

    def getTail(self):
        return self.pieces[len(self.pieces) - 1]

    def update(self):
        (headX, headY) = self.getHead()
        head = ()

        if self.direction == 1:
            head = (headX, headY - 1)
        elif self.direction == 2:
            head = (headX, headY + 1)
        elif self.direction == 3:
            head = (headX - 1, headY)
        elif self.direction == 4:
            head = (headX + 1, headY)

        self.pieces.insert(0, head)
        self.pieces.pop()

    def grow(self):
        (tx, ty) = self.getTail()
        piece = ()

        if self.direction == 1:
            piece = (tx, ty + 1)
        elif self.direction == 2:
            piece = (tx, ty - 1)
        elif self.direction == 3:
            piece = (tx + 1, ty)
        elif self.direction == 4:
            piece = (tx - 1, ty)

        self.pieces.append(piece)

    def collidesWithSelf(self):
        for p in self.pieces:
            if len(self.pieces) - len([c for c in self.pieces if c != p]) > 1:
                return True
            return False
        return len([p for p in self.pieces if p == self.getHead()]) > 1


class SnakeGame:
    def __init__(self, window, screen, clock, font):
        self.window = window
        self.screen = screen
        self.clock = clock
        self.font = font

        self.fps = STARTING_FPS
        self.ticks = 0
        self.playing = True
        self.score = 0

        self.nextDirection = DIRECTION_UP
        self.sizeX = WORLD_SIZE_X
        self.sizeY = WORLD_SIZE_Y
        self.food = []
        self.snake = Snake(WORLD_SIZE_X / 2, WORLD_SIZE_Y / 2, SNAKE_START_LENGTH)

        self.addFood()

    def addFood(self):
        fx = None
        fy = None

        while fx is None or fy is None or (fx, fy) in self.food:
            fx = random.randint(1, self.sizeX)
            fy = random.randint(1, self.sizeY)

        self.food.append((fx, fy))

    def input(self, events):
        for e in events:
            if e.type == QUIT:
                return False

            elif e.type == KEYUP:
                if e.key == K_UP:
                    self.nextDirection = DIRECTION_UP
                elif e.key == K_DOWN:
                    self.nextDirection = DIRECTON_DOWN
                elif e.key == K_LEFT:
                    self.nextDirection = DIRECTION_LEFT
                elif e.key == K_RIGHT:
                    self.nextDirection = DIRECTION_RIGHT
                elif e.key == K_SPACE and not self.playing:
                    self.reset()

        return True

    def update(self):
        self.snake.changeDirection(self.nextDirection)
        self.snake.update()

        for food in self.food:
            if self.snake.getHead() == food:
                self.food.remove(food)
                self.addFood()
                self.snake.grow()
                self.score += len(self.snake.pieces) * 50
                pygame.mixer.music.load('hruste (mp3cut.net).mp3')
                pygame.mixer.music.play(0)

        (hx, hy) = self.snake.getHead()
        if self.snake.collidesWithSelf() or hx < 1 or hy < 1 or hx > self.sizeX or hy > self.sizeY:
            pygame.mixer.music.load('gameofer.mp3')
            pygame.mixer.music.play(0)
            self.playing = False

    def reset(self):
        self.playing = True
        self.nextDirection = DIRECTION_UP
        self.fps = STARTING_FPS
        self.score = 0
        self.snake.reset()

    def draw(self):
        self.screen.fill((45, 45, 45))
        self.screen.blit(IMG, (0, 0))

        (width, height) = self.window.get_size()
        blockWidth = int(width / self.sizeX)
        blockHeight = int(height / self.sizeY)

        for num, (px, py) in enumerate(self.snake.pieces):
            all_sprites = pygame.sprite.Group()
            # создать спрайт для изображения и добавить его в группу all_sprites
            sprite = pygame.sprite.Sprite(all_sprites)
            if num == 0:  # если нужно отобразить голову змеи
                sprite.image = pygame.image.load('zmeika_head.png')  # загрузить в спрайт изображение головы
            else:
                sprite.image = pygame.image.load('zmeika2.png')  # загрузить в спрайт изображение сегмента тела
            sprite.rect = sprite.image.get_rect()
            sprite.rect.x = blockWidth * (px - 1)
            sprite.rect.y = blockHeight * (py - 1)
            sprite.image.set_colorkey((255, 255, 255))
            all_sprites.draw(self.screen)
        pygame.display.flip()


        for (fx, fy) in self.food:
            all_sprites = pygame.sprite.Group()
            # создать спрайт для изображения и добавить его в группу all_sprites
            sprite = pygame.sprite.Sprite(all_sprites)
            sprite.image = pygame.image.load('apple.png')  # загрузить в спрайт изображение
            sprite.rect = sprite.image.get_rect()
            sprite.rect.x = blockWidth * (fx - 1)
            sprite.rect.y = blockHeight * (fy - 1)
            sprite.image.set_colorkey((255, 255, 255))
            all_sprites.draw(self.screen)
        pygame.display.flip()


    def drawDeath(self):
        self.screen.blit(self.font.render("Game over! Нажмите пробел, чтобы начать новую игру", 1, (255, 255, 255)),
                         (150, 300))
        self.screen.blit(self.font.render("Количество очков: %d" % self.score, 1, (255, 255, 255)), (350, 330))
        pygame.display.flip()

    def run(self, events):
        if not self.input(events):
            return False

        if self.playing:
            self.update()
            self.draw()
        else:
            self.drawDeath()

        self.clock.tick(self.fps)

        self.ticks += 1
        if self.ticks % FPS_INCREMENT_FREQUENCY == 0:
            self.fps += 1
        return True


def main():
    pygame.init()
    pygame.display.set_caption('Snake')

    window = pygame.display.set_mode((800, 800))
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()
    font = pygame.font.Font('freesansbold.ttf', 20)
    game = SnakeGame(window, screen, clock, font)

    while game.run(pygame.event.get()):
        pass

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
