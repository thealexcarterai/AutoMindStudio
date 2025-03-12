from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.AudioClip import CompositeAudioClip
import os

def add_watermark(audio_path, output_path):
    """Adds subtle watermark to audio to avoid copyright claims"""
    # Load main audio
    main_audio = AudioFileClip(audio_path)
    
    # Generate AI watermark (or use premade file)
    watermark = AudioFileClip(os.path.join("assets", "watermark.wav")).volumex(0.1)
    
    # Combine
    final_audio = CompositeAudioClip([main_audio, watermark.loop(duration=main_audio.duration)])
    final_audio.write_audiofile(output_path)
    
    # Cleanup
    main_audio.close()
    watermark.close()
