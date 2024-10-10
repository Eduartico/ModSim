# Assignment 1 - Problem statement, methods and tools

## Brief description of the problem to be modelled

Parking lots are incentivizing the use of electric-vehicles by reserving a certain number of parking spaces for these clients. But what scheme is the best for choosing such spaces? 

## Goals of the simulation project

Simulate several schemes and evalute them to understand how they are affected by some variables and figure out if there is a better scheme. The schemes to be tested are:

- Priority: Several parking spaces are set to be only available for electric-vehicles.
- On-Demand: The number of parking spaces for electric-vehicles changes depending on the need of the current system.
- Time-based: For a defined period, some parking spaces are only available for electric-vehicles.
- Membership: Several parking spaces are set to be only available for electric-vehicles, but premium membership vehciles have priority over their spaces.

## Main entities of the system

- Parking Spaces
- Vehicles

## Variables of the system

- Number of regular parking spaces
- Number of electric-vehicle parking spaces
- Number of regular vehicles
- Number of electric-vehicles
- Number of premium-vehicles
- Hour of the day
- Number of regular vehicles on a queue
- Number of electric-vehicles on a queue
- Number of premium-vehicles on a queue

## Operation policies to be tested (scenarios)

How each scenario performs in several parking lot structures, in different ratios of regular/electric vehicles

## Key performance indicators and decision criteria

- Average wait time of a vehicle on a queue
- Maximum wait time of a vehicle on a queue
- Minimum wait time of a vehicle on a queue
- Use of parking spaces in relation to waiting vehicles:  ((Total spaces - spaces in use) / vehicles in queue) - 1

## Data requirements

- Create at least three common different parking lots structures based on used irl ones

## Simulation tools, environments, languages

- Python
- MESA

## Other information the group may find appropriate to describe the problem (remover isto????)