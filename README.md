# Media Automation System (Real Video Version)

## Overview
This project is a small Python-based automation system designed to simulate a **real-world media ingestion pipeline** (similar to YouTube or media automation systems).  
It validates real video files, checks required inputs, extracts basic metadata, and produces clear logs and summaries.

The focus is on:
- Reliability
- Safe failure
- Clear structure
- Ownership of design decisions

---

## Folder Structure

```
media_automation/
│
├── input/
│   ├── videos/
│   │   ├── video1.mp4
│   │   ├── video2.mp4
│   └── metadata/
│       └── info.csv
│
├── output/
│   └── summary_YYYYMMDD_HHMMSS.txt
│
├── logs/
│   └── automation.log
│
├── automation.py
└── README.md
```

---

## Requirements

- Python 3.8+
- FFmpeg

Install dependency:

```bash
winget install --id=Gyan.FFmpeg -e
```

Verify Installation:

```bash
ffmpeg -version
ffprobe -version
```


---

## How to Run

1. Place at least one `.mp4` file inside:
   ```
   input/videos/
   ```

2. Place at least one `.csv` file inside:
   ```
   input/metadata/
   ```

3. Run the automation:

```bash
python automation.py
```

---

## What the Program Does

1. Validates required folders (`videos`, `metadata`)
2. Ensures at least one valid MP4 video exists
3. Ensures metadata CSV exists
4. For each video:
   - Checks file size
   - Reads duration
   - Reads resolution
5. Generates:
   - A timestamped summary file in `output/`
   - A detailed log file in `logs/`

---

## Validation Rules (Design Choices)

| Rule | Reason |
|----|----|
| At least one MP4 file | Prevent empty automation jobs |
| Video size > 1MB | Avoid corrupt or placeholder files |
| Duration > 1 second | Prevent broken videos |
| Metadata CSV required | Common dependency in media pipelines |

These checks simulate **media ingestion validation**, not video processing.

---

## Failure Behavior

If something is wrong:
- The program does **not crash**
- A clear error is printed to the console
- The error is written to the log file
- The program exits safely

Example:
```
[ERROR] No MP4 videos found
```

---

## Logging

All activity is logged in:

```
logs/automation.log
```

Includes:
- Start and end of automation
- Each processed video
- Any validation or runtime errors

---

## Example Successful Output

Console:
```
[SUCCESS] Media automation completed
```

Summary file:
```
Media Automation Summary
========================

Total Videos: 2

- video1.mp4 | 12.4s | 1920x1080 | 8.6MB
- video2.mp4 | 7.9s | 1280x720 | 5.1MB
```

---

## Edge Case Considered

**Corrupt MP4 file with valid extension**  
A video file exists but cannot be opened by FFmpeg.  
The system detects this early and exits safely with a clear error.

---

## Why Real Videos Were Used

Real video files make the automation closer to production media systems.  
The system only **validates and inspects metadata**, which reflects how real ingestion pipelines work before heavy processing.

---

## One Improvement for Scale

- Add multiprocessing for parallel video analysis
- Store results in a database instead of text files

---

## Conclusion

This project demonstrates:
- Safe automation design
- Clear validation logic
- Realistic media handling
- Maintainable structure

### 👨‍💻 Author

Created by **Priyanka Jyoti**
