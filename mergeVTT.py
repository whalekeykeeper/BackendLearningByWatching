import re
import jieba
from datetime import timedelta
from pathlib import Path
from nltk.tokenize import word_tokenize

import srt
import webvtt
from vtt_to_srt.vtt_to_srt import ConvertDirectories


def merge(path1, path2, id):
    with path1.open(encoding='utf-8') as fi1:
        subs1 = {s.index: s for s in srt.parse(fi1)}

        for k, v in subs1.items():
            # To merge two rows into one row
            if "\n" in v.content:
                v.content = v.content.replace("\n", '')
            # To tokenize
            v.content = __tokenize_zh(v.content)

    with path2.open(encoding='utf-8') as fi2:
        subs2 = {s.index: s for s in srt.parse(fi2)}

        # To merge two rows into one row
        for k, v in subs2.items():
            if "\n" in v.content:
                v.content = v.content.replace("\n", ' ')
            #     # To tokenize
            # v.content = __tokenize_en(v.content)

    # To iterate all the lines in subs2 and find the closest existing timeframe slot in subs1
    # Using the library srt
    sub: srt.Subtitle
    start: int
    for index, sub in subs2.items():
        start: timedelta = sub.start

        # For each line in subs2, find the nearest slot in subs1 which has
        # the closest start time as the start time in that line of subs2
        nearest_slot_in_subs1: srt.Subtitle = __nearest(subs1.values(), start)
        nearest_slot_in_subs1.content = f'{nearest_slot_in_subs1.content}§{sub.content}'
        subs1[nearest_slot_in_subs1.index] = nearest_slot_in_subs1

    merged_path = "static/" + id + "/" + id + ".bi.srt"
    merged_srt = Path(merged_path)

    with merged_srt.open(mode='w', encoding='utf-8') as fout:
        fout.write(srt.compose(list(subs1.values())))

    return merged_path


def __tokenize_zh(text):
    # jieba.enable_paddle()
    # words = pseg.cut(text, use_paddle=True)  # paddle模式
    # for word, flag in words:
    #     print('%s %s' % (word, flag))
    #     print('%s %s' % (word, flag))

    words_list = list(jieba.cut(text, use_paddle=True))
    words = ""
    # for i, e in enumerate(words_list):
    #     if e in punc:
    #         words += e.strip()
    #     elif len(e.strip()) == 0:
    #         words += e.strip()
    #     elif re.search('[a-zA-Z0-9]', e) is not None:
    #         words += e.strip()
    #     else:
    #         words += "🀀" + e.strip() + "🀅"
    for i, e in enumerate(words_list):
        words += e + " "

    return words.strip()


def __tokenize_en(text):
    words_list = word_tokenize(text)

    words = ""
    for i, e in enumerate(words_list):
        if e == "'s" or e == "'m":
            words = words[:-1] + e + " "
        elif e.isalpha():
            words += "🀀" + e + "🀅" + " "
        else:  # to remove the whitespace before punctuation
            words = words[:-1] + e + " "
    return words.strip()


def __nearest(items, pivot):
    # Return the item in items which returns the smallest value for the function abs(item.start-pivot)
    return min(items, key=lambda x: abs(x.start - pivot))


def cleanup(id):
    path_zh = "static/" + id + "/" + id + ".zh-CN.vtt"
    path_en = "static/" + id + "/" + id + ".en.vtt"
    __convert_vtt_to_srt(path_zh)
    __convert_vtt_to_srt(path_en)

    path1 = Path(path_zh[:-4] + ".srt")
    path2 = Path(path_en[:-4] + ".srt")
    merged_srt_path = merge(path1, path2, id)

    __convert_srt_to_vtt(merged_srt_path)


def __convert_vtt_to_srt(vtt_path):
    # save in SRT format
    vtt = webvtt.read(vtt_path)
    vtt.save_as_srt()
    srt_path = vtt_path[:-4] + ".srt"

    convert_file = ConvertDirectories(vtt_path, enable_recursive=False, encoding_format="utf-8")
    convert_file.convert_vtt_to_str(srt_path)


def __convert_srt_to_vtt(srt_path):
    srt_input = open(srt_path, "r", encoding='utf8')
    vtt_output = open(Path(srt_path[:-4] + '.vtt'), "w", encoding='utf8')

    lines = srt_input.read().splitlines()

    vtt_output.write('WEBVTT\n\n')

    i = 1
    while i < len(lines):
        if not lines[i].isdigit():
            convline = re.sub(',(?! )', '.', lines[i])
            vtt_output.write(convline + '\n')
        i += 1
    vtt_output.close()


if __name__ == '__main__':
    id = 'aUBawr1hUwo'
    cleanup(id)
