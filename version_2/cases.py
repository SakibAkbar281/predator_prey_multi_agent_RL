import math
from config import *

class Case:
    def __init__(self, n_tigers, n_deers, n_steps, train_tiger, train_deer, num_episodes=100):
        self.n_tigers = n_tigers
        self.n_deers = n_deers
        self.n_steps = n_steps
        self.train_tiger = train_tiger
        self.train_deer = train_deer
        tiger_training_condition = 1 if train_tiger else 0
        deer_training_condition = 1 if train_deer else 0

        self.path = f"./data/{n_tigers}t{n_deers}d{n_steps}/" \
                    f"{tiger_training_condition}t{deer_training_condition}d/"
        self.title = f"{n_tigers} Tigers Vs {n_deers} Deer ({n_steps} steps)"
        self.tiger_epsilon = 0.4 if train_tiger else 1.0
        self.deer_epsilon = 0.4 if train_deer else 1.0
        self.train_condition = {
            (True, True): 'both',
            (True, False): 'only_deer',
            (False, True): 'only_tiger',
            (False, False): 'none'
        }[(train_deer, train_tiger)]
        s = 0
        for n_d in range(1, n_deers+1):
            s += math.perm(WIDTH*HEIGHT//10000, n_d + n_tigers)
        self.total_states = s
        if self.train_condition == 'both':
            self.label = 'Trained Tiger Vs Trained Deer'
            self.color = 'orange'
        if self.train_condition == 'only_deer':
            self.label = 'Untrained Tiger Vs Trained Deer'
            self.color = 'darkred'
        if self.train_condition == 'only_tiger':
            self.label = 'Trained Tiger Vs Untrained Deer'
            self.color = 'navy'
        if self.train_condition == 'none':
            self.label = 'Baseline'
            self.color = 'black'
        self.num_episodes = num_episodes
    def get_hist(self):
        hist = self.path

    def __str__(self):
        return f"{self.n_tigers} tigers Vs. {self.n_deers} deer" \
               f" within {self.n_steps} steps, while training {self.train_condition.replace('_', ' ')}"

    def is_base_case(self):
        return self.train_condition == 'none'
