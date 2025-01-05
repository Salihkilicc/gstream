from flask import Flask, jsonify, request
import subprocess
import threading
from flask_restful import Api, Resource


app = Flask(__name__)
api = Api(app)

gst_process = None

class StreamControl(Resource):
    def post(self):
        global gst_process
        action = request.json.get('action')

        if action == "start":
            if gst_process is None:
                gst_command = [
                    "gst-launch-1.0",
                    "avfvideosrc", "!", "videoconvert", "!", "x264enc", "tune=zerolatency", "!",
                    "rtph264pay", "config-interval=1", "!",
                    "udpsink", "host=127.0.0.1", "port=5000"
                ]
                gst_process = subprocess.Popen(gst_command)
                return jsonify({"status": "Streaming started."})
            else:
                return jsonify({"status": "Stream is already running."}), 400
        
        elif action == "stop":
            if gst_process is not None:
                gst_process.terminate()
                gst_process = None
                return jsonify({"status": "Stream Paused."})
            else:
                return jsonify({"status": "No Stream."}), 400
        
        return jsonify({"status": "Invalid"}), 400

    def get(self):
        status = "running" if gst_process else "stopped"
        return jsonify({"status": status})

api.add_resource(StreamControl, '/control')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8590)
