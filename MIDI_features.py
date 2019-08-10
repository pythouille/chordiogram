import numpy as np
import matplotlib.pyplot as plt
from math import floor, ceil

import music21 as m21

from annotated_features import info_json, root_jazz5_list
from audio_features import compute_beats, compute_HPCP
from hexagram import init_hexagram, plot_chord


def beat_segmentation(beat, duration):
    """
    Return the length of each successive beat,
    from the time 'beat' for a given duration
    Example : beat_segementation(9.75, 1.75) returns [0.25, 1., 0.5]
    """
    res = []
    lim = duration
    time = beat
    while lim > 1e-6:
        prop = min(lim,ceil(time + 1e-6)-time)
        res.append(prop)
        time += prop
        lim -= prop
    return(res)


def extract_voices(midi_file='maple_leaf_ragMIDI.mid'):
    """
    Return a list of m21.voice and/or m21.part extracted from a known MIDI file
    """
    res = []

    if midi_file == 'maple_leaf_ragMIDI.mid':
        strm = m21.converter.parse(midi_file)
        res.append(strm[0])
        res.append(strm[1])
    else:
        print("Error : unknown MIDI file")
    return(res)


def add_voice(spec, voice):
    """
    Add the contribution of a MIDI voice to a chromagram
    Inputs : spec : list of list of 12 float ~ chromagram
             voice : m21.stream.voice or m21.stream.part to add
    """
    i_voice =  0 #index of current element in "voice"
    beat = 0. #number of quarters passed (float)
    tmp=0
    while i_voice < len(voice):
        #add the notes to the vector
        element_duration = voice[i_voice].duration.quarterLength

        typ = type(voice[i_voice])
        if typ == m21.chord.Chord: #it is a chord
            for d in beat_segmentation(beat, element_duration):
                for n in voice[i_voice]: #for each note of the chord
                    spec[floor(beat + 1e-6)][n.pitch.pitchClass] += n.volume.velocityScalar * d
                beat += d
        elif typ == m21.note.Note: #it is a unique note
            for d in beat_segmentation(beat, element_duration):
                spec[floor(beat + 1e-6)][voice[i_voice].pitch.pitchClass] += voice[i_voice].volume.velocityScalar * d
                beat += d
        elif typ == m21.note.Rest: #or it is a rest
            beat += element_duration
        i_voice += 1


def midi_comparison(bpm=116.):
    """
    Plot an animation comparing for each beat / each chord
    three chordiograms computed from 3 sources of the same track
    (Maple Leaf Rag) :
    - In green : annotated source midi file
    - In blue : MIDI synthesized audio
    - In red : real audio (Hyman, 1975)
    """
    #Extract ground truth chords
    _, _, chords = info_json('../json/maple_leaf_rag(hyman).json')
    json_roots, json_jazz5 = root_jazz5_list(chords)

    #Extract real chromagram
    beats = compute_beats('../sounds/maple_leaf_rag(hyman).flac')
    HPCP_audio = compute_HPCP('../sounds/maple_leaf_rag(hyman).flac', beats)

    #Extract synthesized MIDI audio chromagram
    HPCP_midi = [12*[0] for i in range(292)]
    for v in extract_voices('maple_leaf_ragMIDI.mid'):
        add_voice(HPCP_midi, v)
    HPCP_midi = HPCP_midi[1:] #correct an extra beat for alignment

    #Extract chromagram from real audio
    beats = compute_beats('maple_leaf_ragMIDI.flac')
    HPCP_audio_midi = compute_HPCP('maple_leaf_ragMIDI.flac', beats)

    #representation
    fig, hex = plt.subplots(figsize=(6,5))
    for index, r in enumerate(json_roots):
        init_hexagram(hex, r + ' ' + json_jazz5[index])
        plot_chord(hex, HPCP_midi[index], r, 'g')
        #print(HPCP_midi[index])
        plot_chord(hex, HPCP_audio_midi[index], r, 'b')
        plot_chord(hex, HPCP_audio[index], r, 'r')
        #plt.show()
        plt.pause(60./bpm)
        hex.clear()
    plt.close('all')


if __name__ == "__main__":
    midi_comparison()