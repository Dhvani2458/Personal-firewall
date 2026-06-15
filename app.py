from flask import Flask, render_template, request, jsonify, send_file
import firewall_core as fw
import os

app = Flask(__name__)

fw.load_rules()


# ==========================
# PAGE ROUTES
# ==========================

@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/rules")
def rules_page():
    return render_template("rules.html")


@app.route("/logs_page")
def logs_page():
    return render_template("logs.html")


@app.route("/settings")
def settings():
    return render_template("settings.html")


@app.route("/about")
def about():
    return render_template("about.html")


# ==========================
# API ROUTES
# ==========================

@app.route("/api/rules")
def get_rules():
    fw.load_rules()

    return jsonify({
        "mode": fw.rules["mode"],
        "ips": fw.rules["ips"]
    })


@app.route("/api/add_ip", methods=["POST"])
def add_ip():

    data = request.get_json()

    ip = data.get("ip", "").strip()

    if not ip:
        return jsonify({
            "success": False,
            "message": "IP required"
        })

    if fw.add_ip(ip):
        return jsonify({
            "success": True,
            "message": "IP Added"
        })

    return jsonify({
        "success": False,
        "message": "IP already exists"
    })


@app.route("/api/remove_ip", methods=["POST"])
def remove_ip():

    data = request.get_json()

    ip = data.get("ip", "").strip()

    if fw.remove_ip(ip):
        return jsonify({
            "success": True,
            "message": "IP Removed"
        })

    return jsonify({
        "success": False,
        "message": "IP not found"
    })


@app.route("/api/set_mode", methods=["POST"])
def set_mode():

    data = request.get_json()

    mode = data.get("mode")

    if mode not in ["allow", "block"]:
        return jsonify({
            "success": False
        })

    fw.set_mode(mode)

    return jsonify({
        "success": True,
        "message": f"Mode set to {mode}"
    })


@app.route("/api/start_firewall")
def start_firewall():

    try:
        fw.start_firewall()

        return jsonify({
            "success": True,
            "message": "Firewall Started"
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        })


@app.route("/api/stop_firewall")
def stop_firewall():

    fw.stop_firewall()

    return jsonify({
        "success": True,
        "message": "Firewall Stopped"
    })


@app.route("/api/status")
def status():

    return jsonify({
        "running": fw.get_status()
    })


@app.route("/api/logs")
def logs():

    try:

        with open(
            "logs.txt",
            "r",
            encoding="utf-8"
        ) as f:

            data = f.read()

    except:

        data = "No logs available"

    return jsonify({
        "logs": data
    })


@app.route("/download_logs")
def download_logs():

    from flask import send_file

    return send_file(
        "logs.txt",
        as_attachment=True
    )

    return "Log file not found"


@app.route("/api/dashboard")
def dashboard_data():

    fw.load_rules()

    return jsonify({
        "running": fw.get_status(),
        "mode": fw.rules["mode"],
        "total_rules": len(fw.rules["ips"])
    })


if __name__ == "__main__":
    app.run(debug=True)