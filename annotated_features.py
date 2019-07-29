import json


notes = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
root_subst = {
    'C': 0, 'C#': 1, 'Db': 1, 'D': 2,
    'D#': 3, 'Eb': 3, 'E': 4, 'Fb': 4,
    'E#': 5, 'F': 5, 'F#': 6, 'Gb': 6,
    'G': 7, 'G#': 8, 'Ab': 8, 'A': 9,
    'A#': 10, 'Bb': 10, 'B': 11, 'Cb': 11,
    'B#': 0, 'N': 0}


def root_jazz5(chrd):
    """ Renvoie la racine de l'accord et sa classe selon Jazz5 """
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
    return(root, j5)



def info_json(json_file):
    with open(json_file,'r') as inf:
        data = json.load(inf)

    tuning = data['tuning']
    if tuning != 'TODO': #dans minor swing par exemple
        tuning = float(tuning)
    else:
        tuning = 440.

    global_metre = int((data['metre'].split('/'))[0])

    jazz5 = ['N']
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
                            jazz5.append(c)
                    else: #adding implicit chords
                        for i in range(metre):
                            jazz5.append(chords[(i*len(chords))//metre])
        else: #there are subparts
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
                                jazz5.append(c)
                        else:
                            for i in range(metre):
                                jazz5.append(chords[(i*len(chords))//metre])
    jazz5.append('N')
    beats.append(float(data['duration']))

    #Separating root and quality of chords
    roots = []
    for i in  range(len(jazz5)):
        r, c = root_jazz5(jazz5[i])
        roots.append(r)
        jazz5[i] = c

    return(tuning, beats, roots, jazz5)

