from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pygame


class GridRenderer:
	def __init__(self, block_size):
		self.block_size = block_size

	def draw(self, surface, grid):
		for y in range(0, grid.h):
			for x in range(0, grid.w):
				color = pygame.Color(grid.coord_to_block(x, y).color)
				pygame.draw.rect(surface, color, (x * self.block_size, y * self.block_size, self.block_size, self.block_size))
				pygame.draw.rect(surface, (40, 40, 40), (x * self.block_size, y * self.block_size, self.block_size, self.block_size), 1)


