from __future__ import annotations

import json
import math
import os
import re
import time
import urllib.request
import urllib.parse
from html import unescape
from urllib.parse import urlparse
from datetime import datetime, timezone, date
from typing import Any

try:
    from api.data import FORMAT_RULES, H2H_DATA, PITCH_TYPES, TEAM_DATA, TEAM_RECENT_FORM, TOP_ODI_TEAMS, VENUES, WEATHER_TYPES
except ModuleNotFoundError:
    from data import FORMAT_RULES, H2H_DATA, PITCH_TYPES, TEAM_DATA, TEAM_RECENT_FORM, TOP_ODI_TEAMS, VENUES, WEATHER_TYPES

DLS_20 = {
    0: {20: 100.0, 15: 85.1, 10: 62.7, 5: 33.5, 1: 8.4, 0: 0.0},
    1: {20: 93.9, 15: 79.8, 10: 59.5, 5: 32.4, 1: 8.2, 0: 0.0},
    2: {20: 86.9, 15: 74.1, 10: 55.0, 5: 30.7, 1: 7.8, 0: 0.0},
    3: {20: 78.1, 15: 66.3, 10: 49.0, 5: 28.3, 1: 7.4, 0: 0.0},
    4: {20: 67.3, 15: 57.3, 10: 42.5, 5: 25.1, 1: 6.8, 0: 0.0},
    5: {20: 55.6, 15: 47.1, 10: 35.5, 5: 21.4, 1: 6.1, 0: 0.0},
    6: {20: 43.3, 15: 36.1, 10: 28.6, 5: 17.5, 1: 5.2, 0: 0.0},
    7: {20: 31.4, 15: 26.0, 10: 21.1, 5: 13.5, 1: 4.1, 0: 0.0},
    8: {20: 20.6, 15: 17.5, 10: 14.1, 5: 9.4, 1: 3.0, 0: 0.0},
    9: {20: 11.4, 15: 9.8, 10: 7.9, 5: 5.5, 1: 1.8, 0: 0.0},
}

DLS_50 = {
    0: {50: 100.0, 45: 95.0, 40: 88.7, 35: 81.8, 30: 74.0, 25: 65.9, 20: 56.5, 15: 45.8, 10: 34.1, 5: 20.4, 1: 4.8, 0: 0.0},
    1: {50: 93.4, 45: 89.0, 40: 83.0, 35: 76.3, 30: 68.8, 25: 61.0, 20: 52.2, 15: 42.1, 10: 31.4, 5: 18.9, 1: 4.5, 0: 0.0},
    2: {50: 85.1, 45: 81.2, 40: 75.9, 35: 69.8, 30: 63.2, 25: 56.1, 20: 48.0, 15: 38.7, 10: 28.8, 5: 17.3, 1: 4.2, 0: 0.0},
    3: {50: 74.9, 45: 71.6, 40: 67.0, 35: 61.8, 30: 56.1, 25: 49.9, 20: 42.8, 15: 34.5, 10: 25.7, 5: 15.4, 1: 3.8, 0: 0.0},
    4: {50: 62.7, 45: 60.0, 40: 56.3, 35: 52.0, 30: 47.3, 25: 42.0, 20: 36.0, 15: 29.1, 10: 21.8, 5: 13.2, 1: 3.3, 0: 0.0},
    5: {50: 49.0, 45: 46.8, 40: 43.8, 35: 40.4, 30: 36.8, 25: 32.7, 20: 28.3, 15: 22.8, 10: 17.2, 5: 10.7, 1: 2.8, 0: 0.0},
    6: {50: 34.9, 45: 33.4, 40: 31.3, 35: 28.8, 30: 26.2, 25: 23.4, 20: 20.3, 15: 16.5, 10: 12.6, 5: 8.1, 1: 2.2, 0: 0.0},
    7: {50: 22.3, 45: 21.4, 40: 20.1, 35: 18.5, 30: 16.9, 25: 15.2, 20: 13.4, 15: 11.1, 10: 8.6, 5: 5.8, 1: 1.7, 0: 0.0},
    8: {50: 11.2, 45: 10.8, 40: 10.1, 35: 9.3, 30: 8.4, 25: 7.6, 20: 6.7, 15: 5.5, 10: 4.5, 5: 3.0, 1: 1.0, 0: 0.0},
    9: {50: 4.7, 45: 4.5, 40: 4.2, 35: 3.9, 30: 3.5, 25: 3.2, 20: 2.8, 15: 2.4, 10: 1.9, 5: 1.3, 1: 0.4, 0: 0.0},
}

DEMO_LIVE_MATCHES = [
    {
        "id": "demo_t20_1",
        "title": "India vs Australia (T20 Demo Live)",
        "format": "t20",
        "team1": "India",
        "team2": "Australia",
        "batting_team": "India",
        "bowling_team": "Australia",
        "score": 142,
        "wickets": 6,
        "overs": 18.0,
        "target": 177,
        "venue": "Lord's",
        "pitch": "Balanced surface",
        "weather": "Clear",
        "toss_winner": "India",
        "toss_decision": "bat",
        "last_updated": "Demo feed",
    },
    {
        "id": "demo_odi_1",
        "title": "England vs Pakistan (ODI Demo Live)",
        "format": "odi",
        "team1": "England",
        "team2": "Pakistan",
        "batting_team": "Pakistan",
        "bowling_team": "England",
        "score": 214,
        "wickets": 5,
        "overs": 39.3,
        "target": 301,
        "venue": "The Oval",
        "pitch": "Flat batting deck",
        "weather": "Cloudy",
        "toss_winner": "England",
        "toss_decision": "bat",
        "last_updated": "Demo feed",
    },
]

LIVE_PROVIDER_PROFILES: dict[str, dict[str, Any]] = {
    "generic": {
        "label": "Generic JSON",
        "root_paths": ["data", "match", "payload", ""],
        "fields": {
            "format": ["format", "match_format", "type"],
            "team1": ["team1", "home_team", "teams.0"],
            "team2": ["team2", "away_team", "teams.1"],
            "batting_team": ["batting_team", "innings.current.batting_team", "batting"],
            "bowling_team": ["bowling_team", "innings.current.bowling_team", "bowling"],
            "score": ["score", "runs", "innings.current.runs", "batting_score"],
            "wickets": ["wickets", "wkts", "innings.current.wickets", "wickets_lost"],
            "overs": ["overs", "over", "innings.current.overs"],
            "target": ["target", "target_score", "innings.current.target", "chase_target"],
            "venue": ["venue", "ground", "match_venue"],
            "pitch": ["pitch", "pitch_type"],
            "weather": ["weather", "conditions"],
            "toss_winner": ["toss_winner"],
            "toss_decision": ["toss_decision"],
            "title": ["title", "match_title", "name"],
            "last_updated": ["last_updated", "updated_at", "timestamp"],
        },
    },
    "cricapi_like": {
        "label": "CricAPI-like",
        "root_paths": ["data", ""],
        "fields": {
            "format": ["matchType", "format"],
            "team1": ["teams.0", "teamInfo.0.name"],
            "team2": ["teams.1", "teamInfo.1.name"],
            "score": ["score.0.r", "score.0.runs", "scoreCard.0.runs"],
            "wickets": ["score.0.w", "score.0.wickets", "scoreCard.0.wickets"],
            "overs": ["score.0.o", "score.0.overs", "scoreCard.0.overs"],
            "target": ["score.1.r", "score.1.runs", "target"],
            "venue": ["venue", "venueInfo.ground"],
            "title": ["name", "matchTitle", "title"],
            "last_updated": ["dateTimeGMT", "date"],
        },
    },
    "cricapi_free": {
        "label": "CricAPI (free key)",
        "root_paths": ["data.0", "data", ""],
        "fields": {
            "format": ["matchType", "format"],
            "team1": ["teams.0", "teamInfo.0.name"],
            "team2": ["teams.1", "teamInfo.1.name"],
            "score": ["score.0.r", "score.0.runs", "scoreCard.0.runs"],
            "wickets": ["score.0.w", "score.0.wickets", "scoreCard.0.wickets"],
            "overs": ["score.0.o", "score.0.overs", "scoreCard.0.overs"],
            "target": ["score.1.r", "score.1.runs", "target"],
            "venue": ["venue", "venueInfo.ground"],
            "title": ["name", "matchTitle", "title"],
            "last_updated": ["dateTimeGMT", "date"],
        },
    },
    "espn_html": {"label": "ESPN page link (no API)", "root_paths": [""], "fields": {}},
    "cricbuzz_html": {"label": "Cricbuzz page link (no API)", "root_paths": [""], "fields": {}},
}

def _load_local_env(env_path: str = ".env") -> None:
    if not os.path.exists(env_path):
        return
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for raw in f:
                line = raw.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip()
                if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                    val = val[1:-1]
                if key and key not in os.environ:
                    os.environ[key] = val
    except Exception:
        # Non-fatal: app can still run with system env vars.
        return


_load_local_env()
DEFAULT_MATCH_INSIGHT_KEY = os.environ.get("MATCH_INSIGHT_API_KEY", "").strip()

TEAM_ALIASES = {
    "ind": "India",
    "india": "India",
    "aus": "Australia",
    "australia": "Australia",
    "pak": "Pakistan",
    "pakistan": "Pakistan",
    "sa": "South Africa",
    "rsa": "South Africa",
    "south africa": "South Africa",
    "nz": "New Zealand",
    "new zealand": "New Zealand",
    "eng": "England",
    "england": "England",
    "sl": "Sri Lanka",
    "sri lanka": "Sri Lanka",
    "ban": "Bangladesh",
    "bangladesh": "Bangladesh",
    "afg": "Afghanistan",
    "afghanistan": "Afghanistan",
    "wi": "West Indies",
    "west indies": "West Indies",
    "windies": "West Indies",
}


def format_key(value: Any) -> str:
    fmt = str(value or "odi").lower().strip()
    return fmt if fmt in FORMAT_RULES else "odi"


def overs_to_balls(overs: float, max_overs: int) -> int:
    if overs < 0:
        raise ValueError("Overs cannot be negative")
    whole = int(overs)
    balls = round((overs - whole) * 10)
    if balls > 5:
        raise ValueError("Invalid overs format. Use x.y where y is 0-5 balls")
    total = whole * 6 + balls
    if total > max_overs * 6:
        raise ValueError(f"Overs cannot be greater than {max_overs}")
    return total


def _interpolate(table: dict[int, float], overs_remaining: float) -> float:
    keys = sorted(table.keys())
    if overs_remaining <= keys[0]:
        return table[keys[0]]
    if overs_remaining >= keys[-1]:
        return table[keys[-1]]
    lower = max(k for k in keys if k <= overs_remaining)
    upper = min(k for k in keys if k >= overs_remaining)
    if lower == upper:
        return table[lower]
    low_val, high_val = table[lower], table[upper]
    return low_val + ((high_val - low_val) * (overs_remaining - lower) / (upper - lower))


def dls_resource_remaining(fmt: str, overs_remaining: float, wickets_lost: int) -> float:
    overs_remaining = max(0.0, overs_remaining)
    wickets = max(0, min(9, int(wickets_lost)))
    table = DLS_20 if fmt == "t20" else DLS_50
    return _interpolate(table[wickets], overs_remaining)


def get_team_players(team: str, fmt: str) -> list[dict]:
    if team not in TEAM_DATA:
        raise ValueError("Unknown team")
    return TEAM_DATA[team]["squads"][fmt]


def pick_players(players: list[dict], selected_names: list[str] | None) -> list[dict]:
    if not selected_names:
        return players[:11]
    selected_set = set(selected_names)
    chosen = [p for p in players if p["name"] in selected_set]
    if len(chosen) < 11:
        raise ValueError("Select exactly 11 players for each team")
    return chosen[:11]


def venue_average(fmt: str, venue_name: str | None) -> float:
    key = "t20_avg" if fmt == "t20" else "odi_avg"
    if venue_name:
        for venue in VENUES:
            if venue["name"] == venue_name:
                return float(venue[key])
    return FORMAT_RULES[fmt]["default_par"]


def venue_profile(venue_name: str | None) -> dict[str, Any]:
    if venue_name:
        for venue in VENUES:
            if venue["name"] == venue_name:
                return venue
    return {"pitch_type": "Standard / Balanced", "boundary_size": "Medium"}


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def team_breakdown(players: list[dict], fmt: str = "odi") -> dict[str, float]:
    bat_scores: list[float] = []
    bowl_scores: list[float] = []
    rating_scores: list[float] = []
    roles = {"Batter": 0, "WK-Batter": 0, "All-Rounder": 0, "Bowler": 0}
    bat_ref_avg = 30.0 if fmt == "t20" else 42.0
    bat_ref_sr = 140.0 if fmt == "t20" else 90.0
    bowl_ref_avg = 23.0 if fmt == "t20" else 32.0
    bowl_ref_econ = 7.6 if fmt == "t20" else 5.4

    for p in players:
        roles[p["role"]] = roles.get(p["role"], 0) + 1
        rating_scores.append(float(p["rating"]))
        if p["bat_avg"] > 0:
            bat_idx = ((p["bat_avg"] / bat_ref_avg) * 55.0) + ((p["strike_rate"] / bat_ref_sr) * 45.0)
            bat_scores.append(_clamp(bat_idx, 20.0, 140.0))
        if p["bowl_avg"] > 0 and p["economy"] > 0:
            bowl_idx = ((bowl_ref_avg / p["bowl_avg"]) * 60.0) + ((bowl_ref_econ / p["economy"]) * 40.0)
            bowl_scores.append(_clamp(bowl_idx, 20.0, 140.0))

    batting = sum(bat_scores) / max(1, len(bat_scores))
    bowling = sum(bowl_scores) / max(1, len(bowl_scores))
    rating = sum(rating_scores) / max(1, len(rating_scores))
    bowling_options = roles["Bowler"] + roles["All-Rounder"]
    batting_depth = roles["Batter"] + roles["WK-Batter"] + roles["All-Rounder"]
    wk_count = roles["WK-Batter"]
    role_balance = 100.0
    if wk_count == 0:
        role_balance -= 12.0
    if bowling_options < 5:
        role_balance -= (5 - bowling_options) * 7.0
    if batting_depth < 6:
        role_balance -= (6 - batting_depth) * 5.0
    role_balance = _clamp(role_balance, 50.0, 100.0)
    overall = (batting * 0.30) + (bowling * 0.30) + (rating * 0.25) + (role_balance * 0.15)

    return {
        "batting": round(batting, 2),
        "bowling": round(bowling, 2),
        "overall": round(_clamp(overall, 40.0, 99.0), 2),
        "role_balance": round(role_balance, 2),
        "bowling_options": bowling_options,
        "batting_depth": batting_depth,
        "roles": roles,
    }


def condition_multiplier(pitch: str | None, weather: str | None) -> float:
    pitch_impact = next((p["batting_impact"] for p in PITCH_TYPES if p["type"] == pitch), 0.0)
    weather_impact = next((w["batting_impact"] for w in WEATHER_TYPES if w["label"] == weather), 0.0)
    return 1.0 + pitch_impact + weather_impact


def toss_adjustment(fmt: str, toss_winner: str | None, toss_decision: str | None, batting_team: str | None = None, chasing_team: str | None = None) -> float:
    winner = str(toss_winner or "").strip()
    decision = str(toss_decision or "auto").strip().lower()
    if winner in {"", "Auto"}:
        return 0.0
    if decision not in {"bat", "bowl"}:
        return 0.0

    if batting_team:
        is_batting_team_winner = winner == batting_team
        if decision == "bat":
            return 0.03 if is_batting_team_winner else -0.02
        return -0.025 if is_batting_team_winner else 0.015

    if chasing_team:
        is_chasing_winner = winner == chasing_team
        if decision == "bowl":
            return 0.035 if is_chasing_winner else -0.02
        return -0.03 if is_chasing_winner else 0.015

    return 0.0


def xi_validator(players: list[dict], fmt: str) -> dict[str, Any]:
    batter_like = [p for p in players if p["role"] in {"Batter", "WK-Batter", "All-Rounder"}]
    opener_cut_sr = 130 if fmt == "t20" else 88
    opener_cut_avg = 28 if fmt == "t20" else 35
    finisher_cut_sr = 145 if fmt == "t20" else 98
    openers = [p for p in batter_like if p.get("strike_rate", 0) >= opener_cut_sr and p.get("bat_avg", 0) >= opener_cut_avg]
    finishers = [p for p in batter_like if p.get("strike_rate", 0) >= finisher_cut_sr]
    bowling_options = len([p for p in players if p["role"] in {"Bowler", "All-Rounder"}])
    warnings: list[str] = []
    if len(openers) < 2:
        warnings.append("XI may be short of specialist openers.")
    if len(finishers) < 2:
        warnings.append("XI may be short of finishers for end overs.")
    if bowling_options < 5:
        warnings.append("XI has fewer than 5 bowling options.")
    return {
        "openers": len(openers),
        "finishers": len(finishers),
        "bowling_options": bowling_options,
        "warnings": warnings,
    }


def toss_impact(fmt: str, venue_name: str | None, weather: str | None) -> dict[str, Any]:
    venue = venue_profile(venue_name)
    boundary = venue.get("boundary_size", "Medium")
    base_chase = 52.0 if fmt == "t20" else 50.0
    if boundary == "Small":
        base_chase += 3.5
    if boundary == "Large":
        base_chase -= 2.5
    if weather == "Heavy dew":
        base_chase += 8.0
    if weather in {"Cloudy", "Light drizzle risk"}:
        base_chase -= 3.0
    chase_adv = _clamp(base_chase, 35.0, 70.0)
    bat_adv = round(100.0 - chase_adv, 1)
    decision = "Bowl first after winning toss" if chase_adv >= 50 else "Bat first after winning toss"
    return {"chase_advantage": round(chase_adv, 1), "bat_advantage": bat_adv, "suggested_decision": decision}


