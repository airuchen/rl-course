import numpy as np
import matplotlib.pyplot as plt
import random


class GaussianBandit:
    def __init__(self):
        self._arm_means = np.random.uniform(0., 1., 10)  # Sample some means
        self.n_arms = len(self._arm_means)
        self.rewards = []
        self.total_played = 0

    def reset(self):
        self.rewards = []
        self.total_played = 0

    def play_arm(self, a):
        reward = np.random.normal(self._arm_means[a], 1.)  # Use sampled mean and covariance of 1.
        self.total_played += 1
        self.rewards.append(reward)
        return reward


def greedy(bandit, timesteps):
    rewards = np.zeros(bandit.n_arms)
    n_plays = np.zeros(bandit.n_arms)
    Q = np.zeros(bandit.n_arms)
    possible_arms = range(bandit.n_arms)

    # TODO: init variables (rewards, n_plays, Q) by playing each arm once
    rewards = [bandit.play_arm(a) for a in possible_arms]
    n_plays = [1 for a in possible_arms]
    Q = [rewards[a] / n_plays[a] for a in possible_arms]

    # Main loop
    while bandit.total_played < timesteps:
        # This example shows how to play a random arm:
        # a = random.choice(possible_arms)
        # reward_for_a = bandit.play_arm(a)
        # TODO: instead do greedy action selection
        a = np.argmax(Q)
        reward_for_a = bandit.play_arm(a)
        # TODO: update the variables (rewards, n_plays, Q) for the selected arm
        rewards[a] = reward_for_a
        n_plays[a] += 1
        Q[a] = Q[a] + (1 / n_plays[a]) * (reward_for_a - Q[a])


def epsilon_greedy(bandit, timesteps):
    # TODO: epsilon greedy action selection (you can copy your code for greedy as a starting point)
    EPSILON = 0.1

    rewards = np.zeros(bandit.n_arms)
    n_plays = np.zeros(bandit.n_arms)
    Q = np.zeros(bandit.n_arms)
    possible_arms = range(bandit.n_arms)
    # init variables (rewards, n_plays, Q) by playing each arm once
    rewards = [bandit.play_arm(a) for a in possible_arms]
    n_plays = [1 for a in possible_arms]
    Q = [rewards[a] / n_plays[a] for a in possible_arms]

    while bandit.total_played < timesteps:
        # generate a random number between 0 and 1
        rand = np.random.uniform(0, 1)
        if rand < EPSILON:
            a = random.choice(possible_arms)
        else:
            a = np.argmax(Q)
        reward_for_a = bandit.play_arm(a)  # Just play arm 0 as placeholder
        rewards[a] = reward_for_a
        n_plays[a] += 1
        Q[a] = Q[a] + (1 / n_plays[a]) * (reward_for_a - Q[a])


def main():
    n_episodes = 1000  # TODO: set to 10000 to decrease noise in plot
    n_timesteps = 1000
    rewards_greedy = np.zeros(n_timesteps)
    rewards_egreedy = np.zeros(n_timesteps)

    for i in range(n_episodes):
        if i % 100 == 0:
            print ("current episode: " + str(i))

        b = GaussianBandit()  # initializes a random bandit
        greedy(b, n_timesteps)
        rewards_greedy += b.rewards

        b.reset()  # reset the bandit before running epsilon_greedy
        epsilon_greedy(b, n_timesteps)
        rewards_egreedy += b.rewards

    rewards_greedy /= n_episodes
    rewards_egreedy /= n_episodes
    plt.plot(rewards_greedy, label="greedy")
    print("Total reward of greedy strategy averaged over " + str(n_episodes) + " episodes: " + str(np.sum(rewards_greedy)))
    plt.plot(rewards_egreedy, label="e-greedy")
    print("Total reward of epsilon greedy strategy averaged over " + str(n_episodes) + " episodes: " + str(np.sum(rewards_egreedy)))
    plt.legend()
    plt.xlabel("Timesteps")
    plt.ylabel("Reward")
    plt.savefig('bandit_strategies.eps')
    plt.show()


if __name__ == "__main__":
    main()
