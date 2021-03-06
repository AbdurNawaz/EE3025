import numpy as np
import soundfile as sf
from scipy import signal
import matplotlib.pyplot as plt

def  plot_fft(signal, title, fs):
  plt.figure(figsize=(6,2))
  N = len(signal)
  T = 1/fs
  fft  = np.abs(np.fft.fft(signal))
  fft = fft[0:N//2]
  freq = np.fft.fftfreq(signal.size, d=T)
  freq = freq[:N//2]
  plt.plot(freq, fft)
  plt.xlim([0, 6000])
  plt.savefig(title+'.eps')
  plt.show()

  return fft, freq

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

original_fft, freq = plot_fft(input_signal, 'before', fs)
filtered_fft, freq = plot_fft(temp1, 'after-1', fs)
cascaded_fft, freq = plot_fft(temp, 'after-2', fs)

original_pre = 0
filtered_pre = 0
cascaded_pre = 0
original_post = 0
filtered_post = 0
cascaded_post = 0

for i in range(len(freq)):
    if freq[i]<cutoff_freq:
        original_pre += original_fft[i]
        filtered_pre += filtered_fft[i]
        cascaded_pre += cascaded_fft[i]
    else:
        original_post += original_fft[i]
        filtered_post += filtered_fft[i]
        cascaded_post += cascaded_fft[i]
print('Pre fraction: ', original_pre/original_fft.sum(), filtered_pre/filtered_fft.sum(), cascaded_pre/cascaded_fft.sum())
print('Post fraction: ', original_post/original_fft.sum(), filtered_post/filtered_fft.sum(), cascaded_post/cascaded_fft.sum())
