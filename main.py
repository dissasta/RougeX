import pygame
import constants
import time
from random import randint

class Tile:
    def __init__(self, block_path):
        self.block_path = block_path
        self.colour = self.pickColour()

    def pickColour(self):
        if self.block_path:
            return (0,0,0)
        else:
            return (100,100,100)

class Game:
    def __init__(self):
        self.running = True
        self.size = constants.screenSize
        self.FPS = 60
        self.clock = pygame.time.Clock()

    def on_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.map = self.map_create()
        self.running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False

    def on_cleanup(self):
        pygame.quit()

    def findPath(self):
        found = False
        step = 0
        startTile = (constants.playerPostionX, constants.playerPostionY)
        target = (constants.targetPostionX, constants.targetPostionY)
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

                if not self.map[tile[0]-1][tile[1]].block_path and westTile not in checked and westTile not in toCheck:
                    toCheck.append(westTile)

                if not self.map[tile[0]+1][tile[1]].block_path and eastTile not in checked and eastTile not in toCheck:
                    toCheck.append(eastTile)

                if not self.map[tile[0]][tile[1]-1].block_path and northTile not in checked and northTile not in toCheck:
                    toCheck.append(northTile)

                if not self.map[tile[0]][tile[1]+1].block_path and southTile not in checked and southTile not in toCheck:
                    toCheck.append(southTile)

                checked.append(tile)
                path.append((tile[0], tile[1], step))

                if tile == target:
                    found = True
                    break

            step += 1

        step -= 1

        while step != 1:
            nextTile = [x for x in path if x[2] == step - 1 and ((x[1] == target[1] and abs(x[0] - target[0]) == 1) or (x[0] == target[0] and abs(x[1] - target[1]) == 1))]
            randTile = nextTile[randint(0, len(nextTile) - 1)]
            target = randTile
            self.map[target[0]][target[1]].colour = (200,100,100)
            step -= 1

    def map_create(self):
        new_map = [[Tile(False) for y in range(0,constants.mapHeight)] for x in range(0, constants.mapWidth)]
        for x in range(0,constants.mapWidth):
            new_map[x][0].block_path = True
            new_map[x][0].colour = (0,0,0)

        for x in range(0,constants.mapWidth):
            new_map[x][constants.mapHeight - 1].block_path = True
            new_map[x][constants.mapHeight - 1].colour = (0,0,0)

        for x in range(1,45):
            new_map[x][constants.mapHeight -20].block_path = True
            new_map[x][constants.mapHeight -20].colour = (0,0,0)

        for y in range(0,constants.mapHeight):
            new_map[0][y].block_path = True
            new_map[0][y].colour = (0,0,0)

        for y in range(0,constants.mapHeight):
            new_map[constants.mapWidth - 1][y].block_path = True
            new_map[constants.mapWidth - 1][y].colour = (0,0,0)

        new_map[constants.playerPostionX][constants.playerPostionY].player = True
        new_map[constants.playerPostionX][constants.playerPostionY].colour = constants.playerColour

        new_map[constants.targetPostionX][constants.targetPostionY].traget = True
        new_map[constants.targetPostionX][constants.targetPostionY].colour = constants.targetColour

        return new_map

    def on_loop(self):
        self.screen.fill((255,255,255))

    def on_render(self):
        for x in range(0, constants.mapWidth):
            for y in range(0, constants.mapHeight):
                    pygame.draw.rect(self.screen, (self.map[x][y].colour), (x * constants.tileSize,y * constants.tileSize, constants.tileSize, constants.tileSize))

        pygame.display.update()

    def execute(self):
        if self.on_init() == False:
            self.running = False

        self.findPath()

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
