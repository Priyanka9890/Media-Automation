import os
import sys
import json
import subprocess
import logging
from datetime import datetime

# -------------------------------------------------
# Configuration
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_DIR = os.path.join(BASE_DIR, "input")
VIDEO_DIR = os.path.join(INPUT_DIR, "videos")
META_DIR = os.path.join(INPUT_DIR, "metadata")

OUTPUT_DIR = os.path.join(BASE_DIR, "output")
LOG_DIR = os.path.join(BASE_DIR, "logs")

MIN_VIDEO_SIZE_MB = 1        # minimum allowed video size
MIN_DURATION_SEC = 1         # minimum allowed duration

# -------------------------------------------------
# Logging Setup
# -------------------------------------------------
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "automation.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -------------------------------------------------
# Helper Functions
# -------------------------------------------------
def fail_safe(message):
    """Log error, print message, and exit safely"""
    logging.error(message)
    print(f"[ERROR] {message}")
    sys.exit(1)

def check_ffprobe():
    """Ensure ffprobe is available"""
    try:
        subprocess.run(
            ["ffprobe", "-version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
    except Exception:
        fail_safe("ffprobe is not installed or not available in PATH")

def validate_environment():
    """Validate required folders and files"""
    if not os.path.exists(INPUT_DIR):
        fail_safe("Input folder does not exist")

    if not os.path.exists(VIDEO_DIR):
        fail_safe("Missing 'videos' folder")

    if not os.path.exists(META_DIR):
        fail_safe("Missing 'metadata' folder")

    csv_files = [f for f in os.listdir(META_DIR) if f.endswith(".csv")]
    if not csv_files:
        fail_safe("No metadata CSV file found")

def analyze_video(video_path):
    """Validate and extract video metadata using ffprobe"""
    size_mb = os.path.getsize(video_path) / (1024 * 1024)

    if size_mb < MIN_VIDEO_SIZE_MB:
        fail_safe(f"Video too small or corrupt: {os.path.basename(video_path)}")

    cmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height,duration",
        "-of", "json",
        video_path
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        data = json.loads(result.stdout)

        if not data.get("streams"):
            fail_safe(f"No video stream found: {video_path}")

        stream = data["streams"][0]
        duration = float(stream.get("duration", 0))
        width = stream.get("width", 0)
        height = stream.get("height", 0)

    except Exception:
        fail_safe(f"ffprobe failed for video: {video_path}")

    if duration < MIN_DURATION_SEC:
        fail_safe(f"Video duration too short: {video_path}")

    return {
        "name": os.path.basename(video_path),
        "size_mb": round(size_mb, 2),
        "duration_sec": round(duration, 2),
        "resolution": f"{width}x{height}"
    }

# -------------------------------------------------
# Main Execution
# -------------------------------------------------
def main():
    logging.info("Media automation started")

    check_ffprobe()
    validate_environment()

    videos = [f for f in os.listdir(VIDEO_DIR) if f.lower().endswith(".mp4")]
    if not videos:
        fail_safe("No MP4 videos found in videos folder")

    video_stats = []

    for video in videos:
        video_path = os.path.join(VIDEO_DIR, video)
        stats = analyze_video(video_path)
        video_stats.append(stats)
        logging.info(f"Processed video: {video}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    output_file = os.path.join(
        OUTPUT_DIR,
        f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    )

    with open(output_file, "w") as f:
        f.write("Media Automation Summary\n")
        f.write("========================\n\n")
        f.write(f"Total Videos: {len(video_stats)}\n\n")

        for v in video_stats:
            f.write(
                f"- {v['name']} | "
                f"{v['duration_sec']}s | "
                f"{v['resolution']} | "
                f"{v['size_mb']}MB\n"
            )

    logging.info("Media automation completed successfully")
    print("[SUCCESS] Media automation completed successfully")

if __name__ == "__main__":
    main()
