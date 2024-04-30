from flask import Flask, request, abort
import os
import tempfile
from pathlib import Path

from whispercpp import Whisper

app = Flask(__name__)


# Load Whisper model
def load_model():
    if not os.path.exists("./weights/whispercpp/ggml-small.bin"):
        os.makedirs("./weights/whispercpp", exist_ok=True)
        os.system(
            "wget -L 'https://ggml.ggerganov.com/ggml-model-whisper-small.bin' -O './weights/whispercpp/ggml-small.bin'"
        )

    model = Whisper.from_pretrained("small", basedir="weights")
    model.params.with_language("ru")
    return model


model = load_model()


@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    # Check if the part 'file' is present in the request
    print(request.files, "files")
    if "file" not in request.files:
        return abort(400, {"error": "No file part"})

    file = request.files["file"]
    if file.filename == "":
        return abort(400, {"error": "No selected file"})

    if not file:
        return abort(400, {"error": "Invalid file format"})

    temp = tempfile.NamedTemporaryFile(delete=False)
    file.save(temp.name)
    target_name = str(Path(temp.name).with_suffix(".wav"))
    if os.system(f"ffmpeg -i '{temp.name}' -ar 16000 {target_name}") != 0:
        os.unlink(temp.name)
        return abort(
            500, "FFMPreg error: something went wrong! Make sure that file is in"
        )
    try:
        transcription = model.transcribe_from_file(target_name)
        return {"transcription": transcription}
    except Exception as e:
        return abort(500, {"error": str(e)})
    finally:
        os.unlink(temp.name)
        os.unlink(target_name)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
