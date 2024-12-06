# timelapse-maker

Python scripts to create camera timelapses on desktop PCs, raspberry pis, and macbooks.

# Requirements
- Python >= 3.8
- Git
- macOS or Linux (not tested on Windows)
- Homebrew (for macOS users)

## Setup
### Cloning the Project
```bash
git clone https://github.com/Infatoshi/timelapse-maker
cd timelapse-maker
python3 -m venv .venv
source .venv/bin/activate
```

### Linux
```bash
sudo apt install ffmpeg fswebcam
```

### MacOS
```bash 
pip install opencv-python numpy
brew install ffmpeg
#opt. brew install imagesnap timg
```

### Windows
- Open the command prompt with -> Windows key then "cmd"
- `cd` into your project folder. Ex: `cd C:\User\Desktop\python-projs\timelapse-maker`
```bash
.venv\Scripts\activate.bat
pip install opencv-python
```

## Usage
> I recommend trying out a frame or two to see if the position is what you want. If you have more than 1 camera available (even virtual cameras), run the script to see which frames pop into `timelapse_images`. If its the incorrect camera, try increasing `device=0` to `device=1` in the first function of the script (increase until you arrive at the correct camera)

- `python capture_timelapse.y --hours 12 --interval 15` ( interval is in seconds, shorter interval with make the timelapse smoother )
- `python create_timelapse.py` ( uses custom ffmpeg command to turn the individual frames into a video stream. only if you're on mac or linux though )

## To use `add_clock.py`
- you'll have to install `opencv-python` which may throw errors on the raspberry pi. I exclude this from the setup script to ensure setup goes as expected.

## License

MIT

