from globals import notes
from evalutation import evaluate

t_tetrads = {
    #regular jazz5 tetrads
    'maj': [1,0,0,0,1,0,0,1,0,0,0,1],
    'min': [1,0,0,1,0,0,0,1,0,0,1,0],
    'dom': [1,0,0,0,1,0,0,1,0,0,1,0],
    'dim': [1,0,0,1,0,0,1,0,0,1,0,0],
    'hdim7': [1,0,0,1,0,0,1,0,0,0,1,0]}
t_triads = {
    #tedrads, and major/minor triads
    'maj': [1,0,0,0,1,0,0,1,0,0,0,0],
    'min': [1,0,0,1,0,0,0,1,0,0,0,0],
    'dom': [1,0,0,0,1,0,0,1,0,0,1,0],
    'dim': [1,0,0,1,0,0,1,0,0,1,0,0],
    'hdim7': [1,0,0,1,0,0,1,0,0,0,1,0]}
t_majtri = { 
    #tedrads, and only major triads
    #corresponds to the most common chords in JAAH
    'maj': [1,0,0,0,1,0,0,1,0,0,0,0],
    'min': [1,0,0,1,0,0,0,1,0,0,1,0],
    'dom': [1,0,0,0,1,0,0,1,0,0,1,0],
    'dim': [1,0,0,1,0,0,1,0,0,1,0,0],
    'hdim7': [1,0,0,1,0,0,1,0,0,0,1,0]}
t_tetrads_degree = {
    #tetrads built with the 4 strongest degrees
    # (including maj VI)
    'maj': [1,0,0,0,1,0,0,1,0,1,0,0],
    'min': [1,0,0,1,0,0,0,1,0,0,1,0],
    'dom': [1,0,0,0,1,0,0,1,0,0,1,0],
    'dim': [1,0,0,1,0,0,1,0,0,1,0,0],
    'hdim7': [1,0,0,1,0,0,1,0,0,0,1,0]}
t_pentads = {
    #the five strongest degrees
    'maj': [1,0,0,0,1,0,0,1,0,1,0,1],
    'min': [1,0,0,1,0,1,0,1,0,0,1,0],
    'dom': [1,0,1,0,1,0,0,1,0,0,1,0],
    'dim': [1,1,0,1,0,0,1,0,0,1,0,0],
    'hdim7': [1,0,0,1,0,1,1,0,0,0,1,0]}
t_hexads = {
    #the six strongest degrees
    'maj': [1,0,1,0,1,0,0,1,0,1,0,1],
    'min': [1,0,1,1,0,1,0,1,0,0,1,0],
    'dom': [1,0,1,0,1,1,0,1,0,0,1,0],
    'dim': [1,1,0,1,0,0,1,0,0,1,0,1],
    'hdim7': [1,0,0,1,0,1,1,1,0,0,1,0]}
t_anti_hexads = {
    #penalize the six weakest degrees
    'maj': [0,-1,0,-1,0,-1,-1,0,-1,0,-1,0],
    'min': [0,-1,0,0,-1,0,-1,0,-1,-1,0,-1],
    'dom': [0,-1,0,-1,0,0,-1,0,-1,-1,0,-1],
    'dim': [0,0,-1,0,-1,-1,0,-1,-1,0,-1,0],
    'hdim7': [0,-1,-1,0,-1,0,0,0,-1,-1,0,-1]}
t_hybrid = { 
    #regular jazz5 tetrads and
    # penalize the six weakest degrees
    'maj': [1,-1,0,-1,1,-1,-1,1,-1,0,-1,1],
    'min': [1,-1,0,1,-1,0,-1,1,-1,-1,1,-1],
    'dom': [1,-1,0,-1,1,0,-1,1,-1,-1,1,-1],
    'dim': [1,0,-1,1,-1,-1,1,-1,-1,1,-1,0],
    'hdim7': [1,-1,-1,1,-1,0,1,0,-1,-1,1,-1]}
t_heptads = {
    #the seven strongest degrees
    'maj': [1,0,1,0,1,1,0,1,0,1,0,1],
    'min': [1,0,1,1,0,1,0,1,0,1,1,0],
    'dom': [1,0,1,0,1,1,0,1,0,1,1,0],
    'dim': [1,1,1,1,0,0,1,0,0,1,0,1],
    'hdim7': [1,0,1,1,0,1,1,1,1,0,1,0]}
