from interface import Interface
import hyperparams

i = Interface(
	# learning_rate=0.0003353628856001657,
	learning_rate=0.001,
	# hidden_layers=(1024, 512, 128, 128, 128, 64),
	hidden_layers=(512, 512, 256, 64),
	# max_humans=3, max_zombies=3, randomness=True,
	max_humans=1, max_zombies=1, randomness=True,
	state_type="image"
	# render=True
	# network_type="DDQ"
)
i.train_agent(
	check_point_frequency=100,
	# replay_type="truncated",
	save_file="conv_network_update_delay", config=[
	# save_file="target_network_update_delay", config=[
	# "target_network_update_delay",
	"network_update_delay",
	# "log",
	"frame_skip"
])

print("\nTest Score: {}\n".format(i.test_agent()))
