# api/app.py
# Full-featured backend for Cricket Predictor Pro
# - Returns both "realistic" and "usual" score ranges
# - Improved pitch/weather impact
# - Larger venue list
# - DLS calculator
# - Win probability that's smoothed and realistic
# - Ready for Render/Railway (reads PORT env var)
#
# Replace your existing api/app.py with this file.

from flask import Flask, request, jsonify
from flask_cors import CORS
import math
import os
import logging

# --- Setup ---
app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)


# ---------------- DLS RESOURCE TABLE ----------------
DLS_RESOURCES = [
    {"20":100,"15":85.1,"10":62.7,"5":33.5,"1":8.4},
    {"20":93.9,"15":79.8,"10":59.5,"5":32.4,"1":8.2},
    {"20":86.5,"15":73.1,"10":55.1,"5":30.7,"1":7.9},
    {"20":77.5,"15":65.1,"10":49.5,"5":28.3,"1":7.5},
    {"20":66.9,"15":56.1,"10":42.9,"5":25.1,"1":6.9},
    {"20":55.4,"15":46.4,"10":35.7,"5":21.4,"1":6.2},
    {"20":43.4,"15":36.5,"10":28.5,"5":17.5,"1":5.3},
    {"20":31.6,"15":26.8,"10":21.4,"5":13.6,"1":4.2},
    {"20":20.7,"15":17.8,"10":14.6,"5":9.6,"1":3.1},
    {"20":11.5,"15":10,"10":8.4,"5":5.8,"1":2}
]

