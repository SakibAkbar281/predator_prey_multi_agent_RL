import pickle
import random

from agent import *
from config import *


class Env:
    def __init__(self, ground):  # create tigers and deers
        self.tigers = None
        self.deers = None
        self.all_sprites = pygame.sprite.Group()
        self.tiger_group = TigerGroup()
        self.deer_group = DeerGroup()
        self.ground = ground
        self.tiger_Qs = {(-1, -1): 0}
        self.deer_Qs = {(-1, -1): 0}
        self.n_tigers = 0
        self.n_deers = 0
        self.steps = 0
        self.is_training = False

    def add(self, n_tigers, n_deers):
        self.tigers = self._create_agents(Tiger, n_tigers,
                                          all_sprites=self.all_sprites,
                                          specific_group=self.tiger_group)
        self.deers = self._create_agents(Deer, n_deers,
                                         all_sprites=self.all_sprites,
                                         specific_group=self.deer_group)
        for tiger in self.tiger_group:
            tiger.set_Q(self.tiger_Qs)
        for deer in self.deer_group:
            deer.set_Q(self.deer_Qs)

        self.n_tigers = n_tigers
        self.n_deers = n_deers

    def transition(self):
        self.steps += 1
        state = self.get_state()
        tiger_rewards, deer_rewards = self.reward_of()
        for deer in self.deer_group:
            if deer.got_caught:
                deer.kill()
        for tiger_index, tiger in enumerate(self.tiger_group):
            tiger_move = tiger.choose(state, tiger.reward)
            tiger.update(tiger_move, self.all_sprites)
            self.tiger_Qs.update(tiger.Q)
            # print(f'Tiger {tiger_index+1} moved to {tiger.pos}')
        for deer_index, deer in enumerate(self.deer_group):
            deer_move = deer.choose(state, deer.reward)
            deer.update(deer_move, self.all_sprites)
            self.deer_Qs.update(deer.Q)
            if deer.check_captured(self.tiger_group):  # and not self.is_training:
                deer.got_caught = True
            # print(f'Deer {deer_index+1} moved to {deer.pos}')

        return tiger_rewards, deer_rewards

    def reset(self):
        self.steps = 0
        for sprite in self.all_sprites:
            sprite.kill()
        self.add(n_tigers=self.n_tigers, n_deers=self.n_deers)

    def reward_of(self):
        tiger_rewards = []
        deer_rewards = []
        for tiger in self.tiger_group:
            # Movement cost based on distance
            closest_deer_distance = min([tiger.get_distance(deer) for deer in self.deer_group], default=0)
            tiger.reward = PREDATOR_COST_PER_MOVE * closest_deer_distance // 100
            # Coordination and teamwork bonuses

            if self.tiger_group.is_well_spaced():  # Define this method to check optimal spacing
                tiger.reward += TEAMWORK_BONUS
                if self.tiger_group.is_coordinated(
                        self.deer_group):  # Define this method to check for strategic positioning
                    tiger.reward += COORDINATION_BONUS
                    # print('Tiger group is coordinated')
                else:
                    tiger.reward += NOT_COORDINATION_PENALTY
                    # print('Tiger group is not coordinated')
                # print('Tiger group is well spaced')

            # Capture reward

        for deer in self.deer_group:
            deer.reward = PREY_REWARD_MOVE * \
                          sum([deer.get_distance(other=tiger)
                               for tiger in self.tiger_group]) // 100
            if deer.check_captured(self.tiger_group):
                deer.reward += PREY_COST_CAPTURED
                for tiger in self.tiger_group:
                    if tiger.is_close(deer):
                        tiger.reward += PREDATOR_REWARD_CAPTURE

        if self.game_over():
            if not self.tiger_wins():
                for deer in self.deers:
                    deer.reward += PREY_REWARD_SURVIVAL

        for tiger in self.tiger_group:
            tiger_rewards.append(tiger.reward)
        for deer in self.deer_group:
            deer_rewards.append(deer.reward)

        return tiger_rewards, deer_rewards

    def get_state(self):
        tiger_positions = frozenset({tuple(tiger.pos) for tiger in self.tiger_group})
        deer_positions = frozenset({tuple(deer.pos) for deer in self.deer_group})
        return hash((tiger_positions,deer_positions))

    def _create_agents(self, agent_class, count, all_sprites, specific_group):
        agents = []

        for _ in range(count):
            agent = agent_class(ground=self.ground)
            while True:
                max_x = (WIDTH+50)//100
                max_y = (HEIGHT+50)//100
                x_coordinates = [50+100*x for x in range(max_x)]
                y_coordinates = [50+100*x for x in range(max_y)]
                init_pos = Vector2(random.choice(x_coordinates),random.choice(y_coordinates))
                agent.set_pos(init_pos)
                if not agent.is_obstructed(agent.rect, all_sprites):
                    # print(f'A {agent.__class__} landed on {init_pos}')
                    break
            all_sprites.add(agent)
            specific_group.add(agent)
            agents.append(agent)
        return agents

    def update_epsilon(self, current_episode, num_episodes, deer_epsilon=0.4, tiger_epsilon=0.4):
        for deer in self.deer_group:
            if deer_epsilon !=1:
                deer.epsilon = deer_epsilon * (1 - current_episode / (num_episodes + 1))  # 0.4*(1-i/(Neps+1));%0.5*(i)^(-1/3);
            else:
                deer.epsilon = 1

        for tiger in self.tiger_group:
            if tiger_epsilon != 1:
                tiger.epsilon = tiger_epsilon * (1 - current_episode / (num_episodes + 1))  # 0.4*(1-i/(Neps+1));%0.5*(i)^(-1/3);
            else:
                tiger.epsilon = 1

    def training(self, num_episodes, num_steps, deer_epsilon = 0.4, tiger_epsilon = 0.4):
        self.is_training = True
        tiger_wins = 0
        deer_wins = 0
        for episode in range(num_episodes):
            self.update_epsilon(episode, num_episodes, deer_epsilon, tiger_epsilon)
            for steps in range(num_steps):
                self.transition()
                # if steps % 10 == 0:
                #     print(f'Episode: {episode} Steps: {steps} '
                #           # f'\nDeer Epsilon: {[deer.epsilon for deer in self.deer_group]}'
                #           f'\nTigers: {len(self.tiger_group)} Deer: {len(self.deer_group)}'
                #           # f'\nTiger Q_dictionary Length {len(self.tiger_Qs)},'
                #           # f'\nDeer Q_dictionary Length {len(self.deer_Qs)}'
                #           f'\n_______________')
                if len(self.deer_group) == 0:
                    # print('No more deer')
                    break
            if self.tiger_wins():
                tiger_wins += 1
            else:
                deer_wins += 1
            if (episode+1) % 10 ==0:
                print(f'Episode {episode+1}  tiger : deer = {100*tiger_wins/(episode+1)}% : {100*deer_wins/(episode+1)} %.'
                      f'\nTiger visited {(len(self.tiger_Qs)-1)/4} states,'
                      f'\nDeer visited {(len(self.deer_Qs)-1)/4} states')

            if episode % 1000 ==0:
                self.save()
            self.reset()
        self.is_training = False

    def tiger_wins(self):
        return len(self.deer_group) == 0

    def game_over(self):
        return len(self.deer_group) == 0 or self.steps >= N_STEPS

    def save(self, tiger_q_file = 'tiger_q.pkl', deer_q_file='deer_q.pkl'):
        with open(tiger_q_file, 'wb') as f:
            pickle.dump(self.tiger_Qs, f)
        with open(deer_q_file, 'wb') as f:
            pickle.dump(self.deer_Qs, f)

    def load(self, tiger_q_file, deer_q_file):
        with open(tiger_q_file, 'rb') as f:
            self.tiger_Qs = pickle.load(f)
        with open(deer_q_file, 'rb') as f:
            self.deer_Qs = pickle.load(f)
        print(f'Loaded successfully. '
              f'\nLength of tiger_q dict: {len(self.tiger_Qs)}'
              f'\nLength of deer_q dict : {len(self.deer_Qs)}')
