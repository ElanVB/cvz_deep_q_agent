from interface import Interface

i = Interface(max_humans=1, max_zombies=1)
i.initialize_agent(weights="experienced_replay-track-4act.h5")
i.test_agent()
# i.demo_agent()
