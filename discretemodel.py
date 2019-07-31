import numpy as np
import matplotlib.pyplot as plt
from random import shuffle

from annotated_features import info_json
from audio_features import computeHPCP
from globals import name_jazz5, root_subst, degrees, discr_deg
from hexagram import init_hexagram, rotation_sixth

def sub_tr_down(c1, c2, c3,
                resolution=2,
                x_a=0,
                y_a=1,
                x_b=-1/(2*np.sqrt(3)),
                x_c=1/(2*np.sqrt(3)),
                y_c=0.5):
    """
    Returns the sub triangle id for a dot with coordonates (c1,c2,c3)
    in a ternary plot with given resolution;
    The total number of sub triangles in a ternary plot is 4^resolution

    III______A_____IIIb
       \ 2  /\ 3  /
        \  /0 \  /
        B\/____\/C
          \ 1  /
           \  /
            \/
             I
    """
    if resolution <= 0:
        return(0)

    if c1+c2+c3 > 1e-6:
        c1, c2, c3 = c1 / (c1+c2+c3), c2 / (c1+c2+c3), c3 / (c1+c2+c3)
    #we have y_b == y_c
    if 1-c1 < y_c:
        #sub triangle 1
        id = 1
        new_x_a = x_a
        new_y_a = y_c
        new_x_b = (x_a+x_b) / 2
        new_x_c = (x_a+x_c) / 2
        new_y_c = (3*y_c-y_a) / 2
        return(id*(4**(resolution-1)) + 
               sub_tr_down(c1, c2, c3, 
                           resolution-1,
                           new_x_a,
                           new_y_a,
                           new_x_b,
                           new_x_c,
                           new_y_c))
    elif c1-c2+c3 < 1 - y_a + np.sqrt(3)*x_a:
        #sub triangle 2
        id = 2
        new_x_a = x_b
        new_y_a = y_a
        new_x_b = (3*x_b-x_a) / 2
        new_x_c = (x_a+x_b) / 2
        new_y_c = (y_a+y_c) / 2
        return(id*(4**(resolution-1)) +
               sub_tr_down(c1, c2, c3,
                           resolution-1,
                           new_x_a,
                           new_y_a,
                           new_x_b,
                           new_x_c,
                           new_y_c))
    elif c3-c2-c1 > -1 + y_a + np.sqrt(3)*x_a:
        #sub triangle 3
        id = 3
        new_x_a = x_c
        new_y_a = y_a
        new_x_b = (x_a+x_c) / 2
        new_x_c = (3*x_c-x_a) / 2
        new_y_c = (y_a+y_c) / 2
        return(id*(4**(resolution-1)) +
               sub_tr_down(c1, c2, c3,
                           resolution-1,
                           new_x_a,
                           new_y_a,
                           new_x_b,
                           new_x_c,
                           new_y_c))
    else:
        #sub triangle 0
        id = 0
        new_x_a = x_a
        new_y_a = y_c
        new_x_b = (x_a+x_b) / 2
        new_x_c = (x_a+x_c) / 2
        new_y_c = (y_a+y_c) / 2
        return(id*(4**(resolution-1)) +
               sub_tr_up(c1, c2, c3,
                         resolution-1,
                         new_x_a,
                         new_y_a,
                         new_x_b,
                         new_x_c,
                         new_y_c))


