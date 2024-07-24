import simpy
import random
from collections import defaultdict

class ContainerTerminal:
    def _init_(self, env, config):
        self.env = env
        self.config = config
        self.berths = simpy.Resource(env, capacity=config['num_berths'])
        self.quay_cranes = simpy.Resource(env, capacity=config['num_quay_cranes'])
        self.trucks = simpy.Resource(env, capacity=config['num_trucks'])
        self.stats = defaultdict(int)
        self.vessel_log = []

    def log(self, message):
        print(f"{self.env.now:.2f}: {message}")

    def vessel_arrival(self):
        vessel_id = 0
        while True:
            inter_arrival_time = random.expovariate(1/self.config['mean_inter_arrival_time'])
            yield self.env.timeout(inter_arrival_time)
            vessel_id += 1
            vessel = Vessel(self.env, self, vessel_id)
            self.env.process(vessel.handle_vessel())
            self.log(f"Vessel {vessel_id} arrived with {vessel.containers} containers")

    def update_stats(self, stat_name, value):
        self.stats[stat_name] += value

class Vessel:
    def _init_(self, env, terminal, vessel_id):
        self.env = env
        self.terminal = terminal
        self.vessel_id = vessel_id
        self.containers = random.randint(
            terminal.config['min_containers_per_vessel'],
            terminal.config['max_containers_per_vessel']
        )

    def handle_vessel(self):
        arrival_time = self.env.now
        
        with self.terminal.berths.request() as berth_req:
            yield berth_req
            berth_time = self.env.now
            waiting_time = berth_time - arrival_time
            self.terminal.log(f"Vessel {self.vessel_id} berthed after waiting {waiting_time:.2f} minutes")
            self.terminal.update_stats('total_waiting_time', waiting_time)

            crane_req = self.terminal.quay_cranes.request()
            yield crane_req
            
            start_unloading_time = self.env.now
            while self.containers > 0:
                truck_req = self.terminal.trucks.request()
                yield truck_req
                
                unloading_time = self.terminal.config['crane_move_time']
                yield self.env.timeout(unloading_time)
                self.containers -= 1
                self.terminal.log(f"Vessel {self.vessel_id}: Container moved. Remaining: {self.containers}")
                
                self.env.process(self.transport_container(truck_req))

            self.terminal.quay_cranes.release(crane_req)

        departure_time = self.env.now
        turnaround_time = departure_time - arrival_time
        self.terminal.log(f"Vessel {self.vessel_id} departed after {turnaround_time:.2f} minutes")
        self.terminal.update_stats('total_turnaround_time', turnaround_time)
        self.terminal.update_stats('vessels_served', 1)
        self.terminal.vessel_log.append({
            'vessel_id': self.vessel_id,
            'arrival_time': arrival_time,
            'departure_time': departure_time,
            'turnaround_time': turnaround_time
        })

    def transport_container(self, truck_req):
        yield self.env.timeout(self.terminal.config['truck_transport_time'])
        self.terminal.trucks.release(truck_req)

def run_simulation(config):
    env = simpy.Environment()
    terminal = ContainerTerminal(env, config)
    env.process(terminal.vessel_arrival())
    env.run(until=config['simulation_time'])
    return terminal

def print_statistics(terminal):
    print("\nSimulation Statistics:")
    print(f"Total vessels served: {terminal.stats['vessels_served']}")
    print(f"Average turnaround time: {terminal.stats['total_turnaround_time'] / terminal.stats['vessels_served']:.2f} minutes")
    print(f"Average waiting time: {terminal.stats['total_waiting_time'] / terminal.stats['vessels_served']:.2f} minutes")
    
    print("\nVessel Log:")
    for vessel in terminal.vessel_log:
        print(f"Vessel {vessel['vessel_id']}: Arrival: {vessel['arrival_time']:.2f}, "
              f"Departure: {vessel['departure_time']:.2f}, "
              f"Turnaround: {vessel['turnaround_time']:.2f}")

if _name_ == "_main_":
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
    
    terminal = run_simulation(config)
    print_statistics(terminal)