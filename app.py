from flask import Flask, render_template, request, send_file
from pytube import YouTube
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("downloader.html")
@app.route('/download', methods=["POST"])
def download():
    try:
        link = request.form["link"]
        media_type = request.form["mediaType"]
        youtube = YouTube(link)
        if media_type == "video":
            video_stream = youtube.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            if video_stream:
                vid = video_stream.download()
                return send_file(vid, as_attachment=True)
            else:
                return "No MP4 video available for this link!"

        elif media_type == "audio":
            audio_stream = youtube.streams.filter(only_audio=True).first()

            if audio_stream:
                audio = audio_stream.download()
                return send_file(audio, as_attachment=True)
            else:
                return "No audio available for this link!"

        else:
            return "Invalid media type!"

    except Exception as e:
        print(str(e))
        return "Download failed!"

if __name__ == '__main__':
    app.run(debug=True)
