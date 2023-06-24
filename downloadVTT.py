from __future__ import unicode_literals
import youtube_dl
from youtube_transcript_api import YouTubeTranscriptApi
import os


def download_cap_with_youtube_dl(url):
    ydl_opts = {
        'format': '(bestvideo[width>=1080][ext=mp4]/bestvideo)+bestaudio/best',  # Ensures best settings
        'writesubtitles': True,  # Adds a subtitles file if it exists
        'allsubtitles': True,  # Adds auto-generated subtitles file
        'subtitle': '--write-sub --sub-lang zh-Hans',  # writes subtitles file in english
        'subtitlesformat': 'srt',  # writes the subtitles file in "srt" or "ass/srt/best"
        'skip_download': True,  # skips downloading the video file
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print("Download Successful!")


def download_with_youtube_transcript_api(video_id):
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    transcripts = {}
    for element in transcript_list:
        if str(element.language).startswith("Chinese") or str(element.language_code).startswith("zh") or (str(
                element.language_code) == "en" and element.is_generated != True):
            transcripts = __save_subtitle(video_id, element, transcripts)
        else:
            continue
    return transcripts


def __save_subtitle(video_id, element, transcripts):
    lan = element.language
    lan_code = element.language_code
    data = element.fetch()
    no_of_trans = len(data)
    print("The current transcript is in :", lan, "\nit has: ", no_of_trans)

    transcripts[lan_code] = data

    vtt = __convert_to_vtt(data)

    output_file_path = os.path.join(os.getcwd() + "/static/" + video_id, video_id + "." + lan_code + ".vtt")
    with open(output_file_path, "w", encoding="utf-8") as vtt_file:
        vtt_file.write(vtt)
    print(f".vtt file saved at: {output_file_path}")
    return transcripts


def __convert_to_vtt(data):
    vtt_content = "WEBVTT\n\n"

    for item in data:
        start_time = __format_time(item['start'])
        end_time = __format_time(item['start'] + item['duration'])
        text = item['text']

        vtt_content += f"{start_time} --> {end_time}\n{text}\n\n"

    return vtt_content


def __format_time(time):
    minutes = int(time // 60)
    seconds = int(time % 60)
    milliseconds = int((time % 1) * 1000)

    return f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"


if __name__ == '__main__':
    id = "aUBawr1hUwo"
    download_with_youtube_transcript_api(id)
