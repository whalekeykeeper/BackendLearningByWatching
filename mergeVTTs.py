import difflib


def read_vtt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content


def parse_vtt_content(content):
    lines = content.strip().split('\n\n')
    segments = []

    for line in lines:
        if line.startswith("WEBVTT"):
            continue
        linesplit = line.split('\n')
        timing = linesplit[0]
        text = ' '.join(linesplit[1:])
        start, end = timing.split(' --> ')
        start_time = format_time_to_seconds(start)
        duration = format_time_to_seconds(end) - start_time
        segment = {'text': text, 'start': start_time, 'duration': duration}
        segments.append(segment)
    return segments


def format_time_to_seconds(time):
    parts = time.split(':')
    pre = parts[0]
    post = parts[1].split('.')
    parts = [pre, post[0], post[1]]
    h, m, s = map(float, parts)
    return h * 3600 + m * 60 + s


def merge_segments(segments1, segments2):
    merged_segments = []

    for segment1, segment2 in zip(segments1, segments2):
        merged_text = f"{segment1['text']}\n\n{segment2['text']}"
        merged_segment = {'text': merged_text, 'start': segment1['start'], 'duration': segment1['duration']}
        merged_segments.append(merged_segment)
    return merged_segments


def convert_to_vtt(segments):
    vtt_content = "WEBVTT\n\n"

    for segment in segments:
        start_time = format_seconds_to_time(segment['start'])
        end_time = format_seconds_to_time(segment['start'] + segment['duration'])
        text = segment['text']

        vtt_content += f"{start_time} --> {end_time}\n{text}\n\n"

    return vtt_content


def format_seconds_to_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if str(hours) == str(minutes) == str(seconds) == "0.0":
        return "00:00.000"
    else:
        if int(hours) < 10:
            hours = "0" + str(hours)
        if int(minutes) <10:
            minutes = "0" + str(minutes)
        if int(seconds) < 10:
            seconds = "00" + str(seconds)
        elif int(seconds) < 100:
            seconds = "0" + str(seconds)

        return str(hours) + ":" + str(minutes) + "." + str(seconds)


def align_segments(segments1, segments2):
    aligned_segments = []

    for segment1 in segments1:
        best_match = None
        best_ratio = 0

        for segment2 in segments2:
            ratio = difflib.SequenceMatcher(None, segment1['text'], segment2['text']).ratio()

            if ratio > best_ratio:
                best_match = segment2
                best_ratio = ratio

        if best_match is not None:
            aligned_segment = {'text': segment1['text'] + '\n\n' + best_match['text'],
                               'start': segment1['start'], 'duration': segment1['duration']}
            aligned_segments.append(aligned_segment)

    return aligned_segments


def main(id):
    path_zh = "static/" + id + "/" + id + ".zh-CN.vtt"
    path_en = "static/aUBawr1hUwo/aUBawr1hUwo.en.vtt"
    # Read the "zh-CN.vtt" and "en.vtt" files
    zh_content = read_vtt_file(path_zh)
    en_content = read_vtt_file(path_en)

    # Parse the contents of the .vtt files into segments
    zh_segments = parse_vtt_content(zh_content)

    en_segments = parse_vtt_content(en_content)

    # Align the segments
    aligned_segments = align_segments(zh_segments, en_segments)

    # Merge the aligned segments
    merged_segments = merge_segments(aligned_segments, en_segments)

    # Convert the merged segments to .vtt format
    vtt_content = convert_to_vtt(merged_segments)

    # Write the merged segments to a new .vtt file
    output_file_path = 'merged_subtitles.vtt'
    with open(output_file_path, 'w', encoding='utf-8') as vtt_file:
        vtt_file.write(vtt_content)

    print(f"Merged subtitles saved at: {output_file_path}")


if __name__ == '__main__':
    id = "aUBawr1hUwo"
    # main(id)
    