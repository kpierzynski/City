import pygame
from pygame import Vector2

import numpy as np

from math import sqrt, fabs as abs
from random import choice, randint as rnd

from sheet import Sheet
from tile import Tile
from map import Map
from road_tiles import Road
from car import Car, UP, RIGHT, DOWN, LEFT
from util import tile_to_pixel

from config import CONFIG

COLORS = CONFIG["COLORS"]
SCREEN = CONFIG["SCREEN"]

ACTION_STATES = 5
INPUT_STATES = 8

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os


class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)

        self.load()

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x

    def save(self, file_name="model.pth"):
        model_folder_path = "./model"
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)

    def load(self, file_name="model.pth"):
        model_folder_path = "./model"
        file_path = os.path.join(model_folder_path, file_name)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Model file '{file_name}' not found.")
        
        self.load_state_dict(torch.load(file_path))


class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        # (n, x)

        if len(state.shape) == 1:
            # (1, x)
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done,)

        # 1: predicted Q values with current state
        pred = self.model(state)

        target = pred.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(
                    self.model(next_state[idx])
                )

            target[idx][torch.argmax(action[idx]).item()] = Q_new

        # 2: Q_new = r + y * max(next_predicted Q value) -> only do this if not done
        # pred.clone()
        # preds[argmax(action)] = Q_new
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        self.optimizer.step()


import torch
import random
import numpy as np
from collections import deque

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()
        self.model = Linear_QNet(INPUT_STATES, 256, ACTION_STATES)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append(
            (state, action, reward, next_state, done)
        )  # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        # for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        self.epsilon = 10
        final_move = [0 for _ in range(ACTION_STATES)]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, ACTION_STATES - 1)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move


"""
def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGameAI()
    while True:
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print("Game", agent.n_games, "Score", score, "Record:", record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)
"""

agent = Agent()


