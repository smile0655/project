
import numpy as np
import collections


def match(F_q, IL, IL_ref):
    t_q = F_q[:, 0]
    h_q = F_q[:, 1]
    max_shift_count = np.zeros(len(IL)) # store the max occurrences of time shift
    track_offset = np.zeros(len(IL))

    for music in range(len(IL)):
        IL_tmp = IL[music].copy()
        m_tmp = []
        for i in range(len(F_q)):
            l = IL_tmp.get(h_q[i])
            if l != None:
                n = t_q[i]
                m_tmp = m_tmp + (np.round((l[0] - n), 2)).tolist()
                #m_tmp.extend((np.round((l[0] - n), 2)).tolist())
        if (m_tmp != []):
            counter_m_tmp = collections.Counter(m_tmp)  # histogram
            max_m_counter_tmp = counter_m_tmp.most_common(1)

            max_shift_count[music] = max_m_counter_tmp[0][1]
            track_offset[music] = max_m_counter_tmp[0][0]

    maxcount = np.max(max_shift_count)
    identified_file = IL_ref[np.where(max_shift_count == maxcount)][0]
    offset = track_offset[np.where(max_shift_count == maxcount)][0]

    return identified_file, offset, max_shift_count
