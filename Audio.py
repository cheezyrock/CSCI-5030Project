# Create audio_sounds class
    # Create method for background music
    # Create methods for each sound effect
        # If SFX is already playing, don't play another
# Create AudioControls class
    # Create master_volume method
    # Create sound_effects_volume method

import os
import playsound
GAME_ASSET_PATH = os.path.join(os.getcwd(), 'GameAssets')


class BGM:
    def playBGM(filename : str  = 'Mysteriousproblem.mp3'):
        filepath = os.path.join(GAME_ASSET_PATH, filename)
        if os.path.exists(filepath):
            playsound.playsound(filepath, False)


class SFX:
    def playSFX(filename: str = None, asyncronous: bool = True):
        if filename is None:
            raise ValueError("Filename must be provided")
        filepath = os.path.join(GAME_ASSET_PATH, filename)
        if os.path.exists(filepath):
            playsound.playsound(filepath, not asyncronous)
