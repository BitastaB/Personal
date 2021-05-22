import gym
import numpy as np

print("Testing gym")
env = gym.make('Taxi-v3')
#env = gym.make('FrozenLake-v0')

def train():
    print("training")
    q = np.full((env.observation_space.n, env.action_space.n), -0.0015)
    gamma = 0.8
    delta = 0.8
    for t in range(1, 15000):
        steps = 0
        done = False
        current_state = env.reset()  # initial state
        print("starting new episode")
        print("initial state:\n")
        env.render()
        while not done:
            episode_reward = 0
           # print("current state : ", current_state)
           # print("q current state : ",q[current_state])
            #  print("iteration {}", t)
            action = np.argmax(q[current_state])
           # env.render()
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

        print(f"episode converged in {steps} steps")
        print("total reward for this episode", episode_reward)
        print("final state")
        env.render()
        print("==============================================================================")
    return q


Q = train()

def test():
    print("* * * * * * * STARTING testing * * * * * * * ")
    n = 10
    total_mistakes = 0
    for passenger in range(n):
        current_state = env.reset()
        done = False
        rewards, steps, mistakes = 0, 0, 0
        print(f"passenger {passenger+1} starting ...")
        while not done:
            env.render()
            action = np.argmax(Q[current_state])
            next_state, reward, done, info = env.step(action)
            current_state = next_state
            if reward == -10:
                mistakes += 1
            steps += 1
            rewards += reward
        total_mistakes += mistakes
        print(f"passenger {passenger+1} converged with {steps} steps and {rewards} reward and {mistakes} mistakes")
        print("=========================================================================================================")
    print("total mistakes", total_mistakes/n)


test()
