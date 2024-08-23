import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

##### Global variables:

POPULATION = 1

GENERAL_BIRTH_RATE = 0.00002235  # equals ny
GENERAL_DEATH_RATE = 0.00003238  # equals my

##### Scenarios:

WORST_CASE = {
    "infected": 0.01,
    "contact_rate": 1.5,
    "infection_probability": 0.14,
    "human_killed_rate": 0.04,
    "zombie_killed_rate": 0.11,
    "time_in_days": 150,
}

time_interval = (0, days)
t_eval = np.arange(days)

def SIR_manager()

def SIR_model(
    time_interval,
    population,
    general_birth_rate,
    general_death_rate,
    contact_rate,
    infection_probability,
    death_probability_of_human_by_zombies,
    death_probability_of_zombies_by_human,
):
    susceptible, infected, removed = population
    all = susceptible + infected + removed
    d_susceptible = (
        general_birth_rate * all
        - (infection_probability + death_probability_of_human_by_zombies)
        * contact_rate
        * susceptible
        * infected
        / all
        - general_death_rate * susceptible
    )
    d_infected = (
        infection_probability * contact_rate * susceptible * infected / all
        - death_probability_of_zombies_by_human * infected
    )
    d_removed = (
        death_probability_of_human_by_zombies
        * contact_rate
        * susceptible
        * infected
        / all
        + death_probability_of_zombies_by_human * infected
        + general_death_rate * susceptible
    )
    return [d_susceptible, d_infected, d_removed]


# use the solve_ivp function to calculate the integrals
# This function takes a function, a time interval, start
# values, as well as additional arguments and
# in this case the interval in which it is supposed to save its results
model = solve_ivp(
    SIR_model, time_interval, starting_values, args=(rates), t_eval=t_eval
)

# assign the results arrays to the variables
susceptible, infected, removed = model.y

# plot the graph
plt.plot(t_eval, susceptible, label="Susceptible", color="g")
plt.plot(t_eval, infected, label="Infected", color="r")
plt.plot(t_eval, removed, label="Removed", color="black")
plt.xlabel("Time in days")
plt.ylabel("People")
plt.title("SIR-Model Simulation")
plt.legend()
plt.show()


# =============================================================================
# Let's investigate what happens, if after e.g. 40 days we impose a quarantine?
# =============================================================================

# First do the same as above, but only for the first 40 days:
days = 40
time_interval = (0, days)
t_eval = np.arange(days)

# Run the discretized simulation for the first 40 days using the Euler
# algorithm:
model_40d = solve_ivp(
    SIR_model, time_interval, starting_values, args=(rates), t_eval=t_eval
)

# assign the results arrays to the variables
susceptible, infected, removed = model_40d.y

# Now impose the quarantine by reducing the contact rate:
contact_rate = 0.5
infection_rate = (
    contact_rate * infection_probability
)  # equals beta, tells how many people are infected by one infected per day
rates = (GENERAL_BIRTH_RATE, GENERAL_DEATH_RATE, death_recovery_rate, infection_rate)

# Adjust the time frame to 41 to 80 days
days = 81
time_interval = (40, days)
t_eval = np.arange(40, days)

# Start where day 40 left us:
starting_values = [susceptible[-1], infected[-1], removed[-1]]
model_80d = solve_ivp(
    SIR_model, time_interval, starting_values, args=(rates), t_eval=t_eval
)

# append the results from the next 40 days:
susceptible = np.concatenate([susceptible, model_80d.y[0][1:]])
infected = np.concatenate([infected, model_80d.y[1][1:]])
removed = np.concatenate([removed, model_80d.y[2][1:]])

# plot the graph
time_axis = np.arange(0, 80)
plt.plot(time_axis, susceptible, label="Susceptible", color="g")
plt.plot(time_axis, infected, label="Infected", color="r")
plt.plot(time_axis, removed, label="Removed", color="black")
plt.xlabel("Time in days")
plt.ylabel("People")
plt.title("SIR-Model Simulation")
plt.legend()
plt.show()