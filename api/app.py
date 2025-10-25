from flask import Flask, request, jsonify
from flask_cors import CORS
import math

app = Flask(__name__)
CORS(app)

# --- DLS Data ---
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

# --- Expanded Venue List ---
VENUES = [
    # India
    { "name": 'Wankhede Stadium', "avgScore": 175 },
    { "name": 'Eden Gardens', "avgScore": 165 },
    { "name": 'M. Chinnaswamy Stadium', "avgScore": 180 },
    { "name": 'Arun Jaitley Stadium', "avgScore": 170 },
    { "name": 'MA Chidambaram Stadium', "avgScore": 160 },
    { "name": 'Narendra Modi Stadium', "avgScore": 172 },
    { "name": 'HPCA Stadium', "avgScore": 168 },
    { "name": 'Rajiv Gandhi Intl. Stadium', "avgScore": 170 },
    { "name": 'Punjab Cricket Association IS Bindra Stadium', "avgScore": 174 },
    { "name": 'Holkar Cricket Stadium', "avgScore": 177 },
    # Australia
    { "name": 'Melbourne Cricket Ground', "avgScore": 170 },
    { "name": 'Sydney Cricket Ground', "avgScore": 168 },
    { "name": 'Adelaide Oval', "avgScore": 172 },
    { "name": 'Perth Stadium (Optus Stadium)', "avgScore": 165 },
    { "name": 'The Gabba', "avgScore": 170 },
    { "name": 'Bellerive Oval', "avgScore": 160 },
    # England
    { "name": 'Lord\'s', "avgScore": 165 },
    { "name": 'Old Trafford', "avgScore": 162 },
    { "name": 'The Oval', "avgScore": 168 },
    { "name": 'Edgbaston', "avgScore": 170 },
    { "name": 'Trent Bridge', "avgScore": 175 },
    { "name": 'Headingley', "avgScore": 163 },
    { "name": 'Sophia Gardens', "avgScore": 160 },
    # Pakistan/UAE
    { "name": 'Dubai International Stadium', "avgScore": 158 },
    { "name": 'Sharjah Cricket Stadium', "avgScore": 155 },
    { "name": 'Gaddafi Stadium', "avgScore": 170 },
    { "name": 'National Stadium', "avgScore": 172 },
    { "name": 'Sheikh Zayed Stadium', "avgScore": 162 },
    # South Africa
    { "name": 'The Wanderers', "avgScore": 175 },
    { "name": 'Newlands', "avgScore": 168 },
    { "name": 'Kingsmead', "avgScore": 170 },
    { "name": 'SuperSport Park', "avgScore": 178 },
    # New Zealand
    { "name": 'Eden Park', "avgScore": 178 },
    { "name": 'Basin Reserve', "avgScore": 165 },
    { "name": 'Hagley Oval', "avgScore": 168 },
    { "name": 'Sky Stadium (Wellington Regional Stadium)', "avgScore": 170 },
    # West Indies
    { "name": 'Kensington Oval', "avgScore": 172 },
    { "name": 'Queen\'s Park Oval', "avgScore": 168 },
    { "name": 'Sabina Park', "avgScore": 165 },
    { "name": 'Daren Sammy National Cricket Stadium', "avgScore": 166 },
     # Sri Lanka
    { "name": 'R. Premadasa Stadium', "avgScore": 170 },
    { "name": 'Pallekele International Stadium', "avgScore": 165 },
    { "name": 'Galle International Stadium', "avgScore": 160 }, # Known more for Tests, but include
     # Bangladesh
    { "name": 'Shere Bangla National Stadium', "avgScore": 165 },
    { "name": 'Zahur Ahmed Chowdhury Stadium', "avgScore": 162 },
]

PITCH_TYPES = [
    { 'type': 'Flat / Batting Paradise', 'impact': 0.05 }, { 'type': 'Green / Pacer Friendly', 'impact': -0.05 },
    { 'type': 'Dry / Spinner Friendly', 'impact': -0.04 }, { 'type': 'Damp / Slow & Low', 'impact': -0.06 },
    { 'type': 'Standard / Balanced', 'impact': 0 }
]