def death_overs_venue_factor(fmt: str, venue: dict[str, Any], pitch: str | None, weather: str | None, par: float) -> dict[str, Any]:
    boundary = venue.get("boundary_size", "Medium")
    venue_pitch = str(venue.get("pitch_type", "")).lower()
    pitch_txt = str(pitch or "").lower()
    merged_pitch = f"{venue_pitch} {pitch_txt}"

    boundary_adj = {"Small": 0.7, "Medium": 0.0, "Large": -0.7}.get(boundary, 0.0)
    pitch_adj = 0.0
    if "flat" in merged_pitch or "batting" in merged_pitch:
        pitch_adj += 0.7
    if "green" in merged_pitch or "seam" in merged_pitch:
        pitch_adj -= 0.55
    if "spin" in merged_pitch or "slow" in merged_pitch or "tired" in merged_pitch:
        pitch_adj -= 0.35

    weather_adj = {
        "Heavy dew": 0.8,
        "Cloudy": -0.35,
        "Light drizzle risk": -0.45,
        "Hot and dry": 0.2,
    }.get(str(weather or ""), 0.0)

    baseline_final5_rr = 9.1 if fmt == "t20" else 7.0
    par_rr = par / FORMAT_RULES[fmt]["max_overs"]
    est_final5_rr = par_rr * (1.44 if fmt == "t20" else 1.22)
    est_final5_rr += boundary_adj + pitch_adj + weather_adj
    est_final5_rr = _clamp(est_final5_rr, 6.5 if fmt == "t20" else 4.8, 13.5 if fmt == "t20" else 9.5)

    historical_index = est_final5_rr / baseline_final5_rr
    multiplier = _clamp(0.9 + (historical_index - 1.0) * 0.55, 0.86, 1.15)
    return {
        "multiplier": round(multiplier, 3),
        "historical_final5_rr": round(est_final5_rr, 2),
        "historical_index": round(historical_index, 2),
        "boundary_context": boundary,
    }


def death_bowling_impact(fmt: str, bowl_xi: list[dict]) -> dict[str, Any]:
    if not bowl_xi:
        return {"multiplier": 1.0, "attack_score": 70.0, "label": "Neutral", "specialists": []}

    ref_econ = 7.8 if fmt == "t20" else 5.4
    candidates = [p for p in bowl_xi if p.get("role") in {"Bowler", "All-Rounder"} and float(p.get("economy", 0.0)) > 0]
    if not candidates:
        return {"multiplier": 1.0, "attack_score": 70.0, "label": "Neutral", "specialists": []}

    scored: list[tuple[float, dict]] = []
    for p in candidates:
        econ = max(0.1, float(p.get("economy", ref_econ)))
        rating = float(p.get("rating", 75.0))
        econ_score = _clamp((ref_econ / econ) * 65.0, 24.0, 118.0)
        rating_score = _clamp((rating / 100.0) * 35.0, 16.0, 35.0)
        strength = _clamp(econ_score + rating_score, 35.0, 99.0)
        scored.append((strength, p))

    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:4]
    attack_score = sum(s for s, _ in top) / max(1, len(top))
    multiplier = _clamp(1.10 - ((attack_score - 70.0) / 200.0), 0.86, 1.14)
    label = "Strong" if attack_score >= 82 else ("Weak" if attack_score <= 66 else "Balanced")
    specialists = [
        {"name": p["name"], "economy": p.get("economy", 0.0), "rating": p.get("rating", 0), "impact": round(s, 1)}
        for s, p in top
    ]
    return {
        "multiplier": round(multiplier, 3),
        "attack_score": round(attack_score, 1),
        "label": label,
        "specialists": specialists,
    }


def batter_remaining_simulation(
    fmt: str,
    xi: list[dict],
    wickets: int,
    balls_left: int,
    score: int,
) -> dict[str, Any]:
    if balls_left <= 0 or wickets >= 10:
        return {"projected_additional_runs": 0, "projected_total": score, "contributors": []}

    batters_left = xi[wickets:] if wickets < len(xi) else []
    if not batters_left:
        return {"projected_additional_runs": 0, "projected_total": score, "contributors": []}

    active = batters_left[: min(6, len(batters_left))]
    ref_sr = 140.0 if fmt == "t20" else 90.0
    ref_avg = 30.0 if fmt == "t20" else 42.0
    death_boost = 1.08 if (fmt == "t20" and balls_left <= 30) else (1.03 if balls_left <= 60 else 1.0)

    weights: list[float] = []
    for p in active:
        sr = float(p.get("strike_rate", ref_sr))
        bat_avg = float(p.get("bat_avg", ref_avg))
        rating = float(p.get("rating", 75.0))
        role = p.get("role", "")
        intent = ((sr / ref_sr) * 0.62) + ((bat_avg / ref_avg) * 0.38)
        if role == "All-Rounder":
            intent += 0.06
        elif role == "WK-Batter":
            intent += 0.04
        elif role == "Bowler":
            intent -= 0.1
        intent *= 1 + ((rating - 75.0) / 520.0)
        weights.append(max(0.05, intent))

    total_w = sum(weights)
    exact_balls = [(w / total_w) * balls_left for w in weights]
    balls_alloc = [int(math.floor(v)) for v in exact_balls]
    spill = balls_left - sum(balls_alloc)
    frac_idx = sorted(range(len(exact_balls)), key=lambda i: exact_balls[i] - balls_alloc[i], reverse=True)
    for i in frac_idx[:spill]:
        balls_alloc[i] += 1

    contributors: list[dict[str, Any]] = []
    total_runs = 0.0
    for idx, p in enumerate(active):
        balls = balls_alloc[idx]
        if balls <= 0:
            continue
        sr = float(p.get("strike_rate", ref_sr))
        rpb = _clamp((sr / 100.0) * death_boost, 0.62, 2.5 if fmt == "t20" else 1.75)
        runs = balls * rpb
        total_runs += runs
        contributors.append(
            {
                "name": p["name"],
                "role": p.get("role", ""),
                "balls": balls,
                "runs": int(round(runs)),
                "strike_rate": round(sr, 1),
            }
        )

    contributors.sort(key=lambda x: x["runs"], reverse=True)
    add_runs = max(0, int(round(total_runs)))
    return {
        "projected_additional_runs": add_runs,
        "projected_total": score + add_runs,
        "contributors": contributors[:4],
    }


def wicket_shock_model(fmt: str, score: int, avg: int, wickets: int, balls_left: int, base_rr: float, bowling_mult: float) -> dict[str, Any]:
    phase_shock = 0.09 if balls_left <= 18 else (0.06 if balls_left <= 36 else 0.03)
    wicket_load = max(0, wickets - 3) * 0.05
    bowling_shock = max(0.0, (1.0 / max(0.5, bowling_mult)) - 1.0) * 0.35
    next_over_wicket_prob = _clamp(0.12 + phase_shock + wicket_load + bowling_shock, 0.12, 0.72)

    penalty_overs = 1.7 if fmt == "t20" else 2.3
    run_penalty = base_rr * penalty_overs * (1 + next_over_wicket_prob * 0.9)
    wicket_total = max(score, int(round(avg - run_penalty)))

    label = "High" if next_over_wicket_prob >= 0.42 else ("Moderate" if next_over_wicket_prob >= 0.27 else "Low")
    return {
        "next_over_wicket_prob": round(next_over_wicket_prob * 100, 1),
        "if_wicket_next_over_total": wicket_total,
        "label": label,
    }


def phase_projections(fmt: str, overs_done: float, score: int, projected_total: int) -> dict[str, Any]:
    max_overs = FORMAT_RULES[fmt]["max_overs"]
    if fmt == "t20":
        phases = [("Powerplay", 0, 6), ("Middle", 6, 15), ("Death", 15, 20)]
    else:
        phases = [("Powerplay", 0, 10), ("Middle", 10, 40), ("Death", 40, 50)]
    current_rr = score / max(0.1, overs_done)
    out: list[dict[str, Any]] = []
    open_phases: list[dict[str, Any]] = []

    def _phase_multiplier(name: str) -> float:
        if name == "Powerplay":
            return 1.05 if fmt == "t20" else 0.98
        if name == "Middle":
            return 0.95 if fmt == "t20" else 0.94
        return 1.25 if fmt == "t20" else 1.15

    for name, start, end in phases:
        phase_end = min(end, max_overs)
        phase_len = max(0.0, phase_end - start)
        played = _clamp(overs_done - start, 0.0, phase_len)
        remaining = max(0.0, phase_len - played)
        status = "completed" if remaining <= 0 else ("live" if played > 0 else "upcoming")
        raw_add = remaining * current_rr * _phase_multiplier(name)
        row = {
            "phase": name,
            "start_over": start,
            "end_over": phase_end,
            "status": status,
            "played_overs": round(played, 2),
            "remaining_overs": round(remaining, 2),
            "raw_add": max(0.0, raw_add),
            "runs": 0,
            "cumulative": None,
        }
        out.append(row)
        if remaining > 0:
            open_phases.append(row)

    remaining_total = max(0, projected_total - score)
    total_raw = sum(p["raw_add"] for p in open_phases)

    allocated = 0
    for idx, p in enumerate(open_phases):
        if total_raw <= 0:
            add_runs = 0
        elif idx == len(open_phases) - 1:
            add_runs = max(0, remaining_total - allocated)
        else:
            add_runs = int(round((p["raw_add"] / total_raw) * remaining_total))
            allocated += add_runs
        p["runs"] = max(0, add_runs)

    prev_cum = score
    for p in out:
        if p["remaining_overs"] > 0:
            prev_cum += p["runs"]
            p["cumulative"] = min(projected_total, prev_cum)
        del p["raw_add"]

    return {"phases": out}


def head_to_head_overlay(team1: str, team2: str, fmt: str) -> dict[str, Any]:
    key = tuple(sorted([team1, team2]))
    pair = H2H_DATA.get(key, {})
    h2h_fmt = pair.get(fmt, {team1: 0, team2: 0})
    if team1 not in h2h_fmt:
        h2h_fmt[team1] = 0
    if team2 not in h2h_fmt:
        h2h_fmt[team2] = 0
    return {"team1_wins": h2h_fmt[team1], "team2_wins": h2h_fmt[team2], "total": h2h_fmt[team1] + h2h_fmt[team2]}


def predict_score(payload: dict[str, Any]) -> dict[str, Any]:
    fmt = format_key(payload.get("format"))
    rules = FORMAT_RULES[fmt]
    warnings: list[str] = []

    score = int(payload.get("score", 0))
    wickets = int(payload.get("wickets", 0))
    if score < 0:
        raise ValueError("Score cannot be negative")
    if wickets < 0 or wickets > 10:
        raise ValueError("Wickets should be between 0 and 10")

    balls_bowled = overs_to_balls(float(payload.get("overs", 0.0)), rules["max_overs"])
    if balls_bowled == 0:
        raise ValueError("Overs must be greater than 0")

    overs_done = balls_bowled / 6.0
    balls_left = (rules["max_overs"] * 6) - balls_bowled
    overs_left = balls_left / 6.0

    if wickets >= 10 or balls_left <= 0:
        if wickets >= 10:
            warnings.append("All out: innings is already closed.")
        return {
            "low": score,
            "avg": score,
            "high": score,
            "par": int(round(venue_average(fmt, payload.get("venue")))),
            "resource_used": 100.0,
            "team_overall": 0.0,
            "innings_closed": True,
            "batter_projection": {"projected_additional_runs": 0, "projected_total": score, "contributors": []},
            "warnings": warnings,
        }

    batting_team = str(payload.get("batting_team", ""))
    selected = payload.get("selected_xi", [])
    team_players = get_team_players(batting_team, fmt)
    xi = pick_players(team_players, selected)
    team_profile = team_breakdown(xi, fmt)
    xi_check = xi_validator(xi, fmt)
    bowling_team = str(payload.get("bowling_team", "")).strip()
    bowl_xi: list[dict] = []
    if bowling_team and bowling_team in TEAM_DATA:
        try:
            bowl_xi = pick_players(get_team_players(bowling_team, fmt), payload.get("bowling_xi", []))
        except ValueError:
            warnings.append("Bowling XI incomplete; using default bowling profile.")
            bowl_xi = get_team_players(bowling_team, fmt)[:11]

    crr = score / overs_done
    dls_remaining = dls_resource_remaining(fmt, overs_left, wickets)
    dls_used = max(1.0, 100.0 - dls_remaining)
    dls_projection = score * (100.0 / dls_used)

    wickets_in_hand = 10 - wickets
    phase_ratio = overs_done / rules["max_overs"]
    venue = venue_profile(payload.get("venue"))
    boundary_factor = {"Small": 1.03, "Medium": 1.0, "Large": 0.97}.get(venue.get("boundary_size", "Medium"), 1.0)
    base_accel = 1.06 if fmt == "t20" else 1.02
    phase_accel = 0.95 + (phase_ratio * base_accel)
    wickets_curve = max(0.62, (wickets_in_hand / 10.0) ** (0.62 if fmt == "t20" else 0.75))
    tempo_factor = phase_accel * (0.82 + wickets_curve * (0.38 if fmt == "t20" else 0.25))
    pace_projection = score + (crr * overs_left * tempo_factor * boundary_factor)
    par = venue_average(fmt, payload.get("venue"))
    death_context = death_overs_venue_factor(fmt, venue, payload.get("pitch"), payload.get("weather"), par)
    bowling_impact = death_bowling_impact(fmt, bowl_xi)

    live_rr_bias = (crr - (par / rules["max_overs"])) * (7.0 if fmt == "t20" else 3.2)
    combined = (dls_projection * 0.38) + (pace_projection * 0.34) + (par * 0.28) + live_rr_bias
    combined *= condition_multiplier(payload.get("pitch"), payload.get("weather"))
    combined *= 1 + ((team_profile["overall"] - 75.0) / 700.0)
    combined *= 1 + toss_adjustment(
        fmt,
        payload.get("toss_winner"),
        payload.get("toss_decision"),
        batting_team=batting_team,
    )
    death_influence = _clamp((phase_ratio - 0.45) / 0.55, 0.0, 1.0)
    combined *= 1 + ((death_context["multiplier"] - 1.0) * (0.2 + death_influence * 0.8))
    combined *= 1 + ((bowling_impact["multiplier"] - 1.0) * (0.2 + death_influence * 0.8))

    if fmt == "odi":
        max_reasonable = min(rules["score_ceiling"], par + 95)
        combined = min(combined, max_reasonable)

    combined = max(rules["score_floor"], min(rules["score_ceiling"], combined))
    avg_base = max(score, int(round(combined)))

    # Build a phase-aware remaining-runs envelope instead of a flat % spread.
    # This keeps late-innings (death overs) ranges realistic and always anchored
    # to current score + context (overs left, wickets in hand, scoring tempo).
    model_rr = avg_base / rules["max_overs"]
    phase_weight = _clamp(0.45 + (phase_ratio * 0.5), 0.45, 0.9)
    base_rr = (crr * phase_weight) + (model_rr * (1.0 - phase_weight))
    batter_projection = batter_remaining_simulation(fmt, xi, wickets, balls_left, score)
    avg = int(round((avg_base * 0.82) + (batter_projection["projected_total"] * 0.18)))
    avg = max(score, min(rules["score_ceiling"], avg))

    # Late-innings realism cap: avoid exaggerated jumps from current score.
    if fmt == "t20":
        rr_cap = 8.4 + (wickets_in_hand * 0.3) + (0.6 if overs_left <= 4.0 else 0.0)
    else:
        rr_cap = 6.2 + (wickets_in_hand * 0.22) + (0.35 if overs_left <= 10.0 else 0.0)
    max_context_total = score + int(round(max(0.0, overs_left) * rr_cap))
    avg = min(avg, max_context_total)

    # Construct symmetric band around avg; avg is always midpoint.
    base_spread = (7 if fmt == "t20" else 11) + int(round(overs_left * (1.15 if fmt == "t20" else 0.9)))
    wicket_adj = int(round((10 - wickets_in_hand) * (1.2 if fmt == "t20" else 0.9)))
    spread = max(4 if fmt == "t20" else 6, base_spread - wicket_adj)

    low = max(score, avg - spread)
    high = min(rules["score_ceiling"], avg + spread)
    if high <= low:
        high = min(rules["score_ceiling"], low + (2 if fmt == "t20" else 4))
    avg = int(round((low + high) / 2.0))

    shock = wicket_shock_model(fmt, score, avg, wickets, balls_left, base_rr, bowling_impact["multiplier"])
    low = max(score, min(low, shock["if_wicket_next_over_total"]))
    if high <= low:
        high = min(rules["score_ceiling"], low + (2 if fmt == "t20" else 4))
    avg = int(round((low + high) / 2.0))
    uncertainty = (high - low) / max(1.0, float(avg))
    confidence = 38.0 + (phase_ratio * 34.0) + ((1.0 - _clamp(uncertainty, 0.0, 1.0)) * 22.0)
    confidence -= len(xi_check["warnings"]) * 4.0
    if not payload.get("venue"):
        confidence -= 3.0
    if wickets >= 4 and overs_left > (6 if fmt == "t20" else 14):
        confidence -= 5.0
    confidence = _clamp(confidence, 20.0, 96.0)
    confidence_band = "High" if confidence >= 72 else ("Medium" if confidence >= 50 else "Low")

    return {
        "low": low,
        "avg": avg,
        "high": high,
        "par": int(round(par)),
        "resource_used": round(dls_used, 1),
        "team_overall": team_profile["overall"],
        "warnings": warnings + xi_check["warnings"],
        "xi_validation": xi_check,
        "toss_impact": toss_impact(fmt, payload.get("venue"), payload.get("weather")),
        "phase_projection": phase_projections(fmt, overs_done, score, avg),
        "death_context": death_context,
        "opponent_death_bowling": bowling_impact,
        "batter_projection": batter_projection,
        "wicket_shock": shock,
        "confidence": {"score": round(confidence, 1), "band": confidence_band},
        "innings_closed": False,
    }