def sub_tr_up(c1, c2, c3, resolution,
                x_a, y_a, x_b, x_c, y_c):
    """
    Returns the sub triangle id for a dot with coordonates (c1,c2,c3)
    in a triangle with given resolution;
    The total number of sub triangles in a ternary plot is 4^resolution
    
             /\\
            /1 \\
          B/____\C
          /\ 0  /\\
         /2 \  /3 \\
        /____\/____\\
              A
    """
    if resolution <= 0:
        return(0)
    
    #we have y_b = y_c
    if 1-c1 > y_c:
        #sub triangle 1
        id = 1
        new_x_a = x_a
        new_y_a = y_c
        new_x_b = (x_a+x_b) / 2
        new_x_c = (x_a+x_c) / 2
        new_y_c = (3*y_c-y_a) / 2
        return(id*(4**(resolution-1)) +
               sub_tr_up(c1, c2, c3,
                         resolution-1,
                         new_x_a,
                         new_y_a,
                         new_x_b,
                         new_x_c,
                         new_y_c))
    elif c3-c2-c1 < -1 + y_a + np.sqrt(3)*x_a:
        #sub triangle 2
        id = 2
        new_x_a = x_b
        new_y_a = y_a
        new_x_b = (3*x_b-x_a) / 2
        new_x_c = (x_a+x_b) / 2
        new_y_c = (y_a+y_c) / 2
        return(id*(4**(resolution-1)) +
               sub_tr_up(c1, c2, c3,
                         resolution-1,
                         new_x_a,
                         new_y_a,
                         new_x_b,
                         new_x_c,
                         new_y_c))
    elif c1-c2+c3 > 1 - y_a + np.sqrt(3)*x_a:
        #sub triangle 3
        id = 3
        new_x_a = x_c
        new_y_a = y_a
        new_x_b = (x_a+x_c) / 2
        new_x_c = (3*x_c-x_a) / 2
        new_y_c = (y_a+y_c) / 2
        return(id*(4**(resolution-1)) +
               sub_tr_up(c1, c2, c3,
                         resolution-1,
                         new_x_a,
                         new_y_a,
                         new_x_b,
                         new_x_c,
                         new_y_c))
    else:
        #sub triangle 0
        id = 0
        new_x_a = x_a
        new_y_a = y_c
        new_x_b = (x_a+x_b) / 2
        new_x_c = (x_a+x_c) / 2
        new_y_c = (y_a+y_c) / 2
        return(id*(4**(resolution-1)) +
               sub_tr_down(c1, c2, c3,
                           resolution-1,
                           new_x_a,
                           new_y_a,
                           new_x_b,
                           new_x_c,
                           new_y_c))

def coord_subtri(id, max,
                 x_a=0,
                 y_a=0,
                 x_b=-1/sqrt(3),
                 x_c=1/sqrt(3),
                 y_c=1):
    """
    Returns the coordonates of the sub triangle with given 'id'
    in a ternary plot composed by 'max' sub triangles ;

    Recursively, the sub area matches the following :
                 A____________B
            C     \ 2  /\ 3  /
           /\      \  /0 \  /
          /1 \      \/____\/
         /____\  OR  \ 1  /
        /\ 0  /\      \  /
       /2 \  /3 \      \/
     A/____\/____\B     C
    """
    max //= 4
    if max <= 0:
        #the given resolution is reached
        return([[x_a, y_a], [x_b, y_c], [x_c, y_c]]) #y_b=y_c
    area = id // max
    if area == 0:
        return(coord_subtri(id%max,
                            max,
                            x_a = x_a,
                            y_a = y_c,
                            x_b = (x_a+x_b) / 2,
                            x_c = (x_a+x_c) / 2,
                            y_c = (y_a+y_c) / 2))
    elif area == 1:
        return(coord_subtri(id%max,
                            max,
                            x_a = x_a,
                            y_a = y_a,
                            x_b = (x_a+x_b) / 2,
                            x_c = (x_a+x_c) / 2,
                            y_c = (y_a+y_c) / 2))
    elif area == 2:
        return(coord_subtri(id%max,
                            max,
                            x_a = (x_a+x_b) / 2,
                            y_a = (y_a+y_c) / 2,
                            x_b = x_b,
                            x_c = x_a,
                            y_c = y_c))
    else:
        return(coord_subtri(id%max,
                            max,
                            x_a = (x_a+x_c) / 2,
                            y_a = (y_a+y_c) / 2,
                            x_b = x_a,
                            x_c = x_c,
                            y_c = y_c))


def partition(nb_elements=113,nb_parts=5):
    """
    Generates a random partition 
    """
    lst = [k for k in range(nb_elements)]
    shuffle(lst)
    res = []
    for i in range(nb_parts):
        part = lst[int(np.floor(i*nb_elements/nb_parts))
                  :int(np.floor((i+1)*nb_elements/nb_parts))]
        res.append(part)
    return res


