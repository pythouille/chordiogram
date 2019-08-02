import matplotlib.pyplot as plt
from time import monotonic, sleep

import pygame

from annotated_features import info_json

def match_beat_chord(json):
    """
    Synchronize the beats with the ground-truth chords
    """
    synchr = []

    _, beats, chords = info_json(json)
    for i in range(len(chords)):   
        synchr.append([beats[i],chords[i]])
    synchr.append([beats[-1],'END'])
    return(synchr)


def play_basic(json, audio='none'):
    #initialization
    track = match_beat_chord(json)
    i = 1

    #countdown
    print(3)
    sleep(1)
    print(2)
    sleep(1)
    print(1)
    sleep(0.8)

    #audio
    if audio != 'none':
        pygame.mixer.init()
        pygame.mixer.music.load(audio)
        pygame.mixer.music.play()
    sleep(0.2)

    begin = monotonic()
    print(track[0][1])
    while track[i][1] != 'END':
        t = monotonic()
        if t-begin > track[i][0]:
            print(track[i][1])
            i += 1
        sleep(0.01) #pause



def play_plot(json, audio='none'):
    #initialization
    track = match_beat_chord(json)
    l = len(track)
    i = 0
    tmp = 'N' #the last played chord, to avoid repetitions
    fig, ax = plt.subplots(figsize=(14,1))
    ax.set_xlim(0,5)
    ax.get_xaxis().set_visible(False)
    ax.set_ylim(0,0.2)
    ax.get_yaxis().set_visible(False)

    #stop the sound if the window is closed
    closed = False
    def stop_sound(evt):
        pygame.mixer.music.stop()
    fig.canvas.mpl_connect('close_event', stop_sound)

    #countdown
    for d in ['3','2','1']:
        ax.cla()
        ax.set_xlim(0,4.5)
        ax.set_ylim(0,0.5)
        ax.text(0.2, 0.1, d, fontsize=10, fontweight='bold')
        plt.pause(1)
    
    #audio
    if audio != 'none':
        pygame.mixer.init()
        pygame.mixer.music.load(audio)
        pygame.mixer.music.play()
        sleep(0.2)

    #main loop
    begin = monotonic()
    ax.cla()
    ax.set_xlim(0,6.5)
    ax.set_ylim(0,0.2)
    plt.pause(0.1)
    while track[i][1] != 'END' and closed == False:
        t = monotonic()
        if t-begin > track[i][0]:
            ax.cla()
            ax.set_xlim(0,4.5)
            ax.set_ylim(0,0.2)
            for j in range(12):
                ax.plot([0.5*j,0.5*j],[0.1,0.15]) #lines between beats
                if 0 <= i+j < l:
                    if j == 0 or track[i+j][1] != tmp:
                        ax.text(0.05 + 0.5*j,0.1,track[i+j][1], fontsize=10, fontweight='bold')
                        tmp = track[i+j][1]
            ax.text(0.1, 0.05, '^',fontsize=10, fontweight='bold')
            ax.text(4.1, 0.02, 'time ->',fontsize=10)
            i += 1
        plt.pause(0.1)

if __name__ == "__main__":
    jukebox = {
        '1': 'maple_leaf_rag(hyman)',
        '2': 'from_monday_on',
        '3': 'girl_from_ipanema',
        '4': 'blue_7',
        '5': 'giant_steps'
    }
    print(jukebox)
    foo = input('Choose your favorite track : ')
    bar = input('Enter 1 for basic reader, 2 for graphic reader : ')

    if bar == '1':
        play_basic('../json/'+jukebox[foo]+'.json', '../sounds/'+jukebox[foo]+'.flac')
    elif bar == '2':
        play_plot('../json/'+jukebox[foo]+'.json', '../sounds/'+jukebox[foo]+'.flac')