import os
from flask import Flask, request, jsonify
from myjdapi import Myjdapi

JD_EMAIL = os.getenv("JD_EMAIL")
JD_PASSWORD = os.getenv("JD_PASSWORD")
JD_DEVICE = os.getenv("JD_DEVICE")

import logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
jd_client = None

def get_jd_client():
    global jd_client
    if jd_client is None:
        if not all([JD_EMAIL, JD_PASSWORD, JD_DEVICE]):
            raise ValueError("Environment variables JD_EMAIL, JD_PASSWORD, and JD_DEVICE must be set.")
        
        jd_client = Myjdapi()
        jd_client.connect(JD_EMAIL, JD_PASSWORD)
        jd_client.update_devices()
    return jd_client

try:
    get_jd_client()
    logging.info("Successfully connected to MyJDownloader on startup.")
except Exception as e:
    logging.error(f"Failed to connect to MyJDownloader on startup: {e}", exc_info=True)

@app.route('/add', methods=['POST'])
def add_link():
    try:
        data = request.json
        url = data.get('url')
        package_name = data.get('packageName')

        if not url:
            return jsonify({"success": False, "error": "Missing 'url' in request body"}), 400

        jd = get_jd_client()
        
        device = jd.get_device(JD_DEVICE)
        if not device:
            raise Exception(f"Device '{JD_DEVICE}' not found.")

        link_data = {
            "autostart": True,
            "links": url
        }

        if package_name:
            link_data["packageName"] = package_name

        result = device.linkgrabber.add_links([link_data])

        return jsonify({"success": True, "result": result})
    
    except ValueError as ve:
        return jsonify({"success": False, "error": str(ve)}), 500

    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"success": False, "error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000)
