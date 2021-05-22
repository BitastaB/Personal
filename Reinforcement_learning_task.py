import gym
import numpy as np

print("Testing gym")
env = gym.make('Taxi-v3')


def train():
    print("* * * * * * * STARTING training * * * * * * *")
    q = np.full((env.observation_space.n, env.action_space.n), -0.001)
    gamma = 0.6
    delta = 0.1
    for t in range(1, 2000):
        steps = 0
        done = False
        current_state = env.reset()  # initial state
        print("starting new episode")
        print("initial state:\n")
        env.render()
        while not done:
            episode_reward = 0
            action = np.argmax(q[current_state])
            next_state, reward, done, info = env.step(action)
            q[current_state][action] += ((1 / t ** delta) * (reward + (gamma * np.max(q[next_state]) - q[current_state][action])))
            current_state = next_state
            steps += 1
            episode_reward += reward

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
        rewards, steps = 0, 0
        print(f"passenger {passenger+1} starting with initial state...")
        env.render()
        while not done:
            action = np.argmax(Q[current_state])
            next_state, reward, done, info = env.step(action)
            current_state = next_state
            steps += 1
            rewards += reward
        env.render()
        print(f"passenger {passenger+1} converged with {steps} steps and {rewards} reward with the above final state")
        print("=========================================================================================================")


test()