# ---------------- VENUE LIST (expanded) ----------------
# avgScore represents an approximate typical T20 innings aggregate for the venue
VENUES = [
    # India
    { "name": 'Wankhede Stadium', "city": 'Mumbai', "country": 'India', "avgScore": 175, "pitchType": 'Flat / Batting Paradise', "boundarySize": 'Medium' },
    { "name": 'Eden Gardens', "city": 'Kolkata', "country": 'India', "avgScore": 165, "pitchType": 'Damp / Slow & Low', "boundarySize": 'Large' },
    { "name": 'M. Chinnaswamy Stadium', "city": 'Bangalore', "country": 'India', "avgScore": 180, "pitchType": 'Flat / Batting Paradise', "boundarySize": 'Small' },
    { "name": 'Arun Jaitley Stadium', "city": 'Delhi', "country": 'India', "avgScore": 170, "pitchType": 'Dry / Spinner Friendly', "boundarySize": 'Medium' },
    { "name": 'MA Chidambaram Stadium', "city": 'Chennai', "country": 'India', "avgScore": 160, "pitchType": 'Damp / Slow & Low', "boundarySize": 'Large' },
    { "name": 'Narendra Modi Stadium', "city": 'Ahmedabad', "country": 'India', "avgScore": 172, "pitchType": 'Standard / Balanced', "boundarySize": 'Large' },
    { "name": 'HPCA Stadium', "city": 'Dharamshala', "country": 'India', "avgScore": 168, "pitchType": 'Green / Pacer Friendly', "boundarySize": 'Medium' },
    { "name": 'Rajiv Gandhi Intl. Stadium', "city": 'Hyderabad', "country": 'India', "avgScore": 170, "pitchType": 'Flat / Batting Paradise', "boundarySize": 'Medium' },
    { "name": 'Punjab Cricket Association IS Bindra Stadium', "city": 'Mohali', "country": 'India', "avgScore": 174, "pitchType": 'Flat / Batting Paradise', "boundarySize": 'Medium' },
    { "name": 'Holkar Cricket Stadium', "city": 'Indore', "country": 'India', "avgScore": 177, "pitchType": 'Flat / Batting Paradise', "boundarySize": 'Medium' },
    { "name": 'Barsapara Cricket Stadium', "city": 'Guwahati', "country": 'India', "avgScore": 162, "pitchType": 'Standard / Balanced', "boundarySize": 'Large' },

    # Australia
    { "name": 'Melbourne Cricket Ground', "city": 'Melbourne', "country": 'Australia', "avgScore": 170, "pitchType": 'Standard / Balanced', "boundarySize": 'Large' },
    { "name": 'Sydney Cricket Ground', "city": 'Sydney', "country": 'Australia', "avgScore": 168, "pitchType": 'Dry / Spinner Friendly', "boundarySize": 'Large' },
    { "name": 'Adelaide Oval', "city": 'Adelaide', "country": 'Australia', "avgScore": 172, "pitchType": 'Flat / Batting Paradise', "boundarySize": 'Medium' },
    { "name": 'Perth Stadium (Optus Stadium)', "city": 'Perth', "country": 'Australia', "avgScore": 165, "pitchType": 'Green / Pacer Friendly', "boundarySize": 'Large' },
    { "name": 'The Gabba', "city": 'Brisbane', "country": 'Australia', "avgScore": 170, "pitchType": 'Green / Pacer Friendly', "boundarySize": 'Medium' },
    { "name": 'Bellerive Oval', "city": 'Hobart', "country": 'Australia', "avgScore": 160, "pitchType": 'Standard / Balanced', "boundarySize": 'Medium' },

    # England
    { "name": "Lord's", "city": 'London', "country": 'England', "avgScore": 165, "pitchType": 'Green / Pacer Friendly', "boundarySize": 'Large' },
    { "name": 'Old Trafford', "city": 'Manchester', "country": 'England', "avgScore": 162, "pitchType": 'Standard / Balanced', "boundarySize": 'Large' },
    { "name": 'The Oval', "city": 'London', "country": 'England', "avgScore": 168, "pitchType": 'Flat / Batting Paradise', "boundarySize": 'Medium' },
    { "name": 'Edgbaston', "city": 'Birmingham', "country": 'England', "avgScore": 170, "pitchType": 'Flat / Batting Paradise', "boundarySize": 'Medium' },
    { "name": 'Trent Bridge', "city": 'Nottingham', "country": 'England', "avgScore": 175, "pitchType": 'Flat / Batting Paradise', "boundarySize": 'Small' },

    # Pakistan / UAE
    { "name": 'Dubai International Stadium', "city": 'Dubai', "country": 'UAE', "avgScore": 158, "pitchType": 'Damp / Slow & Low', "boundarySize": 'Medium' },
    { "name": 'Sharjah Cricket Stadium', "city": 'Sharjah', "country": 'UAE', "avgScore": 155, "pitchType": 'Dry / Spinner Friendly', "boundarySize": 'Small' },
    { "name": 'Gaddafi Stadium', "city": 'Lahore', "country": 'Pakistan', "avgScore": 170, "pitchType": 'Flat / Batting Paradise', "boundarySize": 'Medium' },
    { "name": 'National Stadium', "city": 'Karachi', "country": 'Pakistan', "avgScore": 172, "pitchType": 'Flat / Batting Paradise', "boundarySize": 'Large' },

    # South Africa
    { "name": 'The Wanderers', "city": 'Johannesburg', "country": 'South Africa', "avgScore": 175, "pitchType": 'Flat / Batting Paradise', "boundarySize": 'Medium' },
    { "name": 'Newlands', "city": 'Cape Town', "country": 'South Africa', "avgScore": 168, "pitchType": 'Standard / Balanced', "boundarySize": 'Medium' },
    { "name": 'Kingsmead', "city": 'Durban', "country": 'South Africa', "avgScore": 170, "pitchType": 'Damp / Slow & Low', "boundarySize": 'Medium' },
    { "name": 'SuperSport Park', "city": 'Centurion', "country": 'South Africa', "avgScore": 178, "pitchType": 'Flat / Batting Paradise', "boundarySize": 'Small' },

    # New Zealand
    { "name": 'Eden Park', "city": 'Auckland', "country": 'New Zealand', "avgScore": 178, "pitchType": 'Flat / Batting Paradise', "boundarySize": 'Small' },
    { "name": 'Basin Reserve', "city": 'Wellington', "country": 'New Zealand', "avgScore": 165, "pitchType": 'Green / Pacer Friendly', "boundarySize": 'Large' },
    { "name": 'Hagley Oval', "city": 'Christchurch', "country": 'New Zealand', "avgScore": 168, "pitchType": 'Green / Pacer Friendly', "boundarySize": 'Large' },

    # West Indies
    { "name": 'Kensington Oval', "city": 'Barbados', "country": 'West Indies', "avgScore": 172, "pitchType": 'Standard / Balanced', "boundarySize": 'Medium' },
    { "name": "Queen's Park Oval", "city": 'Trinidad', "country": 'West Indies', "avgScore": 168, "pitchType": 'Dry / Spinner Friendly', "boundarySize": 'Large' },
    { "name": 'Sabina Park', "city": 'Jamaica', "country": 'West Indies', "avgScore": 165, "pitchType": 'Standard / Balanced', "boundarySize": 'Medium' },
    { "name": 'Daren Sammy National Cricket Stadium', "city": 'St Lucia', "country": 'West Indies', "avgScore": 166, "pitchType": 'Standard / Balanced', "boundarySize": 'Medium' },

    # Sri Lanka
    { "name": 'R. Premadasa Stadium', "city": 'Colombo', "country": 'Sri Lanka', "avgScore": 170, "pitchType": 'Damp / Slow & Low', "boundarySize": 'Medium' },
    { "name": 'Pallekele International Stadium', "city": 'Pallekele', "country": 'Sri Lanka', "avgScore": 165, "pitchType": 'Standard / Balanced', "boundarySize": 'Large' },
    { "name": 'Galle International Stadium', "city": 'Galle', "country": 'Sri Lanka', "avgScore": 160, "pitchType": 'Slow & Low', "boundarySize": 'Large'},

    # Bangladesh
    { "name": 'Shere Bangla National Stadium', "city": 'Dhaka', "country": 'Bangladesh', "avgScore": 165, "pitchType": 'Damp / Slow & Low', "boundarySize": 'Medium' },
    { "name": 'Zahur Ahmed Chowdhury Stadium', "city": 'Chattogram', "country": 'Bangladesh', "avgScore": 162, "pitchType": 'Standard / Balanced', "boundarySize": 'Medium' },

    # A few smaller/oddball grounds
    { "name": 'Maidan', "city": 'Example City', "country": 'Demo', "avgScore": 154, "pitchType": 'Standard / Balanced', "boundarySize": 'Large' }
]

