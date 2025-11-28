# This is a part of addition word
# MECH 5302 final exam question
# Just because easy to use the ide so i take a short cut

import numpy as np
import matplotlib.pyplot as plt

# Frequencies
a = 1.0   # Hz
b = 0.9   # Hz

# Sampling rates
fs_high = 100    # High sampling rate (Hz)
fs_low = 1.33    # Low sampling rate (Hz)

# Duration
T = 40.0         # seconds

# Time arrays
t_high = np.arange(0, T, 1/fs_high)
t_low = np.arange(0, T, 1/fs_low)

# Signal generation
F_high = np.sin(2*np.pi*a*t_high) + np.sin(2*np.pi*b*t_high)
F_low = np.sin(2*np.pi*a*t_low) + np.sin(2*np.pi*b*t_low)

# Plot the signals
plt.figure(figsize=(8, 8))

plt.subplot(2, 1, 1)
plt.plot(t_high, F_high)
plt.title('High Sampling Rate: 100 Hz')
plt.xlabel('Time [s]')
plt.ylabel('$F(t)$')

plt.subplot(2, 1, 2)
plt.plot(t_low, F_low)
plt.title('Low Sampling Rate: 1.33 Hz')
plt.xlabel('Time [s]')
plt.ylabel('$F(t)$')
plt.tight_layout()
plt.show()

# FFT for high sampling rate
fft_high = np.fft.fft(F_high)
freq_high = np.fft.fftfreq(len(F_high), d=1/fs_high)

# FFT for low sampling rate
fft_low = np.fft.fft(F_low)
freq_low = np.fft.fftfreq(len(F_low), d=1/fs_low)

plt.figure(figsize=(8, 8))

plt.subplot(2, 1, 1)
plt.stem(freq_high[:len(freq_high)//2], np.abs(fft_high)[:len(freq_high)//2])
plt.title('FFT Spectrum (High Sampling Rate)')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Magnitude')
plt.xlim(0, 2)

plt.subplot(2, 1, 2)
plt.stem(freq_low[:len(freq_low)//2], np.abs(fft_low)[:len(freq_low)//2])
plt.title('FFT Spectrum (Low Sampling Rate)')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Magnitude')
plt.xlim(0, 2)

plt.tight_layout()
plt.show()