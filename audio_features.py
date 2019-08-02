import numpy as np

import essentia
import essentia.standard as ess
import vamp


#inspired by https://github.com/mip-frontiers/summer-school-2019/blob/master/ChordEstimation/ACE_MIP-Frontiers.ipynb
def compute_beats(filename):
    audio = ess.MonoLoader(filename=filename, sampleRate=44100)()
    
    bt = ess.BeatTrackerMultiFeature()
    
    beats, confidence = bt(audio)
    beats = essentia.array([round(beat,2) for beat in beats])
    np.append(beats, len(audio) / 44100.0)
    
    return beats


#inspired by https://github.com/mip-frontiers/summer-school-2019/blob/master/ChordEstimation/ACE_MIP-Frontiers.ipynb
def compute_HPCP(filename, beats,
                 tuning_frequency=440.0,
                 beatsperframe=1,
                 framesize=16384,
                 hopsize=8192):
    audio = ess.MonoLoader(filename=filename, sampleRate=44100)()
    
    frameGenerator = ess.FrameGenerator(audio, 
                                        frameSize=framesize,
                                        hopSize=hopsize,
                                        startFromZero=True)
    window = ess.Windowing(type='blackmanharris62')
    spectrum = ess.Spectrum()
    spectralPeaks = ess.SpectralPeaks(magnitudeThreshold=1e-05,
                                      maxFrequency=5000,
                                      minFrequency=40,
                                      maxPeaks=1000,
                                      orderBy="frequency",
                                      sampleRate=44100)
    spectralWhitening = ess.SpectralWhitening(maxFrequency=5000,
                                              sampleRate=44100)
    
    hpcp = ess.HPCP(normalized='none',
                    sampleRate=44100,
                    maxFrequency=5000,
                    minFrequency=40,
                    referenceFrequency=tuning_frequency,
                    nonLinear=False,
                    harmonics=8,
                    size=12)
    
    pool = essentia.Pool()
    
    for frame in frameGenerator:
        spectrum_mag = spectrum(window(frame))
        frequencies, magnitudes = spectralPeaks(spectrum_mag)
        w_magnitudes = spectralWhitening(spectrum_mag, frequencies, magnitudes)
        hpcp_vector = hpcp(frequencies, w_magnitudes)
        pool.add('hpcp0', hpcp_vector)

    #Beat-synchronous averaging
    beat_index = 0
    saved_vectors = [pool['hpcp0'][0]]*beatsperframe
    pool.add('hpcp', saved_vectors[0])
    for i, local_hpcp in enumerate(pool['hpcp0'][1:]):
        if beat_index >= len(beats):
            break
        if i*hopsize > beats[beat_index]*44100: #enter a new beat
            beat_index += 1
            hpcp_vector = saved_vectors[0] #take the finished vector
            if max(hpcp_vector) > 1e-5:
                hpcp_vector /= max(hpcp_vector) #UnitMax normalization
            pool.add('hpcp', hpcp_vector)

            saved_vectors = saved_vectors[1:] #alignment
            saved_vectors.append(local_hpcp) #begin next vector
        else:
            for v in saved_vectors:
                v += local_hpcp #add the value to all saved vectors
    
    return np.roll(pool['hpcp'], shift=-3, axis=1)

#inspired by https://github.com/seffka/pychord_tools/blob/master/pychord_tools/third_party.py
def compute_NNLS(filename, beats, beats_per_frame=2, step_size=4096):
    audio = ess.MonoLoader(filename=filename, sampleRate=44100)()
    
    seffkawindow = np.array(
        [0.001769, 0.015848, 0.043608, 0.084265, 0.136670, 0.199341, 0.270509,
         0.348162, 0.430105, 0.514023, 0.597545, 0.678311, 0.754038, 0.822586, 
         0.882019, 0.930656, 0.967124, 0.990393, 0.999803, 0.999803, 0.999803,
         0.999803, 0.999803, 0.999803, 0.999803, 0.999803, 0.999803, 0.999803, 
         0.999803, 0.999803, 0.999803, 0.999803, 0.999803, 0.999803, 0.999803,
         0.999803, 0.999803, 0.999803, 0.999803, 0.999803, 0.999803, 0.999803, 
         0.999650, 0.996856, 0.991283, 0.982963, 0.971942, 0.958281, 0.942058,
         0.923362, 0.902299, 0.878986, 0.853553, 0.826144, 0.796910, 0.766016, 
         0.733634, 0.699946, 0.665140, 0.629410, 0.592956, 0.555982, 0.518696,
         0.481304, 0.444018, 0.407044, 0.370590, 0.334860, 0.300054, 0.266366, 
         0.233984, 0.203090, 0.173856, 0.146447, 0.121014, 0.097701, 0.076638, 
         0.057942, 0.041719, 0.028058, 0.017037, 0.008717, 0.003144, 0.000350])
    
    stepsize, semitones = vamp.collect(audio,
                                       44100,
                                       "nnls-chroma:nnls-chroma",
                                       output="semitonespectrum",
                                       step_size=step_size)["matrix"]
    chroma = np.zeros((semitones.shape[0], 12))

    for i in range(semitones.shape[0]):
        tones = semitones[i] * seffkawindow
        cc = chroma[i]
        for j in range(tones.size):
            cc[j % 12] = cc[j % 12] + tones[j]

    #Beat-synchronous averaging
    beat_index = 0
    saved_vectors = [chroma[0]]*beats_per_frame
    nnls = [saved_vectors[0]]
    for i, local_hpcp in enumerate(chroma[1:]):
        if beat_index >= len(beats):
            break
        if i*step_size > beats[beat_index]*44100: #enter a new beat
            beat_index += 1
            nnls_vector = saved_vectors[0] #take the finished vector
            if max(nnls_vector) > 1e-5:
                nnls_vector /= max(nnls_vector) #UnitMax normalization
            nnls.append(nnls_vector)

            saved_vectors = saved_vectors[1:] #alignment
            saved_vectors.append(local_hpcp) #begin next vector
        else:
            for v in saved_vectors:
                v += local_hpcp #add the value to all saved vectors

    return np.roll(nnls, shift=-3, axis=1)


import matplotlib.pyplot as plt
if __name__ == "__main__":
    test_beats = compute_beats('../sounds/maple_leaf_rag(hyman).flac')
    print('Computed beats for Maple Leaf Rag (Hyman):\n', test_beats)

    test_HPCP = compute_HPCP('../sounds/maple_leaf_rag(hyman).flac', test_beats)
    #print('\nComputed HPCP for Maple Leaf Rag (Hyman):\n', test_HPCP)
    plt.pcolormesh(np.transpose(test_HPCP))

    test_NNLS = compute_NNLS('../sounds/maple_leaf_rag(hyman).flac', test_beats)
    #print('\nComputed NNLS for Maple Leaf Rag (Hyman):\n', test_NNLS)
    plt.pcolormesh(np.transpose(test_NNLS))