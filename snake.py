

import pygame
from settings import *
from copy import deepcopy
from random import randrange


class Square:
    def __init__(self, pos, surface, is_apple=False):
        self.pos = pos
        self.surface = surface
        self.is_apple = is_apple
        self.is_tail = False
        self.dir = [-1, 0]  # [x, y] Direction

        if self.is_apple:
            self.dir = [0, 0]

    def draw(self, clr=SNAKE_CLR):

        x, y = self.pos[0], self.pos[1]
        ss, gs = SQUARE_SIZE, GAP_SIZE

        if self.dir == [-1, 0]:
            if self.is_tail:
                pygame.draw.rect(self.surface, clr, (x * ss + gs, y * ss + gs, ss - 2*gs, ss - 2*gs))
            else:
                pygame.draw.rect(self.surface, clr, (x * ss + gs, y * ss + gs, ss, ss - 2*gs))

        if self.dir == [1, 0]:
            if self.is_tail:
                pygame.draw.rect(self.surface, clr, (x * ss + gs, y * ss + gs, ss - 2*gs, ss - 2*gs))
            else:
                pygame.draw.rect(self.surface, clr, (x * ss - gs, y * ss + gs, ss, ss - 2*gs))

        if self.dir == [0, 1]:
            if self.is_tail:
                pygame.draw.rect(self.surface, clr, (x * ss + gs, y * ss + gs, ss - 2*gs, ss - 2*gs))
            else:
                pygame.draw.rect(self.surface, clr, (x * ss + gs, y * ss - gs, ss - 2*gs, ss))

        if self.dir == [0, -1]:
            if self.is_tail:
                pygame.draw.rect(self.surface, clr, (x * ss + gs, y * ss + gs, ss - 2*gs, ss - 2*gs))
            else:
                pygame.draw.rect(self.surface, clr, (x * ss + gs, y * ss + gs, ss - 2*gs, ss))

        if self.is_apple:
            pygame.draw.rect(self.surface, clr, (x * ss + gs, y * ss + gs, ss - 2*gs, ss - 2*gs))

    def move(self, direction):
        self.dir = direction
        self.pos[0] += self.dir[0]
        self.pos[1] += self.dir[1]

    def hitting_wall(self):
        if (self.pos[0] <= -1) or (self.pos[0] >= ROWS) or (self.pos[1] <= -1) or (self.pos[1] >= ROWS):
            return True
        else:
            return False


class Snake:
    def __init__(self, surface):
        self.surface = surface
        self.is_dead = False
        self.squares_start_pos = [[ROWS // 2 + i, ROWS // 2] for i in range(INITIAL_SNAKE_LENGTH)]
        self.turns = {}
        self.dir = [-1, 0]
        self.score = 0
        self.moves_without_eating = 0
        self.apple = Square([randrange(ROWS), randrange(ROWS)], self.surface, is_apple=True)

        self.squares = []
        for pos in self.squares_start_pos:
            self.squares.append(Square(pos, self.surface))

        self.head = self.squares[0]
        self.tail = self.squares[-1]
        self.tail.is_tail = True

        self.path = []
        self.is_virtual_snake = False
        self.total_moves = 0
        self.won_game = False

    def draw(self):
        self.apple.draw(APPLE_CLR)
        self.head.draw(HEAD_CLR)
        for sqr in self.squares[1:]:
            if self.is_virtual_snake:
                sqr.draw(VIRTUAL_SNAKE_CLR)
            else:
                sqr.draw()

    def set_direction(self, direction):
        if direction == 'left':
            if not self.dir == [1, 0]:
                self.dir = [-1, 0]
                self.turns[self.head.pos[0], self.head.pos[1]] = self.dir
        if direction == "right":
            if not self.dir == [-1, 0]:
                self.dir = [1, 0]
                self.turns[self.head.pos[0], self.head.pos[1]] = self.dir
        if direction == "up":
            if not self.dir == [0, 1]:
                self.dir = [0, -1]
                self.turns[self.head.pos[0], self.head.pos[1]] = self.dir
        if direction == "down":
            if not self.dir == [0, -1]:
                self.dir = [0, 1]
                self.turns[self.head.pos[0], self.head.pos[1]] = self.dir
