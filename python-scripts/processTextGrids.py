# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import csv
from collections import defaultdict
import statistics as stats
import glob
import pandas as pd

keywords =  set(["greek", "sorority", "rush", "rushed", "rushing"])


def capitalize_keywords(text, keywords):
    words = text.split()
    capitalized_words = []
    for word in words:
        if word.lower() in [k.lower() for k in keywords]:  # Case-insensitive comparison
            capitalized_words.append("~" + word.upper() + "~")
        else:
            capitalized_words.append(word)
    return " ".join(capitalized_words)


def processTextGrids(qualtrics_csv, old_coded_csv):
    qualtrics = pd.read_csv(qualtrics_csv)
    qualtrics["speaker"] = qualtrics["speaker"].astype(str)
    qualtrics['Ethnicity'] = qualtrics['Ethnicity'].str.replace('Black or African American', 'Black')
    qualtrics_speakers = set(qualtrics["speaker"].unique())
    qualtrics["demo"] = qualtrics["Ethnicity"] + "_" + qualtrics["Gender"]
    qualtrics_dict = dict(zip(qualtrics.speaker,qualtrics.demo))
    print(qualtrics_dict)
    output = open("speaker_quotes.txt", "w")
    files = sorted(glob.iglob("python-scripts/Textgrids/*.textgrid"))
    textgrid_speakers = set()
    for fname in files:
        speaker = fname.split("_")[0][25:]
        # [25:] because speaker looks like python-scripts/Textgrids\6161, want only digits
        textgrid_speakers.add(speaker)
        reader = open(fname, encoding='utf-8', errors='ignore')
        if speaker in qualtrics_speakers:
            output.write("\n")
            output.write("########\n")
            output.write("\n")
            one_back = ""
            two_back = ""
            already_written = set()
            for line in reader:
                if "sentence - phones" in line:
                    print("BIG PROBLEM with " + str(speaker))
                if "text =" in line and len(line.split(" ")) > 2:
                    linetext = line.split("\"")[1].split("\"")[0].lower()
                    words = set(one_back.replace("\"","").replace("\n","").split(" "))
                    if keywords.intersection(words):
                        for l in [two_back, one_back, linetext]:
                            if l not in already_written:
                                output.write(speaker + " " + capitalize_keywords(l, keywords) + "\n" + "\n")
                                already_written.add(l)
                    two_back = one_back
                    one_back = linetext
        else:
            print("speaker " + str(speaker) + " is not in Qualtrics")

                  
    list_of_dicts = []

    for speaker in sorted(qualtrics_speakers):
        d = defaultdict(str)
        d["speaker"]= speaker
        if speaker in textgrid_speakers:
            d["is_textgrid?"] = True
        else:
            d["is_textgrid?"] = False
        list_of_dicts.append(d)
    df = pd.DataFrame(list_of_dicts)
    # this errors
    df.to_csv('TextGrid_coding_updated.csv', index=False)
    old_coded_csv = pd.read_csv(old_coded_csv)
    old_coded_csv = old_coded_csv.drop(columns = ["is_textgrid?"])
    old_coded_csv["speaker"] = old_coded_csv["speaker"].astype(str)
    df = pd.merge(df, old_coded_csv, on='speaker', how='left')
    df = df.sort_values(by=['is_textgrid?', 'speaker'], ascending=[False, True])
    df.to_csv("TextGrid_coding_updated.csv", index=False)
    
    print("Processed data from " + str(len(textgrid_speakers)) + " speakers")
    missing = qualtrics_speakers - textgrid_speakers
    print("Missing " + str(len(missing)) + " speakers:")
    print("This?",sorted(missing))
    output.close()
                
                







if __name__ == "__main__":
    processTextGrids("qualtrics_for_stats.csv", "TextGrid_coding.csv")
