from python:3.9.19-bookworm
workdir /files
copy main.py /files
run pip install whispercpp flask
run apt-get update  -y
run apt-get install -y ffmpeg wget
