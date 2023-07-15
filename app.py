from __future__ import unicode_literals
from flask import Flask, send_file
import openai
import os
from flask_cors import CORS
from download import download_video_and_subtitles
from mergeVTT import cleanup

app = Flask(__name__)
CORS(app)


# http://127.0.0.1:5000/video/video_id
@app.get("/video/<string:video_id>")
def get_video_id(video_id):
    # print('video_id is: ', video_id, os.getcwd())
    video_path = "./static/" + video_id + "/" + video_id + ".mp4"
    video_existing = os.path.exists(video_path)
    if not video_existing:
        download_video_and_subtitles(video_id)
    else:
        print("The video file exists.")
    vtt_path = "./static/" + video_id + "/" + video_id + ".bi.vtt"
    vtt_existing = os.path.exists(vtt_path)
    if not vtt_existing:
        cleanup(video_id)
    else:
        print("The bi-vtt file exists.")

    return send_file(video_path, mimetype="video")


# http://127.0.0.1:5000/search/clicked_word
@app.get("/search/<string:clicked_word>/<string:clicked_sentence>")
def get_translation(clicked_word, clicked_sentence):
    with open('key.txt') as f:
        openai.api_key = f.readlines()[0]
    openai.Model.list()
    content = "Imagine you are working as a bilingual dictionary between Chinese and English. Please give the most " \
              "likely translation of the given word " \
              "without " \
              "any " \
              "punctuation. If the " \
              "given word is in " \
              "Chinese, " \
              "please give " \
              "the English " \
              "translation. If the given word is in English, please give the Chinese translation. For example, " \
              "given 'travel': '旅行'; given '快乐': 'happy' or 'happiness'. Word: " + clicked_word + "."
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": content},
        ]
    )
    translation = completion.choices[0].message.to_dict()['content']
    corpus_path = "static/corpus.txt"
    check_corpus = os.path.isfile(corpus_path)
    if check_corpus:
        with open(corpus_path, 'a') as file:
            file.write(clicked_word + "\t" + translation + "\t" + clicked_sentence + "\n")
    else:
        with open(corpus_path, "w") as outfile:
            outfile.write(clicked_word + "\t" + translation + "\t" + clicked_sentence + "\n")
    return translation


# http://127.0.0.1:5000/caption/bi/video_id
@app.get("/caption/bi/<string:video_id>")
def get_caption_bi(video_id):
    vtt_path = "./static/" + video_id + "/" + video_id + ".bi.vtt"
    return send_file(vtt_path, mimetype="text/vtt")


@app.post("/anki")
def create_anki_deck():
    pass


if __name__ == '__main__':
    app.run()
