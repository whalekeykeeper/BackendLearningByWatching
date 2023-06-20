from __future__ import unicode_literals
from flask import Flask, jsonify, make_response, request, send_file
import json
import yt_dlp
import requests
import regex as re
from os import listdir
from os.path import isfile, join
import webvtt
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


# localhost:5000/demo
@app.post("/demo")
def demo():
    data = request.get_json()
    print(data)
    return make_response(data, 200)


# http://127.0.0.1:5000/video/video_id
@app.get("/video/<string:video_id>")
def get_video_id(video_id):
    print('video_id is: ', video_id)
    filepath = "./static/" + video_id + "/" + video_id + ".mp4"
    print("filepath is: ", filepath)
    isExisting = os.path.exists(filepath)
    if not isExisting:
        _download_video_with_subtitles(video_id)
    return send_file(filepath, mimetype="video")


# http://127.0.0.1:5000/caption/en/video_id
@app.get("/caption/en/<string:video_id>")
def get_caption_en(video_id):
    filepath = "./static/" + video_id + "/" + video_id + ".en.vtt"
    print("filepath is: ", filepath)
    isExisting = os.path.exists(filepath)
    if not isExisting:
        _download_video_with_subtitles(video_id)
    return send_file(filepath, mimetype="text/vtt")


# http://127.0.0.1:5000/caption/zh/video_id
@app.get("/caption/zh/<string:video_id>")
def get_caption_zh(video_id):
    filepath = "./static/" + video_id + "/" + video_id + ".zh-Hans.vtt"
    print("filepath is: ", filepath)
    isExisting = os.path.exists(filepath)
    if not isExisting:
        _download_video_with_subtitles(video_id)
    return send_file(filepath, mimetype="text/vtt")


# http://127.0.0.1:5000/caption/bi/video_id
@app.get("/caption/bi/<string:video_id>")
def get_caption_bi(video_id):
    filepath = "./static/" + video_id + "/" + video_id + ".bi.vtt"
    print("filepath is: ", filepath)
    isExisting = os.path.exists(filepath)
    if not isExisting:
        _download_video_with_subtitles(video_id)
    return send_file(filepath, mimetype="text/vtt")


def _download_video_with_subtitles(video_id, language=['en', "zh-Hans", 'de']):
    if video_id:
        ydl_opts = {
            'subtitleslangs': language,
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitlesformat': 'vtt',
            "paths": {'home': "./static/" + video_id},
            'outtmpl': f'{video_id}.%(ext)s'
        }
        url = "https://youtu.be/" + video_id
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    else:
        print('Invalid YouTube id.')


# @app.route("/video/<string:video_id>", methods=["GET"])
# def get_video_sub(video_id):
#     URL = "https://youtu.be/" + video_id
#     video_path = "./static"
#     return send_file(video_path, mimetype="video/mp4")


# http://127.0.0.1:5000/caption/VAQMsprq-Ps/en
@app.post("/caption/<string:id>/<string:language>")
def post_caption(id, language):
    folder_path = "./static/" + id
    onlyfiles = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]
    data = ''
    for ele in onlyfiles:
        if ele.endswith("[" + id + "]." + language + ".vtt"):
            data = ele
            for caption in webvtt.read("./static/" + id + "/" + data):
                print(caption.start)
                print(caption.end)
                print(caption.text)
            return make_response(data, 200)
    # ToDo
    return make_response(data, 200)


@app.post("/anki")
def create_anki_deck():
    data = request.get_json()  # [{"word": word, "translation": translation, "sentence": sentence}, ...]

    # ydl = yt_dlp.YoutubeDL({'writesubtitles': True, 'allsubtitles': True, 'writeautomaticsub': True})
    # res = ydl.extract_info(URL, download=False)
    # if res['requested_subtitles'] and res['requested_subtitles']['en']:
    #     print('Grabbing vtt file from ' + res['requested_subtitles']['en']['url'])
    #     response = requests.get(res['requested_subtitles']['en']['url'], stream=True)
    #     f1 = open("testfile01.txt", "w")
    #     new = response.text
    #     # new = re.sub(r'\d{2}\W\d{2}\W\d{2}\W\d{3}\s\W{3}\s\d{2}\W\d{2}\W\d{2}\W\d{3}', '', response.text)
    #     f1.write(new)
    #     f1.close()
    #     if len(res['subtitles']) > 0:
    #         print('manual captions')
    #     else:
    #         print('automatic_captions')
    # else:
    #     print('Youtube Video does not have any english captions')


if __name__ == '__main__':
    app.run()

    # _download_video_with_subtitles("https://www.youtube.com/watch?v=VAQMsprq-Ps")