# Ensure no duplicate names and easier lookup
_VENUE_INDEX = {v['name']: v for v in VENUES}

# ---------------- PITCH / WEATHER ----------------
PITCH_TYPES = [
    { 'type': 'Flat / Batting Paradise', 'impact': 0.08 },
    { 'type': 'Green / Pacer Friendly', 'impact': -0.07 },
    { 'type': 'Dry / Spinner Friendly', 'impact': -0.05 },
    { 'type': 'Damp / Slow & Low', 'impact': -0.09 },
    { 'type': 'Standard / Balanced', 'impact': 0 }
]

WEATHER_CONDITIONS = [
    { 'label': 'Clear & Sunny (Day)', 'impact': 0 },
    { 'label': 'Overcast / Cloudy (Day)', 'impact': -0.05 },
    { 'label': 'Clear Night (No Dew)', 'impact': 0.01 },
    { 'label': 'Night Match (Heavy Dew)', 'impact': 0.08 },
    { 'label': 'Humid Conditions', 'impact': -0.03 },
    { 'label': 'Light Rain / Drizzle', 'impact': -0.06 }
]

# ---------------- Helpers ----------------

def clamp_t20(v, lo=30, hi=300):
    try:
        iv = int(round(v))
    except:
        iv = lo
    return max(lo, min(hi, iv))

def parse_float_safe(x, default=0.0):
    try:
        return float(x)
    except:
        return default

def parse_int_safe(x, default=0):
    try:
        return int(x)
    except:
        try:
            return int(float(x))
        except:
            return default

def overs_to_balls(overs):
    """
    Convert overs representation (float or string like 10.3 meaning 10 overs and 3 balls) to number of balls.
    Accepts:
      - 10 -> 60
      - 10.3 -> 63
      - "10.3" -> 63
      - 10.0 -> 60
    """
    try:
        if overs is None:
            return 0
        s = str(overs).strip()
        if '.' in s:
            a,b = s.split('.')
            full = int(a)
            balls = int(b)
            # normalize any weird input where someone sends 10.12 -> treat as 10.2 (i.e. 10 overs and 2 balls)
            if balls >= 6:
                extra = balls // 6
                balls = balls % 6
                full += extra
            return full*6 + balls
        else:
            return int(float(s))*6
    except Exception:
        return 0

def get_resource_percentage(overs, wickets):
    """Interpolate DLS resource percentage table"""
    try:
        if wickets >= 10 or parse_float_safe(overs) <= 0:
            return 0
        widx = int(wickets)
        table = DLS_RESOURCES[widx]
        # keys in table are strings like "20","15"
        keys = sorted([int(k) for k in table.keys()])
        overs_float = float(overs)
        # if exact exists
        for k in keys:
            if abs(overs_float - k) < 1e-6:
                return table[str(k)]
        # clamp
        if overs_float >= keys[-1]:
            return table[str(keys[-1])]
        if overs_float <= keys[0]:
            return table[str(keys[0])]
        # interpolate
        lower = max(k for k in keys if k <= overs_float)
        upper = min(k for k in keys if k >= overs_float)
        if lower == upper:
            return table[str(lower)]
        lval = table[str(lower)]
        uval = table[str(upper)]
        pct = lval + (uval - lval) * (overs_float - lower) / (upper - lower)
        return pct
    except Exception:
        return 0

