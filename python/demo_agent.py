from interface import Interface
import hyperparams
# environment="web_levels/1504642254851.log"
i = Interface(
	max_humans=1, max_zombies=1, render_delay=0.06
)
# i = Interface(max_humans=4, max_zombies=20, render_delay=0.06, randomness=True)
i.initialize_agent(weights="experienced_replay-track-experimental_network_update_delay-frame_skip.h5")
# i.initialize_agent(weights="hum_4_zom_20.h5")
i.test_agent()
i.demo_agent(infinite=True)
