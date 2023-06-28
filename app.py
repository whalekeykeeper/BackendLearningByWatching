from __future__ import unicode_literals
from flask import Flask, jsonify, make_response, request, send_file
import json
import yt_dlp
import requests
import regex as re
from os import listdir
from os.path import isfile, join
# import webvtt
import os
from flask_cors import CORS
from download import download_video_and_subtitles
from mergeVTT import cleanup

app = Flask(__name__)
CORS(app)

#
# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'
#
#
# # localhost:5000/demo
# @app.post("/demo")
# def demo():
#     data = request.get_json()
#     print(data)
#     return make_response(data, 200)


# http://127.0.0.1:5000/video/video_id
@app.get("/video/<string:video_id>")
def get_video_id(video_id):
    print('video_id is: ', video_id, os.getcwd())

    video_path = "./static/" + video_id + "/" + video_id + ".mp4"
    print("video_path is: ", video_path)
    print("The video file exists.")
    video_existing = os.path.exists(video_path)
    if not video_existing:
        download_video_and_subtitles(video_id)
    else:
        print("The video file exists.")

    vtt_path = "./static/" + video_id + "/" + video_id + ".bi.vtt"
    print("vtt_path is: ", vtt_path)
    vtt_existing = os.path.exists(vtt_path)
    print("------\nvtt_existing: ", vtt_existing)
    if not vtt_existing:
        cleanup(video_id)
    else:
        print("The bi-vtt file exists.")

    return send_file(video_path, mimetype="video")


# # http://127.0.0.1:5000/caption/en/video_id
# @app.get("/caption/en/<string:video_id>")
# def get_caption_en(video_id):
#     filepath = "./static/" + video_id + "/" + video_id + ".en.vtt"
#     print("filepath is: ", filepath)
#     isExisting = os.path.exists(filepath)
#     if not isExisting:
#         _download_video_with_subtitles(video_id)
#     return send_file(filepath, mimetype="text/vtt")


# # http://127.0.0.1:5000/caption/zh/video_id
# @app.get("/caption/zh/<string:video_id>")
# def get_caption_zh(video_id):
#     filepath = "./static/" + video_id + "/" + video_id + ".zh-CN.vtt"
#     print("filepath is: ", filepath)
#     isExisting = os.path.exists(filepath)
#     if not isExisting:
#         _download_video_with_subtitles(video_id)
#     return send_file(filepath, mimetype="text/vtt")


# http://127.0.0.1:5000/caption/bi/video_id
@app.get("/caption/bi/<string:video_id>")
def get_caption_bi(video_id):
    vtt_path = "./static/" + video_id + "/" + video_id + ".bi.vtt"
    return send_file(vtt_path, mimetype="text/vtt")


# @app.route("/video/<string:video_id>", methods=["GET"])
# def get_video_sub(video_id):
#     URL = "https://youtu.be/" + video_id
#     video_path = "./static"
#     return send_file(video_path, mimetype="video/mp4")


# # http://127.0.0.1:5000/caption/VAQMsprq-Ps/en
# @app.post("/caption/bi/<string:id>")
# def post_caption(id):
#     folder_path = "./static/" + id
#     onlyfiles = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]
#     data = ''
#     for ele in onlyfiles:
#         if ele.endswith("[" + id + "]." + 'bi' + ".vtt"):
#             data = ele
#             for caption in webvtt.read("./static/" + id + "/" + data):
#                 print(caption.start)
#                 print(caption.end)
#                 print(caption.text)
#             return make_response(data, 200)
#     return make_response(data, 200)


@app.post("/anki")
def create_anki_deck():
    pass


if __name__ == '__main__':
    app.run()
