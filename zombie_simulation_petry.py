import random

import matplotlib.pyplot as plt
import numpy as np

BASE_CASE = {
    "infected": 0.000001,
    "contact_rate": 10,
    "infection_probability": 0.15,
    "human_killed_rate": 0.15,
    "zombie_killed_rate": 1,
    "time_in_days": 360,
}

POPULATION = {"susceptible": 999999, "infected": 1, "removed": 0}


def petry(population):
    if population["susceptible"] <= 0 & population["infected"] <= 0:
        return population
    for sus in range(population["susceptible"]):
        for contact in range(10):
            if random.random() <= (population["infected"] / population["susceptible"]):
                if random.random() < 0.15:
                    population = infection(population)
                    break
    for inf in range(population["infected"]):
        if random.random() <= 0.15:
            population = human_killed(population)
    for sus in range(population["susceptible"]):
        if random.random() <= 0.15:
            population = zombie_killed(population)
    return population


def infection(population):
    population["susceptible"] -= 1
    population["infected"] += 1
    return population


def human_killed(population):
    population["susceptible"] -= 1
    population["removed"] += 1
    return population


def zombie_killed(population):
    population["infected"] -= 1
    population["removed"] += 1
    return population


print(petry(POPULATION))
