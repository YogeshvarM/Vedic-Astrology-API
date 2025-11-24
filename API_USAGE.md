# Vedic Astrology API - Usage Guide

## Base URL
```
http://localhost:8000
```

## Endpoints

### 1. Search Location (GET)
Search for a location to get coordinates and timezone information.

**Endpoint:** `/search_location?place={place_name}&max_results={number}`

**Example:**
```bash
curl "http://localhost:8000/search_location?place=Karimangalam,%20India&max_results=5"
```

**Response:**
```json
[
  {
    "display_name": "Karimangalam, Salem district, Tamil Nadu, India",
    "latitude": 11.4893,
    "longitude": 77.6781,
    "timezone": "Asia/Kolkata",
    "tz_offset": 5.5
  }
]
```

---

### 2. Generate Birth Chart (POST)
Generate a complete Vedic birth chart.

#### Option A: Using Place Name (Automatic geocoding & timezone)

**Endpoint:** `/birth_chart`

**Request Body:**
```json
{
  "name": "Yogeshvar",
  "date": "05-05-1999",
  "time": "14:35",
  "place": "Karimangalam, India"
}
```

#### Option B: Using Coordinates (Manual)

**Request Body:**
```json
{
  "name": "Yogeshvar",
  "date": "05-05-1999",
  "time": "14:35",
  "latitude": 11.4893,
  "longitude": 77.6781,
  "tz_offset": 5.5
}
```

**Example with curl:**
```bash
curl -X POST "http://localhost:8000/birth_chart" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Yogeshvar",
    "date": "05-05-1999",
    "time": "14:35",
    "place": "Karimangalam, India"
  }'
```

---

## Interactive API Documentation
Visit `http://localhost:8000/docs` to use the interactive Swagger UI where you can:
- See all endpoints
- Try them out directly in your browser
- View request/response schemas

---

## Supported Date Formats
- `YYYY-MM-DD` (e.g., `1999-05-05`)
- `DD-MM-YYYY` (e.g., `05-05-1999`)
- `DD/MM/YYYY` (e.g., `05/05/1999`)

## Supported Time Formats
- `HH:MM` (e.g., `14:35`)
- `HH.MM` (e.g., `14.35`)
- `HH:MM:SS` (e.g., `14:35:00`)
- `12-hour format` (e.g., `2:35 PM`)

---

## Workflow: Handling Multiple Location Matches

1. **Search for location first:**
```bash
curl "http://localhost:8000/search_location?place=Springfield&max_results=5"
```

2. **Review the results** and pick the correct one from the list

3. **Use the exact `display_name`** from your chosen location in the birth chart request:
```json
{
  "name": "John",
  "date": "1990-01-15",
  "time": "10:30",
  "place": "Springfield, Sangamon County, Illinois, United States"
}
```

Or directly use the coordinates:
```json
{
  "name": "John",
  "date": "1990-01-15",
  "time": "10:30",
  "latitude": 39.7817,
  "longitude": -89.6501,
  "tz_offset": -6.0
}
```
