from interface import Interface
import hyperparams

i = Interface(
	learning_rate=0.001,
	hidden_layers=(512, 512, 256, 64),
	max_humans=1, max_zombies=1, randomness=True
)
i.train_agent(save_file="default_params", config=[
	"network_update_delay",
	"frame_skip"
])

print("\nTest Score: {}\n".format(i.test_agent()))
