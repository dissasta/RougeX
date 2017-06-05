import pygame
import constants
import time
from random import randint

class Tile:
    wall = pygame.image.load('Resources/wall.png')
    floor = pygame.image.load('Resources/floor.png')
    def __init__(self, block_path, posX, posY):
        self.block_path = block_path
        self.uncovered = False
        self.obscuring = False
        self.sizeX = 64
        self.sizeY = 64
        self.positionX = posX
        self.positionY = posY
        #self.image = self.choseTile()

    def choseTile(self):
        if self.block_path:
            return Tile.wall
        else:
            return Tile.floor

    def update(self):
        if self.block_path:
            self.image = Tile.wall
        else:
            self.image = Tile.floor

    def render(self, screen, layer):
        if layer == 'MAP':
            screen.blit(self.image, (self.positionX * self.sizeX, self.positionY * self.sizeY))
        elif layer == 'COVER':
            if self.uncovered == 'P':
                #write some fancy edge smoothing
                pygame.draw.rect(screen, (0,0,0), (self.positionX * self.sizeX, self.positionY * self.sizeY, self.sizeX, self.sizeY))
            elif not self.uncovered:
                pygame.draw.rect(screen, (0,0,0), (self.positionX * self.sizeX, self.positionY * self.sizeY, self.sizeX, self.sizeY))

class Player(Tile):
    def __init__(self, posX, posY):
        Tile.__init__(self, True, posX, posY)
        self.colour = (255,255,255)
        self.vision = 5
        self.orientation = None
        self.image = pygame.image.load('Resources/hero.png')

    def update(self, map):
        count = 0
        visible = [(x, self.positionY) for x in range(self.positionX - self.vision, self.positionX + self.vision + 1)]
        for y in range(self.positionY - self.vision, self.positionY):
            for x in range(self.positionX - count, self.positionX + count + 1):
                visible.append((x,y))
                visible.append((x,y + (self.vision - count) * 2))
            count += 1

        for tile in visible:
            count = self.vision

            #if not map[tile[0]][tile[1] - 1].block_path:
            map[tile[0]][tile[1]].uncovered = True

        print visible

    def render(self, screen):
        screen.blit(self.image, (self.positionX * self.sizeX, self.positionY * self.sizeY - self.sizeY / 4))

class Monster(Tile):
    def __init__(self, posX, posY):
        Tile.__init__(self, True, posX, posY)
        self.image = pygame.image.load('Resources/monster.png')

    def update(self):
        pass

    def findPath(self, map):
        found = False
        step = 0
        startTile = (self.positionX, self.positionY)
        target = (hero.positionX, hero.positionY)
        toCheck = [startTile]
        checked = []
        path = []

        while not found:
            for i in range(len(toCheck)):
                tile = toCheck.pop(0)
                northTile = (tile[0], tile[1] - 1)
                southTile = (tile[0], tile[1] + 1)
                westTile = (tile[0] - 1, tile[1])
                eastTile = (tile[0] + 1, tile[1])

                if not map[tile[0]-1][tile[1]].block_path and westTile not in checked and westTile not in toCheck:
                    toCheck.append(westTile)

                if not map[tile[0]+1][tile[1]].block_path and eastTile not in checked and eastTile not in toCheck:
                    toCheck.append(eastTile)

                if not map[tile[0]][tile[1]-1].block_path and northTile not in checked and northTile not in toCheck:
                    toCheck.append(northTile)

                if not map[tile[0]][tile[1]+1].block_path and southTile not in checked and southTile not in toCheck:
                    toCheck.append(southTile)

                checked.append(tile)
                path.append((tile[0], tile[1], step))

                if hero.positionX == tile[0] and hero.positionY == tile[1]:
                    found = True
                    break

            step += 1

        step -= 1
        while step != 1:
            nextTile = [x for x in path if x[2] == step - 1 and ((x[1] == target[1] and abs(x[0] - target[0]) == 1) or (x[0] == target[0] and abs(x[1] - target[1]) == 1))]
            randTile = nextTile[randint(0, len(nextTile) - 1)]
            target = randTile
            map[target[0]][target[1]].colour = (200,100,100)
            step -= 1

    def render(self, screen):
        screen.blit(self.image, (self.positionX * self.sizeX, self.positionY * self.sizeY - self.sizeY / 4))

class Game:
    def __init__(self):
        self.running = True
        self.size = constants.screenSize
        self.FPS = 60
        self.clock = pygame.time.Clock()

    def on_init(self):
        global hero, monster
        pygame.init()
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.map = self.map_create()
        hero = Player(7, 7)
        monster = Monster(15, 10)
        self.running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if not self.map[hero.positionX - 1][hero.positionY].block_path:
                    hero.positionX -= 1
                    hero.orientation = 'W'
            elif event.key == pygame.K_RIGHT:
                if not self.map[hero.positionX + 1][hero.positionY].block_path:
                    hero.positionX += 1
                    hero.orientation = 'E'
            elif event.key == pygame.K_UP:
                if not self.map[hero.positionX][hero.positionY - 1].block_path:
                    hero.positionY -= 1
                    hero.orientation = 'N'
            elif event.key == pygame.K_DOWN:
                if not self.map[hero.positionX][hero.positionY + 1].block_path:
                    hero.positionY += 1
                    hero.orientation = 'S'

    def on_cleanup(self):
        pygame.quit()

    def map_create(self):
        new_map = [[Tile(False, x, y) for y in range(0,constants.mapHeight)] for x in range(0, constants.mapWidth)]
        for x in range(0,constants.mapWidth):
            new_map[x][0].block_path = True

        for x in range(0,constants.mapWidth):
            new_map[x][constants.mapHeight - 1].block_path = True

        for x in range(1,40):
            new_map[x][constants.mapHeight - 45].block_path = True
            new_map[x][constants.mapHeight - 45].obscuring = True

        for y in range(0,constants.mapHeight):
            new_map[0][y].block_path = True

        for y in range(0,constants.mapHeight):
            new_map[constants.mapWidth - 1][y].block_path = True

        return new_map

    def on_loop(self):
        self.screen.fill((255,255,255))

    def on_render(self):

        #monster.findPath(self.map)
        for x in range(0, constants.mapWidth):
            for y in range(0, constants.mapHeight):
                    self.map[x][y].update()
                    self.map[x][y].render(self.screen, 'MAP')

        hero.update(self.map)
        hero.render(self.screen)
        monster.render(self.screen)

        for x in range(0, constants.mapWidth):
            for y in range(0, constants.mapHeight):
                    self.map[x][y].render(self.screen, 'COVER')

        pygame.display.update()

    def execute(self):
        if self.on_init() == False:
            self.running = False

        while self.running:

            self.clock.tick(self.FPS)

            for event in pygame.event.get():
                self.on_event(event)

            self.on_loop()
            self.on_render()

        self.on_cleanup()

if __name__ == "__main__":
    theGame = Game()
    theGame.execute()
