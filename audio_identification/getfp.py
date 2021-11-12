import numpy as np
from scipy import signal
def fingerprint(music_array,rate):
    window_size = int(0.1 * rate)
    hop_size = int(0.05 * rate)
    zero_padding = 4 * window_size
    f, t, stft = signal.stft(music_array, fs=rate, window="hann", nfft=zero_padding, nperseg=window_size,
                             noverlap=window_size - hop_size)
    stft_magnitudes = np.abs(stft)
    db = 20 * np.log10(stft_magnitudes / np.max(stft_magnitudes))
    deltaT = 0.8
    bands = 25
    deltaF = rate / 2 / bands
    time_seg = int(np.floor(t[-1] / deltaT))
    anc = []

    for i in range(bands):
        f_index = (f >= (i * deltaF)) & (f < ((i + 1) * deltaF))
        f_index = np.where(f_index == True)[0]
        for j in range(time_seg):
            t_index = (t >= (j * deltaT)) & (t < ((j + 1) * deltaT))
            t_index = np.where(t_index == True)[0]
            frame = db[f_index[0]:f_index[-1], t_index[0]:t_index[-1]]
            max_index = np.argmax(frame, axis=None)
            max_index = np.unravel_index(max_index, frame.shape)
            f_max_index = f_index[max_index[0]]
            t_max_index = t_index[max_index[1]]
            anc.append([f[f_max_index], t[t_max_index]])
    anc = np.array(anc)

    fingerprint = []

    for A in anc:
        f1 = A[0]
        t1 = A[1]
        freqs_anc = anc[:, 0]
        times_anc = anc[:, 1]
        freq_zone = [2 ** (-0.5), 2 ** (0.5)]
        f_index = ((f1 * freq_zone[0]) <= freqs_anc) & ((f1 * freq_zone[1]) > freqs_anc)
        f_target = np.where(f_index == True)[0]
        t_index = ((t1 + deltaT) <= times_anc) & ((t1 + 6 * deltaT) > times_anc)
        t_target = np.where(t_index == True)[0]
        target_idx = np.intersect1d(f_target, t_target)
        target_anchors = anc[target_idx]
        for t_anch in target_anchors:
            f2 = t_anch[0]
            t2 = t_anch[1]
            dt = t2 - t1
            hash = (f1, f2, dt)
            fingerprint.append([t1, hash])

    fp = np.array(fingerprint, dtype=object)
    return fp