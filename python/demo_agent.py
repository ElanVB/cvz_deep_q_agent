from interface import Interface
import hyperparams
# environment="web_levels/1504642254851.log"
i = Interface(
	max_humans=5, max_zombies=20, render_delay=0.06
)
# i = Interface(max_humans=4, max_zombies=20, render_delay=0.06, randomness=True)
i.initialize_agent(weights="5_20_demo")
# i.initialize_agent(weights="hum_4_zom_20.h5")
i.test_agent()
i.demo_agent(infinite=True)