def norm_ternary(model):
    """
    Normalization of the discrete model such as the sum of coefficients
    of all sub triangles in each single ternary plot equals 1
    """
    size = len(model[0][0]) #number of sub triangles in a ternary plot
    for hex in range(5): #each hexagram
        for ter in range(6): #each ternary plot of the hexagram
            total = 0
            for tri in range(size): #each area of the ternary
                total += model[hex][ter][tri]
            if total > 1e-6:
                for tri in range(size):
                    model[hex][ter][tri] /= total

def norm_jazz5(model):
    """
    Normalization of the discrete model such as the sum of coefficients
    of the 5 sub triangles sharing common ternary plot and position,
    but corresponding to different hexagrams (/chord qualites)
    """
    size = len(model[0][0]) #number of sub triangles in a ternary plot
    for ter in range(6):
        for tri in range(size):
            total = 0
            for hex in range(5):
                total +=  model[hex][ter][tri]
            if total > 1e-6:
                for hex in range(5):
                    model[hex][ter][tri] /= total
    
def norm_hexagram(model):
    """
    Normalization of the discrete model such as the sum of coefficients
    of all sub triangles in a whole hexagram equals 1
    """
    size = len(model[0][0]) #number of sub triangles in a ternary plot
    for hex in range(5):
        total = 0
        for ter in range(6):
            for tri in range(size):
                total +=  model[hex][ter][tri]
        if total > 1e-6:
            for ter in range(6):
                for tri in range(size):
                    model[hex][ter][tri] /= total


def train_pre_model(track_list, annotations, partitions, resolution=2, chroma='hpcp', verbose=True):
    """
    Builds for each folder of the given partition of tracks the
    5 discrete hexagram models corresponding to the analysis of
    chord chroma contents
    """
    #initialization of the structure
    nb_folder = len(partition)
    pre_model = np.zeros((nb_folder,5,6,4**(resolution)),dtype=float)
    
    for folder in range(nb_folder):
        if verbose:
            print('### Training folder', folder+1)
        for i1 in partitions[folder]:
            track = track_list[i1]
            if verbose:
                print('Analysing', track)
            annot = annotations[i1]
            tuning, beats, roots, jazz5 = info_json(annot)
            if chroma == 'hpcp':
                V = computeHPCP(track, beats, tuningFrequency=tuning)
            else:
                raise("unknown chroma extraction, please choose 'hpcp' or 'nnls'")
            for i2, chd in enumerate(jazz5):
                if chd != 'N' and chd != 'unclassified':
                    v = V[i2]
                    root = root_subst[roots[i2]]
                    for ternary in range(6):
                        id_triangle = sub_tr_down(
                            v[root],
                            v[(root+degrees.index(discr_deg[ternary]))%12],
                            v[(root+degrees.index(discr_deg[(ternary+1)%6]))%12],
                            resolution=resolution
                            )
                        #increment the matching triangle
                        pre_model[folder][name_jazz5.index(chd)][ternary][id_triangle] += 1
    return(pre_model)

def build_model(pre_model, n, nb_folder=5):
    """
    Builds the training discrete model to test folder 'n';
    Normalization should be applied after its computation
    """
    size = len(pre_model[0][0][0])
    #sum of the (nb_folder - 1) sub models for training
    model = np.zeros((5,6,size),dtype=float)
    for i in range(nb_folder):
        if i != n: #folder n is kept for testing
            model += pre_model[i]

    return(model)


def print_model(model, quality=['maj','min','dom','dim','hdim7']):
    """
    Plots separately the hexagram models for given chords
    """
    #number of sub triangles in a ternary plot
    resolution = len(model[0][0])
    for q_name in quality:
        q = name_jazz5.index(q_name)
        
        #initialization
        fig, ax = plt.subplots(figsize=(4,3.5))
        init_hexagram(ax, q_name)

        #plot of the sub triangles
        for ternary in range(6):
            for tr in range(4**resolution):
                T = coord_subtri(tr, 4**resolution)
                for d in range(3):
                    T[d][0], T[d][1] = rotation_sixth(T[d][0], T[d][1], ternary)
                m = max(model[q][ternary])
                if m > 1e-10:
                    prop = model[q][ternary][tr] / m
                    t1 = plt.Polygon(T, color=(1,(1-prop),(1-prop)))
                    ax.add_patch(t1)
        plt.show()