import gym
import numpy as np

print("Testing gym")
env = gym.make('Taxi-v3')
#env = gym.make('FrozenLake-v0')



def train():
    print("training")
    q = np.full((env.observation_space.n, env.action_space.n), -0.001)
    gamma = 0.8
    delta = 0.8
    for t in range(1, 300):
        steps = 0
        done = False
        current_state = env.reset()  # initial state
        print("starting new episode")
        print("current q : \n",q,"\n\n")
        while not done:
            episode_reward = 0
           # print("current state : ", current_state)
           # print("q current state : ",q[current_state])
            #  print("iteration {}", t)
            action = np.argmax(q[current_state])
            env.render()
           # print("action : ", action)
            next_state, reward, done, info = env.step(action)
           # print(f"reward : {reward}")
           # print(f"next state : ", next_state)
           # print("q current state before change : ", q[current_state])
            q[current_state][action] += ((1 / t ** delta) * (reward + (gamma * np.max(q[next_state]) - q[current_state][action])))
           # print("q current state after change : ", q[current_state])
           # print("q changed val : ", q[current_state][action])
            current_state = next_state
            steps += 1
            episode_reward += reward
          #  print(f"step {steps} finished\nis it done? {done}\n")
            if done:
                print("total reward for this episode", episode_reward)

        print(f"episode converged in {steps} steps")
train()

