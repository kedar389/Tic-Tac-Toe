import pygame as pg
import os
from symbol import Symbol
import time


class Grid:
    def __init__(self, played_board, window_res, grid_graphics):
        self.board = played_board
        self.grid_2d = grid_graphics
        self.offsetx = window_res[0] // 3.90
        self.offsety = window_res[1] // 5.33
        self.grid_resolution = window_res[0] // 2.048, window_res[1] // 1.6
        self.cell_proportions = self.grid_resolution[0] // self.board.size
        self.grid_surface = pg.Surface(self.grid_resolution)
        self.symbols_to_animate = []
        self.o_symbol = self.prepare_image(('img', "symbols", "O-10.png"))
        self.x_symbol = self.prepare_image(('img', "symbols", "X-10.png"))

    def draw_grid(self):
        self.grid_surface.blit(self.grid_2d, (0, 0))

    def animate_symbol(self, cell_posx, cell_posy, symbol):
        coordx = self.calculate_screen_coords(cell_posx)
        coordy = self.calculate_screen_coords(cell_posy)

        if symbol == "X":
            self.symbols_to_animate.append(Symbol(self.x_symbol,
                                                  (coordy, coordx),
                                                  self.cell_proportions))

        elif symbol == "O":
            self.symbols_to_animate.append(Symbol(self.o_symbol,
                                                  (coordy, coordx),
                                                  self.cell_proportions))

    def calculate_screen_coords(self, coord):
        return coord * self.cell_proportions

    def draw_win_line(self, coords):
        cell_middle = self.cell_proportions // 2

        start = (self.calculate_screen_coords(coords[0][1]) + cell_middle,
                 self.calculate_screen_coords(coords[0][0]) + cell_middle)

        end = (self.calculate_screen_coords(coords[-1][1]) + cell_middle,
               self.calculate_screen_coords(coords[-1][0]) + cell_middle)

        pg.draw.line(self.grid_surface, (0, 0, 0), start, end, 10)

    def update(self):
        for index, symbol in enumerate(self.symbols_to_animate):
            symbol.draw(self.grid_surface)
            self.symbols_to_animate.pop(index)
            time.sleep(0.15)

        if self.board.winner_coords is not None:
            self.draw_win_line(self.board.winner_coords)

    def draw(self, surface):
        surface.blit(self.grid_surface, (self.offsetx, self.offsety))

    def prepare_image(self, paths):
        cell_size = int(self.cell_proportions)
        image = pg.image.load(os.path.join(*paths))
        image = pg.transform.scale(image, (cell_size, cell_size))
        return image
