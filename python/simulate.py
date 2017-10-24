import time, config, sys
from random import randrange
from environment import Environment
from renderer import Renderer

RENDER = False
TIME_DELAY = 0.03
MAX_HUMANS = 3
MAX_ZOMBIES	= 3

if RENDER:
	render = Renderer()

total_score = 0.0
trials = 100000
for _ in range(trials):
	if _ % max(int(trials/1000), 1) == 0:
		sys.stdout.write("\r{:.2f}% complete".format(_ * 100.0/trials))

	env = Environment(
		MAX_HUMANS, MAX_ZOMBIES,
		better_rewards=True
	)
	while len(env.humans) > 0 and len(env.zombies) > 0:
		# x = randrange(config.WIDTH)
		# y = randrange(config.HEIGHT)

		# x = env.zombies[0].x
		# y = env.zombies[0].y

		# x = env.humans[0].x
		# y = env.humans[0].y

		points = [(0, 0), (16000, 0), (0, 9000), (16000, 9000)]
		# x, y = points[randrange(len(points))]

		min_dist = 16000+9000
		index = -1
		for i in range(len(points)):
			dummy_shooter = env.shooter.copy()
			dummy_shooter.move(points[i][0], points[i][1])
			for zombie_i in env.zombies:
				dist = env.zombies[zombie_i].distance(dummy_shooter)

				if dist < min_dist:
					min_dist = dist
					index = i

		x = points[index][0]
		y = points[index][1]

		env.update(x, y)

		if RENDER:
			render.draw_environment(env)
			time.sleep(TIME_DELAY)

	total_score += env.score

print("\nAverage score: ", total_score/trials)
