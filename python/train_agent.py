from interface import Interface
import hyperparams

i = Interface(
	learning_rate=hyperparams.learning_rate,
	state_sequence_length=hyperparams.state_sequence_length,
	hidden_layers=hyperparams.hidden_layers,
	max_humans=1, max_zombies=1
)
i.train_agent(config=[
	# "experienced_replay", "track"
	# "experienced_replay", "track", "frame_skip"
	"experienced_replay", "track", "experimental_network_update_delay",
	"frame_skip"
])
i.test_agent()
