from __future__ import annotations

from copy import deepcopy

FORMAT_RULES = {
    "t20": {
        "label": "T20 International",
        "max_overs": 20,
        "default_par": 168,
        "score_floor": 70,
        "score_ceiling": 280,
    },
    "odi": {
        "label": "ODI International",
        "max_overs": 50,
        "default_par": 268,
        "score_floor": 140,
        "score_ceiling": 390,
    },
}

PITCH_TYPES = [
    {"type": "Flat batting deck", "emoji": "🛣️", "moisture": "Low", "batting_impact": 0.08, "bowling_impact": -0.04},
    {"type": "Balanced surface", "emoji": "⚖️", "moisture": "Medium", "batting_impact": 0.00, "bowling_impact": 0.00},
    {"type": "Green seam-friendly", "emoji": "🌿", "moisture": "High", "batting_impact": -0.06, "bowling_impact": 0.05},
    {"type": "Dry spin-friendly", "emoji": "🌀", "moisture": "Low", "batting_impact": -0.04, "bowling_impact": 0.04},
    {"type": "Slow tired pitch", "emoji": "🐢", "moisture": "Medium", "batting_impact": -0.08, "bowling_impact": 0.07},
]

WEATHER_TYPES = [
    {"label": "Clear", "emoji": "☀️", "batting_impact": 0.00, "chasing_impact": 0.00},
    {"label": "Cloudy", "emoji": "☁️", "batting_impact": -0.03, "chasing_impact": -0.02},
    {"label": "Heavy dew", "emoji": "💧", "batting_impact": 0.03, "chasing_impact": 0.08},
    {"label": "Hot and dry", "emoji": "🥵", "batting_impact": -0.01, "chasing_impact": 0.00},
    {"label": "Humid", "emoji": "🌫️", "batting_impact": -0.02, "chasing_impact": 0.01},
    {"label": "Light drizzle risk", "emoji": "🌦️", "batting_impact": -0.06, "chasing_impact": -0.03},
]

