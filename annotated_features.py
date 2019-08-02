import numpy as np
import json

from audio_features import compute_beats, compute_HPCP
from globals import notes, root_subst

def info_json(json_file):
    with open(json_file,'r') as inf:
        data = json.load(inf)

    tuning = data['tuning']
    if tuning != 'TODO': #in minor swing
        tuning = float(tuning)
    else:
        tuning = 440.

    global_metre = int((data['metre'].split('/'))[0])

    chord_list = ['N']
    beats = [0.]
    for part in data["parts"]:
        if "chords" in part:
            if "metre" in part: #local change in metre
                metre = int((part['metre'].split('/'))[0])
            else: #by default
                metre = global_metre
            beats += part['beats']
            for line in part["chords"]:
                bars = line.split("|") #bar segmentation
                for bar in [x for x in bars if x != '' and x != ' ']:
                    chords = bar.split(' ') #chord segmentation in a bar
                    chords = [x for x in chords if x != '']
                    if len(chords) >= metre:
                        for c in chords:
                            chord_list.append(c)
                    else: #adding implicit chords
                        for i in range(metre):
                            chord_list.append(chords[(i*len(chords))//metre])
        else: #if there are subparts
            for subpart in part["parts"]:
                if "metre" in part: #local change in metre
                    metre = int((subpart['metre'].split('/'))[0])
                else:  #by default
                    metre = global_metre
                beats += subpart['beats']
                for line in subpart["chords"]:
                    bars = line.split("|") #bar segmentation
                    for bar in [x for x in bars if x != '' and x != ' ']:
                        chords = bar.split(' ') #chord segmentation in a bar
                        chords = [x for x in chords if x != '']
                        if len(chords) >= metre:
                            for c in chords:
                                chord_list.append(c)
                        else:
                            for i in range(metre):
                                chord_list.append(chords[(i*len(chords))//metre])
    chord_list.append('N')
    beats.append(float(data['duration']))

    return tuning, beats, chord_list


def root_jazz5(chrd):
    """
    Extract separately the root and jazz5 class of a chord
    """
    j5 = "unclassified" #for sus4, for example
    root = "N"
    #Removing the bass
    if '/' in chrd:
        chrd = chrd.split('/')[0]
    #Case with a single letter
    if ':' not in chrd: 
        if chrd == "N":
            j5 = "N"
        else:
            j5 = "maj"
    #Abbreviated notations
    elif "min" in chrd: #min, min6, min7, minmaj7, min9
        j5 = "min"
    elif "maj" in chrd: #maj, maj6, maj7, maj9
        j5 = "maj"
    elif "hdim" in chrd:
        j5 = "hdim7"
    elif "dim" in chrd:
        j5 = "dim"
    elif "aug" in chrd:
        j5 = "maj"
    elif ":7" in chrd or ":9" in chrd:
        j5 = "dom"
    #Or by analysing degrees
    elif "(" in chrd:
        degrees = (chrd[:-1].split('('))[1].split(',')
        if '3' in degrees: #major 3rd
            if 'b7' in degrees: #minor 7th
                j5 = "dom"
            else:
                j5 = "maj"
        elif 'b3' in degrees: #minor 3rd
            if 'b5' in degrees: #diminished 5th
                if 'b7' in degrees: #minor 7th
                    j5 = "hdim7"
                else:
                    j5 = "dim"
            else:
                j5 = "min"
    #Avoiding enharmonics
    root = notes[root_subst[chrd.split(':')[0]]]
    return root, j5


def root_jazz5_list(chord_list):
    """
    Extract separately the root and jazz5 class
    for each chord of a list
    """
    roots = []
    jazz5 = []
    for i in  range(len(chord_list)):
        r, c = root_jazz5(chord_list[i])
        roots.append(r)
        jazz5.append(c)
    return roots, jazz5


def stat(rep,rep_q):
    diff_chords = len(rep_q)
    print("Number of different chords : ",diff_chords)
    tot_beats = 0
    for key in rep_q:
        tot_beats += rep_q[key]
    print("Total number of beats :",tot_beats)
    print(" Chord  |   Beats   |    Beats %")
    #print('{:>6} | {:<6} | {:<} %'.format('Chord', 'Beats', 'Beats %')
    for key in rep:
        beats = 0
        for ch in rep[key]:
            beats += rep_q[ch]
        #print("  ",key,"        ", beats,"       ", 100 * beats / tot_beats )
        print('{:>6} | {:<6} | {:>6} %'.format(key, beats, 100*beats / tot_beats))


def analyse(track):
    """
    Print information about the track :
    number of beats, types and number of chords
    """
    print('\nRésultat pour', track)

    #initialization of the structure
    d_chords = {"maj": [],
                "min": [],
                "dom": [],
                "hdim": [],
                "dim": [],
                "N": ['N'],
                "unclassified": []
                }
    d_counter = {'N':2} #end and beginning
    
    _, _, grid = info_json(track)
    for chord in grid:
        _, converted = root_jazz5(chord)
        if chord in d_chords[converted]: #chord already known
            d_counter[chord] += 1
        else: #new chord discovered
            d_chords[converted].append(chord)
            d_counter[chord] = 1
    print(d_chords)
    print(d_counter)
    stat(d_chords, d_counter)

def group_by_quality(d_counter):
    """
    Gather all the chords from d_counter which has the same quality,
    remove the root
    """
    d_quality={}
    for chd in d_counter:
        #remove the root
        if ':' in chd:
            quality = chd.split(':')[1]
        elif chd!='N':
            quality = 'maj'
        else:
            quality = chd

        #creating or incrementing the matching chord quality
        if quality in d_quality:
            d_quality[quality] += d_counter[chd]
        else:
            d_quality[quality] = d_counter[chd]
    return(d_quality)

def info_track(track_name, json_name):
    """
    Align beat-synchronous chroma vectors and ground truth chord annotations
    """
    beats = compute_beats(track_name)
    tuning, json_beats, json_chords = info_json(json_name)
    json_roots, json_jazz5 = root_jazz5_list(json_chords)

    chromagram_beat = compute_HPCP(track_name, beats, tuning_frequency=tuning)
    #alignment of the chromagram with the time of the beats
    chromagram = []
    for i in range(min(len(chromagram_beat),len(beats))):
        chromagram.append([beats[i], chromagram_beat[i]])
    chromagram.append([beats[-1]+0.02, np.array(12*[0])])

    #time alignment of ground truth chords
    ground_truth = []
    for i in range(len(json_roots)):
        ground_truth.append([json_beats[i], json_roots[i], json_jazz5[i]])
    ground_truth.append([beats[-1], 'N', 'N'])
    
    return chromagram, ground_truth

