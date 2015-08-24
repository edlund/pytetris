from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pygame


class GridRenderer:
	def __init__(self, block_size):
		self.block_size = block_size

	def draw(self, surface, grid, origo_x = 0, origo_y = 0):
		for y in range(0, grid.h):
			for x in range(0, grid.w):
				color = pygame.Color(grid.coord_to_block(x, y).color)
				real_x = origo_x + x
				real_y = origo_y + y
				pygame.draw.rect(surface, color, (real_x * self.block_size, real_y * self.block_size, self.block_size, self.block_size))
				pygame.draw.rect(surface, (40, 40, 40), (real_x * self.block_size, real_y * self.block_size, self.block_size, self.block_size), 1)

	def draw_shape(self, surface, shape):
		self.draw(surface, shape.grid(), shape.x, shape.y)


