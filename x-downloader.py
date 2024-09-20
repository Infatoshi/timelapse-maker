import yt_dlp


def download_twitter_video(url):
    ydl_opts = {"outtmpl": "%(title)s.%(ext)s"}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


# Example usage
video_url = "https://x.com/i/broadcasts/1yoKMygbVrRKQ"
download_twitter_video(video_url)