# ---------------- API Endpoints ----------------

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({"status": "ok"})

@app.route('/api/venues', methods=['GET'])
def list_venues():
    # simple list for frontend to populate dropdowns
    simplified = [{ 'name': v['name'], 'city': v.get('city',''), 'country': v.get('country',''), 'avgScore': v.get('avgScore',0) } for v in VENUES]
    return jsonify({'venues': simplified})

@app.route('/api/predict_score', methods=['POST'])
def predict_score():
    """
    Returns both 'realistic' and 'usual' score ranges plus legacy low/avg/high mapped to realistic.
    Input JSON expected keys:
      - score (int)
      - wickets (int)
      - overs (float or string like 10.3)
      - venue (string)
      - pitch (string) optional
      - weather (string) optional
      - team_form_factor (float, optional) default 1.0 (1.05 is slightly better)
    """
    data = request.json or {}
    score = parse_int_safe(data.get('score', 0), 0)
    wickets = parse_int_safe(data.get('wickets', 0), 0)
    overs_raw = data.get('overs', 0)
    overs_val = parse_float_safe(overs_raw, 0.0)
    venue_name = data.get('venue', '') or ''
    pitch = data.get('pitch', 'Standard / Balanced') or 'Standard / Balanced'
    weather = data.get('weather', 'Clear & Sunny (Day)') or 'Clear & Sunny (Day)'
    team_form_factor = float(data.get('team_form_factor', 1.0) or 1.0)

    # Basic guardrails
    if overs_val <= 0 or wickets >= 10:
        # not enough info to project, return current as all outputs
        out = {
            'low': score, 'avg': score, 'high': score,
            'realistic_low': score, 'realistic_avg': score, 'realistic_high': score,
            'usual_low': score, 'usual_avg': score, 'usual_high': score
        }
        return jsonify(out)

    # derived values
    remaining_overs = max(0.0, 20.0 - overs_val)
    wickets_in_hand = max(0, 10 - int(wickets))
    current_rate = score / overs_val if overs_val > 0 else 0.0

    # venue baseline anchor
    venue_data = _VENUE_INDEX.get(venue_name)
    venue_avg_score = venue_data['avgScore'] if venue_data else 168  # reasonable default
    venue_rr = venue_avg_score / 20.0

    # pitch & weather impacts
    pitch_impact = next((p['impact'] for p in PITCH_TYPES if p['type'] == pitch), 0.0)
    weather_impact = next((w['impact'] for w in WEATHER_CONDITIONS if w['label'] == weather), 0.0)

    # ----- Realistic model -----
    # Wickets factor: more wickets => more conservative finishing
    if wickets_in_hand >= 7:
        wickets_factor_real = 1.07
    elif wickets_in_hand >= 4:
        wickets_factor_real = 1.00
    else:
        wickets_factor_real = 0.86

    # Blend current scoring rate and venue baseline to avoid runaway prediction
    blended_rate_real = (0.6 * current_rate) + (0.4 * venue_rr)

    # amplify pitch/weather slightly for realistic model
    impact_multiplier_real = 1.0 + (pitch_impact + weather_impact) * 3.0

    adjusted_rate_real = blended_rate_real * wickets_factor_real * impact_multiplier_real * team_form_factor

    realistic_remaining_runs = adjusted_rate_real * remaining_overs
    realistic_avg_raw = score + realistic_remaining_runs

    # Anchor with venue average to avoid extremes (blend)
    realistic_avg_anchored = (0.85 * realistic_avg_raw) + (0.15 * venue_avg_score)

    # realistic spread
    realistic_low = math.floor(realistic_avg_anchored * 0.90)
    realistic_avg = math.floor(realistic_avg_anchored)
    realistic_high = math.ceil(realistic_avg_anchored * 1.08)

    # ----- Usual (conservative) model -----
    if wickets_in_hand >= 7:
        wickets_factor_usual = 1.04
    elif wickets_in_hand >= 4:
        wickets_factor_usual = 0.98
    else:
        wickets_factor_usual = 0.85

    blended_rate_usual = (0.5 * current_rate) + (0.5 * venue_rr)
    impact_multiplier_usual = 1.0 + (pitch_impact + weather_impact) * 2.0
    usual_adj_rate = blended_rate_usual * wickets_factor_usual * impact_multiplier_usual * (0.97 + (team_form_factor - 1.0) * 0.4)

    usual_remaining_runs = usual_adj_rate * remaining_overs
    usual_avg_raw = score + usual_remaining_runs
    usual_avg_anchored = (0.78 * usual_avg_raw) + (0.22 * venue_avg_score)

    usual_avg = math.floor(usual_avg_anchored)
    usual_low = math.floor(usual_avg * 0.94)
    usual_high = math.ceil(usual_avg * 1.06)

    # Recompute to ensure ordering and sensible numeric rounding
    def ensure_order(lowv, midv, highv):
        a = int(lowv); b = int(midv); c = int(highv)
        arr = sorted([a,b,c])
        return arr[0], arr[1], arr[2]

    realistic_low, realistic_avg, realistic_high = ensure_order(realistic_low, realistic_avg, realistic_high)
    usual_low, usual_avg, usual_high = ensure_order(usual_low, usual_avg, usual_high)

    # clamp to reasonable T20 bounds
    realistic_low = clamp_t20(realistic_low, 30, 300)
    realistic_avg = clamp_t20(realistic_avg, 30, 300)
    realistic_high = clamp_t20(realistic_high, 30, 350)
    usual_low = clamp_t20(usual_low, 30, 300)
    usual_avg = clamp_t20(usual_avg, 30, 300)
    usual_high = clamp_t20(usual_high, 30, 300)

    # For backwards compatibility low/avg/high map to realistic set
    response = {
        'low': realistic_low,
        'avg': realistic_avg,
        'high': realistic_high,
        'realistic_low': realistic_low,
        'realistic_avg': realistic_avg,
        'realistic_high': realistic_high,
        'usual_low': usual_low,
        'usual_avg': usual_avg,
        'usual_high': usual_high,
        # helpful debug-ish details (frontend can ignore)
        'meta': {
            'score': score,
            'wickets': wickets,
            'overs': overs_val,
            'venue_avg': venue_avg_score,
            'current_rate': round(current_rate, 3),
            'adjusted_rate_real': round(adjusted_rate_real, 3),
            'adjusted_rate_usual': round(usual_adj_rate, 3),
            'pitch_impact': pitch_impact,
            'weather_impact': weather_impact
        }
    }

    return jsonify(response)


