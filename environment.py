import pickle
from agent import *
from config import *


class Env:
    def __init__(self, ground):  # create tigers and deers
        self.tigers = None
        self.deers = None
        self.all_sprites = pygame.sprite.Group()
        self.tiger_group = pygame.sprite.Group()
        self.deer_group = pygame.sprite.Group()
        self.ground = ground
        self.tiger_Qs = {(-1, -1): 0}
        self.deer_Qs = {(-1, -1): 0}
        self.n_tigers = 0
        self.n_deers = 0
        self.steps = 0
        self.is_training = False

    def add(self, n_tigers, n_deers):
        self.tigers = self._create_agents(Tiger, n_tigers,
                                          offset_from_center=500,
                                          all_sprites=self.all_sprites,
                                          specific_group=self.tiger_group)
        self.deers = self._create_agents(Deer, n_deers,
                                         offset_from_center=500,
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
            tiger_move = tiger.choose(state, tiger_rewards[tiger_index])
            tiger.update(tiger_move, self.all_sprites)
            self.tiger_Qs.update(tiger.Q)
        for deer_index, deer in enumerate(self.deer_group):
            deer_move = deer.choose(state, deer_rewards[deer_index])
            deer.update(deer_move, self.all_sprites)
            self.deer_Qs.update(deer.Q)
            if deer.check_captured(self.tiger_group):  # and not self.is_training:
                deer.got_caught = True
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
            tiger.reward = PREDATOR_COST_PER_MOVE * \
                           max([tiger.get_distance(other=deer) for deer in self.deer_group] if len(self.deer_group)!=0 else [0]) // 100

        for deer in self.deer_group:
            deer.reward = PREY_REWARD_MOVE * \
                          min([deer.get_distance(other=tiger) for tiger in self.tiger_group]) // 100
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
        sprite_positions = tuple([tuple(sprite.pos) for sprite in self.all_sprites])
        return hash(sprite_positions)

    def _create_agents(self, agent_class, count, offset_from_center, all_sprites, specific_group):
        agents = []
        offset_from_center = offset_from_center // 100
        for _ in range(count):
            agent = agent_class(ground=self.ground)
            while True:
                init_pos = self.ground.rect.center + 100 * Vector2(
                    random.randint(-offset_from_center, offset_from_center),
                    random.randint(-offset_from_center, offset_from_center))
                agent.set_pos(init_pos)
                if not agent.is_obstructed(agent.rect, all_sprites):
                    break

            all_sprites.add(agent)
            specific_group.add(agent)
            agents.append(agent)
        return agents

    def update_epsilon(self, current_episode, num_episodes):
        for deer in self.deer_group:
            deer.epsilon = 0.4 * (1 - current_episode / (num_episodes + 1))  # 0.4*(1-i/(Neps+1));%0.5*(i)^(-1/3);
        for tiger in self.tiger_group:
            tiger.epsilon = 0.4 * (1 - current_episode / (num_episodes + 1))  # 0.4*(1-i/(Neps+1));%0.5*(i)^(-1/3);

    def training(self, num_episodes, num_steps):
        self.is_training = True
        tiger_wins = 0
        deer_wins = 0
        for episode in range(num_episodes):
            self.update_epsilon(episode, num_episodes)
            for steps in range(num_steps):
                self.transition()
                if steps % 100 == 0:
                    print(f'Episode: {episode} Steps: {steps} '
                          # f'\nDeer Epsilon: {[deer.epsilon for deer in self.deer_group]}'
                          f'\nTigers: {len(self.tiger_group)} Deer: {len(self.deer_group)}'
                          # f'\nTiger Q_dictionary Length {len(self.tiger_Qs)},'
                          # f'\nDeer Q_dictionary Length {len(self.deer_Qs)}'
                          f'\n_______________')
                    if len(self.deer_group) == 0:
                        # print('No more deer')
                        break
            if self.tiger_wins():
                tiger_wins += 1
                print(f'tiger wins {tiger_wins} times.')
                print('____________')
            else:
                deer_wins += 1
                print(f'deer wins {deer_wins} times.')
                print('____________')
            self.reset()
        self.is_training = False

    def tiger_wins(self):
        return len(self.deer_group) == 0

    def game_over(self):
        return len(self.deer_group) == 0 or self.steps >= N_STEPS

    def save(self):
        with open('tiger_q.pkl', 'wb') as f:
            pickle.dump(self.tiger_Qs, f)
        with open('deer_q.pkl', 'wb') as f:
            pickle.dump(self.deer_Qs, f)

    def load(self, tiger_q_file, deer_q_file):
        with open(tiger_q_file, 'rb') as f:
            self.tiger_Qs = pickle.load(f)
        with open(deer_q_file, 'rb') as f:
            self.deer_Qs = pickle.load(f)
        print(f'Loaded successfully. '
              f'\nLength of tiger_q dict: {len(self.tiger_Qs)}'
              f'\nLength of deer_q dict : {len(self.deer_Qs)}')