RAW_VENUES = [
    {"name": "Wankhede Stadium", "city": "Mumbai", "country": "India", "avg_score": 175, "pitch_type": "Flat / Batting Paradise", "boundary_size": "Medium"},
    {"name": "Eden Gardens", "city": "Kolkata", "country": "India", "avg_score": 165, "pitch_type": "Damp / Slow & Low", "boundary_size": "Large"},
    {"name": "M. Chinnaswamy Stadium", "city": "Bangalore", "country": "India", "avg_score": 180, "pitch_type": "Flat / Batting Paradise", "boundary_size": "Small"},
    {"name": "Arun Jaitley Stadium", "city": "Delhi", "country": "India", "avg_score": 170, "pitch_type": "Dry / Spinner Friendly", "boundary_size": "Medium"},
    {"name": "MA Chidambaram Stadium", "city": "Chennai", "country": "India", "avg_score": 160, "pitch_type": "Damp / Slow & Low", "boundary_size": "Large"},
    {"name": "Narendra Modi Stadium", "city": "Ahmedabad", "country": "India", "avg_score": 172, "pitch_type": "Standard / Balanced", "boundary_size": "Large"},
    {"name": "HPCA Stadium", "city": "Dharamshala", "country": "India", "avg_score": 168, "pitch_type": "Green / Pacer Friendly", "boundary_size": "Medium"},
    {"name": "Rajiv Gandhi Intl. Stadium", "city": "Hyderabad", "country": "India", "avg_score": 170, "pitch_type": "Flat / Batting Paradise", "boundary_size": "Medium"},
    {"name": "Ekana Cricket Stadium", "city": "Lucknow", "country": "India", "avg_score": 160, "pitch_type": "Slow / Variable Bounce", "boundary_size": "Large"},
    {"name": "Holkar Cricket Stadium", "city": "Indore", "country": "India", "avg_score": 185, "pitch_type": "Flat / Batting Paradise", "boundary_size": "Small"},
    {"name": "VCA Stadium", "city": "Nagpur", "country": "India", "avg_score": 155, "pitch_type": "Dry / Spinner Friendly", "boundary_size": "Medium"},
    {"name": "MCA International Stadium", "city": "Pune", "country": "India", "avg_score": 178, "pitch_type": "Flat / Batting Paradise", "boundary_size": "Medium"},
    {"name": "JSCA Intl. Stadium Complex", "city": "Ranchi", "country": "India", "avg_score": 160, "pitch_type": "Standard / Balanced", "boundary_size": "Large"},
    {"name": "ACA-VDCA Stadium", "city": "Visakhapatnam", "country": "India", "avg_score": 172, "pitch_type": "Flat / Batting Paradise", "boundary_size": "Medium"},
    {"name": "Melbourne Cricket Ground", "city": "Melbourne", "country": "Australia", "avg_score": 170, "pitch_type": "Standard / Balanced", "boundary_size": "Large"},
    {"name": "Sydney Cricket Ground", "city": "Sydney", "country": "Australia", "avg_score": 168, "pitch_type": "Dry / Spinner Friendly", "boundary_size": "Large"},
    {"name": "Adelaide Oval", "city": "Adelaide", "country": "Australia", "avg_score": 172, "pitch_type": "Flat / Batting Paradise", "boundary_size": "Medium"},
    {"name": "Perth Stadium (Optus Stadium)", "city": "Perth", "country": "Australia", "avg_score": 165, "pitch_type": "Green / Pacer Friendly", "boundary_size": "Large"},
    {"name": "The Gabba", "city": "Brisbane", "country": "Australia", "avg_score": 170, "pitch_type": "Green / Pacer Friendly", "boundary_size": "Medium"},
    {"name": "Bellerive Oval", "city": "Hobart", "country": "Australia", "avg_score": 160, "pitch_type": "Green / Pacer Friendly", "boundary_size": "Medium"},
    {"name": "WACA Ground", "city": "Perth", "country": "Australia", "avg_score": 172, "pitch_type": "Green / Pacer Friendly", "boundary_size": "Medium"},
    {"name": "Manuka Oval", "city": "Canberra", "country": "Australia", "avg_score": 155, "pitch_type": "Standard / Balanced", "boundary_size": "Medium"},
    {"name": "Lord's", "city": "London", "country": "England", "avg_score": 165, "pitch_type": "Green / Pacer Friendly", "boundary_size": "Large"},
    {"name": "Old Trafford", "city": "Manchester", "country": "England", "avg_score": 162, "pitch_type": "Standard / Balanced", "boundary_size": "Large"},
    {"name": "The Oval", "city": "London", "country": "England", "avg_score": 168, "pitch_type": "Flat / Batting Paradise", "boundary_size": "Medium"},
    {"name": "Edgbaston", "city": "Birmingham", "country": "England", "avg_score": 170, "pitch_type": "Flat / Batting Paradise", "boundary_size": "Medium"},
    {"name": "Trent Bridge", "city": "Nottingham", "country": "England", "avg_score": 175, "pitch_type": "Flat / Batting Paradise", "boundary_size": "Small"},
    {"name": "Headingley", "city": "Leeds", "country": "England", "avg_score": 170, "pitch_type": "Green / Pacer Friendly", "boundary_size": "Medium"},
    {"name": "Sophia Gardens", "city": "Cardiff", "country": "Wales", "avg_score": 165, "pitch_type": "Standard / Balanced", "boundary_size": "Medium"},
    {"name": "Rose Bowl (The Ageas Bowl)", "city": "Southampton", "country": "England", "avg_score": 170, "pitch_type": "Standard / Balanced", "boundary_size": "Large"},
    {"name": "Riverside Ground", "city": "Chester-le-Street", "country": "England", "avg_score": 165, "pitch_type": "Green / Pacer Friendly", "boundary_size": "Large"},
    {"name": "County Ground, Bristol", "city": "Bristol", "country": "England", "avg_score": 168, "pitch_type": "Flat / Batting Paradise", "boundary_size": "Small"},
    {"name": "VRA Cricket Ground", "city": "Amstelveen", "country": "Netherlands", "avg_score": 150, "pitch_type": "Green / Pacer Friendly", "boundary_size": "Medium"},
    {"name": "Sportpark Westvliet", "city": "The Hague", "country": "Netherlands", "avg_score": 145, "pitch_type": "Damp / Slow & Low", "boundary_size": "Medium"},
    {"name": "Stormont", "city": "Belfast", "country": "Northern Ireland", "avg_score": 160, "pitch_type": "Green / Pacer Friendly", "boundary_size": "Medium"},
    {"name": "Dubai International Stadium", "city": "Dubai", "country": "UAE", "avg_score": 158, "pitch_type": "Damp / Slow & Low", "boundary_size": "Medium"},
    {"name": "Sharjah Cricket Stadium", "city": "Sharjah", "country": "UAE", "avg_score": 155, "pitch_type": "Dry / Spinner Friendly", "boundary_size": "Small"},
    {"name": "Gaddafi Stadium", "city": "Lahore", "country": "Pakistan", "avg_score": 170, "pitch_type": "Flat / Batting Paradise", "boundary_size": "Medium"},
    {"name": "National Stadium", "city": "Karachi", "country": "Pakistan", "avg_score": 172, "pitch_type": "Flat / Batting Paradise", "boundary_size": "Large"},
    {"name": "Sheikh Zayed Stadium", "city": "Abu Dhabi", "country": "UAE", "avg_score": 160, "pitch_type": "Standard / Balanced", "boundary_size": "Large"},
    {"name": "Rawalpindi Cricket Stadium", "city": "Rawalpindi", "country": "Pakistan", "avg_score": 175, "pitch_type": "Flat / Batting Paradise", "boundary_size": "Medium"},
    {"name": "ICC Academy Ground", "city": "Dubai", "country": "UAE", "avg_score": 155, "pitch_type": "Standard / Balanced", "boundary_size": "Medium"},
    {"name": "Multan Cricket Stadium", "city": "Multan", "country": "Pakistan", "avg_score": 175, "pitch_type": "Flat / Batting Paradise", "boundary_size": "Medium"},
    {"name": "The Wanderers", "city": "Johannesburg", "country": "South Africa", "avg_score": 175, "pitch_type": "Flat / Batting Paradise", "boundary_size": "Medium"},
    {"name": "Newlands", "city": "Cape Town", "country": "South Africa", "avg_score": 168, "pitch_type": "Standard / Balanced", "boundary_size": "Medium"},
    {"name": "Kingsmead", "city": "Durban", "country": "South Africa", "avg_score": 170, "pitch_type": "Damp / Slow & Low", "boundary_size": "Medium"},
    {"name": "SuperSport Park", "city": "Centurion", "country": "South Africa", "avg_score": 178, "pitch_type": "Flat / Batting Paradise", "boundary_size": "Small"},
    {"name": "St George's Park", "city": "Port Elizabeth", "country": "South Africa", "avg_score": 165, "pitch_type": "Standard / Balanced", "boundary_size": "Medium"},
    {"name": "Mangaung Oval", "city": "Bloemfontein", "country": "South Africa", "avg_score": 168, "pitch_type": "Standard / Balanced", "boundary_size": "Medium"},
    {"name": "Buffalo Park", "city": "East London", "country": "South Africa", "avg_score": 162, "pitch_type": "Standard / Balanced", "boundary_size": "Medium"},
    {"name": "Willowmoore Park", "city": "Benoni", "country": "South Africa", "avg_score": 175, "pitch_type": "Flat / Batting Paradise", "boundary_size": "Small"},
    {"name": "Boland Park", "city": "Paarl", "country": "South Africa", "avg_score": 160, "pitch_type": "Damp / Slow & Low", "boundary_size": "Large"},
    {"name": "Eden Park", "city": "Auckland", "country": "New Zealand", "avg_score": 178, "pitch_type": "Flat / Batting Paradise", "boundary_size": "Small"},
    {"name": "Basin Reserve", "city": "Wellington", "country": "New Zealand", "avg_score": 165, "pitch_type": "Green / Pacer Friendly", "boundary_size": "Large"},
    {"name": "Hagley Oval", "city": "Christchurch", "country": "New Zealand", "avg_score": 168, "pitch_type": "Green / Pacer Friendly", "boundary_size": "Large"},
    {"name": "Seddon Park", "city": "Hamilton", "country": "New Zealand", "avg_score": 175, "pitch_type": "Flat / Batting Paradise", "boundary_size": "Medium"},
    {"name": "Bay Oval", "city": "Mount Maunganui", "country": "New Zealand", "avg_score": 172, "pitch_type": "Flat / Batting Paradise", "boundary_size": "Medium"},
    {"name": "McLean Park", "city": "Napier", "country": "New Zealand", "avg_score": 172, "pitch_type": "Flat / Batting Paradise", "boundary_size": "Medium"},
    {"name": "University Oval", "city": "Dunedin", "country": "New Zealand", "avg_score": 162, "pitch_type": "Green / Pacer Friendly", "boundary_size": "Medium"},
    {"name": "Queenstown Events Centre", "city": "Queenstown", "country": "New Zealand", "avg_score": 170, "pitch_type": "Flat / Batting Paradise", "boundary_size": "Small"},
    {"name": "Kensington Oval", "city": "Bridgetown", "country": "Barbados", "avg_score": 172, "pitch_type": "Standard / Balanced", "boundary_size": "Medium"},
    {"name": "Queen's Park Oval", "city": "Port of Spain", "country": "Trinidad", "avg_score": 168, "pitch_type": "Dry / Spinner Friendly", "boundary_size": "Large"},
    {"name": "Sabina Park", "city": "Kingston", "country": "Jamaica", "avg_score": 165, "pitch_type": "Standard / Balanced", "boundary_size": "Medium"},
    {"name": "Daren Sammy Cricket Ground", "city": "Gros Islet", "country": "St Lucia", "avg_score": 170, "pitch_type": "Flat / Batting Paradise", "boundary_size": "Medium"},
    {"name": "Sir Vivian Richards Stadium", "city": "North Sound", "country": "Antigua", "avg_score": 162, "pitch_type": "Damp / Slow & Low", "boundary_size": "Large"},
    {"name": "Providence Stadium", "city": "Providence", "country": "Guyana", "avg_score": 162, "pitch_type": "Damp / Slow & Low", "boundary_size": "Large"},
    {"name": "Brian Lara Cricket Academy", "city": "Tarouba", "country": "Trinidad & Tobago", "avg_score": 168, "pitch_type": "Standard / Balanced", "boundary_size": "Medium"},
    {"name": "Arnos Vale Ground", "city": "Kingstown", "country": "St Vincent & The G.", "avg_score": 145, "pitch_type": "Damp / Slow & Low", "boundary_size": "Medium"},
    {"name": "Warner Park", "city": "Basseterre", "country": "St Kitts & Nevis", "avg_score": 168, "pitch_type": "Standard / Balanced", "boundary_size": "Medium"},
    {"name": "R. Premadasa Stadium", "city": "Colombo", "country": "Sri Lanka", "avg_score": 170, "pitch_type": "Damp / Slow & Low", "boundary_size": "Medium"},
    {"name": "Pallekele International Stadium", "city": "Pallekele", "country": "Sri Lanka", "avg_score": 165, "pitch_type": "Standard / Balanced", "boundary_size": "Large"},
    {"name": "Galle International Stadium", "city": "Galle", "country": "Sri Lanka", "avg_score": 155, "pitch_type": "Dry / Spinner Friendly", "boundary_size": "Medium"},
    {"name": "Mahinda Rajapaksa Stadium", "city": "Hambantota", "country": "Sri Lanka", "avg_score": 158, "pitch_type": "Standard / Balanced", "boundary_size": "Large"},
    {"name": "Shere Bangla National Stadium", "city": "Dhaka", "country": "Bangladesh", "avg_score": 165, "pitch_type": "Damp / Slow & Low", "boundary_size": "Medium"},
    {"name": "Zohur Ahmed Chowdhury Stadium", "city": "Chattogram", "country": "Bangladesh", "avg_score": 168, "pitch_type": "Standard / Balanced", "boundary_size": "Medium"},
    {"name": "Sylhet International Stadium", "city": "Sylhet", "country": "Bangladesh", "avg_score": 155, "pitch_type": "Damp / Slow & Low", "boundary_size": "Medium"},
    {"name": "Nassau Co. Intl. Cricket Stadium", "city": "New York", "country": "USA", "avg_score": 110, "pitch_type": "Spicy / Seam & Uneven", "boundary_size": "Medium"},
    {"name": "Central Broward Park", "city": "Lauderhill, Florida", "country": "USA", "avg_score": 175, "pitch_type": "Flat / Batting Paradise", "boundary_size": "Medium"},
    {"name": "Grand Prairie Stadium", "city": "Dallas, Texas", "country": "USA", "avg_score": 165, "pitch_type": "Standard / Balanced", "boundary_size": "Medium"},
    {"name": "Moosa Stadium", "city": "Pearland, Texas", "country": "USA", "avg_score": 165, "pitch_type": "Standard / Balanced", "boundary_size": "Medium"},
    {"name": "Harare Sports Club", "city": "Harare", "country": "Zimbabwe", "avg_score": 168, "pitch_type": "Standard / Balanced", "boundary_size": "Medium"},
    {"name": "Queens Sports Club", "city": "Bulawayo", "country": "Zimbabwe", "avg_score": 165, "pitch_type": "Standard / Balanced", "boundary_size": "Medium"},
    {"name": "Malahide Cricket Club Ground", "city": "Dublin", "country": "Ireland", "avg_score": 170, "pitch_type": "Green / Pacer Friendly", "boundary_size": "Medium"},
    {"name": "Grange Cricket Club", "city": "Edinburgh", "country": "Scotland", "avg_score": 158, "pitch_type": "Green / Pacer Friendly", "boundary_size": "Medium"},
    {"name": "Mannofield Park", "city": "Aberdeen", "country": "Scotland", "avg_score": 155, "pitch_type": "Green / Pacer Friendly", "boundary_size": "Medium"},
    {"name": "Al Amerat Cricket Ground", "city": "Muscat", "country": "Oman", "avg_score": 155, "pitch_type": "Dry / Spinner Friendly", "boundary_size": "Medium"},
    {"name": "Tribhuvan University Ground", "city": "Kirtipur", "country": "Nepal", "avg_score": 165, "pitch_type": "Dry / Spinner Friendly", "boundary_size": "Medium"},
    {"name": "Maple Leaf North-West Ground", "city": "King City", "country": "Canada", "avg_score": 168, "pitch_type": "Standard / Balanced", "boundary_size": "Medium"},
    {"name": "Entebbe Cricket Oval", "city": "Entebbe", "country": "Uganda", "avg_score": 140, "pitch_type": "Dry / Spinner Friendly", "boundary_size": "Medium"},
    {"name": "Amini Park", "city": "Port Moresby", "country": "PNG", "avg_score": 150, "pitch_type": "Standard / Balanced", "boundary_size": "Medium"},
    {"name": "Gymkhana Club Ground", "city": "Nairobi", "country": "Kenya", "avg_score": 140, "pitch_type": "Damp / Slow & Low", "boundary_size": "Medium"},
]


