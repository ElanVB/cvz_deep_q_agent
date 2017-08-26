import time, config, sys
from random import randrange
from environment import Environment
from renderer import Renderer

RENDER = True
TIME_DELAY = 0.03
MAX_HUMANS = 5
MAX_ZOMBIES	= 5

if RENDER:
	render = Renderer()

total_score = 0.0
trials = 10
for _ in range(trials):
	if _ % max(int(trials/1000), 1) == 0:
		sys.stdout.write("\r{:.2f}% complete".format(_ * 100.0/trials))

	env = Environment(
		randrange(1, MAX_HUMANS+1),
		randrange(1, MAX_ZOMBIES+1),
		better_rewards=True
	)
	while len(env.humans) > 0 and len(env.zombies) > 0:
		x = randrange(config.WIDTH)
		y = randrange(config.HEIGHT)
		env.update(x, y)

		if RENDER:
			render.draw_environment(env)
			time.sleep(TIME_DELAY)

	total_score += env.score

print("\nAverage score: ", total_score/trials)
