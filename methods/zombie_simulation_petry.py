import random

import matplotlib.pyplot as plt
import numpy as np

case = {
    "case_name": "PETRY_NET",
    "infection_probability": 0.8,
    "human_killed_rate": 0.15,
    "zombie_killed_rate": 0.05,
    "susceptible_at_start": 999999,
    "infected_at_start": 1,
    "number_of_moves": 10000000,
}

population = {"susceptible": 999999, "infected": 1, "removed": 0}


def petry(population, case):
    if population["susceptible"] <= 0 & population["infected"] <= 0:
        return population
    zombie_encounter_chance = (
        population["infected"]
        * population["susceptible"]
        / (
            (population["infected"] + population["susceptible"])
            * (population["infected"] + population["susceptible"])
            / 4
        )
    )
    infection_chance = zombie_encounter_chance * case["infection_probability"]
    human_killed_chance = zombie_encounter_chance * case["human_killed_rate"]
    zombie_killed_chance = zombie_encounter_chance * case["zombie_killed_rate"]
    all_chances = infection_chance + human_killed_chance + zombie_killed_chance
    decider = random.random()
    if decider < infection_chance:
        return infection(population)
    elif decider < (infection_chance + human_killed_chance):
        return human_killed(population)
    elif decider < all_chances:
        return zombie_killed(population)


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


def print_dict(dict):
    res = ""
    for key, value in dict.items():
        res += str(key) + ": " + str(value) + "\n"
    return res


def main():
    results = [[], [], []]
    moves = 10000000
    step_size = int((population["susceptible"] + population["infected"]) / 1000)
    counter = 0
    for i in range(moves):
        petry(population, case)
        counter += 1
        if counter == step_size:
            results[0].append(population["susceptible"])
            results[1].append(population["infected"])
            results[2].append(population["removed"])
            step_size = int((population["susceptible"] + population["infected"]) / 1000)
            counter = 0
    plt.plot(np.arange(len(results[0])), results[0], label="Susceptible", color="g")
    plt.plot(np.arange(len(results[0])), results[1], label="Infected", color="r")
    plt.plot(np.arange(len(results[0])), results[2], label="Removed", color="black")
    plt.xlabel("Time in hours")
    plt.ylabel("People")
    plt.title("Petry Net Simulation")
    plt.ylim(0, 1000000)
    plt.legend()
    plt.subplots_adjust(right=0.74)
    plt.gcf().text(x=0.75, y=0.5, s=print_dict(case))
    plt.savefig("results/" + case["case_name"] + ".png", bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    main()
