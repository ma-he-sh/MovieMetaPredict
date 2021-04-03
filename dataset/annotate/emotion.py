import json
import os
from nrclex import NRCLex


def get_dataset_list():
    file_list = []
    dataset_dir =os.path.abspath(__file__ + "/../../")
    for file in os.listdir(dataset_dir + "/dataset_cleaned"):
        if file.endswith(".json"):
            file_list.append(os.path.join(dataset_dir + "/dataset_cleaned", file))
    return file_list


def emotion_storyline():
    empty_synopsis = "It looks like we don't have a Synopsis for this title yet."
    file_list = get_dataset_list()
    for file in file_list:
        with open(file) as data_file:
            data = json.load(data_file)
        for item in data:
            id = item['id']
            with open('../synopsis/' + id + '.txt', 'r') as f:
                synopsis = f.read()
            if empty_synopsis in synopsis:
                script_txt = item['meta'].get('storyline')
                if script_txt is None:
                    script_txt = item.get('description')
            else:
                script_txt = synopsis
            if len(script_txt)<=0:
                continue
            text_object = NRCLex(script_txt)
            raw_emotion_scores = text_object.raw_emotion_scores
            emotions = raw_emotion_scores.items()
            s = sum(raw_emotion_scores.values())
            for key, value in emotions:
                item[key] = value/s
        with open(file, 'w') as result_file:
            json.dump(data, result_file)
    return

emotion_storyline()