def explain_score(payload: dict[str, Any]) -> dict[str, Any]:
    fmt = format_key(payload.get("format"))
    base = predict_score(payload)
    rules = FORMAT_RULES[fmt]
    max_overs = rules["max_overs"]
    score = int(payload.get("score", 0))
    wickets = int(payload.get("wickets", 0))
    balls_bowled = overs_to_balls(float(payload.get("overs", 0.0)), max_overs)
    overs_done = max(0.1, balls_bowled / 6.0)
    crr = score / overs_done
    par_rr = float(base["par"]) / max_overs
    wickets_in_hand = max(0, 10 - wickets)
    overs_left = max(0.0, (max_overs * 6 - balls_bowled) / 6.0)

    baseline = float(base["par"])
    live_momentum = (crr - par_rr) * max_overs * (0.58 if fmt == "t20" else 0.75)
    wicket_pressure = -max(0.0, (wickets - 3) * (5.2 if fmt == "t20" else 3.7))
    xi_strength = (float(base.get("team_overall", 75.0)) - 75.0) * (1.15 if fmt == "t20" else 1.45)

    toss_hint = base.get("toss_impact", {})
    toss_delta = ((float(toss_hint.get("bat_advantage", 50.0)) - 50.0) / 50.0) * (6.0 if fmt == "t20" else 9.0)

    death = base.get("death_context", {})
    death_delta = (float(death.get("multiplier", 1.0)) - 1.0) * baseline * 0.45
    opp = base.get("opponent_death_bowling", {})
    opposition_delta = (float(opp.get("multiplier", 1.0)) - 1.0) * baseline * 0.4

    batter_proj = base.get("batter_projection", {})
    par_remaining = max(0.0, par_rr * overs_left)
    batter_delta = float(batter_proj.get("projected_additional_runs", 0.0)) - par_remaining
    batter_delta *= 0.25

    approx_total = baseline + live_momentum + wicket_pressure + xi_strength + toss_delta + death_delta + opposition_delta + batter_delta
    residual = float(base["avg"]) - approx_total

    factors = [
        {"factor": "Venue Baseline", "impact": round(baseline, 1), "detail": f"Par at {payload.get('venue') or 'default venue'}"},
        {"factor": "Live Momentum", "impact": round(live_momentum, 1), "detail": f"CRR {crr:.2f} vs par RR {par_rr:.2f}"},
        {"factor": "Wicket Pressure", "impact": round(wicket_pressure, 1), "detail": f"{wickets} down, {wickets_in_hand} in hand"},
        {"factor": "XI Strength", "impact": round(xi_strength, 1), "detail": f"XI overall {base.get('team_overall', '-')}/100"},
        {"factor": "Toss + Conditions", "impact": round(toss_delta, 1), "detail": str(toss_hint.get("suggested_decision", "No toss bias"))},
        {"factor": "Death Venue Effect", "impact": round(death_delta, 1), "detail": f"Death multiplier {death.get('multiplier', 1.0)}x"},
        {"factor": "Opposition Death Bowling", "impact": round(opposition_delta, 1), "detail": f"Attack {opp.get('label', 'Neutral')} ({opp.get('attack_score', '-')})"},
        {"factor": "Remaining Batters Upside", "impact": round(batter_delta, 1), "detail": f"+{batter_proj.get('projected_additional_runs', '-') } projected from batters"},
        {"factor": "Model Residual", "impact": round(residual, 1), "detail": "Calibration correction after blending components"},
    ]
    factors_sorted = sorted(factors, key=lambda x: abs(x["impact"]), reverse=True)
    top_drivers = [f for f in factors_sorted if f["factor"] != "Venue Baseline"][:3]
    storyline = " | ".join([f"{d['factor']}: {d['impact']:+.1f}" for d in top_drivers])

    return {
        "predicted": {"low": base["low"], "avg": base["avg"], "high": base["high"]},
        "factors": factors,
        "top_drivers": top_drivers,
        "storyline": storyline,
        "confidence": base.get("confidence", {}),
    }


def _deterministic_noise(seed: int) -> float:
    x = math.sin((seed * 12.9898) + 78.233) * 43758.5453
    frac = x - math.floor(x)
    return (frac * 2.0) - 1.0


