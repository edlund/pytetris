import pygame

class Game:
	def __init__(self, size):
		pygame.init()

		pygame.display.init()
		self.surface = pygame.display.set_mode(size)

		self.clock = pygame.time.Clock()
		self.x = 10


	def run(self):
		print("Running")
		done = False
		while not done:
			self.clock.tick(60)
			self.tick()
			self.draw()

		quit()

	def tick(self):
		self.x += 1
		pass

	def draw(self):
		self.surface.fill((0, 0, 0))
		pygame.draw.rect(self.surface, (0, 255, 0), (self.x, 0, 10, 10))
		pygame.display.update()

	def quit(self):
		print("Quiting")
