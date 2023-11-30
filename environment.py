import pickle
import random
import matplotlib.pyplot as plt
from agent import *
from config import *
from background import *


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
        self.is_simulating = False
        self.n_steps = 20
    #     self.train_path = './'
    #     self.sim_path = './'
    # def set_train_path(self,path):
    #     self.train_path = path
    # def set_sim_path(self,path):
    #     self.sim_path = path
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
    def set_n_steps(self, n_steps):
        self.n_steps = n_steps
    def transition(self):
        self.steps += 1
        state = self.get_state()
        tiger_rewards, deer_rewards = self.reward_of()
        for deer in self.deer_group:
            if deer.got_caught:
                deer.kill()
        for tiger_index, tiger in enumerate(self.tiger_group):
            if not self.is_simulating:
                tiger_move = tiger.choose(state, tiger.reward)
            else:
                tiger_move = tiger.choose_without_learning(state)
            tiger.update(tiger_move, self.all_sprites)
            if not self.is_simulating:
                self.tiger_Qs.update(tiger.Q)

            # print(f'Tiger {tiger_index+1} moved to {tiger.pos}')
        for deer_index, deer in enumerate(self.deer_group):
            if not self.is_simulating:
                deer_move = deer.choose(state, deer.reward)
            else:
                deer_move = deer.choose_without_learning(state)
            deer.update(deer_move, self.all_sprites)
            if not self.is_simulating:
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
            # Movement cost based on distance
            closest_deer_distance = min([tiger.get_distance(deer) for deer in self.deer_group], default=0)
            tiger.reward = PREDATOR_COST_PER_MOVE * closest_deer_distance // 100
            # Coordination and teamwork bonuses
            if self.tiger_group.is_well_spaced():
                tiger.reward += TEAMWORK_BONUS
                if self.tiger_group.is_coordinated(self.deer_group):  #
                    tiger.reward += COORDINATION_BONUS
                else:
                    tiger.reward += NOT_COORDINATION_PENALTY

            # Penalty for inefficiency

            # Capture reward

        for deer in self.deer_group:

            nearest_tigers_distance_sum = sum(sorted([deer.get_distance(tiger)
                                                      for tiger in self.tiger_group])[:2]) \
                                                if len(self.tiger_group) >=2 \
                                                else 0

            deer.reward = PREY_REWARD_MOVE * nearest_tigers_distance_sum // 200


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
        return hash((tiger_positions, deer_positions))

    def _create_agents(self, agent_class, count, all_sprites, specific_group):
        agents = []

        for _ in range(count):
            agent = agent_class(ground=self.ground)
            while True:
                max_x = (WIDTH + 50) // 100
                max_y = (HEIGHT + 50) // 100
                x_coordinates = [50 + 100 * x for x in range(max_x)]
                y_coordinates = [50 + 100 * x for x in range(max_y)]
                init_pos = Vector2(random.choice(x_coordinates), random.choice(y_coordinates))
                agent.set_pos(init_pos)
                if not agent.is_obstructed(agent.rect, all_sprites):
                    # print(f'A {agent.__class__} landed on {init_pos}')
                    break
            all_sprites.add(agent)
            specific_group.add(agent)
            agents.append(agent)
        return agents
    def set_deer_epsilon(self, deer_epsilon = 0.4):
        for deer in self.deer_group:
            deer.epsilon = deer_epsilon
    def update_deer_epsilon(self, current_episode=1, num_episodes=1):
        for deer in self.deer_group:
            deer.epsilon = deer.epsilon * (1 - current_episode / (num_episodes + 1))

    def set_tiger_epsilon(self, tiger_epsilon=0.4):
        for tiger in self.tiger_group:
            tiger.epsilon = tiger_epsilon
    def update_tiger_epsilon(self, current_episode=1, num_episodes=1):
        for tiger in self.tiger_group:
            tiger.epsilon = tiger.epsilon * (1 - current_episode / (num_episodes + 1))

    def training(self, num_episodes, case='only tiger', path='./train/'):
        tiger_wins = 0
        deer_wins = 0
        hist = dict(tiger_wins=[], deer_wins=[], num_games=[],
                    states_visited_tiger=[], states_visited_deer=[],q_sum=[])
        for episode in range(num_episodes):
            if case=='only tiger':
                self.update_tiger_epsilon()
            elif case =='only deer':
                self.update_deer_epsilon()
            elif case =='both':
                self.update_deer_epsilon()
                self.update_tiger_epsilon()

            for step in range(self.n_steps):
                self.transition()
                if len(self.deer_group) == 0:
                    break
            if self.tiger_wins():
                tiger_wins += 1
            else:
                deer_wins += 1

            states_visited_tiger = (len(self.tiger_Qs) - 1) / 4
            states_visited_deer = (len(self.deer_Qs) - 1) / 4
            q_sum = sum(self.tiger_Qs.values()) + sum(self.deer_Qs.values())

            hist["tiger_wins"].append(tiger_wins)
            hist["deer_wins"].append(deer_wins)
            hist["num_games"].append(episode+1)
            hist["states_visited_tiger"].append(states_visited_tiger)
            hist["states_visited_deer"].append(states_visited_deer)
            hist["q_sum"].append(q_sum)

            if (episode + 1) % 10 == 0:
                print(
                    f'Episode {episode + 1}  tiger : deer = {100 * tiger_wins / (episode + 1)}% : {100 * deer_wins / (episode + 1)} %.'
                    f'\nTiger visited {states_visited_tiger} states,'
                    f'\nDeer visited {states_visited_deer} states')
            if episode % 1000 == 0:
                self.save()
                save_file(hist,'hist.pkl', path=path)
            self.reset()
        save_file(hist, 'hist.pkl', path=path)

    def run_game(self, screen, fps=10):
        # Time
        clock = pygame.time.Clock()
        deer_win_text = Text("Deer win")
        tiger_win_text = Text("Tigers win")
        tiger_scores = 0
        deer_scores = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            screen.blit(self.ground(), dest=(0, 0))
            tiger_reward_list, deer_reward_list = self.transition()
            tiger_scores += sum(tiger_reward_list)
            deer_scores += sum(deer_reward_list)

            self.all_sprites.draw(screen)  # Draw all sprites
            score_tigers = Text(f'Tiger Score: {tiger_scores}')
            score_deers = Text(f'Deer Score: {deer_scores}')
            steps_text = Text(f"Steps: {self.steps}")
            screen.blit(score_tigers(), dest=(10, 10))
            screen.blit(score_deers(), dest=(10, 50))
            screen.blit(steps_text(), dest=(WIDTH - steps_text.get_size().x - 10, 10))

            # Check for game end conditions
            if self.game_over():
                if self.tiger_wins():
                    screen.blit(tiger_win_text(), dest=tiger_win_text.center_of(self.ground.rect))
                else:
                    screen.blit(deer_win_text(), dest=deer_win_text.center_of(self.ground.rect))
                pygame.display.update()
                pygame.time.delay(5000)
                pygame.quit()
                exit()

            pygame.display.update()
            clock.tick(fps)

    def simulate(self, num_games, path='./sim/'):
        tiger_wins = 0
        deer_wins = 0
        hist = dict(tiger_wins = [], deer_wins = [], num_games = [])

        self.is_simulating = True
        for game in range(num_games):
            for step in range(self.n_steps):
                self.transition()
                if len(self.deer_group) == 0:
                    break
            if self.tiger_wins():
                tiger_wins += 1
            else:
                deer_wins += 1
            tiger_wr = 100 * tiger_wins / (game + 1)
            deer_wr = 100 * deer_wins / (game + 1)
            hist["tiger_wins"].append(tiger_wins)
            hist["deer_wins"].append(deer_wins)
            hist["num_games"].append(game+1)
            if (game + 1) % 10 == 0:
                print(f'Game {game + 1}  tiger : deer = {tiger_wr}% : {deer_wr} %.')
                save_file(hist, filename='hist.pkl',path=path)
            self.reset()
        self.is_simulating = False
        winning_ratio = 100 * tiger_wins / num_games, 100 * deer_wins / num_games
        save_file(hist, filename='hist.pkl', path=path)
        return winning_ratio

    def training_step(self):
        pass

    def plot_states_visited(self):
        pass

    def tiger_wins(self):
        return len(self.deer_group) == 0

    def game_over(self):
        return len(self.deer_group) == 0 or self.steps >= self.n_steps

    def save(self, tiger_q_file='tq.pkl', deer_q_file='dq.pkl', path='./'):
        with open(path+tiger_q_file, 'wb') as f:
            pickle.dump(self.tiger_Qs, f)
        with open(path+deer_q_file, 'wb') as f:
            pickle.dump(self.deer_Qs, f)

    def load(self, tiger_q_file='tq.pkl', deer_q_file='dq.pkl',path='./'):
        with open(path+tiger_q_file, 'rb') as f:
            self.tiger_Qs = pickle.load(f)
        with open(path+deer_q_file, 'rb') as f:
            self.deer_Qs = pickle.load(f)
        print(f'Loaded successfully. '
              f'\nTiger visited {(len(self.tiger_Qs) - 1) / 4} states'
              f'\nDeer visited  {(len(self.deer_Qs) - 1) / 4} states')