WEATHER_CONDITIONS = [
    { 'label': 'Clear & Sunny (Day)', 'impact': 0 }, { 'label': 'Overcast / Cloudy (Day)', 'impact': -0.03 },
    { 'label': 'Clear Night (No Dew)', 'impact': 0 }, { 'label': 'Night Match (Heavy Dew)', 'impact': 0.08 },
    { 'label': 'Humid Conditions', 'impact': -0.02 }, { 'label': 'Light Rain / Drizzle', 'impact': -0.05 }
]


def get_resource_percentage(overs, wickets):
    if wickets >= 10 or overs <= 0:
        return 0
    table = DLS_RESOURCES[wickets]
    keys = sorted([int(k) for k in table.keys()])
    overs_float = float(overs)
    
    # Direct match check
    overs_str = str(int(overs_float)) if overs_float == int(overs_float) else str(overs_float) # Handle whole numbers
    if overs_str in table:
      return table[overs_str]

    # Boundary checks
    if overs_float >= keys[-1]:
        return table[str(keys[-1])]
    if overs_float <= keys[0]:
        return table[str(keys[0])]

    # Interpolation
    lower_key = max(k for k in keys if k <= overs_float)
    upper_key = min(k for k in keys if k >= overs_float)

    if lower_key == upper_key: # Should not happen if boundaries are handled, but safety check
        return table[str(lower_key)]

    l_res = table[str(lower_key)]
    u_res = table[str(upper_key)]
    
    return l_res + (u_res - l_res) * (overs_float - lower_key) / (upper_key - lower_key)


def overs_to_balls(overs):
    """
    Convert overs (float or string like 10.3 meaning 10 overs and 3 balls) into total balls bowled.
    Handle floats and strings robustly.
    """
    try:
        if isinstance(overs, (int, float)):
            overs_str = str(overs)
        else:
            overs_str = str(overs)
        if '.' in overs_str:
            parts = overs_str.split('.')
            full_overs = int(parts[0])
            balls = int(parts[1])
            # if user passed something like 10.12 treat it as 10.2 (12 is invalid)
            if balls >= 6:
                # normalize e.g., 10.6 -> 11.0, 10.7 -> 11.1 etc.
                extra_overs = balls // 6
                balls = balls % 6
                full_overs += extra_overs
            return full_overs * 6 + balls
        else:
            return int(float(overs)) * 6
    except Exception:
        # fallback conservative
        return 0


@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({"status": "ok"})


