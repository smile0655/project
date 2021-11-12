import numpy as np
import pydub
from getfp import fingerprint
from match import match


arr = np.load("./last_result/kiki/kiki500.npz",allow_pickle=1)
b500 = arr['arr_0']
arr1 = np.load("./last_result/kiki/kiki_ref500.npz",allow_pickle=1)
b500id = arr1['arr_0']

IL = b500
IL_id = b500id

print("kiki301-500")


for ii in range(1,7):
    music = pydub.AudioSegment.from_wav('./queries/queries/Q'+f"{ii:01d}" + '.wav')
    rate = music.frame_rate
    width = music.frame_width
    duration = music.duration_seconds
    channel = music.channels
    # Convert imported signal to a numeric array, serializing the two channels
    music_array = np.array(music.get_array_of_samples())
    # Normalize array to [-1, 1]
    music_array = (music_array / 2 ** 16) * 2
    if music.channels == 2:
        music_array = music_array[::2]

    F_q = fingerprint(music_array, rate)
    identified_file,offset, track_most_common_offset_counter = match(F_q,IL,IL_id)


    print(f'Q{ii}')
    maxcount = np.max(track_most_common_offset_counter)
    print(maxcount)
    print(f'kiki_{identified_file:04d}.wav')
    print(offset)
    np.savez_compressed('./last_match/kikicounter301-500'+f"Q{ii}", track_most_common_offset_counter)
