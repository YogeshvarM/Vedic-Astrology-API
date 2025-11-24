from datetime import datetime
from typing import Optional, Dict, Any, List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator, model_validator

from jyotishganit import calculate_birth_chart, get_birth_chart_json_string
import json

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from timezonefinder import TimezoneFinder
from datetime import timezone as dt_timezone
import pytz

app = FastAPI(
    title="Vedic Astrology API",
    description="Returns full Vedic charts (including all divisional charts) as JSON.",
    version="1.0.0",
    servers=[
        {"url": "https://vedic-astrology-api-production.up.railway.app", "description": "Production Server"},
        {"url": "http://localhost:8000", "description": "Local Development"}
    ]
)

# Add CORS middleware for API access from different domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class BirthData(BaseModel):
    name: Optional[str] = Field(default=None, description="Name of native")
    date: str = Field(..., description="Date in various formats: YYYY-MM-DD, DD-MM-YYYY, DD.MM.YYYY, etc.")
    time: str = Field(..., description="Time in 24h or 12h format: HH:MM, HH.MM, 02:35pm, etc.")
    place: str = Field(..., description="Place name (e.g., 'Karimangalam, India', 'New York, USA')")
    
    @field_validator('date')
    @classmethod
    def parse_date(cls, v: str) -> str:
        """Parse and normalize date to YYYY-MM-DD format"""
        import re
        
        # Remove ordinal suffixes (st, nd, rd, th) and extra spaces/commas
        v_cleaned = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', v)
        v_cleaned = re.sub(r'\s*,\s*', ' ', v_cleaned)  # Normalize commas
        v_cleaned = re.sub(r'\s+', ' ', v_cleaned).strip()  # Normalize spaces
        
        date_formats = [
            "%Y-%m-%d",  # ISO format: YYYY-MM-DD
            "%d-%m-%Y",  # DD-MM-YYYY
            "%d/%m/%Y",  # DD/MM/YYYY
            "%Y/%m/%d",  # YYYY/MM/DD
            "%d.%m.%Y",  # DD.MM.YYYY
            "%Y.%m.%d",  # YYYY.MM.DD
            "%d %B %Y",  # DD Month YYYY (e.g., 05 May 1999)
            "%d %b %Y",  # DD Mon YYYY (e.g., 05 May 1999)
            "%B %d %Y",  # Month DD YYYY (e.g., May 05 1999)
            "%b %d %Y",  # Mon DD YYYY (e.g., May 05 1999)
            "%d-%B-%Y",  # DD-Month-YYYY
            "%d-%b-%Y",  # DD-Mon-YYYY
        ]
        
        for fmt in date_formats:
            try:
                dt = datetime.strptime(v_cleaned, fmt)
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                continue
        
        raise ValueError(f"Invalid date format: {v}. Supported formats: YYYY-MM-DD, DD-MM-YYYY, DD/MM/YYYY, DD.MM.YYYY, '5th May 1999', 'May 5, 1999'")
    
    @field_validator('time')
    @classmethod
    def parse_time(cls, v: str) -> str:
        """Parse and normalize time to HH:MM format"""
        # Normalize: replace dots with colons
        v = v.replace('.', ':')
        # Normalize: ensure space before AM/PM and make uppercase
        v_upper = v.upper()
        # Handle formats like "02:35PM" -> "02:35 PM"
        import re
        v_normalized = re.sub(r'(\d)([AP]M)', r'\1 \2', v_upper)
        
        time_formats = [
            "%H:%M",     # HH:MM (24-hour)
            "%H:%M:%S",  # HH:MM:SS (24-hour)
            "%I:%M %p",  # 12-hour format with AM/PM (with space)
        ]
        
        for fmt in time_formats:
            try:
                dt = datetime.strptime(v_normalized, fmt)
                return dt.strftime("%H:%M")
            except ValueError:
                continue
        
        raise ValueError(f"Invalid time format: {v}. Supported formats: HH:MM, HH.MM, HH:MM:SS, 02:35 PM, 02:35PM")
    
class BirthChartResponse(BaseModel):
    birth_data: Dict[str, Any]
    panchanga: Dict[str, Any]
    charts: Dict[str, Any]
    raw_chart: Dict[str, Any]


def get_timezone_offset(latitude: float, longitude: float, dt: datetime) -> float:
    """Get timezone offset for a location at a specific datetime"""
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lat=latitude, lng=longitude)
    
    if tz_name is None:
        raise ValueError(f"Could not determine timezone for coordinates ({latitude}, {longitude})")
    
    tz = pytz.timezone(tz_name)
    # Get the offset for the specific datetime (accounts for DST)
    offset_seconds = tz.utcoffset(dt).total_seconds()
    return offset_seconds / 3600  # Convert to hours


