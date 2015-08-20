import pygame
import geometry
import graphics

class Game:
	FILL_COLOR = (100, 0, 0)

	def __init__(self, size):
		pygame.init()

		pygame.display.init()
		self.screen_surf = pygame.display.set_mode(size)

		self.clock = pygame.time.Clock()

		self.playfield = Playfield("tetrominos.json")
		self.field_pos = (50, 50)

		block_size = self.playfield.factory.block_size
		self.grid_renderer = graphics.GridRenderer(block_size)
		self.grid_surface = pygame.Surface((10 * block_size, 20 * block_size))

	def run(self):
		print("Running")
		done = False
		while not done:
			self.clock.tick(60)
			self.tick()
			self.draw()

		quit()

	def tick(self):
		pass

	def draw(self):
		self.screen_surf.fill(self.FILL_COLOR)
		self.grid_surface.fill((0, 0, 0, 0))

		self.grid_renderer.draw(self.grid_surface, self.playfield.grid)
		self.screen_surf.blit(self.grid_surface, self.field_pos)

		pygame.display.update()

	def quit(self):
		print("Quiting")

class Playfield:

	def __init__(self, path):
		self.factory = geometry.Factory(path)
		self.grid = geometry.Grid(self.factory.width, self.factory.height)
		self.shape = self.factory.spawn(self.factory.width)
		self.next_shape = self.factory.spawn(self.factory.width)

