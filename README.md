# timelapse-maker-v2

Python scripts to create camera timelapses on desktop PCs, raspberry pis, and macbooks.

# Requirements
- Python >= 3.8
- Git
- macOS or Linux (not tested on Windows)
- OpenCV for Python (`opencv-python`)
- ffmpeg

## Setup
### Cloning the Project
```bash
git clone https://github.com/Infatoshi/timelapse-maker
cd timelapse-maker-v2
python3 -m venv .venv
source .venv/bin/activate
```

### Linux
```bash
sudo apt install ffmpeg
pip install opencv-python
```

### MacOS
```bash 
pip install opencv-python
brew install ffmpeg
```

### Windows
- Open the command prompt with -> Windows key then "cmd"
- `cd` into your project folder. Ex: `cd C:\User\Desktop\python-projs\timelapse-maker-v2`
```bash
.venv\Scripts\activate.bat
pip install opencv-python
```

## Usage

### Option 1: Complete Workflow (Recommended)
Use the shell script for automated capture and video creation:
```bash
./run_timelapse.sh [--hours <hours>] [--interval <seconds>] [--output-dir <dir>] [--width <w>] [--height <h>] [--no-timestamp]
```

Examples:
```bash
# 20-hour timelapse with 15-second intervals (defaults)
./run_timelapse.sh

# 12-hour timelapse with 30-second intervals
./run_timelapse.sh --hours 12 --interval 30

# Custom resolution without timestamp
./run_timelapse.sh --hours 8 --interval 10 --width 1920 --height 1080 --no-timestamp
```

### Option 2: Manual Steps
Run the Python scripts individually:

#### Capture Images
```bash
python3 capture_timelapse.py --hours 12 --interval 15 --output-dir timelapse_imgs [--width <w>] [--height <h>] [--add-timestamp]
```

#### Create Video
```bash
python3 create_timelapse.py <image_folder> <output_video.mp4>
```

Example:
```bash
python3 capture_timelapse.py --hours 12 --interval 15 --output-dir timelapse_imgs --add-timestamp
python3 create_timelapse.py timelapse_imgs videos/my_timelapse.mp4
```

## Features
- **Automatic camera detection**: Scans for available cameras and uses the first working one
- **Built-in timestamps**: Add military time (HH:MM) to each frame
- **Custom resolution**: Set specific width and height for capture
- **Flexible intervals**: Configure time between captures (seconds)
- **Organized output**: Automatic directory structure for images and videos
- **Error handling**: Graceful handling of camera issues and interruptions

## License

MIT