@app.route('/api/predict_score', methods=['POST'])
def predict_score():
    """
    Returns a dictionary containing:
      - realistic_avg, realistic_low, realistic_high
      - usual_avg, usual_low, usual_high
      - For backwards compatibility we still return low/avg/high mapped to the realistic values.
    The model is heuristic: uses current scoring rate, venue average run-rate, wickets-in-hand, pitch/weather impacts.
    """
    data = request.json
    score = data.get('score', 0)
    wickets = data.get('wickets', 0)
    overs = data.get('overs', 0)
    venue_name = data.get('venue', '')

    # Basic guards
    try:
        overs_val = float(overs)
    except Exception:
        overs_val = 0.0

    if overs_val <= 0 or wickets >= 10:
        # No real projection possible - return current score as all fields
        return jsonify({'low': score, 'avg': score, 'high': score,
                        'realistic_low': score, 'realistic_avg': score, 'realistic_high': score,
                        'usual_low': score, 'usual_avg': score, 'usual_high': score})

    # current scoring rate
    current_rate = score / overs_val if overs_val > 0 else 0.0

    remaining_overs = max(0.0, 20.0 - overs_val)
    wickets_in_hand = max(0, 10 - int(wickets))

    # Venue baseline run-rate (anchor)
    venue_data = next((v for v in VENUES if v['name'] == venue_name), None)
    venue_run_rate = (venue_data['avgScore'] / 20.0) if venue_data else 8.5  # default baseline rr

    # pitch & weather impacts
    pitch_impact = next((p['impact'] for p in PITCH_TYPES if p['type'] == data.get('pitch', 'Standard / Balanced')), 0)
    weather_impact = next((w['impact'] for w in WEATHER_CONDITIONS if w['label'] == data.get('weather', 'Clear & Sunny (Day)')), 0)

    # TEAM FORM (if front-end sends team form in request it can be used, otherwise assume neutral)
    team_form_factor = data.get('team_form_factor', 1.0)  # 1.0 neutral; >1 better; <1 worse

    # ----- Realistic projection model -----
    # Heuristics:
    #  - If many wickets in hand, slight acceleration relative to current_rate
    #  - If few wickets in hand, degrade remaining-rate towards venue baseline
    #  - Also incorporate pitch/weather and team form
    if wickets_in_hand >= 7:
        wickets_factor = 1.03  # plenty of wickets => slight acceleration possible
    elif wickets_in_hand >= 4:
        wickets_factor = 0.95  # neutral
    else:
        wickets_factor = 0.85  # few wickets => conservative finishing

    # Blend current rate and venue baseline to avoid runaway values
    blended_rate = (0.5 * current_rate) + (0.5 * venue_run_rate)

    # apply wickets and pitch/weather/form
    adjusted_rate = blended_rate * wickets_factor * (1 + pitch_impact + weather_impact) * team_form_factor

    # realistic remaining runs is remaining_overs * adjusted_rate
    realistic_remaining_runs = remaining_overs * adjusted_rate
    realistic_avg = math.ceil(score + realistic_remaining_runs)

    # realistic spread
    realistic_low = math.ceil(realistic_avg * 0.92)
    realistic_high = math.ceil(realistic_avg * 1.05)

    # ----- Usual (conservative) projection model -----
    # Usual prediction should give a more 'typical' mid-range for typical T20 behaviour:
    # - be conservative when wickets are few, slightly optimistic if batting powerplay + many wickets
    # - narrower spread than realistic (since "usual" is intended to be the safe expected range)
    if wickets_in_hand >= 7:
        usual_wicket_factor = 1.04
    elif wickets_in_hand >= 4:
        usual_wicket_factor = 0.98
    else:
        usual_wicket_factor = 0.85

    usual_blended_rate = (0.4 * current_rate) + (0.6 * venue_run_rate)
    usual_adjusted_rate = usual_blended_rate * usual_wicket_factor * (1 + pitch_impact * 0.8 + weather_impact * 0.8) * (0.95 + (team_form_factor - 1.0) * 0.5)
    usual_remaining_runs = remaining_overs * usual_adjusted_rate
    usual_avg = math.ceil(score + usual_remaining_runs)
    usual_low = math.ceil(usual_avg * 0.94)
    usual_high = math.ceil(usual_avg * 1.06)

    # Anchor to venue to avoid absurd numbers (blend in venue average more if unrealistic values occur)
    if venue_data:
        realistic_avg = int(round((realistic_avg * 0.75) + (venue_data['avgScore'] * 0.25)))
        realistic_low = int(round(realistic_low * 0.85 + venue_data['avgScore'] * 0.15))
        realistic_high = int(round(realistic_high * 0.95 + venue_data['avgScore'] * 0.05))

        usual_avg = int(round((usual_avg * 0.8) + (venue_data['avgScore'] * 0.2)))
        usual_low = int(round(usual_low * 0.9 + venue_data['avgScore'] * 0.1))
        usual_high = int(round(usual_high * 0.98 + venue_data['avgScore'] * 0.02))

    # sanity clamps (T20 realistic bounds)
    def clamp_t20(v):
        return max(60, min(300, int(v)))

    realistic_low = clamp_t20(realistic_low)
    realistic_avg = clamp_t20(realistic_avg)
    realistic_high = clamp_t20(realistic_high)
    usual_low = clamp_t20(usual_low)
    usual_avg = clamp_t20(usual_avg)
    usual_high = clamp_t20(usual_high)

    # Return both sets. For backward compatibility low/avg/high map to realistic.
    return jsonify({
        'low': realistic_low,
        'avg': realistic_avg,
        'high': realistic_high,
        'realistic_low': realistic_low,
        'realistic_avg': realistic_avg,
        'realistic_high': realistic_high,
        'usual_low': usual_low,
        'usual_avg': usual_avg,
        'usual_high': usual_high
    })


