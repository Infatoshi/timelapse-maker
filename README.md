# timelapse-maker

Python script to create camera timelapses on any unix-based device

# Prereqs
- Python 3.8 or higher
- Using either macOS or Linux (this wasn't tested on windows)

## Setup
```bash
git clone https://github.com/Infatoshi/timelapse-maker && cd timelapse-maker && chmod +x setup.sh && ./setup.sh
```

## Usage

- `python v1.py --hours 12 --interval 15` ( interval is in seconds )
- `python create_timelapse.py` ( uses custom ffmpeg command to turn the individual frames into a video stream )

## To use `add_clock.py`
- you'll have to install `opencv-python` which may throw errors on the raspberry pi. I exclude this from the setup script to ensure setup goes as expected.

## License

MIT

