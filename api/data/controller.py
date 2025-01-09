import os


def get_media_type(file_path):
    _, ext = os.path.splitext(file_path)
    if ext in ['.jpg', '.jpeg', '.png', '.gif', '.heic']:
        return "image/" + ext[1:]
    elif ext in ['.mp3', '.wav', '.ogg']:
        return "audio/" + ext[1:]
    elif ext in ['.mp4', '.avi', '.mkv', '.mov']:
        return "video/" + ext[1:]
    else:
        return "application/octet-stream"
