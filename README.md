# Vedic Astrology API

A FastAPI-based REST API that generates complete Vedic birth charts including all divisional charts (D1-D60), planetary positions, aspects, and astrological calculations.

## Features

- 🌟 **Complete Vedic Chart Calculation**: D1 (Rasi) chart and all divisional charts (D2-D60)
- 🌍 **Smart Location Search**: Automatic geocoding and timezone detection
- 📅 **Flexible Date/Time Input**: Supports multiple formats including natural language
- 🎯 **Comprehensive Data**: Planetary positions, aspects, dignities, Shadbala, Ashtakavarga, and Dashas
- 📊 **JSON Response**: Easy to integrate with any frontend or application

## API Endpoints

### POST `/birth_chart`
Generate a complete Vedic birth chart.

**Request Body:**
```json
{
  "name": "Yogeshvar",
  "date": "05th May, 1999",
  "time": "2:35 PM",
  "place": "Karimangalam, India"
}
```

**Response:** Complete birth chart with all divisional charts, planetary positions, and astrological calculations.

## Supported Input Formats

### Date Formats
- ISO: `1999-05-05`
- DD-MM-YYYY: `05-05-1999`
- DD/MM/YYYY: `05/05/1999`
- DD.MM.YYYY: `05.05.1999`
- Natural: `05th May, 1999`, `May 5, 1999`

### Time Formats
- 24-hour: `14:35`, `14.35`
- 12-hour: `2:35 PM`, `2:35pm`, `02.35pm`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/vedic-astrology-api.git
cd vedic-astrology-api
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the server:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

5. Access the API documentation:
Open `http://localhost:8000/docs` in your browser

## Technologies Used

- **FastAPI**: Modern Python web framework
- **Pydantic**: Data validation
- **jyotishganit**: Vedic astrology calculations
- **geopy**: Geocoding and location services
- **timezonefinder**: Automatic timezone detection
- **pytz**: Timezone handling

## Example Usage

```python
import requests

response = requests.post(
    "http://localhost:8000/birth_chart",
    json={
        "name": "John Doe",
        "date": "15th January, 1990",
        "time": "10:30 AM",
        "place": "New York, USA"
    }
)

chart = response.json()
print(f"Ascendant: {chart['birth_data']['ascendant_sign']}")
print(f"Moon Sign: {chart['birth_data']['moon_sign']}")
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