@app.route('/api/win_probability', methods=['POST'])
def win_probability():
    """
    Return a realistic, smoothed win probability for chasing side.
    Input:
      - target (int)
      - score (int)
      - wickets (int)
      - overs (float or "10.3")
      - pitch (string, optional)
      - weather (string, optional)
    Output:
      - win_prob (1..99)
      - rrr (required run rate per over)
      - runs_needed
      - balls_left
      - crr (current run rate)
    """

    data = request.json or {}
    target = parse_int_safe(data.get('target', 0), 0)
    score = parse_int_safe(data.get('score', 0), 0)
    wickets = parse_int_safe(data.get('wickets', 0), 0)
    overs_raw = data.get('overs', 0)
    overs = parse_float_safe(overs_raw, 0.0)
    pitch = data.get('pitch', 'Standard / Balanced') or 'Standard / Balanced'
    weather = data.get('weather', 'Clear & Sunny (Day)') or 'Clear & Sunny (Day)'

    # Compute balls left correctly
    balls_bowled = overs_to_balls(overs)
    total_balls = 20 * 6
    balls_left = max(0, total_balls - balls_bowled)

    # runs needed
    runs_needed = max(0, target - score)

    # immediate conclusions
    if runs_needed <= 0:
        return jsonify({'win_prob': 100, 'rrr': 0.0, 'runs_needed': 0, 'balls_left': balls_left, 'crr': round(score / (overs if overs>0 else 1),2)})

    if wickets >= 10 or balls_left <= 0:
        return jsonify({'win_prob': 0, 'rrr': float('inf'), 'runs_needed': runs_needed, 'balls_left': balls_left, 'crr': round(score / (overs if overs>0 else 1),2)})

    # required run rate (per over)
    rrr = (runs_needed / (balls_left / 6.0)) if balls_left > 0 else float('inf')

    # current run rate
    crr = (score / overs) if overs > 0 else 0.0

    # pitch & weather impact
    pitch_impact = next((p['impact'] for p in PITCH_TYPES if p['type'] == pitch), 0.0)
    weather_impact = next((w['impact'] for w in WEATHER_CONDITIONS if w['label'] == weather), 0.0)
    impact_factor = 1.0 + (pitch_impact + weather_impact)

    # wickets factor (resource remaining)
    wickets_factor = (10 - wickets) / 10.0  # 1 when 10 wickets in hand, 0 when none

    # momentum: how far ahead crr is vs rrr (positive good for chasers)
    momentum = crr - rrr

    # pressure: how late the chase is (0 early -> 1 late)
    pressure = 1.0 - (balls_left / total_balls)

    # baseline from runs and balls: if required rate is low relative to crr, advantage
    # build a combined score starting at 50 and then nudging
    prob = 50.0

    # momentum contribution: scale so typical crr-rrr swings move probability moderately
    prob += momentum * 9.0

    # wickets contribution centered around 0.5
    prob += (wickets_factor - 0.5) * 28.0

    # rrr penalty: large rrr hurts
    prob -= max(0.0, (rrr - crr)) * 4.0

    # impact of pitch/weather: amplify slightly
    prob += (impact_factor - 1.0) * 55.0

    # pressure: late in game we trust current position more (nudge away from 50 slowly)
    prob += (pressure - 0.45) * 8.0

    # small bonus for small chases with wickets
    if runs_needed <= 12 and balls_left <= 18:
        prob += 6.0 * (wickets_factor)

    # huge rrr clamp
    if rrr > 15:
        prob -= min(20.0, (rrr - 15) * 1.6)

    # if runs_needed extremely high relative to balls_left clamp to low chance
    if runs_needed >= 160:
        prob = min(prob, 12.0)

    # smoothing: prevent 1 or 99 except when nearly decided
    # but allow probabilities to reach those endpoints if game truly decided
    win_prob = round(max(1, min(99, prob)))

    # Extra smoothing logic: if the numeric differences are small, pull towards 50 slightly
    # (avoid wild 80+ swings early)
    if balls_left > 60 and abs(rrr - crr) < 1.2 and wickets >= 5 and 20 < runs_needed < 100:
        # reduce extremes early in the match
        win_prob = int(round(50 + (win_prob - 50) * 0.6))

    # final clamp
    win_prob = max(1, min(99, int(win_prob)))

    return jsonify({
        'win_prob': win_prob,
        'rrr': round(rrr, 2) if rrr != float('inf') else float('inf'),
        'runs_needed': runs_needed,
        'balls_left': balls_left,
        'crr': round(crr, 2),
        'meta': {
            'pitch_impact': pitch_impact,
            'weather_impact': weather_impact,
            'wickets_factor': round(wickets_factor,2),
            'momentum': round(momentum,3),
            'pressure': round(pressure,3)
        }
    })


