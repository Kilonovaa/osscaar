import time


def processAudio(video_data, callback):
    callback(0)
    audio_data = open("sound.wav", "rb").read()
    time.sleep(1)
    callback(26)
    time.sleep(1)

    callback(48)
    time.sleep(1)

    callback(89)
    time.sleep(1)

    callback(100)
    time.sleep(1)

    return audio_data