def _odi_avg_from_t20(avg_score: int) -> int:
    projected = int(round(avg_score * 1.52))
    return max(185, min(340, projected))


COUNTRY_REGION = {
    "India": "Asia",
    "Australia": "Oceania",
    "England": "Europe",
    "Wales": "Europe",
    "Netherlands": "Europe",
    "Northern Ireland": "Europe",
    "UAE": "Middle East",
    "Pakistan": "Asia",
    "South Africa": "Africa",
    "New Zealand": "Oceania",
    "Barbados": "Caribbean",
    "Trinidad": "Caribbean",
    "Jamaica": "Caribbean",
    "St Lucia": "Caribbean",
    "Antigua": "Caribbean",
    "Guyana": "Caribbean",
    "Trinidad & Tobago": "Caribbean",
    "St Vincent & The G.": "Caribbean",
    "St Kitts & Nevis": "Caribbean",
    "Sri Lanka": "Asia",
    "Bangladesh": "Asia",
    "USA": "North America",
    "Zimbabwe": "Africa",
    "Ireland": "Europe",
    "Scotland": "Europe",
}

EXCLUDED_COUNTRIES = {"Oman", "Nepal", "Canada", "Uganda", "PNG", "Kenya"}


VENUES = [
    {
        "name": v["name"],
        "city": v["city"],
        "country": v["country"],
        "region": COUNTRY_REGION.get(v["country"], "Other"),
        "t20_avg": v["avg_score"],
        "odi_avg": _odi_avg_from_t20(v["avg_score"]),
        "pitch_type": v["pitch_type"],
        "boundary_size": v["boundary_size"],
    }
    for v in RAW_VENUES
    if v["country"] not in EXCLUDED_COUNTRIES
]

TOP_ODI_TEAMS = [
    {"name": "India", "flag": "IND", "flag_img": "/static/flags/india.svg"},
    {"name": "Australia", "flag": "AUS", "flag_img": "/static/flags/australia.svg"},
    {"name": "Pakistan", "flag": "PAK", "flag_img": "/static/flags/pakistan.svg"},
    {"name": "South Africa", "flag": "SA", "flag_img": "/static/flags/south_africa.svg"},
    {"name": "New Zealand", "flag": "NZ", "flag_img": "/static/flags/new_zealand.svg"},
    {"name": "England", "flag": "ENG", "flag_img": "/static/flags/england.svg"},
    {"name": "Sri Lanka", "flag": "SL", "flag_img": "/static/flags/sri_lanka.svg"},
    {"name": "Bangladesh", "flag": "BAN", "flag_img": "/static/flags/bangladesh.svg"},
    {"name": "Afghanistan", "flag": "AFG", "flag_img": "/static/flags/afghanistan.svg"},
    {"name": "West Indies", "flag": "WI", "flag_img": "/static/flags/west_indies.svg"},
]

