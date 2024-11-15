# timelapse-maker

Python scripts to create camera timelapses on desktop PCs, raspberry pis, and macbooks.

# Prereqs
- Python 3.8 or higher
- Using either macOS or Linux (this wasn't tested on windows)
- ensure git is installed with `git -V`
- you'll have to modify the setup command if you're using a virtual env like conda or uv
- homebrew if you're using a mac/macbook

## Setup
### Linux
```bash
git clone https://github.com/Infatoshi/timelapse-maker
cd timelapse-maker
sudo apt update && sudo apt upgrade -y
python3 -m venv venv
source venv/bin/activate
pip install argparse
sudo apt install ffmpeg fswebcam
mkdir timelapse_images
```

### MacOS
```bash 
git clone https://github.com/Infatoshi/timelapse-maker
cd timelapse-maker
python3 -m venv venv
source venv/bin/activate
pip install argparse opencv-python numpy
mkdir timelapse_images
brew install ffmpeg
#opt. brew install imagesnap timg

```

### Windows
- first download this github repository to a directory of your choice (or use git if you're like that)
- open the command prompt with -> Windows key then "cmd"
- `cd` into your project folder. Ex: `cd C:\User\Desktop\python-projs\timelapse-maker`
```bash
python3 -m venv venv
venv\Scripts\activate.bat
pip install argparse opencv-python
```

## Usage
> I recommend trying out a frame or two to see if the position is what you want. If you have more than 1 camera available (even virtual cameras), run the script to see which frames pop into `timelapse_images`. If its the incorrect camera, try increasing `device=0` to `device=1` in the first function of the script (increase until you arrive at the correct camera)

- `python v1_macos.py --hours 12 --interval 15` ( interval is in seconds, shorter interval with make the timelapse smoother )
- `python create_timelapse.py` ( uses custom ffmpeg command to turn the individual frames into a video stream. only if you're on mac or linux though )

## To use `add_clock.py`
- you'll have to install `opencv-python` which may throw errors on the raspberry pi. I exclude this from the setup script to ensure setup goes as expected.

## License

MIT

