import pygame
import os

class VideoPlayer:
    def __init__(self, reaction_videos):
        """Initialize the video player with reaction video paths."""
        pygame.init()
        self.reaction_videos = reaction_videos

    def play_reaction_video(self, reaction_type):
        """Play the correct reaction animation video."""
        if reaction_type not in self.reaction_videos:
            print("❌ No video available for this reaction!")
            return
        
        video_path = self.reaction_videos[reaction_type]
        os.system(f'start {video_path}')  # Opens video in default player

# Example Usage:
reaction_videos = {
    "water": "Vedio\one.mp4",  # Example: H2 + O2 → H2O
    "salt": "2nd.mp4",  # Example: Na + Cl → NaCl
}

player = VideoPlayer(reaction_videos)

# Example Calls:
# player.play_reaction_video("water")  # Plays the water formation video
# player.play_reaction_video("salt")  # Plays the salt formation video