# 10 ODI teams x 15 players each.
ODI_SQUADS = {
    "India": [
        {"name": "Rohit Sharma", "role": "Batter", "bat_avg": 49.2, "strike_rate": 92.8, "bowl_avg": 0.0, "economy": 0.0, "rating": 94},
        {"name": "Shubman Gill", "role": "Batter", "bat_avg": 58.4, "strike_rate": 102.7, "bowl_avg": 0.0, "economy": 0.0, "rating": 95},
        {"name": "Virat Kohli", "role": "Batter", "bat_avg": 58.7, "strike_rate": 93.6, "bowl_avg": 0.0, "economy": 0.0, "rating": 96},
        {"name": "Shreyas Iyer", "role": "Batter", "bat_avg": 49.6, "strike_rate": 101.1, "bowl_avg": 0.0, "economy": 0.0, "rating": 90},
        {"name": "KL Rahul", "role": "WK-Batter", "bat_avg": 50.1, "strike_rate": 88.8, "bowl_avg": 0.0, "economy": 0.0, "rating": 89},
        {"name": "Ishan Kishan", "role": "WK-Batter", "bat_avg": 42.3, "strike_rate": 103.5, "bowl_avg": 0.0, "economy": 0.0, "rating": 82},
        {"name": "Hardik Pandya", "role": "All-Rounder", "bat_avg": 34.3, "strike_rate": 112.2, "bowl_avg": 35.7, "economy": 5.6, "rating": 88},
        {"name": "Ravindra Jadeja", "role": "All-Rounder", "bat_avg": 34.8, "strike_rate": 85.3, "bowl_avg": 36.3, "economy": 4.9, "rating": 86},
        {"name": "Axar Patel", "role": "All-Rounder", "bat_avg": 21.3, "strike_rate": 95.0, "bowl_avg": 31.8, "economy": 4.6, "rating": 82},
        {"name": "Kuldeep Yadav", "role": "Bowler", "bat_avg": 11.2, "strike_rate": 71.0, "bowl_avg": 26.7, "economy": 5.0, "rating": 90},
        {"name": "Mohammed Shami", "role": "Bowler", "bat_avg": 8.7, "strike_rate": 84.1, "bowl_avg": 23.9, "economy": 5.6, "rating": 91},
        {"name": "Jasprit Bumrah", "role": "Bowler", "bat_avg": 8.0, "strike_rate": 84.8, "bowl_avg": 23.6, "economy": 4.6, "rating": 95},
        {"name": "Mohammed Siraj", "role": "Bowler", "bat_avg": 9.8, "strike_rate": 88.0, "bowl_avg": 24.0, "economy": 5.1, "rating": 89},
        {"name": "Arshdeep Singh", "role": "Bowler", "bat_avg": 8.8, "strike_rate": 90.0, "bowl_avg": 28.0, "economy": 5.4, "rating": 82},
        {"name": "Washington Sundar", "role": "All-Rounder", "bat_avg": 18.4, "strike_rate": 83.1, "bowl_avg": 37.4, "economy": 4.8, "rating": 78},
    ],
    "Australia": [
        {"name": "David Warner", "role": "Batter", "bat_avg": 45.1, "strike_rate": 97.3, "bowl_avg": 0.0, "economy": 0.0, "rating": 90},
        {"name": "Travis Head", "role": "Batter", "bat_avg": 43.8, "strike_rate": 104.5, "bowl_avg": 0.0, "economy": 0.0, "rating": 92},
        {"name": "Steve Smith", "role": "Batter", "bat_avg": 43.7, "strike_rate": 87.1, "bowl_avg": 0.0, "economy": 0.0, "rating": 88},
        {"name": "Marnus Labuschagne", "role": "Batter", "bat_avg": 36.4, "strike_rate": 84.2, "bowl_avg": 0.0, "economy": 0.0, "rating": 82},
        {"name": "Mitchell Marsh", "role": "All-Rounder", "bat_avg": 34.2, "strike_rate": 101.5, "bowl_avg": 36.8, "economy": 5.6, "rating": 86},
        {"name": "Glenn Maxwell", "role": "All-Rounder", "bat_avg": 34.0, "strike_rate": 124.0, "bowl_avg": 50.0, "economy": 5.5, "rating": 90},
        {"name": "Josh Inglis", "role": "WK-Batter", "bat_avg": 33.2, "strike_rate": 93.5, "bowl_avg": 0.0, "economy": 0.0, "rating": 83},
        {"name": "Alex Carey", "role": "WK-Batter", "bat_avg": 36.5, "strike_rate": 90.2, "bowl_avg": 0.0, "economy": 0.0, "rating": 82},
        {"name": "Cameron Green", "role": "All-Rounder", "bat_avg": 31.2, "strike_rate": 92.3, "bowl_avg": 42.0, "economy": 5.8, "rating": 80},
        {"name": "Pat Cummins", "role": "Bowler", "bat_avg": 16.3, "strike_rate": 92.2, "bowl_avg": 30.5, "economy": 5.4, "rating": 86},
        {"name": "Mitchell Starc", "role": "Bowler", "bat_avg": 12.8, "strike_rate": 95.0, "bowl_avg": 23.4, "economy": 5.2, "rating": 92},
        {"name": "Josh Hazlewood", "role": "Bowler", "bat_avg": 10.8, "strike_rate": 88.0, "bowl_avg": 27.0, "economy": 4.9, "rating": 89},
        {"name": "Adam Zampa", "role": "Bowler", "bat_avg": 13.1, "strike_rate": 83.1, "bowl_avg": 28.5, "economy": 5.5, "rating": 87},
        {"name": "Sean Abbott", "role": "All-Rounder", "bat_avg": 18.0, "strike_rate": 99.0, "bowl_avg": 35.4, "economy": 5.9, "rating": 78},
        {"name": "Marcus Stoinis", "role": "All-Rounder", "bat_avg": 27.4, "strike_rate": 96.0, "bowl_avg": 43.0, "economy": 6.0, "rating": 79},
    ],
    "Pakistan": [
        {"name": "Fakhar Zaman", "role": "Batter", "bat_avg": 46.1, "strike_rate": 93.1, "bowl_avg": 0.0, "economy": 0.0, "rating": 88},
        {"name": "Imam-ul-Haq", "role": "Batter", "bat_avg": 49.2, "strike_rate": 83.0, "bowl_avg": 0.0, "economy": 0.0, "rating": 88},
        {"name": "Babar Azam", "role": "Batter", "bat_avg": 56.8, "strike_rate": 89.8, "bowl_avg": 0.0, "economy": 0.0, "rating": 95},
        {"name": "Mohammad Rizwan", "role": "WK-Batter", "bat_avg": 40.4, "strike_rate": 89.9, "bowl_avg": 0.0, "economy": 0.0, "rating": 86},
        {"name": "Saud Shakeel", "role": "Batter", "bat_avg": 37.3, "strike_rate": 86.7, "bowl_avg": 0.0, "economy": 0.0, "rating": 80},
        {"name": "Agha Salman", "role": "All-Rounder", "bat_avg": 29.8, "strike_rate": 95.4, "bowl_avg": 44.0, "economy": 5.6, "rating": 78},
        {"name": "Shadab Khan", "role": "All-Rounder", "bat_avg": 25.1, "strike_rate": 84.5, "bowl_avg": 33.4, "economy": 5.1, "rating": 83},
        {"name": "Mohammad Nawaz", "role": "All-Rounder", "bat_avg": 24.7, "strike_rate": 85.4, "bowl_avg": 35.0, "economy": 5.1, "rating": 79},
        {"name": "Iftikhar Ahmed", "role": "All-Rounder", "bat_avg": 26.3, "strike_rate": 97.2, "bowl_avg": 41.2, "economy": 5.7, "rating": 77},
        {"name": "Shaheen Shah Afridi", "role": "Bowler", "bat_avg": 11.0, "strike_rate": 92.0, "bowl_avg": 24.0, "economy": 5.5, "rating": 91},
        {"name": "Haris Rauf", "role": "Bowler", "bat_avg": 8.1, "strike_rate": 89.0, "bowl_avg": 28.1, "economy": 6.1, "rating": 84},
        {"name": "Naseem Shah", "role": "Bowler", "bat_avg": 9.4, "strike_rate": 88.0, "bowl_avg": 29.0, "economy": 5.4, "rating": 85},
        {"name": "Mohammad Wasim Jr", "role": "Bowler", "bat_avg": 10.1, "strike_rate": 90.2, "bowl_avg": 30.8, "economy": 5.9, "rating": 80},
        {"name": "Abrar Ahmed", "role": "Bowler", "bat_avg": 8.0, "strike_rate": 85.0, "bowl_avg": 31.4, "economy": 5.3, "rating": 80},
        {"name": "Usama Mir", "role": "Bowler", "bat_avg": 7.8, "strike_rate": 84.0, "bowl_avg": 34.9, "economy": 5.7, "rating": 76},
    ],
    "South Africa": [
        {"name": "Quinton de Kock", "role": "WK-Batter", "bat_avg": 45.7, "strike_rate": 95.8, "bowl_avg": 0.0, "economy": 0.0, "rating": 91},
        {"name": "Temba Bavuma", "role": "Batter", "bat_avg": 35.2, "strike_rate": 88.3, "bowl_avg": 0.0, "economy": 0.0, "rating": 81},
        {"name": "Rassie van der Dussen", "role": "Batter", "bat_avg": 50.9, "strike_rate": 89.6, "bowl_avg": 0.0, "economy": 0.0, "rating": 92},
        {"name": "Aiden Markram", "role": "All-Rounder", "bat_avg": 38.2, "strike_rate": 97.4, "bowl_avg": 43.0, "economy": 5.8, "rating": 86},
        {"name": "Heinrich Klaasen", "role": "WK-Batter", "bat_avg": 44.8, "strike_rate": 116.0, "bowl_avg": 0.0, "economy": 0.0, "rating": 90},
        {"name": "David Miller", "role": "Batter", "bat_avg": 42.6, "strike_rate": 103.8, "bowl_avg": 0.0, "economy": 0.0, "rating": 89},
        {"name": "Tristan Stubbs", "role": "Batter", "bat_avg": 30.2, "strike_rate": 99.6, "bowl_avg": 0.0, "economy": 0.0, "rating": 78},
        {"name": "Marco Jansen", "role": "All-Rounder", "bat_avg": 21.0, "strike_rate": 108.0, "bowl_avg": 32.2, "economy": 5.9, "rating": 82},
        {"name": "Andile Phehlukwayo", "role": "All-Rounder", "bat_avg": 26.4, "strike_rate": 93.1, "bowl_avg": 37.8, "economy": 5.9, "rating": 78},
        {"name": "Keshav Maharaj", "role": "Bowler", "bat_avg": 13.1, "strike_rate": 89.0, "bowl_avg": 34.1, "economy": 4.9, "rating": 82},
        {"name": "Tabraiz Shamsi", "role": "Bowler", "bat_avg": 8.2, "strike_rate": 84.0, "bowl_avg": 35.4, "economy": 5.2, "rating": 79},
        {"name": "Kagiso Rabada", "role": "Bowler", "bat_avg": 13.5, "strike_rate": 96.0, "bowl_avg": 28.7, "economy": 5.3, "rating": 89},
        {"name": "Anrich Nortje", "role": "Bowler", "bat_avg": 10.2, "strike_rate": 92.0, "bowl_avg": 27.5, "economy": 5.4, "rating": 86},
        {"name": "Lungi Ngidi", "role": "Bowler", "bat_avg": 9.8, "strike_rate": 90.0, "bowl_avg": 31.6, "economy": 5.6, "rating": 82},
        {"name": "Gerald Coetzee", "role": "Bowler", "bat_avg": 11.0, "strike_rate": 95.0, "bowl_avg": 29.2, "economy": 5.8, "rating": 83},
    ],
    "New Zealand": [
        {"name": "Devon Conway", "role": "WK-Batter", "bat_avg": 43.9, "strike_rate": 87.3, "bowl_avg": 0.0, "economy": 0.0, "rating": 88},
        {"name": "Will Young", "role": "Batter", "bat_avg": 34.0, "strike_rate": 86.2, "bowl_avg": 0.0, "economy": 0.0, "rating": 80},
        {"name": "Kane Williamson", "role": "Batter", "bat_avg": 48.0, "strike_rate": 81.8, "bowl_avg": 0.0, "economy": 0.0, "rating": 92},
        {"name": "Rachin Ravindra", "role": "All-Rounder", "bat_avg": 41.2, "strike_rate": 93.8, "bowl_avg": 45.9, "economy": 5.3, "rating": 88},
        {"name": "Daryl Mitchell", "role": "All-Rounder", "bat_avg": 48.9, "strike_rate": 95.4, "bowl_avg": 45.5, "economy": 5.9, "rating": 90},
        {"name": "Tom Latham", "role": "WK-Batter", "bat_avg": 34.6, "strike_rate": 88.7, "bowl_avg": 0.0, "economy": 0.0, "rating": 84},
        {"name": "Glenn Phillips", "role": "All-Rounder", "bat_avg": 39.1, "strike_rate": 104.1, "bowl_avg": 46.0, "economy": 5.8, "rating": 85},
        {"name": "Mark Chapman", "role": "Batter", "bat_avg": 31.2, "strike_rate": 90.0, "bowl_avg": 0.0, "economy": 0.0, "rating": 77},
        {"name": "Mitchell Santner", "role": "All-Rounder", "bat_avg": 27.1, "strike_rate": 93.4, "bowl_avg": 36.1, "economy": 4.8, "rating": 84},
        {"name": "Matt Henry", "role": "Bowler", "bat_avg": 12.0, "strike_rate": 88.0, "bowl_avg": 25.8, "economy": 5.1, "rating": 88},
        {"name": "Trent Boult", "role": "Bowler", "bat_avg": 10.4, "strike_rate": 87.0, "bowl_avg": 24.6, "economy": 4.9, "rating": 90},
        {"name": "Lockie Ferguson", "role": "Bowler", "bat_avg": 9.9, "strike_rate": 90.0, "bowl_avg": 31.3, "economy": 5.9, "rating": 82},
        {"name": "Ish Sodhi", "role": "Bowler", "bat_avg": 8.0, "strike_rate": 84.0, "bowl_avg": 42.2, "economy": 5.6, "rating": 75},
        {"name": "Tim Southee", "role": "Bowler", "bat_avg": 11.1, "strike_rate": 88.0, "bowl_avg": 34.6, "economy": 5.8, "rating": 79},
        {"name": "Ben Sears", "role": "Bowler", "bat_avg": 8.6, "strike_rate": 85.0, "bowl_avg": 32.7, "economy": 5.9, "rating": 77},
    ],
    "England": [
        {"name": "Jonny Bairstow", "role": "Batter", "bat_avg": 44.1, "strike_rate": 104.5, "bowl_avg": 0.0, "economy": 0.0, "rating": 88},
        {"name": "Dawid Malan", "role": "Batter", "bat_avg": 54.1, "strike_rate": 96.8, "bowl_avg": 0.0, "economy": 0.0, "rating": 90},
        {"name": "Joe Root", "role": "Batter", "bat_avg": 48.2, "strike_rate": 86.8, "bowl_avg": 0.0, "economy": 0.0, "rating": 91},
        {"name": "Ben Stokes", "role": "All-Rounder", "bat_avg": 39.8, "strike_rate": 95.1, "bowl_avg": 41.0, "economy": 6.0, "rating": 90},
        {"name": "Jos Buttler", "role": "WK-Batter", "bat_avg": 40.5, "strike_rate": 117.5, "bowl_avg": 0.0, "economy": 0.0, "rating": 90},
        {"name": "Harry Brook", "role": "Batter", "bat_avg": 35.4, "strike_rate": 96.4, "bowl_avg": 0.0, "economy": 0.0, "rating": 84},
        {"name": "Liam Livingstone", "role": "All-Rounder", "bat_avg": 28.0, "strike_rate": 105.0, "bowl_avg": 41.5, "economy": 5.9, "rating": 81},
        {"name": "Moeen Ali", "role": "All-Rounder", "bat_avg": 24.8, "strike_rate": 101.0, "bowl_avg": 48.2, "economy": 5.3, "rating": 79},
        {"name": "Sam Curran", "role": "All-Rounder", "bat_avg": 24.4, "strike_rate": 98.5, "bowl_avg": 35.7, "economy": 5.8, "rating": 82},
        {"name": "Chris Woakes", "role": "All-Rounder", "bat_avg": 26.5, "strike_rate": 95.2, "bowl_avg": 30.1, "economy": 5.6, "rating": 84},
        {"name": "Adil Rashid", "role": "Bowler", "bat_avg": 17.0, "strike_rate": 86.0, "bowl_avg": 33.4, "economy": 5.6, "rating": 85},
        {"name": "Mark Wood", "role": "Bowler", "bat_avg": 10.0, "strike_rate": 91.0, "bowl_avg": 35.1, "economy": 5.6, "rating": 82},
        {"name": "Jofra Archer", "role": "Bowler", "bat_avg": 12.1, "strike_rate": 90.0, "bowl_avg": 24.3, "economy": 4.8, "rating": 89},
        {"name": "Reece Topley", "role": "Bowler", "bat_avg": 8.8, "strike_rate": 84.0, "bowl_avg": 30.9, "economy": 5.5, "rating": 80},
        {"name": "Gus Atkinson", "role": "Bowler", "bat_avg": 10.2, "strike_rate": 88.0, "bowl_avg": 29.6, "economy": 5.4, "rating": 81},
    ],
    "Sri Lanka": [
        {"name": "Pathum Nissanka", "role": "Batter", "bat_avg": 43.0, "strike_rate": 86.0, "bowl_avg": 0.0, "economy": 0.0, "rating": 86},
        {"name": "Kusal Mendis", "role": "WK-Batter", "bat_avg": 34.2, "strike_rate": 87.8, "bowl_avg": 0.0, "economy": 0.0, "rating": 82},
        {"name": "Sadeera Samarawickrama", "role": "WK-Batter", "bat_avg": 36.8, "strike_rate": 91.2, "bowl_avg": 0.0, "economy": 0.0, "rating": 81},
        {"name": "Charith Asalanka", "role": "All-Rounder", "bat_avg": 38.1, "strike_rate": 90.5, "bowl_avg": 47.0, "economy": 5.7, "rating": 84},
        {"name": "Dhananjaya de Silva", "role": "All-Rounder", "bat_avg": 35.6, "strike_rate": 84.7, "bowl_avg": 39.1, "economy": 5.2, "rating": 83},
        {"name": "Sahan Arachchige", "role": "All-Rounder", "bat_avg": 28.5, "strike_rate": 87.0, "bowl_avg": 44.5, "economy": 5.6, "rating": 76},
        {"name": "Wanindu Hasaranga", "role": "All-Rounder", "bat_avg": 24.2, "strike_rate": 94.0, "bowl_avg": 31.1, "economy": 5.2, "rating": 86},
        {"name": "Dunith Wellalage", "role": "All-Rounder", "bat_avg": 27.4, "strike_rate": 90.3, "bowl_avg": 33.9, "economy": 4.9, "rating": 82},
        {"name": "Dasun Shanaka", "role": "All-Rounder", "bat_avg": 23.8, "strike_rate": 101.0, "bowl_avg": 45.0, "economy": 6.1, "rating": 78},
        {"name": "Maheesh Theekshana", "role": "Bowler", "bat_avg": 9.6, "strike_rate": 82.0, "bowl_avg": 29.8, "economy": 4.8, "rating": 84},
        {"name": "Dilshan Madushanka", "role": "Bowler", "bat_avg": 8.1, "strike_rate": 80.0, "bowl_avg": 30.2, "economy": 5.7, "rating": 83},
        {"name": "Matheesha Pathirana", "role": "Bowler", "bat_avg": 7.4, "strike_rate": 79.0, "bowl_avg": 31.0, "economy": 6.0, "rating": 81},
        {"name": "Dushmantha Chameera", "role": "Bowler", "bat_avg": 8.0, "strike_rate": 81.0, "bowl_avg": 34.0, "economy": 5.9, "rating": 80},
        {"name": "Pramod Madushan", "role": "Bowler", "bat_avg": 7.2, "strike_rate": 78.0, "bowl_avg": 35.2, "economy": 5.8, "rating": 77},
        {"name": "Kasun Rajitha", "role": "Bowler", "bat_avg": 8.4, "strike_rate": 82.0, "bowl_avg": 33.4, "economy": 5.6, "rating": 79},
    ],
    "Bangladesh": [
        {"name": "Litton Das", "role": "WK-Batter", "bat_avg": 35.2, "strike_rate": 86.4, "bowl_avg": 0.0, "economy": 0.0, "rating": 82},
        {"name": "Tanzid Hasan", "role": "Batter", "bat_avg": 30.0, "strike_rate": 88.1, "bowl_avg": 0.0, "economy": 0.0, "rating": 76},
        {"name": "Najmul Hossain Shanto", "role": "Batter", "bat_avg": 34.5, "strike_rate": 83.3, "bowl_avg": 0.0, "economy": 0.0, "rating": 80},
        {"name": "Mushfiqur Rahim", "role": "WK-Batter", "bat_avg": 37.9, "strike_rate": 80.1, "bowl_avg": 0.0, "economy": 0.0, "rating": 84},
        {"name": "Towhid Hridoy", "role": "Batter", "bat_avg": 33.3, "strike_rate": 92.1, "bowl_avg": 0.0, "economy": 0.0, "rating": 79},
        {"name": "Mahmudullah", "role": "All-Rounder", "bat_avg": 36.8, "strike_rate": 77.9, "bowl_avg": 45.4, "economy": 5.3, "rating": 82},
        {"name": "Shakib Al Hasan", "role": "All-Rounder", "bat_avg": 37.6, "strike_rate": 82.5, "bowl_avg": 29.7, "economy": 4.4, "rating": 91},
        {"name": "Mehidy Hasan Miraz", "role": "All-Rounder", "bat_avg": 25.5, "strike_rate": 82.0, "bowl_avg": 37.8, "economy": 4.9, "rating": 84},
        {"name": "Soumya Sarkar", "role": "All-Rounder", "bat_avg": 27.4, "strike_rate": 93.0, "bowl_avg": 45.2, "economy": 5.7, "rating": 76},
        {"name": "Taskin Ahmed", "role": "Bowler", "bat_avg": 10.4, "strike_rate": 84.0, "bowl_avg": 31.5, "economy": 5.6, "rating": 83},
        {"name": "Mustafizur Rahman", "role": "Bowler", "bat_avg": 8.2, "strike_rate": 80.0, "bowl_avg": 28.9, "economy": 5.4, "rating": 86},
        {"name": "Shoriful Islam", "role": "Bowler", "bat_avg": 7.7, "strike_rate": 79.0, "bowl_avg": 33.2, "economy": 5.8, "rating": 79},
        {"name": "Hasan Mahmud", "role": "Bowler", "bat_avg": 7.9, "strike_rate": 82.0, "bowl_avg": 34.8, "economy": 5.9, "rating": 78},
        {"name": "Nasum Ahmed", "role": "Bowler", "bat_avg": 8.0, "strike_rate": 79.0, "bowl_avg": 35.0, "economy": 5.5, "rating": 77},
        {"name": "Tanzim Hasan Sakib", "role": "Bowler", "bat_avg": 7.4, "strike_rate": 81.0, "bowl_avg": 33.9, "economy": 5.7, "rating": 78},
    ],
    "Afghanistan": [
        {"name": "Rahmanullah Gurbaz", "role": "WK-Batter", "bat_avg": 34.9, "strike_rate": 89.6, "bowl_avg": 0.0, "economy": 0.0, "rating": 83},
        {"name": "Ibrahim Zadran", "role": "Batter", "bat_avg": 46.5, "strike_rate": 83.5, "bowl_avg": 0.0, "economy": 0.0, "rating": 88},
        {"name": "Rahmat Shah", "role": "Batter", "bat_avg": 36.3, "strike_rate": 74.4, "bowl_avg": 0.0, "economy": 0.0, "rating": 80},
        {"name": "Hashmatullah Shahidi", "role": "Batter", "bat_avg": 39.7, "strike_rate": 71.3, "bowl_avg": 0.0, "economy": 0.0, "rating": 81},
        {"name": "Azmatullah Omarzai", "role": "All-Rounder", "bat_avg": 37.2, "strike_rate": 97.0, "bowl_avg": 34.2, "economy": 5.4, "rating": 86},
        {"name": "Najibullah Zadran", "role": "Batter", "bat_avg": 30.3, "strike_rate": 96.5, "bowl_avg": 0.0, "economy": 0.0, "rating": 78},
        {"name": "Mohammad Nabi", "role": "All-Rounder", "bat_avg": 27.1, "strike_rate": 88.2, "bowl_avg": 33.1, "economy": 4.8, "rating": 86},
        {"name": "Gulbadin Naib", "role": "All-Rounder", "bat_avg": 24.7, "strike_rate": 88.9, "bowl_avg": 35.8, "economy": 5.5, "rating": 80},
        {"name": "Rashid Khan", "role": "Bowler", "bat_avg": 18.2, "strike_rate": 100.2, "bowl_avg": 20.3, "economy": 4.2, "rating": 95},
        {"name": "Mujeeb Ur Rahman", "role": "Bowler", "bat_avg": 9.1, "strike_rate": 78.0, "bowl_avg": 26.8, "economy": 4.6, "rating": 87},
        {"name": "Naveen-ul-Haq", "role": "Bowler", "bat_avg": 8.3, "strike_rate": 80.0, "bowl_avg": 31.0, "economy": 5.5, "rating": 82},
        {"name": "Fazalhaq Farooqi", "role": "Bowler", "bat_avg": 7.9, "strike_rate": 77.0, "bowl_avg": 30.5, "economy": 5.3, "rating": 83},
        {"name": "Noor Ahmad", "role": "Bowler", "bat_avg": 7.0, "strike_rate": 74.0, "bowl_avg": 31.4, "economy": 4.9, "rating": 80},
        {"name": "Fareed Ahmad", "role": "Bowler", "bat_avg": 7.1, "strike_rate": 76.0, "bowl_avg": 33.6, "economy": 5.7, "rating": 78},
        {"name": "Ikram Alikhil", "role": "WK-Batter", "bat_avg": 24.4, "strike_rate": 76.0, "bowl_avg": 0.0, "economy": 0.0, "rating": 74},
    ],
    "West Indies": [
        {"name": "Shai Hope", "role": "WK-Batter", "bat_avg": 49.4, "strike_rate": 78.2, "bowl_avg": 0.0, "economy": 0.0, "rating": 89},
        {"name": "Brandon King", "role": "Batter", "bat_avg": 33.6, "strike_rate": 82.0, "bowl_avg": 0.0, "economy": 0.0, "rating": 79},
        {"name": "Kjorn Ottley", "role": "Batter", "bat_avg": 27.3, "strike_rate": 74.0, "bowl_avg": 0.0, "economy": 0.0, "rating": 73},
        {"name": "Nicholas Pooran", "role": "WK-Batter", "bat_avg": 35.6, "strike_rate": 100.4, "bowl_avg": 0.0, "economy": 0.0, "rating": 84},
        {"name": "Shimron Hetmyer", "role": "Batter", "bat_avg": 34.8, "strike_rate": 93.6, "bowl_avg": 0.0, "economy": 0.0, "rating": 82},
        {"name": "Rovman Powell", "role": "All-Rounder", "bat_avg": 24.2, "strike_rate": 92.1, "bowl_avg": 42.2, "economy": 6.1, "rating": 77},
        {"name": "Sherfane Rutherford", "role": "Batter", "bat_avg": 29.5, "strike_rate": 96.2, "bowl_avg": 0.0, "economy": 0.0, "rating": 76},
        {"name": "Jason Holder", "role": "All-Rounder", "bat_avg": 26.3, "strike_rate": 89.1, "bowl_avg": 36.8, "economy": 5.6, "rating": 84},
        {"name": "Romario Shepherd", "role": "All-Rounder", "bat_avg": 20.0, "strike_rate": 103.0, "bowl_avg": 38.0, "economy": 6.2, "rating": 78},
        {"name": "Gudakesh Motie", "role": "All-Rounder", "bat_avg": 17.4, "strike_rate": 80.0, "bowl_avg": 32.1, "economy": 4.9, "rating": 80},
        {"name": "Akeal Hosein", "role": "Bowler", "bat_avg": 13.2, "strike_rate": 76.0, "bowl_avg": 30.4, "economy": 4.8, "rating": 82},
        {"name": "Alzarri Joseph", "role": "Bowler", "bat_avg": 9.8, "strike_rate": 86.0, "bowl_avg": 31.5, "economy": 5.7, "rating": 84},
        {"name": "Shamar Joseph", "role": "Bowler", "bat_avg": 8.7, "strike_rate": 85.0, "bowl_avg": 32.0, "economy": 5.8, "rating": 80},
        {"name": "Jayden Seales", "role": "Bowler", "bat_avg": 8.2, "strike_rate": 83.0, "bowl_avg": 33.4, "economy": 5.6, "rating": 79},
        {"name": "Keemo Paul", "role": "All-Rounder", "bat_avg": 18.8, "strike_rate": 88.0, "bowl_avg": 36.7, "economy": 5.9, "rating": 76},
    ],
}


