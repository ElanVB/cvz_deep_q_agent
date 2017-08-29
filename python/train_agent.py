from interface import Interface

i = Interface(max_humans=1, max_zombies=1)
i.train_agent(config=["experienced_replay", "track"])
