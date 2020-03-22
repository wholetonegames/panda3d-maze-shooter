import z_levels
import z_grid_palette


class MapsModel:
    def __init__(self):
        self.maps = [
            {
                "model": "grid_w17xh13",
                "blockTypes": z_grid_palette.test,
                "pattern": z_levels.test,
                "enemyNumber": self.count_occurrences(z_levels.test, 'e'),
                "startPos": 0,
                "doorList": []
            }
        ]

    def count_occurrences(self, map_str, element):
        count = 0
        for i in map_str:
            if i == element:
                count += 1
        return count
