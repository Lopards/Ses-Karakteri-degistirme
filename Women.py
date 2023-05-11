import parselmouth
from parselmouth.praat import call
from IPython.display import Audio

def women():
    sound = parselmouth.Sound("kayit.wav")

    Audio(data=sound.values, rate=sound.sampling_frequency)


    manipulation = call(sound, "To Manipulation", 0.05, 60, 600)

    type(manipulation)

    pitch_tier = call(manipulation, "Extract pitch tier")

    call(pitch_tier, "Multiply frequencies", sound.xmin, sound.xmax, 3)

    call([pitch_tier, manipulation], "Replace pitch tier")
    sound_octave_up = call(manipulation, "Get resynthesis (overlap-add)")

    Audio(data=sound_octave_up.values, rate=sound_octave_up.sampling_frequency)

    sound_octave_up.save("kadin_sesi.wav", "WAV")
    Audio(filename="kadin_sesi.wav")
