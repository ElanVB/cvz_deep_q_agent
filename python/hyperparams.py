training_episodes = 35000
test_episodes = 1000
training_frames = 10000
# training_frames = 50000000
batch_size = 32
# memory_size = 200000
memory_size = 1000000
replay_start_size = 50000
state_sequence_length = 2
network_update_frequency = 1000
gamma = 0.99
frame_skip_rate = 4
learning_rate = 0.000153816352537 # RMSprop
# learning_rate = 2.5e-4 # RMSprop
gradient_momentum = 0.95 # RMSprop
squared_gradient_momentum = 0.95 # RMSprop
min_squared_gradient = 0.01
initial_epsilon = 1.0
final_epsilon = 0.1
# final_epsilon_frame = 40000
final_epsilon_frame = 1000000
final_epsilon_episode = 30000
hidden_layers = [300,  200]
activation = 'relu'