t_discrim = {
    # based on discriminating degrees
    'maj': [1,0,0,-1,1,0,-1,1,0,0,-1,1],
    'min': [1,0,0,1,-1,0,-1,1,0,0,1,-1],
    'dom': [1,0,0,-1,1,0,-1,1,0,0,1,-1],
    'dim': [1,0,0,1,-1,0,1,-1,0,1,-1,0],
    'hdim7': [1,0,0,1,-1,0,1,-1,0,0,1,-1]}

def predict_binary(chroma_vector, template=t_triads):
    """
    Returns the ordered list of the 60 chord classes and their score,
    from the best predicted chord to the least, using binary templates
    """
    rep_q = {}
    for chd in template: #each jazz5 chord
        norm = sum(template[chd])
        for r in range(12): #each note as first degree / possible root
            root_name = notes[r]

            p = 0
            for i in range(12):
                p += template[chd][(i-r)%12]*chroma_vector[i]
            p /= norm #normalize
            rep_q[root_name + ' ' + chd] = p
    #build and order the list
    lst_q = [[k, v] for k, v in rep_q.items()]
    lst_q.sort(key=lambda e: e[1], reverse = True)
    return(lst_q)

def ACE_binary(chromagram, ground_truth, template=t_triads):
    res = {}
    correct = 0 #perfect prediction
    rank = 0 #rank of the ground truth in the prediction
    dist_first = 0 #distance between ground truth and first predicted
    three_first = 0 #ground truth in the three most probable
    ten_first = 0 #ground truth in the ten most probable

    i_gtruth = 0
    i_vector = 0
    time1 = 0. # beginning of the studied segment
    time2 = 0. # end of the segment 
    total_duration = ground_truth[-1][0] #duration without unclassified chords
    predicted = predict_binary(chromagram[i_vector][1])
    while abs(time2-ground_truth[-1][0]) > 1e-2:
        #update ground truth and/or prediction for the next segment
        if ground_truth[i_gtruth][0] - chromagram[i_vector][0] > 0:
            #next chroma vector
            i_vector += 1
            time2 = ground_truth[i_gtruth][0]
            duration = time2 - time1
            predicted = predict_binary(chromagram[i_vector][1])
            if ground_truth[i_gtruth][2] == 'unclassified':
                total_duration -= duration
            else:
                eval = evaluate(predicted, ground_truth[i_gtruth][1], ground_truth[i_gtruth][2])
        elif ground_truth[i_gtruth][0] - chromagram[i_vector][0] < 0:
            #next ground truth
            i_gtruth += 1
            time2 = chromagram[i_vector][0]
            duration = time2 - time1
            if ground_truth[i_gtruth][2] == 'unclassified':
                total_duration -= duration
            else:
                eval = evaluate(predicted, ground_truth[i_gtruth][1], ground_truth[i_gtruth][2])
        else:
            #next ground truth and chroma vector
            i_gtruth += 1
            i_vector += 1
            time2 = chromagram[i_vector][0]
            duration = time2 - time1
            predicted = predict_binary(chromagram[i_vector][1])
            if ground_truth[i_gtruth][2] == 'unclassified':
                total_duration -= duration
            else:
                eval = evaluate(predicted, ground_truth[i_gtruth][1], ground_truth[i_gtruth][2])

        if ground_truth[i_gtruth][2] != 'unclassified':
            if ground_truth[i_gtruth][2] != 'N':
                if eval['ground-truth rank'] == 0:
                    correct += duration
                if eval['ground-truth rank'] < 3:
                    three_first += duration
                if eval['ground-truth rank'] < 10:
                    ten_first += duration
                rank += duration * eval['ground-truth rank']
            dist_first += duration * eval['first rank distance']

        time1 = time2

    res['CSR'] = 100*correct/total_duration
    res['average rank'] = rank/total_duration
    res['distance first'] = dist_first/total_duration
    res['three first'] = 100*three_first/total_duration
    res['ten first'] = 100*ten_first/total_duration
    res['duration'] = total_duration

    return(res)