import webvtt


def parseVTT(vtt_zh, vtt_en):
    for e in [vtt_en, vtt_zh]:
        for caption in webvtt.read(e):
            # print(caption.start)
            # print(caption.end)
            # print(caption.text)
            pass


if __name__ == '__main__':
    vtt_zh = "static/VAQMsprq-Ps/VAQMsprq-Ps.zh-Hans.vtt"
    vtt_en = "static/VAQMsprq-Ps/VAQMsprq-Ps.en.vtt"
    parseVTT(vtt_zh, vtt_en)
