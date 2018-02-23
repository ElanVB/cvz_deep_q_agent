import pygame, os, config
from pygame.locals import *
from environment import Environment

class Renderer():
	def __init__(self, window_scale=0.5, render_state=False, two_player=False):
		if not isinstance(window_scale, float):
			raise TypeError("window_scale must be a float")

		if window_scale <= 0 or window_scale > 1.0:
			raise ValueError("window_scale must be in the range (0.0, 1.0]")

		pygame.init()
		info_object = pygame.display.Info()

		screen_width = info_object.current_w
		screen_height = info_object.current_h

		window_width = int(screen_width * window_scale)
		window_height = int(window_width / config.WIDTH * config.HEIGHT)

		if window_height > screen_height * 0.94:
			window_height = int(screen_height * 0.94)
			window_width = int(window_height / config.HEIGHT * config.WIDTH)

		self._render_state = render_state
		if render_state or two_player:
			self._window  = pygame.display.set_mode((window_width*2, window_height))
			self._state_window = pygame.display.set_mode((window_width*2, window_height))
		else:
			self._window  = pygame.display.set_mode((window_width, window_height))


		x_scale = window_width / config.WIDTH
		y_scale = window_height / config.HEIGHT

		self._info_object = info_object
		self._window_width = window_width
		self._window_height = window_height
		self._x_scale = x_scale
		self._y_scale = y_scale

		self._load_shooter_image()
		self._load_human_image()
		self._load_zombie_image()

		pygame.font.init()
		self._font = pygame.font.SysFont("Arial", 30)
		self._winner_font = pygame.font.SysFont("Arial", 100)

		self._two_player = two_player

	def _draw_background(self, window):
		window.fill((0, 0, 0))

	def _load_image(self, name):
		path = os.path.join("images", name)
		image = pygame.image.load(path)

		if ".png" in name:
			image = image.convert_alpha()
		else:
			image = image.convert()

		return image

	def _load_shooter_image(self):
		shooter_image = self._load_image("Shooter.png")

		width = int(config.SHOOTER_INTERACT_RANGE * 2 * self._x_scale)
		height = int(config.SHOOTER_INTERACT_RANGE * 2 * self._y_scale)

		self._shooter_image = pygame.transform.scale(
			shooter_image, (width, height)
		)

	def _load_human_image(self):
		human_image = self._load_image("Human.png")

		width = int(config.ZOMBIE_INTERACT_RANGE * 2 * self._x_scale)
		height = int(config.ZOMBIE_INTERACT_RANGE * 2 * self._y_scale)

		self._human_image = pygame.transform.scale(
			human_image, (width, height)
		)

	def _load_zombie_image(self):
		zombie_image = self._load_image("Zombie.png")

		width = int(config.ZOMBIE_INTERACT_RANGE * 2 * self._x_scale)
		height = int(config.ZOMBIE_INTERACT_RANGE * 2 * self._y_scale)

		self._zombie_image = pygame.transform.scale(
			zombie_image, (width, height)
		)

	def _draw_shooter(self, window, x, y, offset):
		x_pos = int((x - config.SHOOTER_INTERACT_RANGE) * self._x_scale) + (offset * self._window_width)
		y_pos = int((y - config.SHOOTER_INTERACT_RANGE) * self._y_scale)
		window.blit(
			self._shooter_image,
			(x_pos, y_pos)
		)

	def _draw_human(self, window, x, y, offset):
		x_pos = int((x - config.ZOMBIE_INTERACT_RANGE) * self._x_scale) + (offset * self._window_width)
		y_pos = int((y - config.ZOMBIE_INTERACT_RANGE) * self._y_scale)
		window.blit(
			self._human_image,
			(x_pos, y_pos)
		)

	def _draw_zombie(self, window, x, y, offset):
		x_pos = int((x - config.ZOMBIE_INTERACT_RANGE) * self._x_scale) + (offset * self._window_width)
		y_pos = int((y - config.ZOMBIE_INTERACT_RANGE) * self._y_scale)
		window.blit(
			self._zombie_image,
			(x_pos, y_pos)
		)

	def _draw_state(self, state):
		for row in range(state.shape[0]):
			for col in range(state.shape[1]):
				color = state[row][col] * 255
				y = row * self._window_height / state.shape[0]
				x = col * self._window_width / state.shape[1] + self._window_width
				width = self._window_width / state.shape[1]
				height = self._window_height / state.shape[0] + 1
				pygame.draw.rect(self._state_window, (color, color, color), (x, y, width, height))

	def draw_environment(self, environment, player_two=False):
		if not isinstance(environment, Environment):
			raise TypeError("environment must be of type Environment")

		if player_two:
			window = self._state_window
		else:
			window = self._window

		if not player_two:
			self._draw_background(window)

		# draw boarder
		color = (255, 0, 0) if player_two else (0, 255, 0)
		pygame.draw.rect(window, color, (0 + (player_two * self._window_width), 0, self._window_width, self._window_height), 10)

		self._draw_shooter(window, environment.shooter.x, environment.shooter.y, player_two)

		for zombie_id in environment.zombies:
			self._draw_zombie(
				window,
				environment.zombies[zombie_id].x,
				environment.zombies[zombie_id].y,
				player_two
			)

		for human_id in environment.humans:
			self._draw_human(
				window,
				environment.humans[human_id].x,
				environment.humans[human_id].y,
				player_two
			)

		if self._render_state:
			self._draw_state(environment.get_state_image())

		score_text = self._font.render("Score: {}".format(environment.score), False, (255, 255, 255))
		window.blit(score_text, (0 + (player_two * self._window_width), 0))

		if self._two_player and player_two:
			pygame.display.update()
		# pygame.display.update()

	def draw_winner(self, player_one, player_two):
		winner_text = self._winner_font.render("WINNER", False, (255, 255, 255))
		
		if player_one > player_two:
			self._window.blit(winner_text, (self._window_width/6, self._window_height/2.5))
		elif player_two > player_one:
			self._window.blit(winner_text, (self._window_width + self._window_width/6, self._window_height/2.5))
		else:
			winner_text = self._winner_font.render("DRAW", False, (255, 255, 255))
			self._window.blit(winner_text, (self._window_width/3.5, self._window_height/2.5))
			self._window.blit(winner_text, (self._window_width + self._window_width/3.5, self._window_height/2.5))

		pygame.display.update()

	def get_mouse_pos(self):
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.MOUSEMOTION:
				self._last_mouse_pos = event.pos

		return self._last_mouse_pos

	def freeze(self):
		loop = True
		while loop:
			for event in pygame.event.get():
				if event.type is QUIT:
					pygame.quit()
					exit()
				elif event.type is KEYDOWN:
					loop = False
				elif event.type is MOUSEBUTTONUP:
					loop = False
