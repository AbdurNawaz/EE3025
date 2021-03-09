import soundfile as sf
from scipy import signal

input_signal, fs = sf.read('Sound_Noise.wav')

sample_freq = fs

order = 4

cutoff_freq = 2570
Wn = 2.4*cutoff_freq/sample_freq

b, a = signal.butter(order, Wn, 'low')

temp1 = signal.filtfilt(b, a, input_signal)

temp = input_signal.copy()

#cascading filters
for i in range(20):
  temp = signal.filtfilt(b, a, temp)

sf.write('ReducedNoise.wav', temp1, fs)
sf.write('betterReducedNoise.wav', temp, fs)
