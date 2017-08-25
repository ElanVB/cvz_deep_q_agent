import time, config, sys
from random import randrange
from environment import Environment
from renderer import Renderer

RENDER = False
TIME_DELAY = 0.05
MAX_HUMANS = 100
MAX_ZOMBIES	= 100

if RENDER:
	render = Renderer()

total_score = 0.0
trials = 100000
for _ in range(trials):
	if _ % int(trials/1000) == 0:
		sys.stdout.write("\r{:.2f}% complete".format(_ * 100.0/trials))

	env = Environment(randrange(1, MAX_HUMANS), randrange(1, MAX_ZOMBIES))
	while len(env.humans) > 0 and len(env.zombies) > 0:
		x = randrange(config.WIDTH)
		y = randrange(config.HEIGHT)
		env.update(x, y)

		if RENDER:
			render.draw_environment(env)
			time.sleep(TIME_DELAY)

	total_score += env.score

print("\nAverage score: ", total_score/trials)
