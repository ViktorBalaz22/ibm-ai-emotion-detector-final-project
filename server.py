"""Server for Web Deployment"""

from flask import Flask, render_template, request
from emotion_detection.emotion_detection import emotion_detector

app = Flask(__name__)


@app.route('/')
def render_homepage() -> str:
    """Render homepage."""
    return render_template("index.html")


@app.route('/emotionDetector', methods=["GET"])
def emotion_analysis() -> str:
    """Analyze text and return emotion detection (analysis result)."""
    text_to_analyze = request.args.get("textToAnalyze", "")
    analysis_result = emotion_detector(text_to_analyze)

    if analysis_result["dominant_emotion"] is None:
        response = "Invalid text! Please try again!"
    else:
        response = "For the given statement, the system response is"

        for key, value in analysis_result.items():
            if key != "dominant_emotion":
                response += f" '{key}': {value},"

        last_comma_index = response.rfind(",")
        if last_comma_index != -1:
            response = (
                response[:last_comma_index]
                + '.'
                + response[last_comma_index + 1:]
            )

        response += (
            f" The dominant emotion is {analysis_result['dominant_emotion']}."
        )

    return response


def main() -> None:
    """Run the Flask application."""
    app.run(debug=True)


if __name__ == "__main__":
    main()