import pygame
import random

class AudioPlayer:
    def __init__(self, appreciation_files, wrong_answer_files):
        """Initialize the audio player with appreciation and wrong answer audio files."""
        pygame.mixer.init()
        self.appreciation_files = appreciation_files
        self.wrong_answer_files = wrong_answer_files

    def play_random_appreciation(self):
        """Play a random appreciation audio."""
        file = random.choice(self.appreciation_files)
        self._play_audio(file)

    def play_random_wrong_answer(self):
        """Play a random wrong answer audio."""
        file = random.choice(self.wrong_answer_files)
        self._play_audio(file)

    def _play_audio(self, file_path):
        """Load and play the given audio file."""
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

    def stop(self):
        """Stop any playing audio."""
        pygame.mixer.music.stop()

# Example Usage:
appreciation_sounds = ["app1.mp3", "app2.mp3", "app3.mp3"]
wrong_sounds = ["wrong1.mp3", "wrong2.mp3"]

player = AudioPlayer(appreciation_sounds, wrong_sounds)

# Example Calls:
# player.play_random_appreciation()  # Plays a random appreciation sound
# player.play_random_wrong_answer()  # Plays a random wrong answer sound
