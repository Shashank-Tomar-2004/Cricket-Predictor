from __future__ import annotations

from datetime import date, timedelta

from flask import Flask, Response, jsonify, render_template, request
from flask_cors import CORS

try:
    from api.data import FORMAT_RULES, PITCH_TYPES, TEAM_DATA, TOP_ODI_TEAMS, VENUES, WEATHER_TYPES
    from api.engine import (
        backtest_report,
        compare_teams,
        dls_target,
        explain_score,
        format_key,
        gemini_live_brief,
        ingest_live_state,
        live_analytics_pack,
        live_demo_matches,
        recent_match_scenarios,
        live_provider_profiles,
        model_card,
        predict_score,
        reproducibility_pdf,
        run_trajectory,
        uncertainty_fan,
        viva_report_pdf,
        win_probability,
    )
except ModuleNotFoundError:
    from data import FORMAT_RULES, PITCH_TYPES, TEAM_DATA, TOP_ODI_TEAMS, VENUES, WEATHER_TYPES
    from engine import (
        backtest_report,
        compare_teams,
        dls_target,
        explain_score,
        format_key,
        gemini_live_brief,
        ingest_live_state,
        live_analytics_pack,
        live_demo_matches,
        recent_match_scenarios,
        live_provider_profiles,
        model_card,
        predict_score,
        reproducibility_pdf,
        run_trajectory,
        uncertainty_fan,
        viva_report_pdf,
        win_probability,
    )

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({"status": "ok", "service": "cricket-predictor", "formats": list(FORMAT_RULES.keys())})


@app.route("/api/meta", methods=["GET"])
def meta():
    fmt = format_key(request.args.get("format"))
    venues = [
        {
            "name": venue["name"],
            "country": venue["country"],
            "region": venue.get("region", "Other"),
            "city": venue.get("city", ""),
            "avg_score": venue["t20_avg"] if fmt == "t20" else venue["odi_avg"],
            "pitch_type": venue.get("pitch_type", ""),
            "boundary_size": venue.get("boundary_size", ""),
        }
        for venue in VENUES
    ]
    regions = sorted({v["region"] for v in venues})
    countries = sorted({v["country"] for v in venues})
    teams = [
        {
            "name": t["name"],
            "flag": TEAM_DATA[t["name"]]["flag"],
            "flag_img": TEAM_DATA[t["name"]].get("flag_img"),
        }
        for t in TOP_ODI_TEAMS
    ]
    return jsonify(
        {
            "format": fmt,
            "rules": FORMAT_RULES[fmt],
            "teams": teams,
            "venues": venues,
            "regions": regions,
            "countries": countries,
            "pitch_types": PITCH_TYPES,
            "weather_types": WEATHER_TYPES,
        }
    )


@app.route("/api/squad", methods=["GET"])
def squad():
    fmt = format_key(request.args.get("format"))
    team = request.args.get("team", "")

    if team not in TEAM_DATA:
        return jsonify({"error": "Unknown team"}), 404

    players = TEAM_DATA[team]["squads"][fmt]
    if len(players) != 15:
        return jsonify({"error": "Squad data misconfigured, expected 15 players"}), 500

    return jsonify(
        {
            "team": team,
            "flag": TEAM_DATA[team]["flag"],
            "flag_img": TEAM_DATA[team].get("flag_img"),
            "format": fmt,
            "players": players,
        }
    )


@app.route("/api/predict_score", methods=["POST"])
def api_predict_score():
    try:
        payload = request.get_json(force=True)
        return jsonify(predict_score(payload))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        return jsonify({"error": "Unable to process score prediction"}), 500


@app.route("/api/explain_score", methods=["POST"])
def api_explain_score():
    try:
        payload = request.get_json(force=True)
        return jsonify(explain_score(payload))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        return jsonify({"error": "Unable to explain score prediction"}), 500


@app.route("/api/live_demo_matches", methods=["GET"])
def api_live_demo_matches():
    return jsonify({"matches": live_demo_matches()})


@app.route("/api/scenarios_recent", methods=["GET"])
def api_scenarios_recent():
    fmt = format_key(request.args.get("format"))
    try:
        limit = int(request.args.get("limit", 30))
    except Exception:
        limit = 30
    limit = max(1, min(60, limit))
    return jsonify({"format": fmt, "scenarios": recent_match_scenarios(fmt, limit)})


@app.route("/api/live_providers", methods=["GET"])
def api_live_providers():
    return jsonify({"providers": live_provider_profiles()})


