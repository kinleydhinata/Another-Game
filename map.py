from settings import *

class GameMap:
    def __init__(self):
        self.map = [
            '################',
            '#..............#',
            '#....######....#',
            '#..............#',
            '#...........####',
            '#..............#',
            '#....#####.....#',
            '#..............#',
            '###............#',
            '#..............#',
            '#....######....#',
            '#..............#',
            '#...........####',
            '#..............#',
            '#..............#',
            '################',
        ]
        self.world_map = {}
        self.get_map()

    def get_map(self):
        self.world_map = {(i * TILE, j * TILE): char
                          for j, row in enumerate(self.map)
                          for i, char in enumerate(row) if char != '.'}

    def is_wall(self, x, y):
        return (int(x) // TILE * TILE, int(y) // TILE * TILE) in self.world_map