import argparse
import os
import re
import sys
from datetime import timedelta
from pathlib import Path

import srt
import webvtt
from vtt_to_srt.vtt_to_srt import ConvertDirectories


def convert_vtt_to_srt(vtt_path):
    # save in SRT format
    vtt = webvtt.read(vtt_path)
    vtt.save_as_srt()
    srt_path = vtt_path[:-4] + ".srt"

    convert_file = ConvertDirectories(vtt_path, enable_recursive=False, encoding_format="utf-8")
    convert_file.convert_vtt_to_str(srt_path)


def convert_srt_to_vtt(srt_path):
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


def nearest(items, pivot):
    return min(items, key=lambda x: abs(x.start - pivot))


def merge(path1, path2, id):
    with path1.open(encoding='utf-8') as fi1:
        subs1 = {s.index: s for s in srt.parse(fi1)}

    with path2.open(encoding='utf-8') as fi2:
        subs2 = {s.index: s for s in srt.parse(fi2)}

    # iterate all subs in srt2 and find the closest EXISTING slot in srt1
    sub: srt.Subtitle
    start: int
    for idx, sub in subs2.items():
        start: timedelta = sub.start
        sub_nearest_slot: srt.Subtitle = nearest(subs1.values(), start)
        sub_nearest_slot.content = f'{sub_nearest_slot.content}\n<br>{sub.content}'
        subs1[sub_nearest_slot.index] = sub_nearest_slot

    merged_path = "static/" + id + "/" + id + ".bi.srt"
    merged_srt = Path(merged_path)

    with merged_srt.open(mode='w', encoding='utf-8') as fout:
        fout.write(srt.compose(list(subs1.values())))

    return merged_path


if __name__ == '__main__':
    # id = 'aUBawr1hUwo'
    # path_zh = "static/" + id + "/" + id + ".zh-CN.vtt"
    # path_en = "static/" + id + "/" + id + ".en.vtt"
    # convert_vtt_to_srt(path_zh)
    # convert_vtt_to_srt(path_en)
    #
    # path1 = Path(path_zh[:-4] + ".srt")
    # path2 = Path(path_en[:-4] + ".srt")
    # merged_srt_path = merge(path1, path2, id)
    #
    # convert_srt_to_vtt(merged_srt_path)


    pwd = os.getcwd()
    print(pwd)
    vtt = "static/aUBawr1hUwo/aUBawr1hUwo.bi.vtt"
    count_br = 0
    count_arrow = 0
    with open(vtt) as f:
        lines = f.readlines()
        for index, element in enumerate(lines):
            # print(index, element)
            if "<br>" in element:
                count_br += 1
            if "-->" in element:
                count_arrow += 1
            if count_arrow == count_br:
                print(index, element)
            print(count_br, count_arrow)
            print(count_br==count_arrow)


