import pygame
import geometry
import graphics

class Game:
	FILL_COLOR = (100, 0, 0)
	MAX_EVENTS = 0

	def __init__(self, size):
		pygame.init()

		pygame.display.init()
		pygame.display.set_caption('PyTetris')
		self.screen_surf = pygame.display.set_mode(size)
		
		self.done = False

		self.clock = pygame.time.Clock()

		self.playfield = Playfield("resources/config.json")
		self.field_pos = (50, 50)

		self.block_size = self.playfield.factory.block_size
		self.grid_renderer = graphics.GridRenderer(self.block_size)
		self.grid_surface = pygame.Surface((10 * self.block_size, 20 * self.block_size))
		self.next_shape_surface = pygame.Surface((5 * self.block_size, 5 * self.block_size))

		self.step_intervall = 1070 # in ms
		self.step_clock = 0

		self.event_handlers = []

		self.set_callbacks()
		
		self.font = pygame.font.Font(
			"resources/fonts/hack/Hack-Regular.ttf",
			22
		)


	def set_callbacks(self):

		def keydown(event):
			s = self.playfield.shape
			g = self.playfield.grid
			
			if event.key == pygame.K_w:
				s.rotate_cw()
				if geometry.collide(s, g, 0, 0):
					s.rotate_ccw()
			
			if event.key == pygame.K_ESCAPE:
				self.done = True
			if event.key == pygame.K_SPACE:
				while not geometry.collide(s, g, 0, +1):
					s.y += 1
			
			if event.key == pygame.K_s and not geometry.collide(s, g, +0, +1):
				s.y += 1
			if event.key == pygame.K_a and not geometry.collide(s, g, -1, +0):
				s.x -= 1
			if event.key == pygame.K_d and not geometry.collide(s, g, +1, +0):
				s.x += 1
		
		self.event_handlers.append(EventHandler(pygame.KEYDOWN, keydown))


	def run(self):
		while not self.done:
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
		if self.step_clock >= (self.step_intervall - self.playfield.level * 70):
			self.step_clock = 0
			if geometry.collide(self.playfield.shape, self.playfield.grid, 0, 1):
				self.playfield.shape_land()
			else:
				self.playfield.shape_tick()

	def draw(self):
		self.screen_surf.fill(self.FILL_COLOR)
		self.grid_surface.fill((0, 0, 0, 0))
		self.next_shape_surface.fill((0, 0, 0, 0))
		
		shadow = geometry.shadow(self.playfield.shape, self.playfield.grid)
		
		self.grid_renderer.draw_shape(self.grid_surface, shadow)
		self.grid_renderer.draw_shape(self.grid_surface, self.playfield.shape)
		self.grid_renderer.draw(self.grid_surface, self.playfield.grid)
		self.grid_renderer.draw_shape(self.next_shape_surface,
			self.playfield.next_shape, 0, 0,
			self.next_shape_surface.get_rect().centerx
				- self.block_size * self.playfield.next_shape.side / 2,
			self.next_shape_surface.get_rect().centery
				- self.block_size * self.playfield.next_shape.side / 2)
		
		self.screen_surf.blit(self.grid_surface, self.field_pos)
		self.screen_surf.blit(self.next_shape_surface, (400, 50))
		
		text = self.font.render(
			"Score: {0}".format(self.playfield.score),
			1,
			(10, 10, 10)
		)
		text2 = self.font.render(
			"Level: {0}".format(self.playfield.level),
			1,
			(10, 10, 10)
		)

		self.screen_surf.blit(text, (400, 250))
		self.screen_surf.blit(text2, (400, 270))
		
		pygame.display.update()

	def quit(self):
		print("Quiting")

class Playfield:

	def __init__(self, path):
		self.factory = geometry.Factory(path)
		self.grid = geometry.Grid(self.factory.width, self.factory.height)
		self.shape = self.factory.spawn(self.factory.width)
		self.next_shape = self.factory.spawn(self.factory.width)
		self.scorefn = geometry.score
		self.score = 0
		self.level = 1
		self.level_clears = 0

	def shape_land(self):
		geometry.freeze(self.shape, self.grid)
		self.shape = self.next_shape
		self.next_shape = self.factory.spawn(self.factory.width)
		lines = geometry.clear(self.grid)
		geometry.drop(self.grid, lines)
		score, message = self.scorefn(lines, self.level)
		self.score += score
		self.level_clears += len(lines)
		if geometry.collide(self.shape, self.grid, 0, 0):
			print("Game Over, your score was {0} pts!".format(self.score))
			quit()

		if self.level_clears >= 10:
			self.level += 1
			self.level_clears = 0
			print("Level up! Level: {0}".format(self.level))
	
	def shape_tick(self):
		self.shape.y += 1

class EventHandler:

	def __init__(self, event_type, callback):
		self.event_type = event_type
		self.callback = callback

	def call(self, event):
		self.callback(event)