def main():
    print("Hello, World!")

    # Initialize the game engine
    pygame.init()
    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 36)

    camera = Vector2(400, 200)
    target_coords = (100, 100)

    # Set the height and width of the screen
    size = [SCREEN["WIDTH"], SCREEN["HEIGHT"]]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("AI CITY")

    timer_interval = 7500
    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, timer_interval)

    timer_1s = 100
    timer_1s_event = pygame.USEREVENT + 2
    pygame.time.set_timer(timer_1s_event, timer_1s)

    map = Map((4, 4))
    car = Car((0, 150))

    possible_actions = [
        (1 << UP),
        (1 << RIGHT),
        (1 << LEFT),
        (1 << DOWN),
        0,
        (1 << UP) | (1 << RIGHT),
        (1 << LEFT) | (1 << UP),
        (1 << RIGHT) | (1 << DOWN),
        (1 << DOWN) | (1 << LEFT),
    ]

    def cast_ray(car_pos, angle, max_distance):
        import math
        x, y = car_pos
        dx = pygame.math.Vector2(math.cos(angle), -math.sin(angle)).normalize()
        end_point = (int(x + dx.x), int(y + dx.y))

        inverse = map.is_on_road(car_pos)

        while pygame.math.Vector2(car_pos).distance_to(end_point) <= max_distance:
            if inverse:
                if not map.is_on_road(end_point):
                    return end_point
            else:
                if map.is_on_road(end_point):
                    return end_point
            end_point += dx

        return end_point

    def distance(v1, v2):
        x1, y1 = v1
        x2, y2 = v2

        return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    time_elapsed = 0
    import math

    # PyGame main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                x, y = mouse_pos
                x, y = x - camera.x, y - camera.y

                if event.button == pygame.BUTTON_RIGHT:
                    car.position = (x, y)
                else:
                    target_coords = Vector2(x, y)

            if event.type == timer_event:
                agent.n_games += 1
                while True:
                    x, y = tile_to_pixel((rnd(1, 3), rnd(1, 3)))
                    if map.get_tile(x, y).kind == "road_empty":
                        continue
                    target_coords = (x, y)
                    break

                x, y = tile_to_pixel((rnd(2, 3), rnd(2, 3)))
                car.position = Vector2(x, y)
                time_elapsed = 0

            if event.type == timer_1s_event:
                time_elapsed += timer_1s / 1000

        direction = 0
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            camera += (0, 5)
        if pressed[pygame.K_LEFT]:
            camera += (5, 0)
        if pressed[pygame.K_DOWN]:
            camera += (0, -5)
        if pressed[pygame.K_RIGHT]:
            camera += (-5, 0)
        if pressed[pygame.K_w]:
            direction |= 1 << UP
        if pressed[pygame.K_d]:
            direction |= 1 << RIGHT
        if pressed[pygame.K_s]:
            direction |= 1 << DOWN
        if pressed[pygame.K_a]:
            direction |= 1 << LEFT
        if pressed[pygame.K_u]:
            agent.model.save()
            print("Model saved")

        if direction:
            car.set_direction(direction)
            car.move()


        rays = {
            "left": [ (0,0), 0 ],
            "forward": [ (0,0), 0 ],
            "right": [ (0,0), 0 ]
        }

        for key,value in rays.items():
            
            if car.direction == (1<<UP):
                angle = math.atan2(101/3, -132/2)
            if car.direction == (1<<LEFT):
                angle = math.atan2(-101/3, -132/2)
            if car.direction == (1<<RIGHT):
                angle = math.atan2(101/3, 132/2)
            if car.direction == (1<<DOWN):
                angle = math.atan2(-101/3, 132/2)

            if key == "left":
                angle += 2*math.atan2(101/3, 132/2) - math.pi
            if key == "right":
                angle += 2*math.atan2(101/3, 132/2)

            if car.direction == (1<<LEFT) or car.direction == (1<<RIGHT):
                if key != "forward":
                    angle += 5*math.atan2(101/3, 132/2)/2

            value[0] = cast_ray(car.position, angle, 132)
            value[1] = distance(car.position, value[0])

        state = [
            (
                1
                if car.position[0] < target_coords[0]
                and car.position[1] < target_coords[1]
                else 0
            ),
            (
                1
                if car.position[0] > target_coords[0]
                and car.position[1] < target_coords[1]
                else 0
            ),
            (
                1
                if car.position[0] > target_coords[0]
                and car.position[1] > target_coords[1]
                else 0
            ),
            (
                1
                if car.position[0] < target_coords[0]
                and car.position[1] > target_coords[1]
                else 0
            ),
            distance(car.position, target_coords) / (132 * 6),
            rays['left'][1] / 132,
            rays['forward'][1] / 132,
            rays['right'][1] / 132
        ]

        move = agent.get_action(state)
        direction = possible_actions[np.argmax(move)]
        hit = False
        if direction:
            car.set_direction(direction)
            hit = car.move()

        for key,value in rays.items():
            
            if car.direction == (1<<UP):
                angle = math.atan2(101/3, -132/2)
            if car.direction == (1<<LEFT):
                angle = math.atan2(-101/3, -132/2)
            if car.direction == (1<<RIGHT):
                angle = math.atan2(101/3, 132/2)
            if car.direction == (1<<DOWN):
                angle = math.atan2(-101/3, 132/2)

            if key == "left":
                angle += 2*math.atan2(101/3, 132/2) - math.pi
            if key == "right":
                angle += 2*math.atan2(101/3, 132/2)

            if car.direction == (1<<LEFT) or car.direction == (1<<RIGHT):
                if key != "forward":
                    angle += 5*math.atan2(101/3, 132/2)/2

            value[0] = cast_ray(car.position, angle, 132)
            value[1] = distance(car.position, value[0])

        new_state = [
            (
                1
                if car.position[0] < target_coords[0]
                and car.position[1] < target_coords[1]
                else 0
            ),
            (
                1
                if car.position[0] > target_coords[0]
                and car.position[1] < target_coords[1]
                else 0
            ),
            (
                1
                if car.position[0] > target_coords[0]
                and car.position[1] > target_coords[1]
                else 0
            ),
            (
                1
                if car.position[0] < target_coords[0]
                and car.position[1] > target_coords[1]
                else 0
            ),
            distance(car.position, target_coords) / (132 * 6),
            rays['left'][1] / 132,
            rays['forward'][1] / 132,
            rays['right'][1] / 132
        ]

        reward = (
            (timer_interval / 1000)
            if map.is_on_road(car.position)
            else -3*(timer_interval / 1000)
        )
        if hit:
            reward = -10

        reward -= time_elapsed

        done = False
        if distance(car.position, target_coords) < 20:
            done = True
            reward = 50

        agent.train_short_memory(state, move, reward, new_state, done)
        agent.remember(state, move, reward, new_state, done)

        if done:
            agent.n_games += 1
            agent.train_long_memory()

            while True:
                x, y = tile_to_pixel((rnd(1, 3), rnd(1, 3)))
                if map.get_tile(x, y).kind == "road_empty":
                    continue
                target_coords = (x, y)
                break

            x, y = tile_to_pixel((rnd(2, 3), rnd(2, 3)))
            car.position = Vector2(x, y)
            time_elapsed = 0
            pygame.time.set_timer(timer_event, timer_interval)




        map.update()
        car.update()

        # Set the screen background
        screen.fill(COLORS["SKYBLUE"])

        map.draw(screen, camera)
        car.draw(screen, camera)

        colors = [(255,0,0), (0,255,0), (0,0,255)]
        color_i = 0
        for key, (ray_end, ray_dist) in rays.items():
            pygame.draw.line(screen, colors[color_i], camera + car.position, camera + ray_end)
            color_i += 1

        text = font.render(
            f"Game: {agent.n_games}, Car: ({car.position[0]:.2f},{car.position[1]:.2f}), Reward: {reward:.2f}",
            True,
            COLORS["BLACK"],
        )
        screen.blit(text, (10, 10))

        # draw dot in target_coords
        pygame.draw.circle(screen, (255, 221, 0), camera + target_coords, 5)

        for pos in car.get_grid():
            color = (0, 255, 127)
            if not map.is_on_road(pos):
                color = (255, 0, 0)
            pygame.draw.circle(screen, color, camera + pos, 1)

        pygame.display.flip()

        # clock.tick(CONFIG["SCREEN"]["FPS"])


if __name__ == "__main__":
    main()
