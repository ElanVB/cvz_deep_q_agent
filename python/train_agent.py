from interface import Interface
import hyperparams

i = Interface(
	learning_rate=0.001,
	hidden_layers=(1024, 512, 128, 128, 128, 64),
	max_humans=1, max_zombies=1, randomness=True, render=True
)
i.train_agent(save_file="1_5k_online", config=[
	"experienced_replay",
	# "experimental_network_update_delay",
	"frame_skip"
])

print("\nTest Score: {}\n".format(i.test_agent()))
