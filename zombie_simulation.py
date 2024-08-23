import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

##### Scenarios:

BASE_CASE = {
    "case_name": "BASE_CASE",
    "infected": 0.000001,
    "contact_rate": 10,
    "infection_probability": 0.15,
    "human_killed_rate": 0.15,
    "zombie_killed_rate": 1,
    "time_in_days": 360,
    "changing": False,
}

WORST_CASE = {
    "case_name": "WORST_CASE",
    "infected": 0.000001,
    "contact_rate": 10,
    "infection_probability": 0.45,
    "human_killed_rate": 0.45,
    "zombie_killed_rate": 1,
    "time_in_days": 360,
    "changing": False,
}

BEST_CASE = {
    "case_name": "BEST_CASE",
    "infected": 0.000001,
    "contact_rate": 10,
    "infection_probability": 0.10,
    "human_killed_rate": 0.10,
    "zombie_killed_rate": 1,
    "time_in_days": 360,
    "changing": False,
}

CHANGING_CASE_14d = {
    "case_name": "CHANGING_BASE_CASE_14d",
    "infected": 0.000001,
    "contact_rate": 10,
    "infection_probability": 0.15,
    "human_killed_rate": 0.15,
    "zombie_killed_rate": 1,
    "time_in_days": 14,
    "changing": True,
    "zombie_killed_rate_2": 10,
    "contact_rate_2": 3,
    "time_in_days_2": 330,
}

CHANGING_CASE_21d = {
    "case_name": "CHANGING_BASE_CASE_21d",
    "infected": 0.000001,
    "contact_rate": 10,
    "infection_probability": 0.15,
    "human_killed_rate": 0.15,
    "zombie_killed_rate": 1,
    "time_in_days": 21,
    "changing": True,
    "zombie_killed_rate_2": 10,
    "contact_rate_2": 3,
    "time_in_days_2": 330,
}

CHANGING_CASE_28d = {
    "case_name": "CHANGING_BASE_CASE_28d",
    "infected": 0.000001,
    "contact_rate": 10,
    "infection_probability": 0.15,
    "human_killed_rate": 0.15,
    "zombie_killed_rate": 1,
    "time_in_days": 28,
    "changing": True,
    "zombie_killed_rate_2": 10,
    "contact_rate_2": 3,
    "time_in_days_2": 330,
}


def SIR_manager(case):
    starting_values = (1 - case["infected"], case["infected"], 0)
    rates = (
        case["contact_rate"],
        case["infection_probability"],
        case["human_killed_rate"],
        case["zombie_killed_rate"],
    )
    days = case["time_in_days"]
    model = solve_ivp(
        SIR_model,
        (0, case["time_in_days"]),
        starting_values,
        args=(rates),
        t_eval=np.arange(case["time_in_days"]),
    )
    susceptible, infected, removed = model.y
    if case["changing"]:
        contact_rate = (
            case["contact_rate_2"] if "contact_rate_2" in case else case["contact_rate"]
        )
        infection_probability = (
            case["infection_probability_2"]
            if "infection_probability_2" in case
            else case["infection_probability"]
        )
        human_killed_rate = (
            case["human_killed_rate_2"]
            if "human_killed_rate_2" in case
            else case["human_killed_rate"]
        )
        zombie_killed_rate = (
            case["zombie_killed_rate_2"]
            if "zombie_killed_rate_2" in case
            else case["zombie_killed_rate"]
        )
        days += case["time_in_days_2"]
        model_2 = solve_ivp(
            SIR_model,
            (case["time_in_days"], case["time_in_days"] + case["time_in_days_2"]),
            (susceptible[-1], infected[-1], removed[-1]),
            args=(
                contact_rate,
                infection_probability,
                human_killed_rate,
                zombie_killed_rate,
            ),
            t_eval=np.arange(
                case["time_in_days"], case["time_in_days"] + case["time_in_days_2"]
            ),
        )
        susceptible_2, infected_2, removed_2 = model_2.y
        susceptible = np.concatenate([susceptible, susceptible_2[1:]])
        infected = np.concatenate([infected, infected_2[1:]])
        removed = np.concatenate([removed, removed_2[1:]])
    plt.plot(np.arange(len(susceptible)), susceptible, label="Susceptible", color="g")
    plt.plot(np.arange(len(infected)), infected, label="Infected", color="r")
    plt.plot(np.arange(len(removed)), removed, label="Removed", color="black")
    plt.xlabel("Time in days")
    plt.ylabel("People")
    plt.title("SIR-Model Simulation")
    plt.legend()
    plt.savefig("figures/" + case["case_name"] + ".png")


def SIR_model(
    time_interval,
    population,
    contact_rate,
    infection_probability,
    human_killed_rate,
    zombie_killed_rate,
):
    susceptible, infected, removed = population
    d_susceptible = (
        -(infection_probability + human_killed_rate)
        * contact_rate
        * susceptible
        * infected
        / (susceptible + infected)
    )
    d_infected = infection_probability * contact_rate * susceptible * infected / (
        susceptible + infected
    ) - zombie_killed_rate * infected * susceptible / (susceptible + infected)
    d_removed = human_killed_rate * contact_rate * susceptible * infected / (
        susceptible + infected
    ) + zombie_killed_rate * infected * susceptible / (susceptible + infected)
    return [d_susceptible, d_infected, d_removed]


def main():

    SIR_manager(BASE_CASE)

    SIR_manager(WORST_CASE)

    SIR_manager(BEST_CASE)

    SIR_manager(CHANGING_CASE_14d)

    SIR_manager(CHANGING_CASE_21d)

    SIR_manager(CHANGING_CASE_28d)


if __name__ == "__main__":
    main()
