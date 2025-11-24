from jyotishganit import calculate_birth_chart
from datetime import datetime
import inspect

# Create a dummy chart
dt = datetime(2023, 1, 1, 12, 0, 0)
chart = calculate_birth_chart(
    birth_date=dt,
    latitude=28.6139,
    longitude=77.2090,
    timezone_offset=5.5,
    name="Test"
)

print("--- Chart Object Attributes ---")
print(dir(chart))

print("\n--- D1 Chart Attributes ---")
print(dir(chart.d1_chart))

# Check for Dashas
if hasattr(chart, 'dashas') or hasattr(chart, 'vimshottari_dasha'):
    print("\n--- Dasha Attributes Found ---")
else:
    print("\n--- No explicit Dasha attribute found in root ---")

# Check for Aspects in Planets
print("\n--- Planet Attributes ---")
if len(chart.d1_chart.planets) > 0:
    p = chart.d1_chart.planets[0]
    print(dir(p))
