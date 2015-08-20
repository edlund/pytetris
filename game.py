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

		self.playfield = geometry.Grid(10, 20)
		# TODO: load from config
		self.block_size = 32
		self.field_pos = (50, 50)

		self.grid_renderer = graphics.GridRenderer(self.block_size)
		self.grid_surface = pygame.Surface((10*self.block_size, 20*self.block_size))

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

		self.grid_renderer.draw(self.grid_surface, self.playfield)
		self.screen_surf.blit(self.grid_surface, self.field_pos)

		pygame.display.update()

	def quit(self):
		print("Quiting")
