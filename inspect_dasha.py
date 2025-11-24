from jyotishganit import calculate_birth_chart
from datetime import datetime

dt = datetime(2023, 1, 1, 12, 0, 0)
chart = calculate_birth_chart(
    birth_date=dt,
    latitude=28.6139,
    longitude=77.2090,
    timezone_offset=5.5,
    name="Test"
)

print(f"Has 'dashas': {hasattr(chart, 'dashas')}")
print(f"Has 'vimshottari_dasha': {hasattr(chart, 'vimshottari_dasha')}")
if hasattr(chart, 'vimshottari_dasha'):
    print(f"Type: {type(chart.vimshottari_dasha)}")
