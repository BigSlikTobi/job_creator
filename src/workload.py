import math
from datetime import datetime, timedelta

class SimulationClock:
    def __init__(self, real_start: datetime, sim_start: datetime, scale_factor: float):
        """
        :param real_start: When the script started in real life.
        :param sim_start: The starting time in the simulated world.
        :param scale_factor: For example, 720 means 1 real second = 720 sim seconds (12 mins).
        """
        self.real_start = real_start
        self.sim_start = sim_start
        self.scale_factor = scale_factor
        
    def get_simulated_time(self, current_real: datetime) -> datetime:
        elapsed_real = (current_real - self.real_start).total_seconds()
        elapsed_sim = elapsed_real * self.scale_factor
        return self.sim_start + timedelta(seconds=elapsed_sim)

def get_workload_rate(sim_time: datetime) -> float:
    """
    Returns the expected number of jobs per hour at the given simulated time.
    """
    base_rate = 10.0
    
    # Daily sinusoidal curve: peaks around midday, drops around midnight.
    # We map 0-24 hours to a sine wave where min is at 0:00 and max is at 12:00.
    # sin((hour - 6) / 24 * 2 * pi) gives -1 at 0 and +1 at 12.
    # We add 1.0 so the modifier is between 0 and 2.
    hour = sim_time.hour + (sim_time.minute / 60.0)
    daily_modifier = math.sin((hour - 6) / 24.0 * 2 * math.pi) + 1.0
    
    # Weekend modifier: drop by half on weekends
    # weekday() returns 0 for Monday, 6 for Sunday
    weekend_modifier = 0.5 if sim_time.weekday() >= 5 else 1.0
    
    # Prevent complete 0 rate to maintain a minimal heartbeat
    modifier = max(0.1, daily_modifier * weekend_modifier)
    
    return base_rate * modifier
