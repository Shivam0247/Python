import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt


audio_file_path = 'C:\Data\workspace\Advance Python\Audio\moj.wav'
audio_data, sample_rate = librosa.load(audio_file_path, sr=None)
 
 
plt.figure(figsize=(14, 5))
librosa.display.waveshow(audio_data, sr=sample_rate)
plt.title('Original Waveform')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.show()


speed_audio = librosa.effects.time_stretch(audio_data, rate=1.5)


pitch_audio = librosa.effects.pitch_shift(audio_data, sr=sample_rate, n_steps=2)


silence = np.zeros(int(sample_rate * 1))
audio_with_silence = np.concatenate((audio_data, silence))


plt.figure(figsize=(14, 5))
librosa.display.waveshow(audio_with_silence, sr=sample_rate)
plt.title('Waveform after Adding Silence')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.show()


spectrogram = librosa.stft(audio_data)
spectrogram_db = librosa.amplitude_to_db(abs(spectrogram))

plt.figure(figsize=(14, 5))
librosa.display.specshow(spectrogram_db, sr=sample_rate, x_axis='time', y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.title('Spectrogram')
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.show()


plt.figure(figsize=(14, 5))
librosa.display.waveshow(speed_audio, sr=sample_rate)
plt.title('Waveform after Changing Playback Speed')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.show()


plt.figure(figsize=(14, 5))
librosa.display.waveshow(pitch_audio, sr=sample_rate)
plt.title('Waveform after Changing Pitch')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.show()

