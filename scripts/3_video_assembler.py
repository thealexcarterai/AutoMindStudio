from moviepy.editor import *
import requests

def create_video(script):
    clips = []
    for scene in script['scenes']:
        # Get CC-BY footage
        pexels_response = requests.get(
            f"https://api.pexels.com/videos/search?query={scene['keywords']}&per_page=1",
            headers={"Authorization": config['pexels']}
        )
        video_url = pexels_response.json()['videos'][0]['video_files'][0]['link']
        
        # Apply transformative edits
        clip = VideoFileClip(video_url)\
            .speedx(factor=1.1)\
            .fx(vfx.colorx, 0.9)\
            .margin(10)\
            .set_duration(scene['duration'])
        
        clips.append(clip)
    
    final_video = concatenate_videoclips(clips)
    final_video.write_videofile(f"outputs/final_videos/{script['title']}.mp4")
