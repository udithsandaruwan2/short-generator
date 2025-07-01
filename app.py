from flask import Flask, request, jsonify
from main import generate_video  # We'll refactor your main code into this function
import os

app = Flask(__name__)

@app.route("/generate-video", methods=["POST"])
def generate_video_api():
    data = request.get_json()

    input_text = data.get("input_text")
    video_query = data.get("video_query")

    if not input_text or not video_query:
        return jsonify({"error": "Missing input_text or video_query"}), 400

    try:
        final_path = generate_video(input_text, video_query)
        return jsonify({
            "message": "Video generated successfully",
            "video_path": final_path
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5050)