@app.route('/api/dls_calculate', methods=['POST'])
def dls_calculate():
    """
    Basic DLS style calculator using our resource table.
    Input:
      - team1_score
      - team1_overs
      - team2_overs
      - team2_wickets_lost
    Response:
      - target
    """
    data = request.json or {}
    t1_score = parse_int_safe(data.get('team1_score', 0), 0)
    t1_overs = parse_float_safe(data.get('team1_overs', 20.0))
    t2_overs = parse_float_safe(data.get('team2_overs', 0.0))
    t2_wickets = parse_int_safe(data.get('team2_wickets_lost', 0), 0)

    r1 = get_resource_percentage(t1_overs, 0)
    r2 = get_resource_percentage(t2_overs, t2_wickets)
    if r1 == 0:
        # fallback conservative target
        target = max(50, t1_score)
    else:
        # formula: revised target = floor(team1_score * (r2/r1)) + 1
        try:
            target = math.floor(t1_score * (r2 / r1)) + 1
        except Exception:
            target = t1_score

    return jsonify({'target': int(target), 'meta': {'r1': r1, 'r2': r2}})


# ---------------- MAIN ----------------
if __name__ == '__main__':
    # Port must be read from environment for hosts like Render / Railway
    port = int(os.environ.get('PORT', 5000))
    debug_flag = os.environ.get('FLASK_DEBUG', 'false').lower() in ('1','true','yes')
    app.run(host='0.0.0.0', port=port, debug=debug_flag)
