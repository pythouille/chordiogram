import matplotlib.pyplot as plt

from globals import root_subst

t_triads = {
    #tedrads, and major/minor triads
    'maj': [1,0,0,0,1,0,0,1,0,0,0,0],
    'min': [1,0,0,1,0,0,0,1,0,0,0,0],
    'dom': [1,0,0,0,1,0,0,1,0,0,1,0],
    'dim': [1,0,0,1,0,0,1,0,0,1,0,0],
    'hdim7': [1,0,0,1,0,0,1,0,0,0,1,0]}
t_tetrads = {
    #regular jazz5 tetrads
    'maj': [1,0,0,0,1,0,0,1,0,0,0,1],
    'min': [1,0,0,1,0,0,0,1,0,0,1,0],
    'dom': [1,0,0,0,1,0,0,1,0,0,1,0],
    'dim': [1,0,0,1,0,0,1,0,0,1,0,0],
    'hdim7': [1,0,0,1,0,0,1,0,0,0,1,0]}

def dist_triads(root1, jazz5_1, root2, jazz5_2):
    """
    jazz5 maj and min considered as triads, the others as tetrads ;
    manhattan distance computed between the templates
    """
    r1 = root_subst[root1]
    r2 = root_subst[root2]
    dist = 0
    for i in range(12):
        if t_triads[jazz5_1][(i-r1)%12] != t_triads[jazz5_2][(i-r2)%12]:
            dist += 1
    return dist

def dist_tetrads(root1, jazz5_1, root2, jazz5_2):
    """
    jazz5 chords considered as tetrads ;
    manhattan distance computed between the templates and divided by 2
    """
    r1 = root_subst[root1]
    r2 = root_subst[root2]
    diff = 0
    for i in range(12):
        if t_tetrads[jazz5_1][(i-r1)%12] != t_tetrads[jazz5_2][(i-r2)%12]:
            diff += 1
    return diff/2 #with tetrads, diff is always even

def order_chord(rep_q, top=20):
    """
    Builds an ordered histogram for chords
    """
    lst_q = [[k, v] for k, v in rep_q.items()]
    lst_q.sort(key=lambda e: e[1], reverse = True)
    lst_q = lst_q[:top]
    top = min(top,len(lst_q))
    chord_names = [ k[0] for k in lst_q ]
    chord_pb = [ k[1] for k in lst_q ]
    fig, ax = plt.subplots()
    ax.barh(range(top,0,-1), chord_pb, color='red', tick_label=chord_names)
    for i,v in enumerate(chord_pb):
        ax.text(v+0.01, top-i-0.3, str(v), color='black', fontsize= 8)
    ax.get_xaxis().set_visible(False)
    ax.set_ylabel('Chord')
    ax.set_title('Most probable chords')
    plt.show()

def evaluate(prediction, gt_root, gt_jazz5):
    """
    Returns information about the quality of the prediction,
    an ordered list of the most probable chord classes, compared
    to the ground truth chord (gt_root, gt_jazz5)
    """
    res = {}
    res['first'] = prediction[0][0]
    res['first rank score'] = prediction[0][1]
    if gt_jazz5 != 'N':
        ind = 0
        while prediction[ind][0] != gt_root + ' ' + gt_jazz5:
            ind += 1
        res['ground-truth rank'] = ind
        res['ground-truth score'] = prediction[ind][1]
        most_probable = prediction[0][0].split(' ')
        res['first rank distance'] = dist_tetrads(most_probable[0],
                                                  most_probable[1],
                                                  gt_root,
                                                  gt_jazz5)
    else:
        #particular case of N
        # TODO : add a criteria to predict N
        res['ground-truth rank'] = 61
        res['ground-truth score'] = 0
        res['first rank distance'] = 2
    return res