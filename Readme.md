## Overview

This project simulates the operations of a container terminal using SimPy, a process-based discrete-event simulation framework for Python. The simulation models the arrival of vessels, berthing process, container unloading, and transportation within the terminal.

## Features

- Simulates vessel arrivals with configurable inter-arrival times
- Models berth allocation, quay crane operations, and truck transportation
- Configurable number of berths, quay cranes, and trucks
- Random number of containers per vessel within a specified range
- Detailed event logging and statistics tracking
- Easily adjustable simulation parameters

## Requirements

- Python 3.6+
- SimPy library

## Installation

- 1. Clone this repository:
- 2. git clone https://github.com/anuragsingh1409/Container-Terminal-Simulation-Simpy.git
- 3. cd container-terminal-simulation
- 4. Install the required library:
- 5. pip install simpy

## Usage

- 1. Open the container_terminal_simulation.py file.

- 2. Adjust the simulation parameters in the config dictionary as needed:

```python
config = {
    'simulation_time': 10000,
    'num_berths': 2,
    'num_quay_cranes': 2,
    'num_trucks': 3,
    'mean_inter_arrival_time': 300,
    'min_containers_per_vessel': 100,
    'max_containers_per_vessel': 200,
    'crane_move_time': 3,
    'truck_transport_time': 6
}
```
## Run the simulation:

- Copypython port_simulation.py

- The simulation will output detailed logs of events and summary statistics upon completion.

- simulation_time: Total simulation time (in minutes)
- num_berths: Number of available berths
- num_quay_cranes: Number of quay cranes
- num_trucks: Number of trucks for container transportation
- mean_inter_arrival_time: Average time between vessel arrivals (in minutes)
- min_containers_per_vessel: Minimum number of containers per vessel
- max_containers_per_vessel: Maximum number of containers per vessel
- crane_move_time: Time taken by a crane to move one container (in minutes)
- truck_transport_time: Time taken by a truck to transport a container and # return (in minutes)

## Output

- The simulation provides two types of output:

- Detailed event logs during the simulation run.
- Summary statistics after the simulation, including:

- Total number of vessels served
- Average turnaround time
- Average waiting time
- Detailed log of each vessel's arrival, departure, and turnaround time

## Extending the Simulation
- This simulation provides a foundation that can be extended to include more complex scenarios:

- 1. Different types of vessels or containers
- 2. Equipment breakdowns
- 3. Weather effects
- 4. Multiple terminal areas
- 5. Customs and inspection processes
