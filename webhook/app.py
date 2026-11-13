from flask import Flask, request, jsonify
import logging
import subprocess

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)


@app.route("/alert", methods=["POST"])
def receive_alert():
    if not request.is_json:
        return jsonify({"error": "JSON required"}), 400

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON payload"}), 400

    alerts = data.get("alerts")

    if not isinstance(alerts, list):
        return jsonify({"error": "Missing alerts list"}), 400

    accepted = 0

    for alert in alerts:
        if not isinstance(alert, dict):
            continue

        labels = alert.get("labels", {})

        if not isinstance(labels, dict):
            continue

        if (
            labels.get("alertname") == "NginxDown"
            and alert.get("status") == "firing"
        ):
            accepted += 1

    if accepted == 0:
        return jsonify({
            "status": "received",
            "accepted_alerts": 0
        }), 200

    logging.warning("NGINX DOWN alert received. Starting recovery.")

    try:
        result = subprocess.run(
            ["/usr/bin/sudo", "-n", "/usr/local/sbin/recover-nginx"],
            capture_output=True,
            text=True,
            timeout=120,
            check=False
        )

        if result.returncode != 0:
            logging.error(
                "NGINX recovery failed (exit %s): %s",
                result.returncode,
                result.stderr
            )
            return jsonify({
                "status": "recovery_failed"
            }), 500

        logging.info("NGINX recovery completed:\n%s", result.stdout)

    except subprocess.TimeoutExpired:
        logging.error("NGINX recovery timed out.")
        return jsonify({"status": "recovery_timeout"}), 500

    return jsonify({
        "status": "recovery_completed",
        "accepted_alerts": accepted
    }), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5001,
        debug=False
    )
