import argparse
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
        sub_nearest_slot.content = f'{sub_nearest_slot.content}<br>{sub.content}'
        subs1[sub_nearest_slot.index] = sub_nearest_slot

    generated_srt = Path("static/" + id + "/" + id + ".bi.vtt")

    with generated_srt.open(mode='w', encoding='utf-8') as fout:
        fout.write(srt.compose(list(subs1.values())))


if __name__ == '__main__':
    id = 'aUBawr1hUwo'
    path_zh = "static/" + id + "/" + id + ".zh-CN.vtt"
    path_en = "static/" + id + "/" + id + ".en.vtt"
    convert_vtt_to_srt(path_zh)
    convert_vtt_to_srt(path_en)

    path1 = Path(path_zh[:-4] + ".srt")
    path2 = Path(path_en[:-4] + ".srt")
    merge(path1, path2, id)