@app.route('/api/win_probability', methods=['POST'])
def win_probability():
    """
    Returns a smoothed, more realistic win probability for the chasing side based on:
      - runs needed, balls left, current run rate, required run rate,
      - wickets in hand, pitch and weather impacts,
      - and a smooth weighting that avoids frequent 99% or 1% outputs unless game truly decided.
    """
    data = request.json
    target = data.get('target', 0)
    score = data.get('score', 0)
    wickets = int(data.get('wickets', 0))
    overs = data.get('overs', 0)
    pitch = data.get('pitch', 'Standard / Balanced')
    weather = data.get('weather', 'Clear & Sunny (Day)')

    balls_bowled = overs_to_balls(overs)
    total_balls = 20 * 6
    balls_left = max(0, total_balls - balls_bowled)
    crr = (score / (overs if overs > 0 else 1.0)) if overs > 0 else 0.0

    # immediate conclusions
    runs_needed = max(0, int(target - score))
    if runs_needed <= 0:
        return jsonify({'win_prob': 100, 'rrr': 0.0, 'runs_needed': 0, 'balls_left': balls_left, 'crr': round(crr, 2)})

    if wickets >= 10 or balls_left <= 0:
        return jsonify({'win_prob': 0, 'rrr': float('inf'), 'runs_needed': runs_needed, 'balls_left': balls_left, 'crr': round(crr, 2)})

    # required run rate per over (rrr)
    rrr = (runs_needed / (balls_left / 6.0)) if balls_left > 0 else float('inf')

    # pitch & weather
    pitch_impact = next((p['impact'] for p in PITCH_TYPES if p['type'] == pitch), 0)
    weather_impact = next((w['impact'] for w in WEATHER_CONDITIONS if w['label'] == weather), 0)

    # wickets factor as fraction of remaining batting resources (0..1)
    wickets_factor = max(0.0, min(1.0, (10 - wickets) / 10.0))

    # momentum: positive if chasing side scoring faster than required (good), negative otherwise
    momentum = crr - rrr

    # time pressure factor: proportion of balls left (small balls_left -> higher pressure)
    time_pressure = 1.0 - (balls_left / float(total_balls))  # 0 early, towards 1 late

    # produce a baseline expectation using weighted factors, tuned heuristically
    # - start from 50 (even) and then move based on momentum, wickets, time pressure and pitch/weather.
    # - the multipliers below are tuned to avoid producing extreme 99s unless game is clearly done.
    prob = 50.0
    prob += momentum * 5.0           # momentum scaled (crr - rrr) typically in small numbers
    prob += (wickets_factor - 0.5) * 18.0   # wickets factor centered around 0.5 yields +/- scale
    prob -= (rrr - crr) * 2.5       # penalty for very high required run rates
    prob += (pitch_impact + weather_impact) * 20.0  # pitch/weather can swing probability but large impacts rare
    prob += (time_pressure - 0.5) * 6.0  # late-game time pressure moves probability slowly

    # Add small smoothing that nudges the probability towards more realistic expectation when runs_needed is small
    # or when runs_needed is massive for remaining balls.
    if runs_needed <= 12 and balls_left <= 18:
        prob += 5.0 * ( (10 - wickets) / 10.0 )  # small chases with wickets give advantage
    if rrr > 12:
        prob -= min(25.0, (rrr - 12) * 2.5)

    # If runs needed are huge (beyond typical T20 norms), clamp down for chasing side
    if runs_needed >= 160:
        prob = min(prob, 10.0)

    # Final smoothing and clamping
    prob = (prob * 0.9) + 5                     # prevents hard edges, centers average cases

    win_prob = round(max(1, min(99, prob)))

    return jsonify({
        'win_prob': win_prob,
        'rrr': round(rrr, 2) if rrr != float('inf') else float('inf'),
        'runs_needed': runs_needed,
        'balls_left': balls_left,
        'crr': round(crr, 2)
    })


@app.route('/api/dls_calculate', methods=['POST'])
def dls_calculate():
    data = request.json
    t1_score = data.get('team1_score', 0)
    t1_overs = data.get('team1_overs', 20)
    t2_overs = data.get('team2_overs', 0)
    t2_wickets = data.get('team2_wickets_lost', 0)

    r1 = get_resource_percentage(t1_overs, 0)
    r2 = get_resource_percentage(t2_overs, t2_wickets)
    
    if r1 == 0:
        # fallback conservative
        target = 250
    else:
        target = math.floor(t1_score * (r2 / r1)) + 1

    return jsonify({'target': target})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

