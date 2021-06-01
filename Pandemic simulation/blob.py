import numpy as np
from math import pi, sqrt
from abc import ABC, abstractmethod
import random

Alive_and_well = 0
Contagious = 1
Immuned = 2
Recovered = 3

Blue = (135, 206, 235)
Red = (255, 0, 0)
Gold = (255, 215, 0)
Green = (0, 255, 0)

Infection_rate = 0.1
virus_living_time = 1000
blob_living_time = 10000
vaccination_rate = 0.6
vaccine_didnt_work = 0.94

class Creature:
    def __init__(self,  active, age=0, living_time=200):
        self.age = age
        self.living_time = living_time
        self._active = active

    def aging(self):
        self.age += 1

    def is_dead(self):
        if self.age >= self.living_time:
            return True

    def is_active(self):
        if self.is_dead():
            self._active = False
        return self._active

    def rebirth(self):
        self.age = 0
        self._active = False


class Blob(Creature):
    def __init__(self, mass, X_0, Y_0, V, limits, age=0, living_time=blob_living_time, state=Alive_and_well, active=True,
                 active_virus=False):
        super().__init__(age=age, living_time=living_time, active=active)
        self.mass = mass
        self.state = state
        self.virus = Virus(active=active_virus)
        self.color = self._get_color()
        self.position = np.array([X_0, Y_0], dtype=float)
        self.V = V
        self.R = self._get_radius()
        self.limits = limits

    def get_X(self):
        return self.position[0]

    def get_Y(self):
        return self.position[1]

    def _get_radius(self):
        """
        getting the radius by the mass per density distribution
        assuming the density to all bodies is 1
        V=(4πr3)/3
        """
        return (3 * pi * self.mass / 4)**(1/3)

    def _get_color(self):
        if self.state == Alive_and_well:
            return Blue
        elif self.state == Contagious:
            return Red
        elif self.state == Immuned:
            return Gold
        elif self.state == Recovered:
            return Green

    def distance_from(self, other):
        """Pythagoras' theorem"""
        return round(sqrt(pow(self.get_X() - other.get_X(), 2) + pow(self.get_Y() - other.get_Y(), 2)))

    def is_collision(self, other):
        dR = round(self.R + other.R)
        if self.distance_from(other) <= dR:
            return True
        else:
            return False

    def collision(self, other):
        """should change the speed of the blob if it hits another blob"""
        if self.is_collision(other):
            self.change(other)

    def out_of_bounds(self):
        if self.is_out_of_bounds(0):
            revere_x = np.array([-1, 1])
            self.V = np.multiply(self.V, revere_x)

        if self.is_out_of_bounds(1):
            reverse_y = np.array([1, -1])
            self.V = np.multiply(self.V, reverse_y)

    def is_out_of_bounds(self, i):
        return self.position[i] - self.R < 0 or self.position[i] + self.R > self.limits[i]

    def change(self, other):
        self.change_state_by_collision(other)
        self.change_speed(other)

    def change_state_by_collision(self, other):
        if self.state is Alive_and_well and other.virus.is_active():
            if random.random() <= other.virus.contagious_rate:
                self.make_contagious()

        elif self.state is Immuned or self.state is Recovered and other.virus.is_active():
            if random.random() <= vaccine_didnt_work:
                self.make_contagious()

    def make_contagious(self):
        self.state = Contagious
        self.color = Red
        self.virus.activate()

    def change_speed(self, other):
        """
        f = ma
        """
        force = self.get_force(other)
        a = np.true_divide(force, self.mass)
        self.V += a

    def get_force(self, other):
        """
        J = dP
        J = F dT
        dT = 1
        F = m1V - m2V
        """
        return other.mass * other.V - self.mass * self.V

    def change_position(self):
        self.out_of_bounds()
        self.position += self.V

    def move_and_age(self):
        if self.is_active():
            self.change_position()
            self.aging()
        else:
            self.position = self.get_random_position()
            self.rebirth()
            self.virus.rebirth()

        if self.virus.is_active():
            self.virus.aging()
        else:
            if self.virus.is_dead():
                self.recover()

    def rebirth(self):
        self.age = 0
        self._active = True
        if random.random() <= vaccination_rate:
            self.state = Immuned
            self.color = Gold
        else:
            self.state = Alive_and_well
            self.color = Blue

    def recover(self):
        self.virus.age = 0
        self.state = Recovered
        self.color = Green

    def get_random_position(self):
        return np.array([np.random.uniform(0, self.limits[0]), np.random.uniform(0, self.limits[1])])


class Virus(Creature):
    def __init__(self, active=False, contagious_rate=Infection_rate, living_time=virus_living_time):
        super().__init__(living_time=living_time, active=active)
        self.contagious_rate = contagious_rate

    def activate(self):
        self._active = True






