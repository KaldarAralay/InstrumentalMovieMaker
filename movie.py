
import os
from PIL import Image
from pydub import AudioSegment
from moviepy.editor import *

# Standard video dimensions (you can adjust these as needed)
video_width = 1024
video_height = 768

# Function to check if file is an image and resize it
def check_and_resize_image(file_path):
    try:
        img = Image.open(file_path)
        # Resize image to match video dimensions
        img = img.resize((video_width, video_height))
        img.save(file_path)
        return True
    except IOError:
        return False

# Function to check if file is audio
def is_audio(file_path):
    try:
        AudioSegment.from_file(file_path)
        return True
    except:
        return False

def create_video(image_file, audio_files, root):
    print("Creating video...")
    # Concatenate all audio files into one
    combined_audio = AudioSegment.empty()
    for audio_file in audio_files:
        combined_audio += AudioSegment.from_file(audio_file)

    duration = len(combined_audio) / 1000  # Duration of audio file in seconds

    # Save combined audio to a file
    combined_audio_path = os.path.join(root, "combined_audio.wav")
    combined_audio.export(combined_audio_path, format="wav")

    # Use the image file to create a video clip
    clip = ImageSequenceClip([image_file], durations=[duration])
    clip.fps = 24  # Set the frames per second

    # Create the final video clip with audio
    final_clip = clip.set_audio(AudioFileClip(combined_audio_path))

    # Write the result to a file
    final_clip.write_videofile(os.path.join(root, "video.mp4"), fps=24)
    print("Video created!")

def main():
    print("Starting directory search...")

    # Search through directories
    for entry in os.scandir('.'):
        if entry.is_dir():
            root = entry.path
            print(f"Checking directory: {root}")
            # Check if directory has both image and audio
            has_image = False
            image_file = ""
            audio_files = []
            for file in os.listdir(root):
                file_path = os.path.join(root, file)
                if check_and_resize_image(file_path):
                    has_image = True
                    image_file = file_path
                    print(f"Image file found: {file_path}")
                if is_audio(file_path):
                    audio_files.append(file_path)
                    print(f"Audio file found: {file_path}")

            # If both image and audio files are found, create video
            if has_image and audio_files:
                # Create the video
                create_video(image_file, audio_files, root)

if __name__ == '__main__':
    main()
