import pygame
from blob import *
import numpy as np

class Board:
    def __init__(self, width=600, height=400,  caption='Panmdemic simulation'):
        self.__caption = caption
        self.__width = width
        self.__height = height
        self.__size = width, height
        self.Green = (0, 255, 0)
        self.Red = (255, 0, 0)
        self.Yellow = (255, 255, 0)
        self.Black = (0, 0, 0)

        pygame.init()
        self.screen = pygame.display.set_mode(self.__size)
        pygame.display.set_caption(self.__caption)

        self.__running = None

    def set_up(self):
        self.__running = True

    def terminate(self):
        self.__running = False

    def is_running(self):
        return self.__running

    def draw(self, blob):
        pygame.draw.circle(self.screen, blob.color, blob.position, blob.R)

    def fill(self):
        self.screen.fill(self.Black)


class BlobFactory:
    def get_random_healthy_blob(self, limits):
        return self.get_healthy_blob(
            mass=np.random.uniform(10, 100),
            x=np.random.uniform(0, limits[0]),
            y=np.random.uniform(0, limits[1]),
            v=np.array([np.random.uniform(-0.5, 0.5), np.random.uniform(-0.5, 0.5)]),
            limits=limits,
            age=np.random.randint(blob_living_time)
            )

    def get_random_infected_blob(self, limits):
        return self.get_infected_blob(
            mass=np.random.uniform(10, 100),
            x=np.random.uniform(0, limits[0]),
            y=np.random.uniform(0, limits[1]),
            v=np.array([np.random.uniform(-0.5, 0.5), np.random.uniform(-0.5, 0.5)]),
            limits=limits,
            age=np.random.randint(blob_living_time)
        )

    @staticmethod
    def get_healthy_blob(mass, x, y, v, limits, age):
        return Blob(mass, x, y, v, limits, age=age)

    @staticmethod
    def get_infected_blob(mass, x, y, v, limits, age):
        return Blob(mass, x, y, v, limits, active_virus=True, state=Contagious, age=age)