def get_location_data(place_name: str, dt: datetime) -> tuple[float, float, float]:
    """Get latitude, longitude, and timezone offset for a place name"""
    geolocator = Nominatim(user_agent="vedic-astrology-api")
    
    try:
        location = geolocator.geocode(place_name, timeout=10)
        
        if not location:
            raise HTTPException(status_code=404, detail=f"Could not find location '{place_name}'. Please try a more specific name (e.g., 'City, State, Country').")
        
        latitude = location.latitude
        longitude = location.longitude
        
        # Get timezone offset
        tf = TimezoneFinder()
        tz_name = tf.timezone_at(lat=latitude, lng=longitude)
        
        if tz_name is None:
            raise HTTPException(status_code=500, detail=f"Could not determine timezone for '{place_name}'")
        
        tz = pytz.timezone(tz_name)
        offset_seconds = tz.utcoffset(dt).total_seconds()
        tz_offset = offset_seconds / 3600
        
        return latitude, longitude, tz_offset
        
    except GeocoderTimedOut:
        raise HTTPException(status_code=504, detail="Geocoding service timed out. Please try again.")
    except GeocoderServiceError as e:
        raise HTTPException(status_code=503, detail=f"Geocoding service error: {str(e)}")


def datetime_from_strings(date_str: str, time_str: str) -> datetime:
    """Create datetime from validated date and time strings (already normalized by Pydantic)"""
    return datetime.fromisoformat(f"{date_str}T{time_str}:00")


def divisional_chart_to_json(dchart) -> Dict[str, Any]:
    houses_json = []
    for house in dchart.houses:
        occupants_json = []
        for p in house.occupants:
            occupants_json.append(
                {
                    "planet": getattr(getattr(p, "celestial_body", None), "name", str(getattr(p, "celestial_body", ""))),
                    "sign": getattr(getattr(p, "sign", None), "name", str(getattr(p, "sign", ""))),
                }
            )

        houses_json.append(
            {
                "house_number": getattr(house, "number", None),
                "sign": getattr(getattr(house, "sign", None), "name", str(getattr(house, "sign", ""))),
                "occupants": occupants_json,
            }
        )
    return {"houses": houses_json}


def all_divisional_charts_to_json(chart) -> Dict[str, Any]:
    result = {}
    for key, dchart in chart.divisional_charts.items():
        result[key] = divisional_chart_to_json(dchart)
    return result


def panchanga_to_json(chart) -> Dict[str, Any]:
    p = chart.panchanga
    return {
        "tithi": getattr(p, "tithi", None),
        "nakshatra": getattr(p, "nakshatra", None),
        "yoga": getattr(p, "yoga", None),
        "karana": getattr(p, "karana", None),
        "vaara": getattr(p, "vaara", None),
    }


@app.get("/")
def health_check():
    """Health check endpoint for Railway and monitoring"""
    return {
        "status": "healthy",
        "service": "Vedic Astrology API",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "birth_chart": "/birth_chart"
        }
    }


@app.post("/birth_chart", response_model=BirthChartResponse)
def birth_chart(data: BirthData):
    birth_dt = datetime_from_strings(data.date, data.time)
    
    # Geocode the place and get timezone
    latitude, longitude, tz_offset = get_location_data(data.place, birth_dt)

    chart = calculate_birth_chart(
        birth_date=birth_dt,
        latitude=latitude,
        longitude=longitude,
        timezone_offset=tz_offset,
        name=data.name or "User",
    )

    raw_chart = json.loads(get_birth_chart_json_string(chart))
    charts_json = all_divisional_charts_to_json(chart)
    panchanga_json = panchanga_to_json(chart)

    birth_data_json = {
        "name": data.name or "User",
        "datetime": birth_dt.isoformat(),
        "date": data.date,
        "time": data.time,
        "place": data.place,
        "tz_offset": tz_offset,
        "latitude": latitude,
        "longitude": longitude,
        "ascendant_sign": getattr(chart.d1_chart.houses[0].sign, "name", str(chart.d1_chart.houses[0].sign)),
        "moon_sign": getattr(chart.d1_chart.planets[1].sign, "name", str(chart.d1_chart.planets[1].sign)),
    }

    return BirthChartResponse(
        birth_data=birth_data_json,
        panchanga=panchanga_json,
        charts=charts_json,
        raw_chart=raw_chart,
    )