def backtest_report(payload: dict[str, Any]) -> dict[str, Any]:
    fmt = format_key(payload.get("format"))
    rules = FORMAT_RULES[fmt]
    max_overs = rules["max_overs"]
    team1 = str(payload.get("team1", ""))
    team2 = str(payload.get("team2", ""))
    if team1 not in TEAM_DATA or team2 not in TEAM_DATA:
        raise ValueError("Unknown teams for backtest")

    xi1_names = payload.get("xi1") or [p["name"] for p in TEAM_DATA[team1]["squads"][fmt][:11]]
    xi2_names = payload.get("xi2") or [p["name"] for p in TEAM_DATA[team2]["squads"][fmt][:11]]
    venue = payload.get("venue")
    pitch = payload.get("pitch")
    weather = payload.get("weather")

    checkpoints = [2.0, 5.0, 8.0, 11.0, 14.0, 17.0, 19.0] if fmt == "t20" else [5.0, 10.0, 18.0, 26.0, 34.0, 42.0, 48.0]
    phase_bounds = {"Powerplay": 6 if fmt == "t20" else 10, "Middle": 15 if fmt == "t20" else 40}

    rows: list[dict[str, Any]] = []
    err_abs: list[float] = []
    err_sq: list[float] = []
    within = 0
    over = 0
    under = 0
    by_phase: dict[str, list[float]] = {"Powerplay": [], "Middle": [], "Death": []}

    sample_count = int(payload.get("samples", 42))
    sample_count = int(_clamp(sample_count, 18, 90))
    scenarios = max(1, sample_count // len(checkpoints))
    seed_base = sum(ord(c) for c in f"{fmt}:{team1}:{team2}:{venue}:{pitch}:{weather}")

    for s in range(scenarios):
        batting_team = team1 if s % 2 == 0 else team2
        bowling_team = team2 if batting_team == team1 else team1
        bat_xi = xi1_names if batting_team == team1 else xi2_names
        bowl_xi = xi2_names if batting_team == team1 else xi1_names
        par = venue_average(fmt, venue)
        par_rr = par / max_overs

        for cp in checkpoints:
            progress = cp / max_overs
            seed = seed_base + (s * 31) + int(cp * 10)
            noise = _deterministic_noise(seed)
            rr_mult = 0.92 + (progress * 0.2) + (noise * 0.06)
            score = int(round(par_rr * cp * rr_mult))
            score = max(1, score)
            wickets = int(_clamp(round((cp / max_overs) * (4.8 if fmt == "t20" else 6.0) + ((noise + 1.0) * 0.8)), 0, 9))

            pred = predict_score(
                {
                    "format": fmt,
                    "batting_team": batting_team,
                    "selected_xi": bat_xi,
                    "bowling_team": bowling_team,
                    "bowling_xi": bowl_xi,
                    "toss_winner": "Auto",
                    "toss_decision": "auto",
                    "venue": venue,
                    "pitch": pitch,
                    "weather": weather,
                    "score": score,
                    "wickets": wickets,
                    "overs": cp,
                }
            )

            overs_left = max_overs - cp
            momentum_rr = score / max(0.1, cp)
            actual = score + (momentum_rr * overs_left * (0.9 + ((10 - wickets) / 12.0)))
            actual += (par - actual) * 0.16
            actual += _deterministic_noise(seed + 7) * (10.0 if fmt == "t20" else 18.0)
            actual = int(round(_clamp(actual, score, rules["score_ceiling"])))

            e = abs(pred["avg"] - actual)
            err_abs.append(e)
            err_sq.append(e * e)
            if pred["low"] <= actual <= pred["high"]:
                within += 1
            elif pred["avg"] > actual:
                over += 1
            else:
                under += 1

            phase = "Powerplay" if cp <= phase_bounds["Powerplay"] else ("Middle" if cp <= phase_bounds["Middle"] else "Death")
            by_phase[phase].append(e)
            rows.append({"overs": cp, "predicted": pred["avg"], "actual": actual, "phase": phase, "error": round(e, 1)})

    if not rows:
        raise ValueError("Unable to generate backtest scenarios")

    mae = sum(err_abs) / len(err_abs)
    rmse = math.sqrt(sum(err_sq) / len(err_sq))
    phase_mae = {k: round(sum(v) / len(v), 2) if v else None for k, v in by_phase.items()}
    calibration = round((within / len(rows)) * 100.0, 1)
    over_pct = round((over / len(rows)) * 100.0, 1)
    under_pct = round((under / len(rows)) * 100.0, 1)

    preview = rows[: min(24, len(rows))]
    return {
        "summary": {
            "samples": len(rows),
            "mae": round(mae, 2),
            "rmse": round(rmse, 2),
            "calibration_in_range_pct": calibration,
            "over_predict_pct": over_pct,
            "under_predict_pct": under_pct,
        },
        "phase_mae": phase_mae,
        "rows": preview,
        "notes": [
            "Backtest uses deterministic synthetic innings snapshots for reproducible benchmarking.",
            "Use this as model calibration signal, not official historical stats.",
        ],
    }


def live_demo_matches() -> list[dict[str, Any]]:
    return [{"id": m["id"], "title": m["title"], "format": m["format"], "teams": [m["team1"], m["team2"]]} for m in DEMO_LIVE_MATCHES]


def live_provider_profiles() -> list[dict[str, Any]]:
    return [{"id": key, "label": val.get("label", key)} for key, val in LIVE_PROVIDER_PROFILES.items()]


def _synthetic_timeline(overs_done: float, score: int, wickets: int, max_overs: int) -> dict[str, Any]:
    done = max(0.0, min(float(max_overs), float(overs_done)))
    if done <= 0:
        return {"overs": [], "runs": [], "wicket_overs": []}
    cps = [float(i) for i in range(1, int(done) + 1)]
    if done > int(done):
        cps.append(round(done, 1))
    runs = [int(round(score * (cp / done))) for cp in cps]
    wk_marks: list[float] = []
    if wickets > 0:
        for i in range(1, wickets + 1):
            wk_marks.append(round(done * (i / (wickets + 1)), 1))
    return {"overs": cps, "runs": runs, "wicket_overs": wk_marks}


def _recent_scenarios_synthetic(fmt: str, limit: int = 30) -> list[dict[str, Any]]:
    f = format_key(fmt)
    max_overs = FORMAT_RULES[f]["max_overs"]
    teams = [t["name"] for t in TOP_ODI_TEAMS][:10]
    if len(teams) < 2:
        return []
    out: list[dict[str, Any]] = []
    now = datetime.now(timezone.utc)
    # Use unique team pair combinations first to avoid repeated "same two matches".
    pairs: list[tuple[str, str]] = []
    for i in range(len(teams)):
        for j in range(i + 1, len(teams)):
            pairs.append((teams[i], teams[j]))
    if not pairs:
        return []
    need = max(1, int(limit))
    for i in range(need):
        t1, t2 = pairs[i % len(pairs)]
        # flip home/away alternate cycles for variation
        if (i // len(pairs)) % 2 == 1:
            t1, t2 = t2, t1
        venue = VENUES[(i * 11 + 3) % len(VENUES)]["name"] if VENUES else "Neutral Venue"
        d = now.date().toordinal() - (i + 1)
        match_date = datetime.fromordinal(d).date().isoformat()

        first_score = (170 if f == "t20" else 260) + ((i * 13) % (56 if f == "t20" else 85))
        first_wk = 5 + (i % 5)
        target = first_score + 1

        # Always completed scenarios in fallback.
        chase_overs = round((max_overs * (0.72 + ((i % 8) * 0.03))), 1)
        chase_overs = min(float(max_overs), max(8.0 if f == "t20" else 22.0, chase_overs))
        chase_wk = min(10, 2 + ((i * 3) % 9))
        chase_strength = 0.78 + ((i % 9) * 0.03)
        chase_score = int(round(target * min(1.04, chase_strength)))
        if chase_score >= target:
            chase_wk = min(chase_wk, 9)
            wk_left = max(0, 10 - chase_wk)
            result = f"{t2} won by {wk_left} wickets"
        else:
            chase_wk = 10
            chase_overs = min(float(max_overs), chase_overs)
            result = f"{t1} won by {max(1, target - chase_score - 1)} runs"
        chase_complete = True

        tl1 = _synthetic_timeline(float(max_overs), int(first_score), int(first_wk), int(max_overs))
        tl2 = _synthetic_timeline(float(chase_overs), int(chase_score), int(chase_wk), int(max_overs))
        scoring = {
            t1: _phase_breakdown_from_timeline(f, tl1),
            t2: _phase_breakdown_from_timeline(f, tl2),
        }

        out.append(
            {
                "id": f"{f}_recent_{i + 1}",
                "date": match_date,
                "format": f,
                "team1": t1,
                "team2": t2,
                "batting_team": t2,
                "bowling_team": t1,
                "score": int(chase_score),
                "wickets": int(chase_wk),
                "overs": float(chase_overs),
                "target": int(target),
                "first_innings_score": int(first_score),
                "first_innings_wickets": int(first_wk),
                "venue": venue,
                "toss_winner": t1 if i % 2 == 0 else t2,
                "toss_decision": "bat" if i % 3 == 0 else "bowl",
                "status": "completed" if chase_complete else "in_progress",
                "result": result,
                "title": f"{t1} vs {t2}, {f.upper()} (Recent Scenario #{i + 1})",
                "team1_xi": [p["name"] for p in TEAM_DATA[t1]["squads"][f][:11]],
                "team2_xi": [p["name"] for p in TEAM_DATA[t2]["squads"][f][:11]],
                "team1_squad_raw": [p["name"] for p in TEAM_DATA[t1]["squads"][f][:15]],
                "team2_squad_raw": [p["name"] for p in TEAM_DATA[t2]["squads"][f][:15]],
                "team_timelines": {t1: tl1, t2: tl2},
                "team_progress_points": {
                    t1: [{"over": float(o), "score": int(r)} for o, r in zip(tl1["overs"], tl1["runs"])],
                    t2: [{"over": float(o), "score": int(r)} for o, r in zip(tl2["overs"], tl2["runs"])],
                },
                "scoring_breakdown": scoring,
                "last_updated": "scenario-library",
                "provider": "scenario_library",
                "ingestion_source": "recent_scenario",
                "innings_complete": bool(chase_complete),
                "innings_timeline": tl2,
                "fow_events": [],
            }
        )
    return out


def _fmt_from_match_type(match_type: str) -> str | None:
    mt = str(match_type or "").lower()
    if "odi" in mt:
        return "odi"
    if "t20" in mt:
        return "t20"
    return None


def _to_num(v: Any, default: float = 0.0) -> float:
    try:
        return float(v)
    except Exception:
        return default


def _recent_scenarios_from_cricapi(fmt: str, limit: int, api_key: str) -> list[dict[str, Any]]:
    f = format_key(fmt)
    max_overs = FORMAT_RULES[f]["max_overs"]
    supported = {t["name"] for t in TOP_ODI_TEAMS[:10]}
    out: list[dict[str, Any]] = []
    seen_ids: set[str] = set()

    def fetch_json(path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        qp = {"apikey": api_key}
        if params:
            qp.update({k: v for k, v in params.items() if v not in (None, "")})
        url = f"https://api.cricapi.com/v1/{path}?{urllib.parse.urlencode(qp)}"
        req = urllib.request.Request(url, headers={"User-Agent": "CricketPredictorPro/1.0", "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=14) as resp:
            raw = resp.read().decode("utf-8", errors="ignore")
        return json.loads(raw)

    def extract_teams(row: dict[str, Any]) -> tuple[str, str] | None:
        teams_raw: list[str] = []
        if isinstance(row.get("teams"), list):
            teams_raw = [str(x) for x in row.get("teams", [])[:2]]
        elif isinstance(row.get("teamInfo"), list):
            for ti in row.get("teamInfo", [])[:2]:
                if isinstance(ti, dict):
                    teams_raw.append(str(ti.get("name", "")))
        else:
            a = str(row.get("team1", row.get("t1", ""))).strip()
            b = str(row.get("team2", row.get("t2", ""))).strip()
            if a and b:
                teams_raw = [a, b]
        if len(teams_raw) < 2:
            return None
        t1 = _canonical_team(teams_raw[0])
        t2 = _canonical_team(teams_raw[1])
        if t1 in supported and t2 in supported and t1 != t2:
            return t1, t2
        return None

    def normalize_row(row: dict[str, Any]) -> dict[str, Any] | None:
        row_fmt = _fmt_from_match_type(str(row.get("matchType", row.get("format", ""))))
        if row_fmt != f:
            return None
        teams = extract_teams(row)
        if not teams:
            return None
        team1, team2 = teams
        match_id = str(row.get("id") or row.get("unique_id") or row.get("matchId") or "")
        if not match_id:
            match_id = f"{team1}_{team2}_{row.get('dateTimeGMT', row.get('date', ''))}"
        if match_id in seen_ids:
            return None
        seen_ids.add(match_id)

        status_text = str(row.get("status", "")).strip()
        ended = bool(row.get("matchEnded")) or bool(re.search(r"won by|tied|no result|abandoned", status_text, flags=re.IGNORECASE))
        if not ended:
            return None

        date_raw = str(row.get("dateTimeGMT", row.get("date", "")))
        date_val = date_raw[:10] if len(date_raw) >= 10 else ""
        if date_val:
            try:
                if datetime.strptime(date_val, "%Y-%m-%d").date() > date.today():
                    return None
            except Exception:
                pass

        score_rows = row.get("score", []) if isinstance(row.get("score"), list) else []
        innings: list[dict[str, Any]] = []
        for idx, sr in enumerate(score_rows):
            if not isinstance(sr, dict):
                continue
            inn_text = str(sr.get("inning", sr.get("inningName", sr.get("inningInfo", ""))))
            inn_no = idx + 1
            m_no = re.search(r"\b(?:inning|innings)\s*([12])\b", inn_text, flags=re.IGNORECASE)
            if m_no:
                try:
                    inn_no = int(m_no.group(1))
                except Exception:
                    inn_no = idx + 1
            mapped_team = ""
            for cand in [team1, team2]:
                if cand.lower() in inn_text.lower():
                    mapped_team = cand
                    break
            if not mapped_team:
                mapped_team = _canonical_team(sr.get("team", sr.get("battingTeam", "")))
            if mapped_team not in {team1, team2}:
                mapped_team = team1 if idx == 0 else team2
            innings.append(
                {
                    "team": mapped_team,
                    "no": inn_no,
                    "runs": int(_to_num(sr.get("r", sr.get("runs", 0)), 0)),
                    "wk": int(_to_num(sr.get("w", sr.get("wickets", 0)), 0)),
                    "ov": _to_num(sr.get("o", sr.get("overs", 0.0)), 0.0),
                }
            )
        if len(innings) < 2:
            return None
        innings = sorted(innings, key=lambda x: (x["no"], 0 if x["team"] == team1 else 1))
        first_inn = innings[0]
        chase_inn = None
        for inn in innings[1:]:
            if inn["team"] != first_inn["team"]:
                chase_inn = inn
                break
        if chase_inn is None:
            chase_inn = innings[1]

        first_team = first_inn["team"]
        chase_team = chase_inn["team"]
        first_runs = int(first_inn["runs"])
        first_wk = int(first_inn["wk"])
        second_runs = int(chase_inn["runs"])
        second_wk = int(chase_inn["wk"])
        second_overs = float(chase_inn["ov"])
        if second_overs <= 0 and ended:
            second_overs = float(max_overs)
        target = first_runs + 1 if first_runs > 0 else None
        innings_complete = True

        tl1 = _synthetic_timeline(float(max_overs), first_runs, first_wk, int(max_overs))
        tl2 = _synthetic_timeline(float(second_overs), second_runs, second_wk, int(max_overs))
        scoring = {
            first_team: _phase_breakdown_from_timeline(f, tl1),
            chase_team: _phase_breakdown_from_timeline(f, tl2),
        }
        if not date_val:
            date_val = datetime.now(timezone.utc).date().isoformat()
        venue = str(row.get("venue", "") or "Unknown Venue")
        title = str(row.get("name", "")).strip() or f"{team1} vs {team2}"
        if not status_text:
            if target is not None and second_runs >= target:
                status_text = f"{chase_team} won by {max(0, 10 - second_wk)} wickets"
            else:
                status_text = f"{first_team} won by {max(1, (target or 0) - second_runs - 1)} runs"

        return {
            "id": str(match_id),
            "date": date_val,
            "format": f,
            "team1": team1,
            "team2": team2,
            "batting_team": chase_team,
            "bowling_team": first_team,
            "score": int(second_runs),
            "wickets": int(second_wk),
            "overs": float(second_overs),
            "target": int(target) if target is not None else None,
            "first_innings_score": int(first_runs),
            "first_innings_wickets": int(first_wk),
            "first_innings_team": first_team,
            "chasing_team": chase_team,
            "venue": venue,
            "toss_winner": _canonical_team(row.get("tossWinner", "Auto")) or "Auto",
            "toss_decision": str(row.get("tossChoice", "auto")).strip().lower() or "auto",
            "status": "completed",
            "result": status_text or "Completed",
            "title": title,
            "team1_xi": [p["name"] for p in TEAM_DATA[team1]["squads"][f][:11]],
            "team2_xi": [p["name"] for p in TEAM_DATA[team2]["squads"][f][:11]],
            "team1_squad_raw": [p["name"] for p in TEAM_DATA[team1]["squads"][f][:15]],
            "team2_squad_raw": [p["name"] for p in TEAM_DATA[team2]["squads"][f][:15]],
            "team_timelines": {first_team: tl1, chase_team: tl2},
            "team_progress_points": {
                first_team: [{"over": float(o), "score": int(r)} for o, r in zip(tl1["overs"], tl1["runs"])],
                chase_team: [{"over": float(o), "score": int(r)} for o, r in zip(tl2["overs"], tl2["runs"])],
            },
            "scoring_breakdown": scoring,
            "last_updated": "cricapi",
            "provider": "cricapi_free",
            "ingestion_source": "recent_scenario_api",
            "innings_complete": bool(innings_complete),
            "innings_timeline": tl2,
            "fow_events": [],
            "data_source": "free_api",
        }

    def push_rows(rows: list[dict[str, Any]]) -> None:
        for row in rows:
            if len(out) >= limit:
                return
            if not isinstance(row, dict):
                continue
            norm = normalize_row(row)
            if norm:
                out.append(norm)

    # 1) Try matches style endpoints with paging.
    for endpoint in ["matches", "currentMatches"]:
        for offset in [0, 25, 50, 75, 100]:
            if len(out) >= limit:
                break
            try:
                data = fetch_json(endpoint, {"offset": offset})
            except Exception:
                continue
            rows = data.get("data", []) if isinstance(data, dict) else []
            if isinstance(rows, list):
                push_rows(rows)

    # 2) If still short, crawl recent series then fetch series_info match lists.
    if len(out) < limit:
        try:
            series_data = fetch_json("series")
        except Exception:
            series_data = {}
        series_rows = series_data.get("data", []) if isinstance(series_data, dict) else []
        if isinstance(series_rows, list):
            for s in series_rows[:18]:
                if len(out) >= limit:
                    break
                if not isinstance(s, dict):
                    continue
                s_fmt = _fmt_from_match_type(str(s.get("matchType", s.get("format", ""))))
                if s_fmt != f:
                    continue
                sid = str(s.get("id", "")).strip()
                if not sid:
                    continue
                try:
                    info = fetch_json("series_info", {"id": sid})
                except Exception:
                    continue
                bucket = []
                if isinstance(info, dict):
                    data_block = info.get("data", {})
                    if isinstance(data_block, dict):
                        for k in ["matchList", "matches", "match_list"]:
                            if isinstance(data_block.get(k), list):
                                bucket = data_block.get(k)
                                break
                    if not bucket and isinstance(info.get("data"), list):
                        bucket = info.get("data")
                if isinstance(bucket, list):
                    push_rows(bucket)

    out.sort(key=lambda x: str(x.get("date", "")), reverse=True)
    return out[:limit]


def recent_match_scenarios(fmt: str, limit: int = 30) -> list[dict[str, Any]]:
    f = format_key(fmt)
    lim = max(1, int(limit))
    api_key = str(
        os.environ.get("CRICAPI_KEY", "")
        or os.environ.get("SCENARIO_API_KEY", "")
        or os.environ.get("FREE_CRICKET_API_KEY", "")
    ).strip()
    if api_key:
        api_rows = _recent_scenarios_from_cricapi(f, lim, api_key)
        if len(api_rows) >= min(8, lim):
            return api_rows
    fallback = _recent_scenarios_synthetic(f, lim)
    for row in fallback:
        row["data_source"] = "synthetic_fallback"
    return fallback


def model_card() -> dict[str, Any]:
    return {
        "model_type": "Deterministic hybrid statistical engine (not a generative LLM predictor).",
        "version": "v1.4-rule-hybrid",
        "what_it_uses": [
            "DLS-style resource curves (overs and wickets).",
            "Live momentum features (current run rate vs par).",
            "XI composition scoring (batting, bowling, role balance).",
            "Pitch, weather, toss and venue effects.",
            "Death overs venue/opposition calibration multipliers.",
        ],
        "what_it_does_not_use": [
            "No deep neural network trained on ball-by-ball proprietary data.",
            "No black-box LLM deciding numeric predictions.",
            "No betting-market odds ingestion.",
        ],
        "explainability": {
            "method": "Factor attribution with additive impact decomposition.",
            "endpoint": "/api/explain_score",
        },
        "limitations": [
            "Predictions are scenario estimates, not guarantees.",
            "Synthetic backtesting is for calibration demonstration, not official benchmarking.",
            "Live ingestion quality depends on source API correctness and field mapping.",
        ],
        "ethics_and_usage": [
            "Built for education and cricket analytics demos.",
            "Avoid financial gambling reliance.",
            "Always communicate uncertainty bands, not only point estimates.",
        ],
    }


def gemini_live_brief(payload: dict[str, Any]) -> dict[str, Any]:
    live = payload.get("live")
    if not isinstance(live, dict):
        raise ValueError("Live payload missing for match insight.")

    compact_live = {
        "title": live.get("title"),
        "format": live.get("format"),
        "team1": live.get("team1"),
        "team2": live.get("team2"),
        "batting_team": live.get("batting_team"),
        "score": live.get("score"),
        "wickets": live.get("wickets"),
        "overs": live.get("overs"),
        "target": live.get("target"),
        "toss_winner": live.get("toss_winner"),
        "toss_decision": live.get("toss_decision"),
        "venue": live.get("venue"),
        "scoring_breakdown": live.get("scoring_breakdown"),
        "innings_complete": live.get("innings_complete"),
        "fow_events": (live.get("fow_events") or [])[:12],
        "team_timelines": {
            str(k): {
                "overs": (v.get("overs", []) if isinstance(v, dict) else [])[:12],
                "runs": (v.get("runs", []) if isinstance(v, dict) else [])[:12],
                "wicket_overs": (v.get("wicket_overs", []) if isinstance(v, dict) else [])[:12],
            }
            for k, v in (live.get("team_timelines", {}) or {}).items()
            if isinstance(v, dict)
        },
    }
    prompt = (
        "You are a cricket analytics assistant.\n"
        "Return plain text only. Do not use markdown, bold, numbering, or headings with symbols.\n"
        "Write a detailed but concise analysis (8 to 12 lines).\n"
        "Use this structure exactly:\n"
        "Match Context: <one line>\n"
        "Key Insights:\n"
        "- <momentum insight>\n"
        "- <wickets-pressure insight>\n"
        "- <phase-split insight>\n"
        "- <tactical insight for next phase>\n"
        "Turning Point: <one line>\n"
        "Method Notes: <one line saying this summary combines scraped live data + statistical engine + AI synthesis>\n"
        "Caution: <one line on uncertainty/data limits>\n\n"
        f"Live state JSON:\n{json.dumps(compact_live, ensure_ascii=True)}"
    )

    def local_fallback(live_state: dict[str, Any], errors: list[str] | None = None) -> dict[str, Any]:
        team = str(live_state.get("batting_team", "Batting side"))
        score = int(live_state.get("score", 0) or 0)
        wickets = int(live_state.get("wickets", 0) or 0)
        overs = float(live_state.get("overs", 0.0) or 0.0)
        fmt = format_key(live_state.get("format", "odi"))
        max_overs = float(FORMAT_RULES[fmt]["max_overs"])
        crr = (score / overs) if overs > 0 else 0.0
        phase = "Powerplay" if (fmt == "t20" and overs <= 6) or (fmt == "odi" and overs <= 10) else ("Middle Overs" if overs < (15 if fmt == "t20" else 40) else "Death Overs")
        wk_pressure = "high" if wickets >= 7 else ("moderate" if wickets >= 4 else "low")
        bd = live_state.get("scoring_breakdown", {}) if isinstance(live_state.get("scoring_breakdown"), dict) else {}
        p = bd.get(team, {}) if isinstance(bd.get(team), dict) else {}
        pp = p.get("powerplay", {}) if isinstance(p.get("powerplay"), dict) else {"runs": 0, "wickets": 0}
        mid = p.get("middle", {}) if isinstance(p.get("middle"), dict) else {"runs": 0, "wickets": 0}
        death = p.get("death", {}) if isinstance(p.get("death"), dict) else {"runs": 0, "wickets": 0}
        insight = (
            f"Match Context: {team} are {score}/{wickets} in {overs} overs.\n"
            "Key Insights:\n"
            f"- Momentum: current run rate is {crr:.2f}; innings phase is {phase}.\n"
            f"- Wickets pressure: {wk_pressure} (wickets lost: {wickets}).\n"
            f"- Phase split: PP {pp.get('runs', 0)}/{pp.get('wickets', 0)}, Middle {mid.get('runs', 0)}/{mid.get('wickets', 0)}, Final {death.get('runs', 0)}/{death.get('wickets', 0)}.\n"
            f"Caution: Cloud AI insight is temporarily unavailable; showing local analytic summary (max overs {int(max_overs)})."
        )
        out = {"model": "ai-insight-local-fallback", "insight": insight}
        if errors:
            out["provider_errors"] = errors[-3:]
        return out

    api_key = str(
        payload.get("insight_api_key", "")
        or payload.get("gemini_api_key", "")
        or os.environ.get("MATCH_INSIGHT_API_KEY", "")
        or os.environ.get("GEMINI_API_KEY", "")
        or DEFAULT_MATCH_INSIGHT_KEY
    ).strip()
    # Never hard-fail for missing key; return local summary so UI stays useful.
    if not api_key:
        return local_fallback(live, ["No cloud insight key found."])

    req_body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.25, "maxOutputTokens": 650},
    }
    def call_model(model_name: str) -> str:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={urllib.parse.quote(api_key)}"
        req = urllib.request.Request(
            url,
            data=json.dumps(req_body).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="ignore"))
        candidates = data.get("candidates", []) if isinstance(data, dict) else []
        if candidates and isinstance(candidates[0], dict):
            content = candidates[0].get("content", {})
            parts = content.get("parts", []) if isinstance(content, dict) else []
            text = "\n".join(str(p.get("text", "")).strip() for p in parts if isinstance(p, dict) and p.get("text"))
            if text:
                return text
        raise ValueError("AI insight model returned empty content.")

    models = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
    errors: list[str] = []
    for model_name in models:
        for attempt in range(3):
            try:
                text = call_model(model_name)
                text = re.sub(r"[*_`#]+", "", text)
                text = re.sub(r"^\s*\d+\)\s*", "- ", text, flags=re.MULTILINE)
                text = re.sub(r"\n{3,}", "\n\n", text).strip()
                if len(text) < 45:
                    # Keep cloud output if any meaningful text is returned; just enrich it.
                    text = f"{text}\n\nNote: concise cloud response; expanded with engine trace below."
                # Always append deterministic trace so viva explanation is explicit.
                team = str(live.get("batting_team", "Batting side"))
                score = int(live.get("score", 0) or 0)
                wickets = int(live.get("wickets", 0) or 0)
                overs = float(live.get("overs", 0.0) or 0.0)
                fmt = format_key(live.get("format", "odi"))
                crr = (score / overs) if overs > 0 else 0.0
                trace = (
                    "\nEngine Trace:\n"
                    f"- Inputs used: format={fmt.upper()}, score={score}/{wickets}, overs={overs}, batting_team={team}.\n"
                    f"- Derived metric: current run rate={crr:.2f}.\n"
                    "- Pipeline: live scrape -> phase/wicket feature extraction -> deterministic scoring model -> AI narrative synthesis."
                )
                return {"model": "ai-insight", "insight": f"{text}\n{trace}"}
            except Exception as exc:
                errors.append(f"{model_name} attempt {attempt + 1}: {exc}")
                # Retry only on service-pressure style failures.
                msg = str(exc).lower()
                transient = ("503" in msg) or ("429" in msg) or ("timed out" in msg) or ("reset" in msg)
                if transient and attempt < 2:
                    time.sleep(1.2 * (attempt + 1))
                    continue
                break

    # Local fallback so UI never hard-fails when provider is down.
    return local_fallback(live, errors)


def _extract_path(data: Any, path: str) -> Any:
    if path == "" or path is None:
        return data
    cur = data
    for part in path.split("."):
        if isinstance(cur, list):
            if part.isdigit():
                idx = int(part)
                if idx < 0 or idx >= len(cur):
                    return None
                cur = cur[idx]
                continue
            found = None
            for item in cur:
                if isinstance(item, dict) and part in item:
                    found = item[part]
                    break
            if found is None:
                return None
            cur = found
            continue
        if isinstance(cur, dict):
            if part not in cur:
                return None
            cur = cur[part]
            continue
        return None
    return cur


def _to_text(blob: str) -> str:
    text = re.sub(r"<script[\s\S]*?</script>", " ", blob, flags=re.IGNORECASE)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = unescape(text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _meta_content(html: str, key: str, is_property: bool = True) -> str | None:
    attr = "property" if is_property else "name"
    pat = rf'<meta[^>]+{attr}="{re.escape(key)}"[^>]+content="([^"]+)"'
    m = re.search(pat, html, flags=re.IGNORECASE)
    return unescape(m.group(1)).strip() if m else None


def _canonical_team(name: Any) -> str:
    raw_name = str(name or "").strip()
    if not raw_name:
        return raw_name
    key = raw_name.lower()
    if key in TEAM_ALIASES:
        return TEAM_ALIASES[key]

    norm = re.sub(r"[^a-z ]+", " ", key)
    norm = re.sub(r"\s+", " ", norm).strip()
    stop_words = {
        "cricket",
        "score",
        "scorecard",
        "live",
        "match",
        "result",
        "commentary",
        "full",
        "card",
    }
    tokens = [t for t in norm.split() if t not in stop_words]
    norm = " ".join(tokens)

    if norm in TEAM_ALIASES:
        return TEAM_ALIASES[norm]
    if re.search(r"\bsa\b", norm):
        return "South Africa"
    if re.search(r"\bnz\b", norm):
        return "New Zealand"
    if re.search(r"\bwi\b|\bwindies\b", norm):
        return "West Indies"
    if re.search(r"\beng\b", norm):
        return "England"
    if re.search(r"\bind\b", norm):
        return "India"
    if re.search(r"\bpak\b", norm):
        return "Pakistan"
    if re.search(r"\bban\b", norm):
        return "Bangladesh"
    if re.search(r"\bafg\b", norm):
        return "Afghanistan"
    if re.search(r"\baus\b", norm):
        return "Australia"
    if re.search(r"\bsl\b", norm):
        return "Sri Lanka"

    for team in TEAM_DATA.keys():
        tl = team.lower()
        if tl in norm or norm in tl:
            return team
    return raw_name


def _find_teams_from_text(text: str) -> tuple[str, str]:
    matches = re.finditer(r"([A-Za-z .&'-]{2,45})\s+v(?:s|\.)\s+([A-Za-z .&'-]{2,45})", text, flags=re.IGNORECASE)
    for m in matches:
        t1 = _canonical_team(m.group(1).strip())
        t2 = _canonical_team(m.group(2).strip())
        if t1 in TEAM_DATA and t2 in TEAM_DATA and t1 != t2:
            return t1, t2
    return "", ""


def _find_teams_from_url(url: str) -> tuple[str, str]:
    path = urlparse(url).path.lower()
    parts = [p for p in path.strip("/").split("/") if p]
    for seg in reversed(parts):
        slug = re.sub(r"-\d{6,}$", "", seg)
        if "-vs-" not in slug:
            continue
        left, right = slug.split("-vs-", 1)
        right = re.split(r"-\d", right, 1)[0]
        t1 = _canonical_team(left.replace("-", " "))
        t2 = _canonical_team(right.replace("-", " "))
        if t1 in TEAM_DATA and t2 in TEAM_DATA and t1 != t2:
            return t1, t2
    return "", ""


def _extract_score_tuple(text: str) -> tuple[int, int, float] | None:
    patterns = [
        r"(\d{1,3})\s*/\s*(\d{1,2})\s*\(?\s*(\d{1,2}(?:\.\d)?)\s*(?:ov|overs?)\s*\)?",
        r"(\d{1,3})\s*/\s*(\d{1,2})",
    ]
    for idx, pat in enumerate(patterns):
        m = re.search(pat, text, flags=re.IGNORECASE)
        if not m:
            continue
        runs = int(m.group(1))
        wkts = int(m.group(2))
        overs = float(m.group(3)) if idx == 0 and m.lastindex and m.lastindex >= 3 else 0.0
        return runs, wkts, overs
    return None


def _extract_target(text: str) -> int | None:
    patterns = [
        r"target\s*[:\-]?\s*(\d{2,3})",
        r"need\s+\d+\s+runs?\s+from\s+\d+\s+balls?\s+to\s+win\s*(?:\(target\s*(\d{2,3})\))?",
        r"to win by.*?target\s*(\d{2,3})",
    ]
    for pat in patterns:
        m = re.search(pat, text, flags=re.IGNORECASE)
        if m:
            if m.lastindex and m.group(1):
                return int(m.group(1))
    return None


def _infer_format_from_url(url: str) -> str | None:
    low = str(url).lower()
    if re.search(r"(\b|[-_/])(odi|one-day|one_day)(\b|[-_/])", low):
        return "odi"
    if re.search(r"(\b|[-_/])(t20|t20i|ipl)(\b|[-_/])", low):
        return "t20"
    return None


def _infer_format(text: str, url: str | None = None) -> str:
    url_fmt = _infer_format_from_url(url or "")
    if url_fmt:
        return url_fmt
    low = text.lower()
    if "odi" in low or "one day" in low:
        return "odi"
    if "t20" in low or "ipl" in low:
        return "t20"
    return "t20"


def _extract_batting_team_from_text(text: str) -> str:
    m = re.search(r"([A-Za-z .&'-]{2,35})\s+\d{1,3}\s*/\s*\d{1,2}", text)
    if m:
        return _canonical_team(m.group(1).strip())
    return ""


def _extract_toss_info(text: str) -> tuple[str, str]:
    patterns = [
        r"([A-Za-z .&'-]{2,40})\s+won the toss and\s+(?:elect(?:ed)?|opt(?:ed)?|chose)\s+to\s+(bat|bowl|field)",
        r"([A-Za-z .&'-]{2,40})\s+won the toss\s*&?\s*(?:elect(?:ed)?|opt(?:ed)?|chose)\s+to\s+(bat|bowl|field)",
        r"([A-Za-z .&'-]{2,40})\s+won the toss",
    ]
    for pat in patterns:
        m = re.search(pat, text, flags=re.IGNORECASE)
        if not m:
            continue
        team = _canonical_team(m.group(1).strip())
        decision = "auto"
        if m.lastindex and m.lastindex >= 2 and m.group(2):
            choice = m.group(2).strip().lower()
            decision = "bowl" if choice == "field" else choice
            if decision not in {"bat", "bowl"}:
                decision = "auto"
        return (team if team in TEAM_DATA else "Auto"), decision
    return "Auto", "auto"


def _extract_toss_info_from_raw_html(html: str) -> tuple[str, str]:
    raw = unescape(html)
    patterns = [
        r"([A-Za-z .&'-]{2,40})\s+won the toss and\s+(?:elect(?:ed)?|opt(?:ed)?|chose)\s+to\s+(bat|bowl|field)",
        r"([A-Za-z .&'-]{2,40})\s+won the toss\s*&?\s*(?:elect(?:ed)?|opt(?:ed)?|chose)\s+to\s+(bat|bowl|field)",
        r"([A-Za-z .&'-]{2,40})\s+won the toss",
    ]
    for pat in patterns:
        m = re.search(pat, raw, flags=re.IGNORECASE)
        if not m:
            continue
        team = _canonical_team(m.group(1).strip())
        decision = "auto"
        if m.lastindex and m.lastindex >= 2 and m.group(2):
            choice = m.group(2).strip().lower()
            decision = "bowl" if choice == "field" else choice
            if decision not in {"bat", "bowl"}:
                decision = "auto"
        return (team if team in TEAM_DATA else "Auto"), decision
    m_team = re.search(r'\\"toss(?:Winner|winner)\\"?\s*:\s*\\"([^\\"]+)\\"', raw, flags=re.IGNORECASE)
    m_dec = re.search(r'\\"toss(?:Decision|decision)\\"?\s*:\s*\\"([^\\"]+)\\"', raw, flags=re.IGNORECASE)
    if m_team:
        team = _canonical_team(m_team.group(1).strip())
        decision = "auto"
        if m_dec:
            choice = m_dec.group(1).strip().lower()
            decision = "bowl" if choice == "field" else choice
            if decision not in {"bat", "bowl"}:
                decision = "auto"
        return (team if team in TEAM_DATA else "Auto"), decision
    return "Auto", "auto"


def _extract_venue_from_text(text: str) -> str | None:
    patterns = [
        r"\bvenue\s*[:\-]\s*([A-Za-z0-9 .,&'()/-]{4,110})(?:\||$|\s{2,})",
        r"\bat\s+([A-Za-z0-9 .,&'()/-]{4,110}?)(?:\s*\(|,|\s+\d{4}|\s+match|\s+t20|\s+odi|$)",
    ]
    for pat in patterns:
        m = re.search(pat, text, flags=re.IGNORECASE)
        if not m:
            continue
        venue_raw = re.sub(r"\s+", " ", m.group(1)).strip(" ,.-")
        if "," in venue_raw and len(venue_raw) >= 8:
            return venue_raw[:80]
        for v in VENUES:
            if v["name"].lower() in venue_raw.lower() or venue_raw.lower() in v["name"].lower():
                return v["name"]
        if len(venue_raw) >= 4 and re.search(r"stadium|ground|park|oval|arena|field", venue_raw, flags=re.IGNORECASE):
            return venue_raw[:80]
    return None


def _extract_venue_from_raw_html(html: str) -> str | None:
    raw = unescape(html)
    patterns = [
        r'title="View Venue ([^"]{4,140}) Details"',
        r"Venue</div><a[^>]*>([^<]{4,120})<",
        r'"venue"\s*:\s*"([^"]{4,120})"',
        r'"ground"\s*:\s*"([^"]{4,120})"',
        r"\bvenue\s*[:\-]\s*([A-Za-z0-9 .,&'()/-]{4,110})(?:\||$|\s{2,})",
    ]
    for pat in patterns:
        m = re.search(pat, raw, flags=re.IGNORECASE)
        if not m:
            continue
        venue_raw = re.sub(r"\s+", " ", m.group(1)).strip(" ,.-")
        if "," in venue_raw and len(venue_raw) >= 8:
            return venue_raw[:80]
        for v in VENUES:
            if v["name"].lower() in venue_raw.lower() or venue_raw.lower() in v["name"].lower():
                return v["name"]
        if len(venue_raw) >= 4 and re.search(r"stadium|ground|park|oval|arena|field", venue_raw, flags=re.IGNORECASE):
            return venue_raw[:80]
    return None


def _normalize_live_url(url: str, provider: str) -> tuple[str, str]:
    norm = str(url).strip()
    prov = provider
    low = norm.lower()
    if "cricbuzz.com" in low and "/live-cricket-scores/" in low:
        norm = re.sub(r"/live-cricket-scores/", "/live-cricket-scorecard/", norm, count=1, flags=re.IGNORECASE)
    if prov == "generic":
        if "cricbuzz.com" in low:
            prov = "cricbuzz_html"
        elif "espncricinfo.com" in low or "espn" in low:
            prov = "espn_html"
    return norm, prov


def _try_fetch_html(url: str, timeout: int = 10) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "CricketPredictorPro/1.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def _espn_companion_urls(url: str) -> list[str]:
    parsed = urlparse(url)
    if "espncricinfo.com" not in parsed.netloc.lower():
        return []
    path = parsed.path.strip("/")
    if not path:
        return []
    base, _, tail = path.rpartition("/")
    if not base:
        return []
    if tail in {"full-scorecard", "match-statistics"}:
        variants = ["full-scorecard", "match-statistics"]
    else:
        variants = [tail, "full-scorecard", "match-statistics"]
    out: list[str] = []
    for v in variants:
        p = f"/{base}/{v}"
        out.append(f"{parsed.scheme}://{parsed.netloc}{p}")
    dedup: list[str] = []
    seen: set[str] = set()
    for u in out:
        if u not in seen:
            seen.add(u)
            dedup.append(u)
    return dedup


def _cricbuzz_companion_urls(url: str) -> list[str]:
    parsed = urlparse(url)
    if "cricbuzz.com" not in parsed.netloc.lower():
        return []
    m = re.search(r"/(live-cricket-scores|live-cricket-scorecard)/(\d+)(?:/|$)", parsed.path, flags=re.IGNORECASE)
    if not m:
        return [url]
    match_id = m.group(2)
    roots = ["live-cricket-scorecard", "live-cricket-scores"]
    out = [f"{parsed.scheme}://{parsed.netloc}/{root}/{match_id}" for root in roots]
    dedup: list[str] = []
    seen: set[str] = set()
    for u in out:
        if u not in seen:
            seen.add(u)
            dedup.append(u)
    return dedup


def _cross_source_context(url: str) -> str:
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    urls: list[str] = []
    if "espncricinfo.com" in domain:
        urls = _espn_companion_urls(url)
    elif "cricbuzz.com" in domain:
        urls = _cricbuzz_companion_urls(url)
    if not urls:
        return ""

    chunks: list[str] = []
    base_url = url.rstrip("/")
    for u in urls:
        if u.rstrip("/") == base_url:
            continue
        try:
            chunks.append(_try_fetch_html(u, timeout=8))
        except Exception:
            continue
    return "\n".join(chunks)


def _extract_max_overs_hint(text: str, fmt: str) -> float | None:
    max_overs = FORMAT_RULES[fmt]["max_overs"]
    vals: list[float] = []
    for m in re.finditer(r"\b(\d{1,2}(?:\.\d)?)\s*(?:ov|overs?)\b", text, flags=re.IGNORECASE):
        try:
            ov = float(m.group(1))
        except Exception:
            continue
        if 0.0 < ov <= float(max_overs):
            vals.append(ov)
    if not vals:
        return None
    return max(vals)


def _extract_overs_hints(text: str, fmt: str) -> list[float]:
    max_overs = FORMAT_RULES[fmt]["max_overs"]
    vals: list[float] = []
    for m in re.finditer(r"\b(\d{1,2}(?:\.\d)?)\s*(?:ov|overs?)\b", text, flags=re.IGNORECASE):
        try:
            ov = float(m.group(1))
        except Exception:
            continue
        if 0.0 < ov <= float(max_overs):
            vals.append(ov)
    return sorted(vals)


def _extract_exact_innings_overs(text: str, team: str, score: int, wickets: int, fmt: str) -> float | None:
    max_overs = float(FORMAT_RULES[fmt]["max_overs"])
    team_pat = re.escape(team)
    score_pat = rf"{int(score)}\s*/\s*{int(wickets)}"
    patterns = [
        rf"{team_pat}[^\d]{{0,40}}{score_pat}[^\d]{{0,25}}(\d{{1,2}}(?:\.\d)?)\s*(?:ov|overs?)",
        rf"{score_pat}[^\d]{{0,25}}(\d{{1,2}}(?:\.\d)?)\s*(?:ov|overs?)",
        rf"{score_pat}[^\d]{{0,25}}(?:all out|ao)[^\d]{{0,20}}(\d{{1,2}}(?:\.\d)?)\s*(?:ov|overs?)",
        rf"{int(score)}\s*(?:all out|ao)[^\d]{{0,20}}(\d{{1,2}}(?:\.\d)?)\s*(?:ov|overs?)",
        rf"{team_pat}[^\d]{{0,30}}(\d{{1,2}}(?:\.\d)?)\s*(?:ov|overs?)[^\d]{{0,20}}{score_pat}",
    ]
    for pat in patterns:
        m = re.search(pat, text, flags=re.IGNORECASE)
        if not m:
            continue
        try:
            ov = float(m.group(1))
        except Exception:
            continue
        if 0.0 < ov <= max_overs:
            return ov
    return None


def _name_key(name: str) -> str:
    norm = re.sub(r"[^a-z]", "", name.lower())
    return norm


def _extract_fow_events(text: str) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    patterns = re.finditer(r"(\d{1,3})-(\d{1,2})\s*\([^)]*?,\s*(\d{1,2}(?:\.\d)?)\s*ov", text, flags=re.IGNORECASE)
    for m in patterns:
        score_at = int(m.group(1))
        wicket_no = int(m.group(2))
        over_at = float(m.group(3))
        events.append({"score": score_at, "wicket": wicket_no, "over": over_at})
    events.sort(key=lambda x: x["over"])
    return events


def _build_timeline_from_fow(
    fmt: str,
    score: int,
    wickets: int,
    overs_done: float,
    fow_events: list[dict[str, Any]],
) -> dict[str, Any]:
    max_overs = FORMAT_RULES[fmt]["max_overs"]
    overs_done = _clamp(overs_done, 0.1, float(max_overs))
    checkpoints: list[float] = []
    whole = int(overs_done)
    checkpoints.extend(float(o) for o in range(1, whole + 1))
    if overs_done > whole:
        checkpoints.append(round(overs_done, 1))
    if not checkpoints:
        checkpoints = [round(overs_done, 1)]

    points = [{"over": 0.0, "score": 0}]
    for e in fow_events:
        if 0 < e["over"] <= overs_done:
            points.append({"over": float(e["over"]), "score": int(e["score"])})
    points.append({"over": overs_done, "score": score})
    points = sorted(points, key=lambda x: x["over"])

    runs: list[int] = []
    wkts: list[int] = []
    wicket_marks: list[float] = []
    for cp in checkpoints:
        left = points[0]
        right = points[-1]
        for i in range(len(points) - 1):
            a = points[i]
            b = points[i + 1]
            if a["over"] <= cp <= b["over"]:
                left, right = a, b
                break
        if right["over"] == left["over"]:
            val = right["score"]
        else:
            frac = (cp - left["over"]) / (right["over"] - left["over"])
            val = left["score"] + ((right["score"] - left["score"]) * frac)
        runs.append(int(round(_clamp(val, 0, score))))
        fall = [e for e in fow_events if e["over"] <= cp]
        wk = max((f["wicket"] for f in fall), default=0)
        wkts.append(int(_clamp(wk, 0, wickets)))
    for e in fow_events:
        if 0 < e["over"] <= overs_done:
            wicket_marks.append(round(e["over"], 1))

    return {
        "labels": [str(c).rstrip("0").rstrip(".") if "." in str(c) else str(int(c)) for c in checkpoints],
        "overs": checkpoints,
        "runs": runs,
        "wickets": wkts,
        "wicket_overs": wicket_marks,
    }


def _extract_team_score_events(text: str, team1: str, team2: str) -> list[dict[str, Any]]:
    pat = re.finditer(
        r"([A-Za-z .&'-]{2,45})\s+(\d{1,3})\s*/\s*(\d{1,2})\s*(?:\(?\s*(\d{1,2}(?:\.\d)?)\s*(?:ov|overs?)\s*\)?)?",
        text,
        flags=re.IGNORECASE,
    )
    out = []
    for m in pat:
        tm = _canonical_team(m.group(1).strip())
        if tm not in {team1, team2}:
            continue
        out.append(
            {
                "team": tm,
                "score": int(m.group(2)),
                "wickets": int(m.group(3)),
                "overs": float(m.group(4)) if m.group(4) else None,
                "pos": m.start(),
            }
        )
    return out


def _events_to_points(events: list[dict[str, Any]], team: str) -> list[dict[str, float]]:
    pts: dict[float, int] = {0.0: 0}
    ordered = sorted([e for e in events if e.get("team") == team and e.get("overs") is not None], key=lambda x: x.get("pos", 0))
    for e in ordered:
        try:
            ov = float(e["overs"])
            sc = int(e["score"])
        except Exception:
            continue
        if ov < 0:
            continue
        ov = round(ov, 1)
        pts[ov] = max(pts.get(ov, 0), sc)
    return [{"over": ov, "score": pts[ov]} for ov in sorted(pts.keys())]


def _build_timeline_from_score_events(
    fmt: str,
    score: int,
    wickets: int,
    overs_done: float,
    score_events: list[dict[str, Any]],
    fow_events: list[dict[str, Any]],
) -> dict[str, Any]:
    max_overs = FORMAT_RULES[fmt]["max_overs"]
    overs_done = _clamp(overs_done, 0.1, float(max_overs))
    checkpoints: list[float] = [float(o) for o in range(1, int(overs_done) + 1)]
    if overs_done > int(overs_done):
        checkpoints.append(round(overs_done, 1))
    if not checkpoints:
        checkpoints = [round(overs_done, 1)]

    points = [{"over": 0.0, "score": 0}]
    compact: dict[float, int] = {}
    for e in score_events:
        try:
            ov = float(e.get("overs", 0.0))
            rs = int(e.get("score", 0))
        except Exception:
            continue
        if 0.0 < ov <= overs_done:
            key = round(ov, 1)
            compact[key] = max(compact.get(key, 0), rs)
    for ov in sorted(compact.keys()):
        points.append({"over": ov, "score": compact[ov]})
    points.append({"over": overs_done, "score": score})
    points = sorted(points, key=lambda x: x["over"])

    runs: list[int] = []
    wkts: list[int] = []
    wicket_marks: list[float] = []
    for cp in checkpoints:
        left = points[0]
        right = points[-1]
        for i in range(len(points) - 1):
            a = points[i]
            b = points[i + 1]
            if a["over"] <= cp <= b["over"]:
                left, right = a, b
                break
        if right["over"] == left["over"]:
            val = right["score"]
        else:
            frac = (cp - left["over"]) / (right["over"] - left["over"])
            val = left["score"] + ((right["score"] - left["score"]) * frac)
        runs.append(int(round(_clamp(val, 0, score))))
        fall = [e for e in fow_events if e["over"] <= cp]
        wk = max((f["wicket"] for f in fall), default=0)
        wkts.append(int(_clamp(wk, 0, wickets)))
    for e in fow_events:
        if 0 < e["over"] <= overs_done:
            wicket_marks.append(round(e["over"], 1))

    return {
        "labels": [str(c).rstrip("0").rstrip(".") if "." in str(c) else str(int(c)) for c in checkpoints],
        "overs": checkpoints,
        "runs": runs,
        "wickets": wkts,
        "wicket_overs": wicket_marks,
    }


def _phase_breakdown_from_timeline(fmt: str, timeline: dict[str, Any]) -> dict[str, dict[str, int]]:
    max_overs = FORMAT_RULES[fmt]["max_overs"]
    if fmt == "t20":
        bins = [("powerplay", 0.0, 6.0), ("middle", 6.0, 15.0), ("death", 15.0, 20.0)]
    else:
        bins = [("powerplay", 0.0, 10.0), ("middle", 10.0, 40.0), ("death", 40.0, float(max_overs))]

    overs = timeline.get("overs", []) if isinstance(timeline, dict) else []
    runs = timeline.get("runs", []) if isinstance(timeline, dict) else []
    if not overs or not runs:
        return {k: {"runs": 0, "wickets": 0} for k, _, _ in bins}

    points = [{"over": 0.0, "score": 0}]
    for ov, rs in zip(overs, runs):
        try:
            points.append({"over": float(ov), "score": int(rs)})
        except Exception:
            continue
    points = sorted(points, key=lambda x: x["over"])
    wk_overs = [float(x) for x in timeline.get("wicket_overs", [])] if isinstance(timeline, dict) else []

    out: dict[str, dict[str, int]] = {}
    for key, lo, hi in bins:
        run_sum = 0.0
        for i in range(len(points) - 1):
            a = points[i]
            b = points[i + 1]
            seg_lo = max(lo, a["over"])
            seg_hi = min(hi, b["over"])
            if seg_hi <= seg_lo:
                continue
            dur = b["over"] - a["over"]
            if dur <= 0:
                continue
            delta = b["score"] - a["score"]
            run_sum += delta * ((seg_hi - seg_lo) / dur)
        wkts = len([w for w in wk_overs if lo < w <= hi])
        out[key] = {"runs": int(round(max(0.0, run_sum))), "wickets": int(max(0, wkts))}
    return out


def _extract_raw_player_names_from_html(html: str) -> list[str]:
    # Try to capture player links from scorecard-style pages.
    names = re.findall(r"/cricketers/[^\"']+[\"'][^>]*>([^<]{2,60})<", html, flags=re.IGNORECASE)
    cleaned = []
    for n in names:
        name = re.sub(r"\s+", " ", unescape(n)).strip()
        if not name:
            continue
        if re.search(r"^(live|scorecard|commentary|table)$", name, flags=re.IGNORECASE):
            continue
        cleaned.append(name)
    # de-dup keep order
    seen = set()
    ordered = []
    for n in cleaned:
        key = n.lower()
        if key in seen:
            continue
        seen.add(key)
        ordered.append(n)
    return ordered


def _map_raw_names_to_local(raw_names: list[str], team: str) -> list[str]:
    squad = TEAM_DATA[team]["squads"]["t20"] + TEAM_DATA[team]["squads"]["odi"]
    exact = {p["name"].lower(): p["name"] for p in squad}
    norm = {_name_key(p["name"]): p["name"] for p in squad}
    out: list[str] = []
    for name in raw_names:
        lk = name.lower()
        nk = _name_key(name)
        mapped = exact.get(lk) or norm.get(nk)
        if mapped and mapped not in out:
            out.append(mapped)
        if len(out) >= 11:
            break
    return out


def _extract_cricbuzz_innings(html: str) -> list[dict[str, Any]]:
    innings: list[dict[str, Any]] = []
    pat = re.finditer(
        r'\\"inningsId\\":(\d+).*?\\"batTeamName\\":\\"([^\\"]+)\\".*?\\"scoreDetails\\":\{.*?\\"overs\\":([0-9]+(?:\.[0-9])?).*?\\"runs\\":([0-9]{1,3}).*?\\"wickets\\":([0-9]{1,2})',
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    for m in pat:
        team = _canonical_team(m.group(2).strip())
        innings.append(
            {
                "innings_id": int(m.group(1)),
                "team": team,
                "overs": float(m.group(3)),
                "score": int(m.group(4)),
                "wickets": int(m.group(5)),
                "pos": m.start(),
            }
        )
    return sorted(innings, key=lambda x: (x["innings_id"], x["pos"]))


def _extract_json_object_after(text: str, marker: str) -> dict[str, Any] | None:
    idx = text.find(marker)
    if idx < 0:
        return None
    start = text.find("{", idx)
    if start < 0:
        return None
    depth = 0
    in_str = False
    esc = False
    end = -1
    for i in range(start, len(text)):
        ch = text[i]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end = i
                break
    if end < 0:
        return None
    block = text[start : end + 1]
    try:
        return json.loads(block)
    except Exception:
        return None


def _extract_cricbuzz_scorecard_data(html: str) -> dict[str, Any] | None:
    raw = html.replace('\\"', '"').replace("\\/", "/")
    data = _extract_json_object_after(raw, "scorecardApiData")
    if isinstance(data, dict) and isinstance(data.get("scoreCard"), list):
        return data
    return None


def _cricbuzz_points_from_innings(innings_obj: dict[str, Any]) -> list[dict[str, float]]:
    pts: dict[float, int] = {0.0: 0}
    sd = innings_obj.get("scoreDetails", {}) if isinstance(innings_obj, dict) else {}
    final_overs = float(sd.get("overs", 0.0) or 0.0)
    final_runs = int(sd.get("runs", 0) or 0)

    pp = innings_obj.get("ppData", {})
    if isinstance(pp, dict):
        for val in pp.values():
            if not isinstance(val, dict):
                continue
            try:
                ov_to = float(val.get("ppOversTo", 0.0) or 0.0)
                runs_scored = int(val.get("runsScored", 0) or 0)
            except Exception:
                continue
            if ov_to > 0:
                pts[round(ov_to, 1)] = max(pts.get(round(ov_to, 1), 0), runs_scored)

    wk = innings_obj.get("wicketsData", {})
    if isinstance(wk, dict):
        for val in wk.values():
            if not isinstance(val, dict):
                continue
            try:
                ov = float(val.get("wktOver", 0.0) or 0.0)
                rs = int(val.get("wktRuns", 0) or 0)
            except Exception:
                continue
            if ov > 0:
                pts[round(ov, 1)] = max(pts.get(round(ov, 1), 0), rs)

    if final_overs > 0:
        pts[round(final_overs, 1)] = max(pts.get(round(final_overs, 1), 0), final_runs)
    return [{"over": ov, "score": pts[ov]} for ov in sorted(pts.keys())]


def _extract_cricbuzz_xi_raw(html: str, team1: str, team2: str) -> tuple[list[str], list[str]]:
    team_names = {team1: [], team2: []}
    for m in re.finditer(r'\\"batTeamName\\":\\"([^\\"]+)\\"(.*?)\\"bowlTeamDetails\\":\{', html, flags=re.IGNORECASE | re.DOTALL):
        team = _canonical_team(m.group(1).strip())
        if team not in team_names:
            continue
        chunk = m.group(2)
        names = re.findall(r'\\"batName\\":\\"([^\\"]+)\\"', chunk, flags=re.IGNORECASE)
        for n in names:
            clean = n.strip()
            if clean and clean not in team_names[team]:
                team_names[team].append(clean)
    for m in re.finditer(r'\\"bowlTeamName\\":\\"([^\\"]+)\\"(.*?)\\"scoreDetails\\":\{', html, flags=re.IGNORECASE | re.DOTALL):
        team = _canonical_team(m.group(1).strip())
        if team not in team_names:
            continue
        chunk = m.group(2)
        names = re.findall(r'\\"bowlName\\":\\"([^\\"]+)\\"', chunk, flags=re.IGNORECASE)
        for n in names:
            clean = n.strip()
            if clean and clean not in team_names[team]:
                team_names[team].append(clean)
    return team_names.get(team1, [])[:11], team_names.get(team2, [])[:11]


def _extract_xi_from_html(html: str, team1: str, team2: str) -> tuple[list[str], list[str], list[str], list[str]]:
    ordered = _extract_raw_player_names_from_html(html)

    squad1 = TEAM_DATA[team1]["squads"]["t20"] + TEAM_DATA[team1]["squads"]["odi"]
    squad2 = TEAM_DATA[team2]["squads"]["t20"] + TEAM_DATA[team2]["squads"]["odi"]
    squad1_exact = {p["name"].lower(): p["name"] for p in squad1}
    squad2_exact = {p["name"].lower(): p["name"] for p in squad2}
    squad1_norm = {_name_key(p["name"]): p["name"] for p in squad1}
    squad2_norm = {_name_key(p["name"]): p["name"] for p in squad2}

    xi1: list[str] = []
    xi2: list[str] = []
    raw1: list[str] = []
    raw2: list[str] = []
    for n in ordered:
        lk = n.lower()
        nk = _name_key(n)
        p1 = squad1_exact.get(lk) or squad1_norm.get(nk)
        p2 = squad2_exact.get(lk) or squad2_norm.get(nk)
        if p1 and p1 not in xi1 and len(xi1) < 11:
            xi1.append(p1)
            raw1.append(n)
            continue
        if p2 and p2 not in xi2 and len(xi2) < 11:
            xi2.append(p2)
            raw2.append(n)
            continue

    return xi1[:11], xi2[:11], raw1[:11], raw2[:11]


def _extract_live_squads_from_html(
    merged_html: str,
    team1: str,
    team2: str,
    xi1_raw: list[str],
    xi2_raw: list[str],
) -> tuple[list[str], list[str]]:
    text = _to_text(merged_html)
    text = re.sub(r"\s+", " ", text).strip()

    def pick_squad(team: str, seed: list[str]) -> list[str]:
        names: list[str] = []
        team_pat = re.escape(team)
        # Capture common "TEAM squad Players ... Bench ..." style sections.
        patterns = [
            rf"{team_pat}\s+squad\s+players\s+(.+?)(?:\s+bench\s+|support staff|{re.escape(team1)}\s+squad|{re.escape(team2)}\s+squad|$)",
            rf"{team_pat}\s+squad\s+(.+?)(?:support staff|{re.escape(team1)}\s+squad|{re.escape(team2)}\s+squad|$)",
        ]
        chunk = ""
        for pat in patterns:
            m = re.search(pat, text, flags=re.IGNORECASE)
            if m:
                chunk = m.group(1)
                break
        if chunk:
            chunk = re.sub(r"\b(players|bench)\b", ",", chunk, flags=re.IGNORECASE)
            for part in chunk.split(","):
                nm = re.sub(r"\s+", " ", part).strip(" .,-")
                if len(nm) < 3:
                    continue
                if re.search(r"support staff|coach|manager|trainer", nm, flags=re.IGNORECASE):
                    continue
                if nm not in names:
                    names.append(nm)

        # Keep XI at top and de-duplicate; cap to practical 18 for display.
        ordered: list[str] = []
        for n in (seed or []) + names:
            if n and n not in ordered:
                ordered.append(n)
        return ordered[:18]

    return pick_squad(team1, xi1_raw), pick_squad(team2, xi2_raw)


def _parse_html_live_state(url: str, html: str) -> dict[str, Any]:
    companion_html = _cross_source_context(url)
    merged_html = f"{html}\n{companion_html}" if companion_html else html
    title_match = re.search(r"<title[^>]*>(.*?)</title>", html, flags=re.IGNORECASE | re.DOTALL)
    title = unescape(title_match.group(1)).strip() if title_match else ""
    og_title = _meta_content(html, "og:title", is_property=True) or ""
    og_desc = _meta_content(html, "og:description", is_property=True) or ""
    tw_title = _meta_content(html, "twitter:title", is_property=False) or ""
    tw_desc = _meta_content(html, "twitter:description", is_property=False) or ""
    corpus = " ".join([title, og_title, og_desc, tw_title, tw_desc, _to_text(merged_html[:500000])])
    corpus = re.sub(r"\s+", " ", corpus).strip()

    team1, team2 = _find_teams_from_text(corpus)
    if not team1 or not team2:
        team1, team2 = _find_teams_from_url(url)
    if not team1 or not team2:
        raise ValueError("Could not detect teams from page content. Try URL mode with field map.")
    if team1 not in TEAM_DATA or team2 not in TEAM_DATA:
        raise ValueError(f"Detected teams '{team1}' vs '{team2}' are not in local dataset.")
    team1_xi, team2_xi, team1_raw_xi, team2_raw_xi = _extract_xi_from_html(merged_html, team1, team2)
    domain = urlparse(url).netloc.lower()
    cb_score_data = _extract_cricbuzz_scorecard_data(html) if "cricbuzz" in domain else None
    cb_innings_objs: list[dict[str, Any]] = []
    cb_points_map: dict[str, list[dict[str, float]]] = {}
    cb_wickets_map: dict[str, int] = {}
    cb_wicket_events_map: dict[str, list[dict[str, Any]]] = {}
    if isinstance(cb_score_data, dict):
        cards = cb_score_data.get("scoreCard", [])
        if isinstance(cards, list):
            for idx, inn in enumerate(cards):
                if not isinstance(inn, dict):
                    continue
                bat = inn.get("batTeamDetails", {}) if isinstance(inn.get("batTeamDetails"), dict) else {}
                sd = inn.get("scoreDetails", {}) if isinstance(inn.get("scoreDetails"), dict) else {}
                tm = _canonical_team(bat.get("batTeamName", ""))
                if tm not in {team1, team2}:
                    continue
                cb_innings_objs.append(
                    {
                        "innings_id": int(inn.get("inningsId", idx + 1) or (idx + 1)),
                        "team": tm,
                        "score": int(sd.get("runs", 0) or 0),
                        "wickets": int(sd.get("wickets", 0) or 0),
                        "overs": float(sd.get("overs", 0.0) or 0.0),
                        "pos": idx + 1,
                        "obj": inn,
                    }
                )
                cb_points_map[tm] = _cricbuzz_points_from_innings(inn)
                cb_wickets_map[tm] = int(sd.get("wickets", 0) or 0)
                wk_events: list[dict[str, Any]] = []
                wk_data = inn.get("wicketsData", {}) if isinstance(inn.get("wicketsData"), dict) else {}
                for widx, val in enumerate(wk_data.values(), start=1):
                    if not isinstance(val, dict):
                        continue
                    try:
                        ov = float(val.get("wktOver", 0.0) or 0.0)
                        rs = int(val.get("wktRuns", 0) or 0)
                        wn = int(val.get("wktNbr", widx) or widx)
                    except Exception:
                        continue
                    if ov > 0:
                        wk_events.append({"score": rs, "wicket": wn, "over": ov})
                wk_events.sort(key=lambda x: x["over"])
                cb_wicket_events_map[tm] = wk_events
    if "cricbuzz" in domain:
        cb_raw1, cb_raw2 = _extract_cricbuzz_xi_raw(html, team1, team2)
        if cb_raw1:
            team1_raw_xi = cb_raw1
            team1_xi = _map_raw_names_to_local(cb_raw1, team1)
        if cb_raw2:
            team2_raw_xi = cb_raw2
            team2_xi = _map_raw_names_to_local(cb_raw2, team2)
    team1_squad_raw, team2_squad_raw = _extract_live_squads_from_html(merged_html, team1, team2, team1_raw_xi, team2_raw_xi)

    fmt = _infer_format(corpus, url=url)
    events = _extract_team_score_events(corpus, team1, team2)
    if cb_innings_objs:
        events = [
            {
                "team": c["team"],
                "score": c["score"],
                "wickets": c["wickets"],
                "overs": c["overs"],
                "pos": c["pos"],
            }
            for c in cb_innings_objs
        ]
    cb_current_innings_obj: dict[str, Any] | None = None
    if not events:
        score_tuple = _extract_score_tuple(corpus)
        if not score_tuple:
            raise ValueError("Could not detect live score from page content.")
        score, wickets, overs = score_tuple
        batting_team = _extract_batting_team_from_text(corpus) or team1
        if batting_team not in {team1, team2}:
            batting_team = team1
    else:
        by_team: dict[str, list[dict[str, Any]]] = {team1: [], team2: []}
        for e in events:
            by_team[e["team"]].append(e)

        for tm in (team1, team2):
            by_team[tm] = sorted(by_team[tm], key=lambda x: x["pos"])

        target_hint = _extract_target(corpus)
        batting_team = ""
        if target_hint is not None:
            t1_last = by_team[team1][-1] if by_team[team1] else None
            t2_last = by_team[team2][-1] if by_team[team2] else None
            first_team = None
            if t1_last and t1_last["score"] + 1 == target_hint:
                first_team = team1
            elif t2_last and t2_last["score"] + 1 == target_hint:
                first_team = team2
            if first_team:
                batting_team = team2 if first_team == team1 else team1
                if not by_team.get(batting_team):
                    batting_team = first_team
        if not batting_team:
            bt = _extract_batting_team_from_text(corpus)
            if bt in {team1, team2} and by_team.get(bt):
                batting_team = bt
        if not batting_team:
            last_t1 = by_team[team1][-1] if by_team[team1] else None
            last_t2 = by_team[team2][-1] if by_team[team2] else None
            if last_t1 and last_t2:
                batting_team = team1 if last_t1["pos"] >= last_t2["pos"] else team2
            else:
                batting_team = team1 if last_t1 else team2

        latest = by_team[batting_team][-1]
        score = latest["score"]
        wickets = latest["wickets"]
        overs = latest["overs"] or 0.0
        if cb_innings_objs:
            same_team = [c for c in cb_innings_objs if c["team"] == batting_team]
            if same_team:
                cb_current_innings_obj = sorted(same_team, key=lambda x: x["innings_id"])[-1].get("obj")

    target = _extract_target(corpus)
    bowling_team = team2 if batting_team == team1 else team1
    toss_winner, toss_decision = _extract_toss_info(corpus)
    if toss_winner == "Auto":
        toss_winner, toss_decision = _extract_toss_info_from_raw_html(html)
    venue = _extract_venue_from_text(corpus) or _extract_venue_from_raw_html(html)
    max_overs = FORMAT_RULES[fmt]["max_overs"]
    if cb_current_innings_obj and isinstance(cb_current_innings_obj.get("scoreDetails"), dict):
        try:
            cb_ov = float(cb_current_innings_obj["scoreDetails"].get("overs", 0.0) or 0.0)
            if cb_ov > 0:
                overs = cb_ov
        except Exception:
            pass
    if overs <= 0:
        overs = _extract_exact_innings_overs(corpus, batting_team, score, wickets, fmt) or 0.0
    if overs <= 0:
        overs = _extract_max_overs_hint(corpus, fmt) or 0.1
    fow = cb_wicket_events_map.get(batting_team, []) or _extract_fow_events(corpus)
    if wickets >= 10 and fow:
        last_wkt_over = max(float(e.get("over", 0.0)) for e in fow)
        if 0.0 < last_wkt_over <= float(max_overs):
            if overs <= 0.5 or overs >= float(max_overs):
                overs = last_wkt_over

    innings_complete = bool(re.search(r"\bwon by\b|\bmatch tied\b|\bresult\b|\binnings break\b|\bstumps\b", corpus, flags=re.IGNORECASE)) or wickets >= 10 or overs >= max_overs
    if innings_complete and wickets >= 10 and overs <= 0.5:
        overs = _extract_exact_innings_overs(corpus, batting_team, score, wickets, fmt) or overs
    if innings_complete and overs <= 0.5:
        hints = _extract_overs_hints(corpus, fmt)
        if hints:
            overs = min(hints)
    innings_events = [e for e in events if e["team"] == batting_team and e.get("overs") is not None]
    if cb_points_map.get(batting_team):
        innings_events = [{"score": int(p["score"]), "overs": float(p["over"]), "team": batting_team, "pos": i} for i, p in enumerate(cb_points_map[batting_team])]
    timeline = _build_timeline_from_score_events(fmt, score, wickets, overs, innings_events, fow) if innings_events else _build_timeline_from_fow(fmt, score, wickets, overs, fow)
    team1_points = cb_points_map.get(team1) or _events_to_points(events, team1)
    team2_points = cb_points_map.get(team2) or _events_to_points(events, team2)
    team1_w = cb_wickets_map.get(team1, max([int(e.get("wickets", 0)) for e in events if e.get("team") == team1] or [0]))
    team2_w = cb_wickets_map.get(team2, max([int(e.get("wickets", 0)) for e in events if e.get("team") == team2] or [0]))
    team_timelines = {
        team1: _build_timeline_from_score_events(
            fmt,
            int(team1_points[-1]["score"]) if team1_points else 0,
            team1_w,
            float(team1_points[-1]["over"]) if team1_points else 0.1,
            [{"score": int(p["score"]), "overs": float(p["over"]), "team": team1, "pos": i} for i, p in enumerate(team1_points)],
            cb_wicket_events_map.get(team1, []),
        ) if len(team1_points) >= 2 else {"overs": [], "runs": [], "wicket_overs": []},
        team2: _build_timeline_from_score_events(
            fmt,
            int(team2_points[-1]["score"]) if team2_points else 0,
            team2_w,
            float(team2_points[-1]["over"]) if team2_points else 0.1,
            [{"score": int(p["score"]), "overs": float(p["over"]), "team": team2, "pos": i} for i, p in enumerate(team2_points)],
            cb_wicket_events_map.get(team2, []),
        ) if len(team2_points) >= 2 else {"overs": [], "runs": [], "wicket_overs": []},
    }
    scoring_breakdown = {
        team1: _phase_breakdown_from_timeline(fmt, team_timelines.get(team1, {})),
        team2: _phase_breakdown_from_timeline(fmt, team_timelines.get(team2, {})),
    }

    # infer target when scorecard has both innings but no explicit target text
    if target is None and len(events) >= 2:
        prior = [e for e in events if e["team"] != batting_team]
        if prior:
            target = int(prior[-1]["score"] + 1)

    page_title = title or og_title or tw_title or f"{team1} vs {team2}"
    if "|" in page_title:
        page_title = page_title.split("|", 1)[0].strip()
    page_title = re.sub(r"\s+", " ", page_title).strip()
    if len(page_title) > 120:
        page_title = f"{team1} vs {team2}"
    if "cricbuzz" in domain and ("scorecard" in page_title.lower() or "cricket scorecard" in page_title.lower()):
        page_title = f"{team1} vs {team2}"

    return {
        "id": "html_feed",
        "title": page_title,
        "format": fmt,
        "team1": team1,
        "team2": team2,
        "batting_team": batting_team,
        "bowling_team": bowling_team,
        "score": max(0, score),
        "wickets": int(_clamp(wickets, 0, 10)),
        "overs": max(0.0, overs),
        "target": target,
        "venue": venue,
        "pitch": "Balanced surface",
        "weather": "Clear",
        "toss_winner": toss_winner,
        "toss_decision": toss_decision,
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "provider": "espn_html" if "espn" in domain else ("cricbuzz_html" if "cricbuzz" in domain else "generic"),
        "ingestion_source": "url_html",
        "team1_xi": team1_xi,
        "team2_xi": team2_xi,
        "team1_xi_raw": team1_raw_xi,
        "team2_xi_raw": team2_raw_xi,
        "team1_squad_raw": team1_squad_raw,
        "team2_squad_raw": team2_squad_raw,
        "raw_player_names": _extract_raw_player_names_from_html(merged_html)[:60],
        "innings_complete": innings_complete,
        "innings_timeline": timeline,
        "team_progress_points": {team1: team1_points, team2: team2_points},
        "team_timelines": team_timelines,
        "scoring_breakdown": scoring_breakdown,
        "fow_events": fow,
    }


def _json_pick(data: Any, keys: list[str], fallback: Any = None) -> Any:
    for k in keys:
        val = _extract_path(data, k)
        if val not in (None, ""):
            return val
    return fallback


def ingest_live_state(payload: dict[str, Any]) -> dict[str, Any]:
    source = str(payload.get("source", "demo")).strip().lower()
    if source == "demo":
        match_id = str(payload.get("match_id", "demo_t20_1"))
        match = next((m for m in DEMO_LIVE_MATCHES if m["id"] == match_id), None)
        if not match:
            raise ValueError("Unknown demo match id")
        team1 = match["team1"]
        team2 = match["team2"]
        return {
            **match,
            "ingestion_source": "demo",
            "team1_xi": [p["name"] for p in TEAM_DATA[team1]["squads"]["t20"][:11]],
            "team2_xi": [p["name"] for p in TEAM_DATA[team2]["squads"]["t20"][:11]],
            "team1_squad_raw": [p["name"] for p in TEAM_DATA[team1]["squads"][fmt][:15]],
            "team2_squad_raw": [p["name"] for p in TEAM_DATA[team2]["squads"][fmt][:15]],
            "innings_complete": False,
            "innings_timeline": _build_timeline_from_fow(
                fmt, max(0, score), int(_clamp(wickets, 0, 10)), max(0.1, overs), []
            ),
        }

    if source == "url":
        url = str(payload.get("url", "")).strip()
        if not url:
            raise ValueError("Provide a URL for live ingestion")
        if not (url.startswith("http://") or url.startswith("https://")):
            raise ValueError("URL must start with http:// or https://")
        provider = str(payload.get("provider", "generic")).strip().lower()
        url, provider = _normalize_live_url(url, provider)
        domain = urlparse(url).netloc.lower()
        if provider == "generic":
            if "espn" in domain:
                provider = "espn_html"
            elif "cricbuzz" in domain:
                provider = "cricbuzz_html"
        profile = LIVE_PROVIDER_PROFILES.get(provider, LIVE_PROVIDER_PROFILES["generic"])
        headers: dict[str, str] = {"User-Agent": "CricketPredictorPro/1.0", "Accept": "application/json"}
        custom_headers = payload.get("headers")
        if isinstance(custom_headers, dict):
            headers.update({str(k): str(v) for k, v in custom_headers.items()})
        api_key_env = str(payload.get("api_key_env", ""))
        api_key = str(payload.get("api_key", "")) or (os.environ.get(api_key_env, "") if api_key_env else "")
        if api_key:
            auth_header = str(payload.get("api_key_header", "Authorization"))
            auth_prefix = str(payload.get("api_key_prefix", "Bearer "))
            headers[auth_header] = f"{auth_prefix}{api_key}" if auth_prefix is not None else api_key

        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=12) as resp:
                raw = resp.read()
                content_type = str(resp.headers.get("Content-Type", "")).lower()
        except Exception as exc:
            raise ValueError(f"Unable to fetch live URL: {exc}") from exc
        body = raw.decode("utf-8", errors="ignore")
        is_json_like = "application/json" in content_type or body.lstrip().startswith("{") or body.lstrip().startswith("[")
        if provider in {"espn_html", "cricbuzz_html"} or not is_json_like:
            return _parse_html_live_state(url, body)
        try:
            data = json.loads(body)
        except Exception as exc:
            raise ValueError("Live URL response is not valid JSON (or use provider=espn_html/cricbuzz_html)") from exc
        root_path = str(payload.get("root_path", "")).strip()
        root_candidates = [root_path] if root_path else list(profile.get("root_paths", [""]))
        root_data = None
        for cand in root_candidates:
            candidate = _extract_path(data, cand)
            if candidate is not None:
                root_data = candidate
                break
        if root_data is None:
            root_data = data
        if isinstance(root_data, list):
            best = None
            for item in root_data:
                if not isinstance(item, dict):
                    continue
                if item.get("matchStarted") is True and item.get("matchEnded") is not True:
                    best = item
                    break
                if best is None:
                    best = item
            if best is not None:
                root_data = best

        profile_fields = dict(profile.get("fields", {}))
        user_field_map = payload.get("field_map")
        if isinstance(user_field_map, dict):
            for k, v in user_field_map.items():
                if isinstance(v, list):
                    profile_fields[str(k)] = [str(x) for x in v]
                else:
                    profile_fields[str(k)] = [str(v)]

        def pick_field(name: str, default: Any = None) -> Any:
            keys = profile_fields.get(name, [])
            return _json_pick(root_data, keys, default)

        def as_float(v: Any, default: float = 0.0) -> float:
            try:
                return float(v)
            except (TypeError, ValueError):
                return default

        def as_int(v: Any, default: int = 0) -> int:
            try:
                return int(float(v))
            except (TypeError, ValueError):
                return default

        raw_fmt = str(pick_field("format", "") or "").strip().lower()
        if raw_fmt:
            fmt = format_key(raw_fmt)
        else:
            fmt = _infer_format("", url=url)
        team1 = _canonical_team(pick_field("team1", ""))
        team2 = _canonical_team(pick_field("team2", ""))
        batting_team = _canonical_team(pick_field("batting_team", team1))
        bowling_team = _canonical_team(pick_field("bowling_team", team2))
        score = as_int(pick_field("score", 0), 0)
        wickets = as_int(pick_field("wickets", 0), 0)
        overs = as_float(pick_field("overs", 0.0), 0.0)
        target = pick_field("target", None)
        venue = str(pick_field("venue", "")).strip() or None
        pitch = str(pick_field("pitch", "Balanced surface"))
        weather = str(pick_field("weather", "Clear"))
        toss_winner = _canonical_team(pick_field("toss_winner", "Auto"))
        toss_decision = str(pick_field("toss_decision", "auto")).strip().lower()

        if team1 not in TEAM_DATA or team2 not in TEAM_DATA:
            raise ValueError(
                f"Ingested teams not supported: '{team1}' vs '{team2}'. Use supported dataset teams or provide field_map/team aliases."
            )

        return {
            "id": "url_feed",
            "title": str(pick_field("title", f"{team1} vs {team2}")),
            "format": fmt,
            "team1": team1,
            "team2": team2,
            "batting_team": batting_team,
            "bowling_team": bowling_team,
            "score": max(0, score),
            "wickets": int(_clamp(wickets, 0, 10)),
            "overs": max(0.0, overs),
            "target": as_int(target, 0) if target not in (None, "") else None,
            "venue": venue,
            "pitch": pitch,
            "weather": weather,
            "toss_winner": toss_winner if toss_winner else "Auto",
            "toss_decision": toss_decision if toss_decision in {"auto", "bat", "bowl"} else "auto",
            "last_updated": str(pick_field("last_updated", datetime.now(timezone.utc).isoformat())),
            "provider": provider,
            "ingestion_source": "url",
            "team1_xi": [p["name"] for p in TEAM_DATA[team1]["squads"]["t20"][:11]],
            "team2_xi": [p["name"] for p in TEAM_DATA[team2]["squads"]["t20"][:11]],
            "team1_squad_raw": [p["name"] for p in TEAM_DATA[team1]["squads"][fmt][:15]],
            "team2_squad_raw": [p["name"] for p in TEAM_DATA[team2]["squads"][fmt][:15]],
        }

    raise ValueError("Unsupported ingestion source")


def uncertainty_fan(payload: dict[str, Any]) -> dict[str, Any]:
    fmt = format_key(payload.get("format"))
    rules = FORMAT_RULES[fmt]
    max_overs = rules["max_overs"]
    score = int(payload.get("score", 0))
    wickets = int(payload.get("wickets", 0))
    overs = float(payload.get("overs", 0.0))
    if score < 0:
        raise ValueError("Score cannot be negative")
    if wickets < 0 or wickets > 10:
        raise ValueError("Wickets should be between 0 and 10")

    pred = predict_score(payload)
    traj = run_trajectory({"format": fmt, "score": score, "wickets": wickets, "overs": overs})
    balls_done = overs_to_balls(overs, max_overs)
    current_label = f"{balls_done // 6}.{balls_done % 6}"
    labels = [current_label]
    low = [score]
    avg = [score]
    high = [score]

    max_proj = len(traj["projected"])
    for idx, over_label in enumerate(traj["labels"]):
        over_num = int(over_label)
        phase = over_num / max_overs
        phase_spread = 0.16 - (phase * 0.085)
        wicket_spread = max(0.0, wickets - 5) * 0.008
        horizon_spread = (max_proj - idx) / max(1, max_proj) * 0.035
        spread = _clamp(phase_spread + wicket_spread + horizon_spread, 0.045, 0.26 if fmt == "t20" else 0.22)
        a = traj["projected"][idx]
        l = max(score, int(round(a * (1 - spread))))
        h = max(a, int(round(a * (1 + spread))))
        labels.append(over_label)
        low.append(l)
        avg.append(a)
        high.append(h)

    low[-1] = min(low[-1], pred["low"])
    avg[-1] = pred["avg"]
    high[-1] = max(high[-1], pred["high"])
    return {
        "labels": labels,
        "low": low,
        "avg": avg,
        "high": high,
    }


def _pdf_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _simple_text_pdf(lines: list[str]) -> bytes:
    content = "BT\n/F1 11 Tf\n40 790 Td\n14 TL\n"
    for i, line in enumerate(lines):
        if i > 0:
            content += "T*\n"
        content += f"({_pdf_escape(line)}) Tj\n"
    content += "ET\n"
    stream = content.encode("latin-1", errors="replace")

    objects: list[bytes] = []
    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    objects.append(b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
    objects.append(b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>")
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    objects.append(f"<< /Length {len(stream)} >>\nstream\n".encode("latin-1") + stream + b"endstream")

    pdf = b"%PDF-1.4\n"
    offsets = [0]
    for idx, obj in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf += f"{idx} 0 obj\n".encode("latin-1") + obj + b"\nendobj\n"
    xref_pos = len(pdf)
    pdf += f"xref\n0 {len(objects) + 1}\n".encode("latin-1")
    pdf += b"0000000000 65535 f \n"
    for off in offsets[1:]:
        pdf += f"{off:010d} 00000 n \n".encode("latin-1")
    pdf += f"trailer << /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n".encode("latin-1")
    return pdf


def reproducibility_pdf(payload: dict[str, Any]) -> bytes:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines = [
        "Cricket Predictor Pro - Reproducibility Report",
        f"Generated: {now}",
        f"Format: {payload.get('format', '-')}",
        f"Teams: {payload.get('team1', '-')} vs {payload.get('team2', '-')}",
        f"Venue: {payload.get('venue', '-')}, Pitch: {payload.get('pitch', '-')}, Weather: {payload.get('weather', '-')}",
        "",
        "Inputs:",
        f"Score: {payload.get('score', '-')}/{payload.get('wickets', '-')} in {payload.get('overs', '-')} overs",
        f"Target: {payload.get('target', '-')}",
        "",
        "Outputs:",
        f"Score Range: {payload.get('score_low', '-')} - {payload.get('score_avg', '-')} - {payload.get('score_high', '-')}",
        f"Win Probability: {payload.get('win_prob', '-')}",
        f"Backtest MAE/RMSE: {payload.get('backtest_mae', '-')} / {payload.get('backtest_rmse', '-')}",
        f"Model Confidence: {payload.get('confidence', '-')}",
        "",
        "Note: This report captures current UI state for reproducibility and viva/demo evidence.",
    ]
    return _simple_text_pdf(lines)


def viva_report_pdf(payload: dict[str, Any]) -> bytes:
    live = payload.get("live", {}) if isinstance(payload.get("live"), dict) else {}
    insights = str(payload.get("insight", ""))
    analytics = payload.get("analytics", {}) if isinstance(payload.get("analytics"), dict) else {}
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines = [
        "Cricket Predictor Pro - Viva Demo Report",
        f"Generated: {now}",
        "",
        "Live Snapshot:",
        f"Title: {live.get('title', '-')}",
        f"Format: {str(live.get('format', '-')).upper()}",
        f"Teams: {live.get('team1', '-')} vs {live.get('team2', '-')}",
        f"Current: {live.get('batting_team', '-')} {live.get('score', '-')}/{live.get('wickets', '-')} ({live.get('overs', '-')})",
        f"Toss: {live.get('toss_winner', '-')} / {live.get('toss_decision', '-')}",
        f"Venue: {live.get('venue', '-')}",
        "",
        "Model + Method:",
        "- Live scrape from scorecard/statistics pages",
        "- Deterministic cricket engine (phase, wicket, venue, toss, XI signals)",
        "- AI narrative synthesis for explainable match insight",
        "",
        "Quality + Confidence:",
        f"Data quality: {analytics.get('data_quality', {}).get('score', '-')}",
        f"Prediction confidence: {analytics.get('confidence', {}).get('score', '-')}",
        "",
        "Coach Notes:",
    ]
    for note in analytics.get("coach_notes", [])[:5]:
        lines.append(f"- {note}")
    lines += ["", "AI Match Insight:"]
    if insights.strip():
        for ln in insights.splitlines()[:14]:
            lines.append(ln[:120])
    else:
        lines.append("- Not available")
    lines += [
        "",
        "Disclaimer:",
        "This report is educational and analytical, not a guarantee of outcomes.",
    ]
    return _simple_text_pdf(lines)


def _player_role(team: str, player_name: str) -> str:
    all_players = TEAM_DATA[team]["squads"]["t20"] + TEAM_DATA[team]["squads"]["odi"]
    for p in all_players:
        if p["name"] == player_name:
            return str(p.get("role", "Player"))
    return "Player"


def live_analytics_pack(payload: dict[str, Any]) -> dict[str, Any]:
    live = payload.get("live")
    if not isinstance(live, dict):
        raise ValueError("Live payload missing for analytics pack.")
    fmt = format_key(live.get("format"))
    max_overs = FORMAT_RULES[fmt]["max_overs"]
    score = int(live.get("score", 0) or 0)
    wickets = int(live.get("wickets", 0) or 0)
    overs = float(live.get("overs", 0.0) or 0.0)
    target = live.get("target")
    team1 = str(live.get("team1", "Team 1"))
    team2 = str(live.get("team2", "Team 2"))
    batting = str(live.get("batting_team", team1))
    bowling = team2 if batting == team1 else team1

    crr = (score / overs) if overs > 0 else 0.0
    rrr = None
    if target not in (None, ""):
        try:
            tgt = float(target)
            remain_overs = max(0.1, max_overs - overs)
            remain_runs = max(0.0, tgt - score)
            rrr = remain_runs / remain_overs
        except Exception:
            rrr = None

    fields = ["team1", "team2", "batting_team", "score", "wickets", "overs", "venue", "toss_winner", "toss_decision", "team_timelines", "scoring_breakdown"]
    present = sum(1 for f in fields if live.get(f) not in (None, "", [], {}))
    data_quality = int(round((present / len(fields)) * 100))

    progress = _clamp(overs / max_overs, 0.0, 1.0)
    confidence = int(round(_clamp(40 + (progress * 35) + (data_quality * 0.25) - max(0, wickets - 7) * 2.5, 35, 96)))

    pressure_raw = 0.0
    if rrr is not None:
        pressure_raw = rrr - crr
    else:
        pressure_raw = (wickets - 3) * 0.2
    pressure_score = int(round(_clamp(50 + (pressure_raw * 14), 1, 99)))

    timeline = live.get("team_timelines", {}).get(batting, {}) if isinstance(live.get("team_timelines"), dict) else {}
    tl_overs = timeline.get("overs", []) if isinstance(timeline, dict) else []
    tl_runs = timeline.get("runs", []) if isinstance(timeline, dict) else []
    wk_overs = timeline.get("wicket_overs", []) if isinstance(timeline, dict) else []
    wk_set: set[float] = set()
    for w in wk_overs:
        try:
            wk_set.add(round(float(w), 1))
        except Exception:
            continue
    momentum = []
    prev = 0
    for ov, rs in zip(tl_overs, tl_runs):
        try:
            over_num = float(ov)
            now = int(rs)
        except Exception:
            continue
        delta = max(0, now - prev)
        prev = now
        flag = ""
        if round(over_num, 1) in wk_set:
            flag = "W"
        momentum.append({"over": round(over_num, 1), "runs": delta, "event": flag})

    commentary = []
    for m in momentum[-10:]:
        label = "quiet over"
        if m["runs"] >= 14:
            label = "explosive over"
        elif m["runs"] >= 9:
            label = "strong scoring over"
        elif m["runs"] <= 3:
            label = "pressure over"
        wtxt = " with wicket" if m["event"] == "W" else ""
        commentary.append(f"Over {m['over']}: {m['runs']} runs, {label}{wtxt}.")

    fow = live.get("fow_events", []) if isinstance(live.get("fow_events"), list) else []
    partnerships: list[dict[str, Any]] = []
    prev_score = 0
    prev_over = 0.0
    prev_w = 0
    for ev in fow:
        try:
            w = int(ev.get("wicket", prev_w + 1))
            sc = int(ev.get("score", prev_score))
            ov = float(ev.get("over", prev_over))
        except Exception:
            continue
        partnerships.append(
            {
                "label": f"W{prev_w + 1} stand",
                "runs": max(0, sc - prev_score),
                "balls": max(1, int(round((ov - prev_over) * 6))),
            }
        )
        prev_score, prev_over, prev_w = sc, ov, w

    if score > prev_score:
        partnerships.append(
            {
                "label": f"W{prev_w + 1} stand",
                "runs": max(0, score - prev_score),
                "balls": max(1, int(round((max(overs, prev_over) - prev_over) * 6))),
            }
        )
    partnerships = sorted(partnerships, key=lambda x: x["runs"], reverse=True)[:6]

    # Similarity finder: combine in-match historical states + reference library.
    refs = [
        {"match": "IND vs AUS ODI 2023", "score": 286, "wickets": 8, "overs": 50.0, "result": "Defended by 12", "final": "286/8"},
        {"match": "PAK vs BAN ODI 2026", "score": 279, "wickets": 10, "overs": 50.0, "result": "Lost by 11", "final": "279/10"},
        {"match": "NZ vs SA T20 2026", "score": 173, "wickets": 8, "overs": 20.0, "result": "Won by 67", "final": "173/8"},
        {"match": "ENG vs PAK T20 2024", "score": 166, "wickets": 7, "overs": 20.0, "result": "Won by 9", "final": "166/7"},
        {"match": "AUS vs IND ODI 2024", "score": 302, "wickets": 9, "overs": 50.0, "result": "Won by 4", "final": "302/9"},
    ]
    in_match_states: list[dict[str, Any]] = []
    if isinstance(live.get("team_timelines"), dict):
        for team, tl in live.get("team_timelines", {}).items():
            if not isinstance(tl, dict):
                continue
            ovs = tl.get("overs", []) if isinstance(tl.get("overs"), list) else []
            rns = tl.get("runs", []) if isinstance(tl.get("runs"), list) else []
            wk_ov = []
            if isinstance(tl.get("wicket_overs"), list):
                for x in tl.get("wicket_overs"):
                    try:
                        wk_ov.append(float(x))
                    except Exception:
                        continue
            if not ovs or not rns:
                continue
            final_score = int(rns[-1])
            final_wk = len([w for w in wk_ov if w <= float(ovs[-1])])
            for ov, rs in zip(ovs, rns):
                try:
                    ovf = float(ov)
                    rsi = int(rs)
                except Exception:
                    continue
                if ovf <= 0:
                    continue
                wk_at = len([w for w in wk_ov if w <= ovf])
                # skip the exact current state to avoid trivial 100% similarity card.
                if team == batting and abs(ovf - overs) < 0.25 and abs(rsi - score) <= 2 and abs(wk_at - wickets) <= 0:
                    continue
                in_match_states.append(
                    {
                        "match": f"{team} (same match)",
                        "score": rsi,
                        "wickets": wk_at,
                        "overs": ovf,
                        "result": "In-match reference state",
                        "final": f"{final_score}/{final_wk}",
                    }
                )
    bank = in_match_states + refs
    sims = []
    for r in bank:
        d = abs(r["score"] - score) + (abs(r["wickets"] - wickets) * 11) + abs((r["overs"] / max_overs) - (overs / max_overs)) * 45
        similarity = int(round(_clamp(100.0 - (d * 0.45), 1.0, 99.0)))
        sims.append(
            {
                "match": r["match"],
                "distance": round(d, 1),
                "similarity": similarity,
                "result": r["result"],
                "final_score": r["final"],
                "at_compare_point": f"{r['score']}/{r['wickets']} ({r['overs']})",
            }
        )
    sims = sorted(sims, key=lambda x: x["distance"])[:5]

    # Bowler matchup hints (from known squad roles for the bowling team).
    bowlers = []
    live_bowl_xi = live.get("team1_xi", []) if bowling == team1 else live.get("team2_xi", [])
    if isinstance(live_bowl_xi, list):
        for name in live_bowl_xi:
            role = _player_role(bowling, str(name))
            if "Bowler" in role or "All-Rounder" in role:
                bowlers.append({"name": name, "role": role})
    bowlers = bowlers[:5]
    bowler_matchups = [
        {
            "bowler": b["name"],
            "phase": "Powerplay" if i < 2 else ("Middle" if i < 4 else "Death"),
            "note": "Use attacking fields" if i < 2 else ("Squeeze singles" if i < 4 else "Yorker-heavy finish"),
        }
        for i, b in enumerate(bowlers)
    ]

    coach_notes = [
        f"{batting}: preserve wickets till over {15 if fmt == 't20' else 35} and target acceleration after that.",
        f"{bowling}: deploy best death option by over {16 if fmt == 't20' else 41}.",
        f"Pressure meter is {pressure_score}/100; {'focus strike rotation' if pressure_score > 62 else 'maintain tempo with low-risk boundaries'}.",
    ]

    return {
        "confidence": {"score": confidence, "label": "High" if confidence >= 75 else ("Medium" if confidence >= 55 else "Low")},
        "data_quality": {"score": data_quality, "label": "Reliable" if data_quality >= 75 else ("Partial" if data_quality >= 55 else "Sparse")},
        "pressure_meter": {"score": pressure_score, "crr": round(crr, 2), "rrr": round(rrr, 2) if rrr is not None else None},
        "momentum_strip": momentum,
        "mini_commentary": commentary,
        "partnership_impact": partnerships,
        "similar_matches": sims,
        "similarity_metric_note": "Similarity % compares runs, wickets, and overs progression. 100% is very close; lower values mean less similar.",
        "bowler_matchups": bowler_matchups,
        "coach_notes": coach_notes,
    }


def win_probability(payload: dict[str, Any]) -> dict[str, Any]:
    fmt = format_key(payload.get("format"))
    rules = FORMAT_RULES[fmt]
    warnings: list[str] = []

    target = int(payload.get("target", 0))
    score = int(payload.get("score", 0))
    wickets = int(payload.get("wickets", 0))
    if target <= 0:
        raise ValueError("Target must be greater than 0")
    if score < 0:
        raise ValueError("Score cannot be negative")
    if score > target + (12 if fmt == "t20" else 25):
        raise ValueError("Current score is unrealistically higher than target")
    balls_bowled = overs_to_balls(float(payload.get("overs", 0.0)), rules["max_overs"])
    balls_left = (rules["max_overs"] * 6) - balls_bowled

    if wickets < 0 or wickets > 10:
        raise ValueError("Wickets should be between 0 and 10")

    runs_needed = max(0, target - score)
    crr = (score / (balls_bowled / 6.0)) if balls_bowled > 0 else 0.0
    rrr = (runs_needed / (balls_left / 6.0)) if balls_left > 0 else math.inf

    if runs_needed == 0:
        warnings.append("Target already achieved.")
        return {"win_prob": 100, "runs_needed": 0, "balls_left": balls_left, "crr": round(crr, 2), "rrr": 0.0, "warnings": warnings}
    if wickets >= 10 or balls_left <= 0:
        warnings.append("Chasing side innings completed.")
        return {"win_prob": 0, "runs_needed": runs_needed, "balls_left": 0, "crr": round(crr, 2), "rrr": None, "warnings": warnings}

    chasing_team = str(payload.get("chasing_team", ""))
    bowling_team = str(payload.get("bowling_team", ""))

    chase_xi = pick_players(get_team_players(chasing_team, fmt), payload.get("chasing_xi", []))
    bowl_xi = pick_players(get_team_players(bowling_team, fmt), payload.get("bowling_xi", []))

    chase_strength = team_breakdown(chase_xi, fmt)
    bowl_strength = team_breakdown(bowl_xi, fmt)
    chase_xi_check = xi_validator(chase_xi, fmt)

    pressure = (rrr - crr)
    base = 50.0 - (pressure * (13 if fmt == "t20" else 9))
    base += (10 - wickets) * 3.8
    base += (balls_left / (rules["max_overs"] * 6) - 0.5) * 18.0
    base += (chase_strength["overall"] - bowl_strength["overall"]) * 0.35
    base *= 1 + toss_adjustment(
        fmt,
        payload.get("toss_winner"),
        payload.get("toss_decision"),
        chasing_team=chasing_team,
    )

    dew_bonus = next((w["chasing_impact"] for w in WEATHER_TYPES if w["label"] == payload.get("weather")), 0.0)
    base *= 1 + dew_bonus

    prob = int(round(max(1, min(99, base))))
    return {
        "win_prob": prob,
        "runs_needed": runs_needed,
        "balls_left": balls_left,
        "crr": round(crr, 2),
        "rrr": round(rrr, 2),
        "warnings": warnings + chase_xi_check["warnings"],
        "xi_validation": chase_xi_check,
        "toss_impact": toss_impact(fmt, payload.get("venue"), payload.get("weather")),
    }


def dls_target(payload: dict[str, Any]) -> dict[str, Any]:
    fmt = format_key(payload.get("format"))
    max_overs = FORMAT_RULES[fmt]["max_overs"]
    warnings: list[str] = []

    first_score = int(payload.get("first_innings_score", 0))
    if first_score <= 0:
        raise ValueError("First innings score must be positive")

    first_overs = float(payload.get("first_innings_overs", max_overs))
    second_overs = float(payload.get("second_innings_overs", max_overs))
    second_wickets = int(payload.get("second_innings_wickets", 0))
    play_stopped_over = payload.get("play_stopped_over")
    wickets_at_stop = payload.get("wickets_at_stop")
    revised_total_overs = payload.get("revised_total_overs")

    if second_wickets < 0 or second_wickets > 10:
        raise ValueError("Second innings wickets should be between 0 and 10")
    if second_wickets == 10:
        raise ValueError("Team 2 already all out (10 wickets). DLS target no longer applicable.")

    # Validate overs format and bounds.
    overs_to_balls(first_overs, max_overs)
    overs_to_balls(second_overs, max_overs)

    r1 = dls_resource_remaining(fmt, first_overs, 0)
    r2 = dls_resource_remaining(fmt, second_overs, second_wickets)

    if play_stopped_over is not None and wickets_at_stop is not None and revised_total_overs is not None:
        stop_overs = float(play_stopped_over)
        revised_overs = float(revised_total_overs)
        stop_wickets = int(wickets_at_stop)
        if stop_wickets < 0 or stop_wickets > 10:
            raise ValueError("Wickets at stoppage should be between 0 and 10")
        if stop_wickets == 10:
            raise ValueError("Team 2 all out at stoppage; no revised target is needed.")
        overs_to_balls(stop_overs, max_overs)
        overs_to_balls(revised_overs, max_overs)
        if revised_overs < stop_overs:
            raise ValueError("Revised total overs cannot be lower than overs already bowled at stoppage")
        if revised_overs > second_overs:
            raise ValueError("Revised total overs cannot exceed scheduled second innings overs")

        scheduled_resource = dls_resource_remaining(fmt, second_overs, 0)
        remaining_at_stop = dls_resource_remaining(fmt, second_overs - stop_overs, stop_wickets)
        used_before_stop = max(0.0, scheduled_resource - remaining_at_stop)
        remaining_after_resume = dls_resource_remaining(fmt, revised_overs - stop_overs, stop_wickets)
        r2 = used_before_stop + remaining_after_resume
        warnings.append("DLS used stoppage-stage + revised-overs model.")

    if r1 <= 0:
        raise ValueError("Invalid resource for team 1 innings")

    target = math.floor(first_score * (r2 / r1)) + 1
    return {
        "target": target,
        "par_score": target - 1,
        "resource_team1": round(r1, 2),
        "resource_team2": round(r2, 2),
        "warnings": warnings,
    }


def compare_teams(team1: str, team2: str, fmt: str, xi1: list[str], xi2: list[str], venue: str | None = None, weather: str | None = None) -> dict[str, Any]:
    a_xi = pick_players(get_team_players(team1, fmt), xi1)
    b_xi = pick_players(get_team_players(team2, fmt), xi2)

    a = team_breakdown(a_xi, fmt)
    b = team_breakdown(b_xi, fmt)
    a_xi_check = xi_validator(a_xi, fmt)
    b_xi_check = xi_validator(b_xi, fmt)
    diff = a["overall"] - b["overall"]
    team1_win_chance = _clamp(50.0 + (diff * 3.0), 1.0, 99.0)
    h2h = head_to_head_overlay(team1, team2, fmt)
    team1_form = TEAM_RECENT_FORM.get(team1, {}).get(fmt, "N/A")
    team2_form = TEAM_RECENT_FORM.get(team2, {}).get(fmt, "N/A")

    return {
        "team1": {"name": team1, **a},
        "team2": {"name": team2, **b},
        "edge": team1 if a["overall"] >= b["overall"] else team2,
        "gap": round(abs(a["overall"] - b["overall"]), 2),
        "team1_win_chance": round(team1_win_chance, 1),
        "team2_win_chance": round(100.0 - team1_win_chance, 1),
        "h2h": h2h,
        "recent_form": {"team1": team1_form, "team2": team2_form},
        "xi_validation": {"team1": a_xi_check, "team2": b_xi_check},
        "toss_impact": toss_impact(fmt, venue, weather),
        "radar_labels": ["Batting", "Bowling", "Role Balance", "Overall"],
        "radar_team1": [a["batting"], a["bowling"], a["role_balance"], a["overall"]],
        "radar_team2": [b["batting"], b["bowling"], b["role_balance"], b["overall"]],
    }


def run_trajectory(payload: dict[str, Any]) -> dict[str, Any]:
    fmt = format_key(payload.get("format"))
    rules = FORMAT_RULES[fmt]
    max_overs = rules["max_overs"]

    score = int(payload.get("score", 0))
    wickets = int(payload.get("wickets", 0))
    overs_done = float(payload.get("overs", 0.0))
    target = payload.get("target")
    if score < 0:
        raise ValueError("Score cannot be negative")
    if wickets < 0 or wickets > 10:
        raise ValueError("Wickets should be between 0 and 10")

    balls_done = overs_to_balls(overs_done, max_overs)
    if balls_done <= 0:
        raise ValueError("Overs must be greater than 0 for trajectory")
    innings_complete = bool(payload.get("innings_complete")) or wickets >= 10 or balls_done >= (max_overs * 6)

    over_start = math.ceil(balls_done / 6)
    current_rr = score / (balls_done / 6.0)
    wickets_in_hand = 10 - wickets

    labels: list[str] = []
    projected: list[int] = []
    chase_line: list[float] = []

    if not innings_complete:
        current_projection = float(score)
        target_f = float(target) if target is not None else None
        for over in range(over_start, max_overs + 1):
            if fmt == "t20":
                if over <= 6:
                    phase_boost = 1.06
                elif over <= 15:
                    phase_boost = 0.93
                else:
                    phase_boost = 1.18
                min_rr, max_rr = 4.0, 16.0
            else:
                if over <= 10:
                    phase_boost = 1.04
                elif over <= 35:
                    phase_boost = 0.91
                else:
                    phase_boost = 1.1
                min_rr, max_rr = 2.8, 12.2

            phase = over / max_overs
            accel_curve = (0.9 + (0.42 * (phase ** 1.6))) if fmt == "t20" else (0.86 + (0.54 * (phase ** 1.9)))
            wicket_factor = _clamp(0.79 + (wickets_in_hand * 0.028), 0.66, 1.07)
            rhythm = 1.0 + (0.055 * math.sin((over * 0.84) + (wickets * 0.45)))
            surge = 1.075 if (over % 5 == 0 or over % 7 == 0) else 1.0

            chase_factor = 1.0
            if target_f is not None:
                expected_at_over = (target_f / max_overs) * over
                gap = expected_at_over - current_projection
                chase_factor = _clamp(1.0 + (gap / max(80.0, target_f * 0.34)), 0.9, 1.18)

            over_rr = current_rr * phase_boost * accel_curve * wicket_factor * rhythm * surge * chase_factor
            over_rr = _clamp(over_rr, min_rr, max_rr + (wickets_in_hand * 0.22))
            current_projection += over_rr
            labels.append(str(over))
            projected.append(int(round(current_projection)))
            if target is not None:
                chase_line.append(round((target_f / max_overs) * over, 1))

    # Build current timeline line if available from live ingestion.
    current_line: list[int | None] = [None] * max_overs
    timeline = payload.get("current_timeline")
    if isinstance(timeline, dict) and isinstance(timeline.get("overs"), list) and isinstance(timeline.get("runs"), list):
        overs_list = timeline.get("overs", [])
        runs_list = timeline.get("runs", [])
        for ov, rs in zip(overs_list, runs_list):
            try:
                ovf = float(ov)
                if ovf.is_integer():
                    over_idx = max(1, int(ovf))
                else:
                    over_idx = max(1, int(math.floor(ovf)))
                if over_idx <= max_overs:
                    current_line[over_idx - 1] = int(rs)
            except Exception:
                continue
    else:
        overs_used = max(1, int(math.ceil(balls_done / 6.0)))
        weights: list[float] = []
        for i in range(1, overs_used + 1):
            phase = i / max_overs
            if fmt == "t20":
                base_w = 1.14 if i <= 6 else (0.9 if i <= 15 else 1.22)
            else:
                base_w = 1.08 if i <= 10 else (0.88 if i <= 35 else 1.18)
            accel = 0.9 + (0.45 * (phase ** 1.8))
            wobble = 1.0 + (0.06 * math.sin((i * 0.9) + (wickets * 0.35)))
            weights.append(max(0.28, base_w * accel * wobble))
        total_w = sum(weights) or 1.0
        running = 0.0
        for i, w in enumerate(weights, start=1):
            running += score * (w / total_w)
            current_line[i - 1] = int(round(min(score, running)))

    full_labels = [str(i) for i in range(1, max_overs + 1)]
    projected_full: list[int | None] = [None] * max_overs
    for lab, val in zip(labels, projected):
        idx = int(lab) - 1
        if 0 <= idx < max_overs:
            projected_full[idx] = int(val)

    out = {"labels": labels, "projected": projected, "full_labels": full_labels, "current_line": current_line, "projected_line": projected_full}
    if isinstance(timeline, dict) and isinstance(timeline.get("wicket_overs"), list):
        out["wicket_overs"] = timeline.get("wicket_overs", [])
    if target is not None:
        if chase_line:
            out["target_line"] = chase_line
        else:
            out["target_line"] = [round((float(target) / max_overs) * over, 1) for over in range(1, max_overs + 1)]
    return out
