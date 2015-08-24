import pygame
import geometry
import graphics

class Game:
	FILL_COLOR = (100, 0, 0)
	MAX_EVENTS = 0

	def __init__(self, size):
		pygame.init()

		pygame.display.init()
		self.screen_surf = pygame.display.set_mode(size)

		self.clock = pygame.time.Clock()

		self.playfield = Playfield("config.json")
		self.field_pos = (50, 50)

		block_size = self.playfield.factory.block_size
		self.grid_renderer = graphics.GridRenderer(block_size)
		self.grid_surface = pygame.Surface((10 * block_size, 20 * block_size))

		self.step_intervall = 1000 # in ms
		self.step_clock = 0

		self.event_handlers = []

		self.set_callbacks()


	def set_callbacks(self):

		def keydown(event):
			self.playfield.shape.y += 1
			print("KEYDOWN")

		self.event_handlers.append(EventHandler(pygame.KEYDOWN, keydown))


	def run(self):
		print("Running")


		done = False
		while not done:
			delta_tick = self.clock.tick(60)
			self.step_clock += delta_tick

			event = pygame.event.poll()
			events_processed = 0
			while event.type != pygame.NOEVENT:
				for handler in self.event_handlers:
					if handler.event_type == event.type:
						handler.call(event)

				event = pygame.event.poll()

				events_processed += 1
				if events_processed > self.MAX_EVENTS:
					break

			self.tick()
			self.draw()

		quit()

	def tick(self):
		if self.step_clock >= self.step_intervall:
			self.step_clock = 0
			if geometry.collide(self.playfield.shape, self.playfield.grid, 0, 1):
				geometry.freeze(self.playfield.shape, self.playfield.grid)
				self.playfield.shape_landed()
			else:
				self.playfield.shape.y += 1



	def draw(self):
		self.screen_surf.fill(self.FILL_COLOR)
		self.grid_surface.fill((0, 0, 0, 0))

		self.grid_renderer.draw_shape(self.grid_surface, self.playfield.shape)

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

	def shape_landed(self):
		self.shape = self.next_shape
		self.next_shape = self.factory.spawn(self.factory.width)

class EventHandler:

	def __init__(self, event_type, callback):
		self.event_type = event_type
		self.callback = callback

	def call(self, event):
		self.callback(event)

