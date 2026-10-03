from flask import Flask, render_template, request, send_file
import os

from modules.hash_analysis import calculate_hashes
from modules.metadata import get_metadata
from modules.audio_analysis import analyze_audio
from modules.anomaly_analysis import analyze_anomalies
from modules.report import generate_report


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "static"
REPORT_FOLDER = "reports"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)


@app.route("/")
def home():

    return render_template(
        "index.html"
    )


@app.route("/upload", methods=["POST"])
def upload_file():

    if "audio" not in request.files:

        return "No file selected"

    file = request.files["audio"]

    if file.filename == "":

        return "No file selected"

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    # -------------------------
    # File Hashes
    # -------------------------

    hashes = calculate_hashes(
        filepath
    )

    # -------------------------
    # File Size
    # -------------------------

    filesize = os.path.getsize(
        filepath
    )

    # -------------------------
    # Metadata
    # -------------------------

    metadata = get_metadata(
        filepath
    )

    # -------------------------
    # Audio Analysis
    # -------------------------

    audio_results = analyze_audio(
        filepath,
        OUTPUT_FOLDER
    )

    # -------------------------
    # Anomaly Analysis
    # -------------------------

    anomaly_results = analyze_anomalies(
        filepath
    )

    # -------------------------
    # PDF Report Path
    # -------------------------

    report_filename = (
        os.path.splitext(file.filename)[0]
        + "_forensic_report.pdf"
    )

    report_path = os.path.join(
        REPORT_FOLDER,
        report_filename
    )

    # -------------------------
    # Generate PDF Report
    # -------------------------

    generate_report(
        filepath=filepath,
        filename=file.filename,
        filesize=filesize,
        md5=hashes["md5"],
        sha256=hashes["sha256"],
        metadata=metadata,
        audio_results=audio_results,
        anomaly_results=anomaly_results,
        output_path=report_path
    )

    # -------------------------
    # Show Result Page
    # -------------------------

    return render_template(
        "result.html",
        filename=file.filename,
        filesize=filesize,
        md5=hashes["md5"],
        sha256=hashes["sha256"],
        metadata=metadata,
        audio_results=audio_results,
        anomaly_results=anomaly_results,
        report_filename=report_filename
    )


@app.route("/download-report/<filename>")
def download_report(filename):

    report_path = os.path.join(
        REPORT_FOLDER,
        filename
    )

    if not os.path.exists(report_path):

        return "Report not found"

    return send_file(
        report_path,
        as_attachment=True
    )


if __name__ == "__main__":

    app.run(
        debug=True,
        use_reloader=False
    )