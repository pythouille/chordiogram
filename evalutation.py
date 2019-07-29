root_subst = {
    'C': 0, 'C#': 1, 'Db': 1, 'D': 2,
    'D#': 3, 'Eb': 3, 'E': 4, 'Fb': 4,
    'E#': 5, 'F': 5, 'F#': 6, 'Gb': 6,
    'G': 7, 'G#': 8, 'Ab': 8, 'A': 9,
    'A#': 10, 'Bb': 10, 'B': 11, 'Cb': 11,
    'B#': 0, 'N': 0}
template_tetrads = {
    'maj': [1,0,0,0,1,0,0,1,0,0,0,1],
    'min': [1,0,0,1,0,0,0,1,0,0,1,0],
    'dom': [1,0,0,0,1,0,0,1,0,0,1,0],
    'dim': [1,0,0,1,0,0,1,0,0,1,0,0],
    'hdim7': [1,0,0,1,0,0,1,0,0,0,1,0],
    'N': [0,0,0,0,0,0,0,0,0,0,0,0]
}

def distance_tetrads(root1, jazz5_1, root2, jazz5_2):
    """
    jazz5 en tetrades ; puis manhattan distance
    """
    r1 = root_subst[root1]
    r2 = root_subst[root2]
    diff = 0
    for i in range(12):
        if template_tetrads[jazz5_1][(i-r1)%12] != template_tetrads[jazz5_2][(i-r2)%12]:
            diff += 1
    return diff/2 #with tetrads, diff is always even
