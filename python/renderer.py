import pygame, os, config
from pygame.locals import *
from environment import Environment

class Renderer():
	def __init__(self, window_scale=0.5):
		pygame.init()
		info_object = pygame.display.Info()

		screen_width = info_object.current_w
		screen_height = info_object.current_h

		window_width = int(screen_width * window_scale)
		window_height = int(screen_height * window_scale)

		window = pygame.display.set_mode((window_width, window_height))
		x_scale = window_width / config.WIDTH
		y_scale = window_height / config.HEIGHT

		self._info_object = info_object
		self._window = window
		self._window_width = window_width
		self._window_height = window_height
		self._x_scale = x_scale
		self._y_scale = y_scale

		self._load_shooter_image()
		self._load_human_image()
		self._load_zombie_image()

	def _draw_background(self):
		self._window.fill((0, 0, 0))

	def _load_image(self, name):
		path = os.path.join("images", name)
		image = pygame.image.load(path)

		if ".png" in name:
			image = image.convert_alpha()
		else:
			image = image.convert()

		return image