@app.route("/api/fixtures", methods=["GET"])
def api_fixtures():
    fmt = format_key(request.args.get("format"))
    teams = [t["name"] for t in TOP_ODI_TEAMS]
    start = date.today()
    fixtures = []
    day_jump = 2 if fmt == "t20" else 4
    idx = 0
    for i, team1 in enumerate(teams):
        for team2 in teams[i + 1 :]:
            d = start + timedelta(days=idx * day_jump)
            status = "upcoming"
            if d == start:
                status = "live"
            elif d < start:
                status = "recent"
            fixtures.append(
                {
                    "date": d.isoformat(),
                    "format": fmt,
                    "team1": team1,
                    "team2": team2,
                    "title": f"{team1} vs {team2}",
                    "home": team1,
                    "away": team2,
                    "status": status,
                }
            )
            idx += 1
    return jsonify({"fixtures": fixtures[:24]})


@app.route("/api/model_card", methods=["GET"])
def api_model_card():
    return jsonify(model_card())


@app.route("/api/live_ingest", methods=["POST"])
def api_live_ingest():
    try:
        payload = request.get_json(force=True)
        return jsonify(ingest_live_state(payload))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        return jsonify({"error": "Unable to ingest live match"}), 500


@app.route("/api/live_ai_brief", methods=["POST"])
def api_live_ai_brief():
    try:
        payload = request.get_json(force=True)
        return jsonify(gemini_live_brief(payload))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        return jsonify({"error": "Unable to generate match insight"}), 500


@app.route("/api/live_pack", methods=["POST"])
def api_live_pack():
    try:
        payload = request.get_json(force=True)
        return jsonify(live_analytics_pack(payload))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        return jsonify({"error": "Unable to generate live analytics pack"}), 500


@app.route("/api/win_probability", methods=["POST"])
def api_win_probability():
    try:
        payload = request.get_json(force=True)
        return jsonify(win_probability(payload))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        return jsonify({"error": "Unable to process win probability"}), 500


@app.route("/api/dls", methods=["POST"])
def api_dls():
    try:
        payload = request.get_json(force=True)
        return jsonify(dls_target(payload))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        return jsonify({"error": "Unable to process DLS"}), 500


@app.route("/api/compare", methods=["POST"])
def api_compare():
    try:
        payload = request.get_json(force=True)
        fmt = format_key(payload.get("format"))
        result = compare_teams(
            team1=str(payload.get("team1", "")),
            team2=str(payload.get("team2", "")),
            fmt=fmt,
            xi1=payload.get("xi1", []),
            xi2=payload.get("xi2", []),
            venue=payload.get("venue"),
            weather=payload.get("weather"),
        )
        return jsonify(result)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        return jsonify({"error": "Unable to compare teams"}), 500


@app.route("/api/uncertainty", methods=["POST"])
def api_uncertainty():
    try:
        payload = request.get_json(force=True)
        return jsonify(uncertainty_fan(payload))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        return jsonify({"error": "Unable to generate uncertainty fan"}), 500


@app.route("/api/backtest", methods=["POST"])
def api_backtest():
    try:
        payload = request.get_json(force=True)
        return jsonify(backtest_report(payload))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        return jsonify({"error": "Unable to run backtest"}), 500


@app.route("/api/repro_pdf", methods=["POST"])
def api_repro_pdf():
    try:
        payload = request.get_json(force=True)
        pdf_bytes = reproducibility_pdf(payload)
        return Response(
            pdf_bytes,
            mimetype="application/pdf",
            headers={"Content-Disposition": 'attachment; filename="cricket_repro_report.pdf"'},
        )
    except Exception:
        return jsonify({"error": "Unable to build reproducibility PDF"}), 500


@app.route("/api/viva_pdf", methods=["POST"])
def api_viva_pdf():
    try:
        payload = request.get_json(force=True)
        pdf_bytes = viva_report_pdf(payload)
        return Response(
            pdf_bytes,
            mimetype="application/pdf",
            headers={"Content-Disposition": 'attachment; filename="cricket_viva_report.pdf"'},
        )
    except Exception:
        return jsonify({"error": "Unable to build viva report PDF"}), 500


@app.route("/api/trajectory", methods=["POST"])
def api_trajectory():
    try:
        payload = request.get_json(force=True)
        return jsonify(run_trajectory(payload))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        return jsonify({"error": "Unable to generate run trajectory"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
