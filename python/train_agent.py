from interface import Interface

i = Interface(max_humans=1, max_zombies=1)
# i = Interface(max_humans=10, max_zombies=10)
i.train_agent(config=[
	# "experienced_replay", "track"
	# "experienced_replay", "track", "frame_skip"
	"experienced_replay", "track", "experimental_network_update_delay", "frame_skip"
])
