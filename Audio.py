# Create audio_sounds class
    # Create method for background music
    # Create methods for each sound effect
        # If SFX is already playing, don't play another
# Create AudioControls class
    # Create master_volume method
    # Create sound_effects_volume method

import os
import playsound


class BGM:
    def playBGM(filename : str  = 'Mysteriousproblem.mp3'):
        filepath = os.path.join(os.getcwd(), 'GameAssets', filename)
        if (os.path.exists(filepath) and filename != ''):
            playsound.playsound(filepath, False)


class SFX:
    def playSFX(filename: str = '', asyncronous: bool = True):
        filepath = os.path.join(os.getcwd(), 'GameAssets', filename)
        if (os.path.exists(filepath) and filename != ''):
            playsound.playsound(filepath, not asyncronous)
