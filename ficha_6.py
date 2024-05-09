import numpy as np
import gym
import random

# Create environment
# Even though the original problem description has slippery environment, we are working in a non-slippery environment.
# In our environment, if you go right, you only go right; in the original environment, if you intend to go right, you 
# can go right, up or down with 1/3 probability.

from gym.envs.registration import register
register(
    id='FrozenLakeNotSlippery-v0',
    entry_point='gym.envs.toy_text:FrozenLakeEnv',
    kwargs={'map_name' : '4x4', 'is_slippery': False},
    max_episode_steps=100,
    reward_threshold=0.8196, # optimum = .8196, changing this seems have no influence
)

#env = gym.make("FrozenLakeNotSlippery-v0")

env = gym.make('FrozenLake-v1', is_slippery=True)


action_size = env.action_space.n
state_size = env.observation_space.n
print(f'action size: {action_size}, state size: {state_size}')

qtable = np.zeros((state_size, action_size))
print(qtable)


# Set hyperparameters for Q-learning

# @hyperparameters

total_episodes = 200        # Total episodes
max_steps = 99                # Max steps per episode

learning_rate = 0.8           # Learning rate
gamma = 0.95                  # Discounting rate

# Exploration parameters
epsilon = 1.0                 # Exploration rate
max_epsilon = 1.0             # Exploration probability at start
min_epsilon = 0.01            # Minimum exploration probability 
decay_rate = 0.001             # Exponential decay rate for exploration prob
#I find that decay_rate=0.001 works much better than 0.01

# Learn through Q-learning

# List of rewards
rewards = []

# For life or until learning is stopped
for episode in range(total_episodes):
    # Reset the environment
    state = env.reset()
#     print(f"state: {state}")
    step = 0
    done = False
    total_rewards = 0
    
    for step in range(max_steps):
#         print(f"start step...")
        # Choose an action (a) in the current world state (s)
        
        # Shall we explore or exploit?
        exp_exp_tradeoff = random.uniform(0, 1)
        
#         print(f"exp_exp_tradeoff: {exp_exp_tradeoff}")
        
        ## If this number > greater than epsilon --> exploitation 
        #(taking the biggest Q value for this state)
        if exp_exp_tradeoff > epsilon:
#             print(f"qtable[state,:] {qtable[state,:]}")
            action = np.argmax(qtable[state,:])

        # Else doing a random choice --> exploration
        else:
            action = env.action_space.sample()
            
#         print(f"action is {action}")

        # Take the action (a) and observe the outcome state(s') and reward (r)
        new_state, reward, done, info = env.step(action)
        
#         print(f"new_state: {new_state}, reward: {reward}, done: {done}, info: {info}")

        # Update Q(s,a):= Q(s,a) + lr [R(s,a) + gamma * max Q(s',a') - Q(s,a)]
        # qtable[new_state, :] : all the actions we can take from new state
        qtable[state, action] = qtable[state, action] + learning_rate * (reward + gamma * np.max(qtable[new_state, :]) - qtable[state, action])
        
#         print(f'qtable: {qtable}')
        
        total_rewards = total_rewards + reward
        
#         print(f'total_rewards {total_rewards}')
        
        # Our new state is state
        state = new_state
        
#         print(f'new state: {state}')
        
        # If done (if we're dead) : finish episode
        if done == True: 
            break
        
    # reduce epsilon (because we need less and less exploration)
    epsilon = min_epsilon + (max_epsilon - min_epsilon)*np.exp(-decay_rate*episode)
    
    rewards.append(total_rewards)

print ("Score/time: " +  str(sum(rewards)/total_episodes))
print(qtable)
print(epsilon)

# Visualize learning outcome
env.reset()
env.render()
        


# Print the action in every place
#LEFT = 0 DOWN = 1 RIGHT = 2 UP = 3
print(np.argmax(qtable,axis=1).reshape(4,4))

# Exploit!

#All the episodes are the same taking the maximum of Qtable value every time
env.reset()

for episode in range(5):
    state = env.reset()
    step = 0
    done = False
    print("****************************************************")
    print("EPISODE ", episode)

    for step in range(max_steps):
        env.render()
        # Take the action (index) that have the maximum expected future reward given that state
        action = np.argmax(qtable[state,:])
        
        new_state, reward, done, info = env.step(action)
        
        if done:
            break
        state = new_state
    env.render()

env.reset()
env.close()