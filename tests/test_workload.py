import pytest
from datetime import datetime, timedelta
from src.workload import SimulationClock, get_workload_rate

def test_simulation_clock_scaling():
    # 30 days in 1 hour => scale factor = (30 * 24 * 3600) / 3600 = 720
    start_real = datetime(2026, 1, 1, 0, 0, 0)
    start_sim = datetime(2026, 1, 1, 0, 0, 0)
    
    clock = SimulationClock(start_real, start_sim, scale_factor=720)
    
    # After 10 real seconds, sim time should advance by 7200 seconds (2 hours)
    current_real = start_real + timedelta(seconds=10)
    current_sim = clock.get_simulated_time(current_real)
    
    assert current_sim == start_sim + timedelta(hours=2)

def test_workload_rate_daily_peak():
    # Midday (12:00) should have a higher rate than Midnight (00:00)
    midday = datetime(2026, 1, 1, 12, 0, 0) # Thursday
    midnight = datetime(2026, 1, 1, 0, 0, 0) # Thursday
    
    rate_midday = get_workload_rate(midday)
    rate_midnight = get_workload_rate(midnight)
    
    assert rate_midday > rate_midnight

def test_workload_rate_weekend_lull():
    # Thursday midday vs Saturday midday
    thursday = datetime(2026, 1, 1, 12, 0, 0) # Jan 1 2026 is Thursday
    saturday = datetime(2026, 1, 3, 12, 0, 0) # Jan 3 2026 is Saturday
    
    rate_thursday = get_workload_rate(thursday)
    rate_saturday = get_workload_rate(saturday)
    
    assert rate_thursday > rate_saturday
