#!/usr/bin/env python 
# -*- coding:utf-8 -*-

import numpy as np
import pydub
from getdataset import getdataset
import time

inverted_lists = []
inverted_lists_ref = []


# bouba
bouba_zero_crossings_train = []
for i in range(1,501):
  time1 = time.time()
  music = pydub.AudioSegment.from_file('./kikibouba_data/bouba/bouba_'  + f"{i:04d}" + '.wav',format="wav")
  #print('Processing file kiki_' + f"{i:04d}" + '.m4a')
  rate = music.frame_rate
  width = music.frame_width
  duration = music.duration_seconds
  channel = music.channels
  # Convert imported signal to a numeric array, serializing the two chhaels
  music_array = np.array(music.get_array_of_samples())
  # Normalize array to [-1, 1]
  music_array = (music_array / 2 ** 16) * 2
  if music.channels == 2:
      music_array = music_array[::2]
  inverted_list_tmp=getdataset(music_array,rate)
  inverted_lists.append(inverted_list_tmp)
  inverted_lists_ref.append(i)
  if i % 50 == 0:
    np.savez_compressed('./last_result/bouba'+f"{i}", inverted_lists)
    np.savez_compressed('./last_result/bouba_ref'+f"{i}", inverted_lists_ref)
  print(i)
  print(time.time()-time1)
  del inverted_list_tmp
