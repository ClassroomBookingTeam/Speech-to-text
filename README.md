# Speech-to-text

Supports all audio/video formats that ffmpreg supports. Does conversion to .wav and correct sample rate using said ffmpreg.

You can POST .mp4, .mp3, .ogg, .wav, .webm, whatever you want.

Concurrency is not supported, so a load balancer should be used to handle multiple requests.

**This thing can only handle one request at a time.**

```sh
sudo apt-get install ffmpeg
pip install whispercpp flask
flask --app main --debug run
curl -X POST -F "file=@/path/to/file.webm" http://localhost:5000/transcribe
```
