import parselmouth
from parselmouth.praat import call, run_file
import glob
import pandas as pd
import numpy as np
import scipy
from scipy.stats import binom
from scipy.stats import ks_2samp
from scipy.stats import ttest_ind
import os


snd = parselmouth.Sound("audio_files/sample.wav")

def mysptotal(m,p):
    sound=p+"/"+m+".wav"
    sourcerun=p+"/myspsolution.praat"
    path=p+"/"
    try:
        objects= run_file(sourcerun, -20, 2, 0.3, "yes",sound,path, 80, 400, 0.01, capture_output=True)
        print (objects[0]) # This will print the info from the sound object, and objects[0] is a parselmouth.Sound object
        z1=str( objects[1]) # This will print the info from the textgrid object, and objects[1] is a parselmouth.Data object with a TextGrid inside
        z2=z1.strip().split()
        z3=np.array(z2)
        z4=np.array(z3)[np.newaxis]
        z5=z4.T
        dataset=pd.DataFrame({"number_ of_syllables":z5[0,:],"number_of_pauses":z5[1,:],"rate_of_speech":z5[2,:],"articulation_rate":z5[3,:],"speaking_duration":z5[4,:],
                          "original_duration":z5[5,:],"balance":z5[6,:],"f0_mean":z5[7,:],"f0_std":z5[8,:],"f0_median":z5[9,:],"f0_min":z5[10,:],"f0_max":z5[11,:],
                          "f0_quantile25":z5[12,:],"f0_quan75":z5[13,:]})
        print (dataset.T)
        
        z5_float_type=z5.astype('f') 

        # pause_duration_mean
        pause_dur_mean = round(z5_float_type[5].item() - z5_float_type[4].item(), 2)
        print("pause_dur_mean:          ", pause_dur_mean)
        # pause_duration_percentage
        pause_dur_percentage = round(pause_dur_mean/z5_float_type[5].item()*100, 2)
        print("pause_dur_percentage    ", pause_dur_percentage)
        # speaking_duration_percentage
        speak_dur_percentage = round(z5_float_type[4].item()/z5_float_type[5].item()*100, 2)
        print("speaking_dur_percentage     ", speak_dur_percentage)
        # avg_syllable_duration
        avg_syllable_duration = round(z5_float_type[5].item()/z5_float_type[0].item(), 2)
        print("avg_syllable_duration        ", avg_syllable_duration)
    except:
        print ("Try again the sound of the audio was not clear")
    return;

m = 'sample'
p=r'/home/matic/PROJEKT/audio_files'
mysptotal(m,p)



pointProcess = parselmouth.praat.call(snd, "To PointProcess (periodic, cc)...", 75.0, 600.0)
# local jitter
jitter_local = parselmouth.praat.call(pointProcess, "Get jitter (local)...", 0, 0, 0.0001, 0.02, 1.3)
print("local jitter     ", round(jitter_local, 2))
# absolute jitter
jitter_absolute_local = parselmouth.praat.call(pointProcess, "Get jitter (local, absolute)...", 0.0, 0.0, 0.0001, 0.02, 1.3)
print("local absolute jitter    ", round(jitter_absolute_local,2))
# local shimmer
shimmer_local = parselmouth.praat.call([snd, pointProcess], "Get shimmer (local)...", 0.0, 0.0, 0.001, 0.02, 1.3, 1.6)
print("local shimmer    ", round(shimmer_local, 2))
# local db shimmer
shimmer_local_dB = parselmouth.praat.call([snd, pointProcess], "Get shimmer (local_dB)...", 0.0, 0.0, 0.001, 0.02, 1.3, 1.6)
print("local db shimmer     ", round(shimmer_local_dB, 2))
# harmonicity
harmonicity = parselmouth.praat.call(snd, "To Harmonicity (ac)...", 0.002, 75.0, 0.1, 4.5)
# mean harmonics to noise ratio
meanhnr = parselmouth.praat.call(harmonicity, "Get mean...", 0.0, 0.0)
print("mean hnr     ", round(meanhnr, 2))

formant = parselmouth.praat.call(snd, "To Formant (burg)...", 0.002, 4.0, 5500.0, 0.025, 50.0)
# f2_range
f2_min = parselmouth.praat.call(formant, "Get minimum...", 2, 0.0, 0.0, "hertz", "parabolic")
f2_max = parselmouth.praat.call(formant, "Get maximum...", 2, 0.0, 0.0, "hertz", "parabolic")
f2_range = f2_max-f2_min
print("f2 range     ", round(f2_range, 2))
# f1_avg
f1_avg = parselmouth.praat.call(formant, "Get mean...", 1, 0.0 ,0.0, "hertz")
print("f1 average   ", round(f1_avg,2))
# f2_ avg
f2_avg = parselmouth.praat.call(formant, "Get mean...", 2, 0.0 ,0.0, "hertz")
print("f2 average   ", round(f2_avg, 2))
# f3_avg
f3_avg = parselmouth.praat.call(formant, "Get mean...", 3, 0.0 ,0.0, "hertz")
print("f3 average   ", round(f3_avg,2))
# f4_avg
f4_avg = parselmouth.praat.call(formant, "Get mean...", 4, 0.0 ,0.0, "hertz")
print("f4 average   ", round(f4_avg, 2))


pitch = parselmouth.praat.call(snd, "To Pitch", 0.0, 60, 350)
# pitch_avg
pitch_avg = parselmouth.praat.call(pitch, "Get mean...", 0.0, 0.0, "Hertz")
print("pitch average    ", round(pitch_avg, 2))

ltas = parselmouth.praat.call(snd, "To Ltas...", 100)
h1 = parselmouth.praat.call(ltas, "Get value in bin...", 2)
third_formant = parselmouth.praat.call(formant, "Get maximum...", 3, 0.0, 0.0, "hertz", "parabolic")
# aplitude_diff_H!_A3
amplitude_diff_H1_A3 = h1 - third_formant
print("amplitude diff H1_A3     ", round(amplitude_diff_H1_A3, 2))
# mean intensity
intensity = parselmouth.praat.call(snd, "To Intensity", 100.0, 0.0, True)
intensity_mean = parselmouth.praat.call(intensity, "Get mean...", 0.0, 0.0, "energy")
print("mean intensity    ", round(intensity_mean, 2))