def _to_t20_player(player: dict, rating_shift: int = 0) -> dict:
    p = deepcopy(player)
    p["bat_avg"] = round(p["bat_avg"] * 0.64, 1) if p["bat_avg"] else 0.0
    p["strike_rate"] = round((p["strike_rate"] * 1.35) if p["strike_rate"] else 0.0, 1)
    p["bowl_avg"] = round((p["bowl_avg"] * 0.82) if p["bowl_avg"] else 0.0, 1)
    p["economy"] = round((p["economy"] * 1.33) if p["economy"] else 0.0, 1)
    p["rating"] = max(60, min(98, p["rating"] + rating_shift))
    return p


def _replacement(name: str, role: str, bat_avg: float, strike_rate: float, bowl_avg: float, economy: float, rating: int) -> dict:
    return {
        "name": name,
        "role": role,
        "bat_avg": bat_avg,
        "strike_rate": strike_rate,
        "bowl_avg": bowl_avg,
        "economy": economy,
        "rating": rating,
    }


def build_t20_squads() -> dict[str, list[dict]]:
    transformed = {team: [_to_t20_player(player) for player in players] for team, players in ODI_SQUADS.items()}

    swaps: dict[str, dict[str, list[dict]]] = {
        "India": {
            "remove": ["Rohit Sharma", "Mohammed Shami", "Shreyas Iyer"],
            "add": [
                _replacement("Suryakumar Yadav", "Batter", 44.2, 171.6, 0.0, 0.0, 92),
                _replacement("Ruturaj Gaikwad", "Batter", 38.1, 141.8, 0.0, 0.0, 84),
                _replacement("Tilak Varma", "Batter", 33.9, 146.7, 0.0, 0.0, 82),
            ],
        },
        "Australia": {
            "remove": ["Steve Smith", "Marnus Labuschagne", "Alex Carey"],
            "add": [
                _replacement("Tim David", "Batter", 24.7, 161.4, 0.0, 0.0, 80),
                _replacement("Jake Fraser-McGurk", "Batter", 27.3, 158.1, 0.0, 0.0, 79),
                _replacement("Nathan Ellis", "Bowler", 8.8, 90.0, 21.5, 8.1, 81),
            ],
        },
        "Pakistan": {
            "remove": ["Imam-ul-Haq", "Saud Shakeel", "Usama Mir"],
            "add": [
                _replacement("Saim Ayub", "Batter", 25.9, 135.8, 0.0, 0.0, 77),
                _replacement("Mohammad Haris", "WK-Batter", 24.4, 138.9, 0.0, 0.0, 76),
                _replacement("Mohammad Amir", "Bowler", 9.2, 99.1, 21.6, 7.1, 86),
            ],
        },
        "England": {
            "remove": ["Joe Root", "Dawid Malan", "Ben Stokes"],
            "add": [
                _replacement("Phil Salt", "WK-Batter", 31.5, 161.0, 0.0, 0.0, 89),
                _replacement("Will Jacks", "All-Rounder", 29.1, 153.4, 29.8, 7.7, 84),
                _replacement("Rehan Ahmed", "Bowler", 11.0, 102.0, 24.0, 7.4, 79),
            ],
        },
        "New Zealand": {
            "remove": ["Will Young", "Tim Southee", "Tom Latham"],
            "add": [
                _replacement("Finn Allen", "Batter", 24.7, 158.6, 0.0, 0.0, 82),
                _replacement("James Neesham", "All-Rounder", 22.0, 143.0, 27.9, 8.5, 81),
                _replacement("Michael Bracewell", "All-Rounder", 20.5, 138.0, 29.4, 7.5, 80),
            ],
        },
        "South Africa": {
            "remove": ["Temba Bavuma", "Andile Phehlukwayo", "Tabraiz Shamsi"],
            "add": [
                _replacement("Reeza Hendricks", "Batter", 29.3, 131.8, 0.0, 0.0, 80),
                _replacement("Donovan Ferreira", "WK-Batter", 25.6, 149.3, 0.0, 0.0, 78),
                _replacement("Nandre Burger", "Bowler", 7.8, 90.0, 24.9, 8.2, 80),
            ],
        },
        "Sri Lanka": {
            "remove": ["Sahan Arachchige", "Pramod Madushan", "Kasun Rajitha"],
            "add": [
                _replacement("Bhanuka Rajapaksa", "Batter", 27.0, 138.2, 0.0, 0.0, 78),
                _replacement("Kamindu Mendis", "All-Rounder", 26.0, 136.4, 28.3, 7.4, 81),
                _replacement("Nuwan Thushara", "Bowler", 7.0, 86.0, 24.8, 7.9, 80),
            ],
        },
        "Bangladesh": {
            "remove": ["Mushfiqur Rahim", "Mahmudullah", "Nasum Ahmed"],
            "add": [
                _replacement("Jaker Ali", "WK-Batter", 24.3, 136.2, 0.0, 0.0, 76),
                _replacement("Afif Hossain", "All-Rounder", 22.2, 130.0, 32.1, 7.6, 78),
                _replacement("Rishad Hossain", "Bowler", 8.0, 94.0, 23.3, 7.3, 79),
            ],
        },
        "Afghanistan": {
            "remove": ["Rahmat Shah", "Hashmatullah Shahidi", "Ikram Alikhil"],
            "add": [
                _replacement("Hazratullah Zazai", "Batter", 23.0, 143.0, 0.0, 0.0, 77),
                _replacement("Karim Janat", "All-Rounder", 21.5, 137.3, 29.8, 7.8, 79),
                _replacement("Qais Ahmad", "Bowler", 7.4, 88.0, 24.8, 7.4, 78),
            ],
        },
        "West Indies": {
            "remove": ["Kjorn Ottley", "Shai Hope", "Keemo Paul"],
            "add": [
                _replacement("Nicholas Pooran", "WK-Batter", 30.5, 145.2, 0.0, 0.0, 88),
                _replacement("Andre Russell", "All-Rounder", 24.1, 163.0, 25.4, 8.5, 90),
                _replacement("Akeal Hosein", "Bowler", 13.0, 102.0, 24.2, 6.8, 84),
            ],
        },
    }

    for team, config in swaps.items():
        base = [p for p in transformed[team] if p["name"] not in config["remove"]]
        base.extend(config["add"])
        transformed[team] = base[:15]

    return transformed


T20_SQUADS = build_t20_squads()

TEAM_DATA = {
    t["name"]: {
        "flag": t["flag"],
        "flag_img": t.get("flag_img"),
        "squads": {
            "odi": ODI_SQUADS[t["name"]],
            "t20": T20_SQUADS[t["name"]],
        },
    }
    for t in TOP_ODI_TEAMS
}

TEAM_RECENT_FORM = {
    "India": {"odi": "W W W L W", "t20": "W W L W W"},
    "Australia": {"odi": "W L W W W", "t20": "L W W W L"},
    "Pakistan": {"odi": "L W W L W", "t20": "W L W L W"},
    "South Africa": {"odi": "W W L W L", "t20": "W W W L L"},
    "New Zealand": {"odi": "L W L W W", "t20": "W L W W L"},
    "England": {"odi": "L L W W L", "t20": "W W L L W"},
    "Sri Lanka": {"odi": "W L W L W", "t20": "L W W L W"},
    "Bangladesh": {"odi": "L W L L W", "t20": "W L L W L"},
    "Afghanistan": {"odi": "W W L W L", "t20": "W W W L W"},
    "West Indies": {"odi": "L W W L L", "t20": "W L W W W"},
}

# Symmetric pair key is sorted tuple: (team_a, team_b)
H2H_DATA = {
    ("Australia", "India"): {"odi": {"Australia": 83, "India": 57}, "t20": {"Australia": 11, "India": 20}},
    ("England", "India"): {"odi": {"England": 44, "India": 58}, "t20": {"England": 11, "India": 13}},
    ("India", "Pakistan"): {"odi": {"India": 58, "Pakistan": 73}, "t20": {"India": 10, "Pakistan": 3}},
    ("Australia", "Pakistan"): {"odi": {"Australia": 70, "Pakistan": 34}, "t20": {"Australia": 12, "Pakistan": 13}},
    ("England", "Pakistan"): {"odi": {"England": 56, "Pakistan": 33}, "t20": {"England": 21, "Pakistan": 9}},
    ("Australia", "England"): {"odi": {"Australia": 88, "England": 64}, "t20": {"Australia": 11, "England": 12}},
    ("New Zealand", "South Africa"): {"odi": {"New Zealand": 26, "South Africa": 42}, "t20": {"New Zealand": 5, "South Africa": 11}},
    ("South Africa", "West Indies"): {"odi": {"South Africa": 32, "West Indies": 15}, "t20": {"South Africa": 12, "West Indies": 7}},
    ("Bangladesh", "Sri Lanka"): {"odi": {"Bangladesh": 12, "Sri Lanka": 43}, "t20": {"Bangladesh": 5, "Sri Lanka": 11}},
    ("Afghanistan", "Pakistan"): {"odi": {"Afghanistan": 1, "Pakistan": 8}, "t20": {"Afghanistan": 2, "Pakistan": 6}},
}
