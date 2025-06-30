from PIL import Image

# Patch for Pillow >= 10 compatibility with MoviePy
if not hasattr(Image, "ANTIALIAS") and hasattr(Image, "Resampling"):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

import os
os.environ["IMAGEMAGICK_BINARY"] = r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"


import os
import uuid
import srt
import requests
import whisper
from typing import List
from gtts import gTTS
from dotenv import load_dotenv
from datetime import timedelta
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
from termcolor import colored
from moviepy.video.fx.all import crop

# ... rest of your code


load_dotenv(".env")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def text_to_speech(text: str, path: str = "voiceover.wav"):
    print(colored("[+] Generating voiceover...", "blue"))
    tts = gTTS(text)
    tts.save(path)
    return path

def search_pexels_videos(query: str, api_key: str, it: int, min_dur: int) -> List[str]:
    headers = {"Authorization": api_key}
    qurl = f"https://api.pexels.com/videos/search?query={query}&per_page={it}"
    r = requests.get(qurl, headers=headers)
    response = r.json()

    video_urls = []
    for i in range(it):
        try:
            if response["videos"][i]["duration"] < min_dur:
                continue
            best_url = ""
            best_res = 0
            for file in response["videos"][i]["video_files"]:
                if ".com/video-files" in file["link"]:
                    resolution = file["width"] * file["height"]
                    if resolution > best_res:
                        best_res = resolution
                        best_url = file["link"]
            if best_url:
                video_urls.append(best_url)
        except:
            continue
    print(colored(f"[+] Found {len(video_urls)} videos for query", "cyan"))
    return video_urls

def download_video(url: str, directory: str = "./temp") -> str:
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, f"{uuid.uuid4()}.mp4")
    with open(path, "wb") as f:
        f.write(requests.get(url).content)
    return path

def combine_video_clips(video_paths: List[str], target_duration: int = 45) -> str:
    clips = []
    total_dur = 0
    target_w, target_h = 1080, 1920
    target_ratio = target_w / target_h  # 0.5625 (9:16)

    for path in video_paths:
        clip = VideoFileClip(path).without_audio()
        clip = clip.set_fps(30)

        # Calculate clip's aspect ratio
        clip_ratio = clip.w / clip.h

        # Use 'cover' logic: crop either width or height to fill target ratio
        if clip_ratio > target_ratio:
            # Clip is wider than target => crop width
            new_width = int(clip.h * target_ratio)
            clip = crop(clip, width=new_width, height=clip.h, x_center=clip.w // 2, y_center=clip.h // 2)
        else:
            # Clip is taller than target => crop height
            new_height = int(clip.w / target_ratio)
            clip = crop(clip, width=clip.w, height=new_height, x_center=clip.w // 2, y_center=clip.h // 2)

        # Resize to target size (1080x1920)
        clip = clip.resize((target_w, target_h))

        dur = min(clip.duration, target_duration - total_dur)
        clip = clip.subclip(0, dur)

        clips.append(clip)
        total_dur += dur
        if total_dur >= target_duration:
            break

    final = concatenate_videoclips(clips)
    path = f"./temp/{uuid.uuid4()}_combined.mp4"
    final.write_videofile(path, fps=30)
    return path


def transcribe_audio_locally(audio_path: str, model_size: str = "base"):
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path)
    return result['text'], result['segments']

def whisper_segments_to_srt(segments, output_path: str):
    subtitles = []
    for i, seg in enumerate(segments):
        start = timedelta(seconds=seg["start"])
        end = timedelta(seconds=seg["end"])
        subtitles.append(srt.Subtitle(index=i+1, start=start, end=end, content=seg["text"]))
    srt_data = srt.compose(subtitles)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(srt_data)
    return output_path

def add_subs_and_audio(video_path: str, audio_path: str, srt_path: str, color="white") -> str:
    def generator(txt):
        return TextClip(
            txt,
            font="./fonts/bold_font.ttf",
            fontsize=60,
            color=color,
            stroke_color="black",
            stroke_width=1,
            method="caption",                 # Enables word wrapping
            size=(1000, None),               # Max width to wrap text at 1000px (inside 1080px)
            align="center",                  # Center text horizontally
        )

    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    duration = video.duration  # Ensure all overlays match this

    # Subtitles
    subs = SubtitlesClip(srt_path, generator).set_duration(duration)

    # Black transparent mask
    mask_height = 1920
    mask = ColorClip(size=(1080, mask_height), color=(0, 0, 0), ismask=False).set_opacity(0.2)
    mask = mask.set_position(("center", "center")).set_duration(duration)

    # Composite
    final = CompositeVideoClip([video, mask, subs.set_position(("center", "center"))], size=(1080, 1920)).set_audio(audio)
    out_path = f"./temp/final_{uuid.uuid4()}.mp4"
    final.write_videofile(out_path, fps=30)
    return out_path


def main():
    # ✅ STEP 1: Psychology input fact
    input_text = """
        Did you know? Practicing gratitude daily rewires your brain to focus on positivity.  
        Just 5 minutes a day can improve your mental health and emotional resilience.  

        Gratitude boosts happiness chemicals like dopamine and serotonin.  
        It can reduce stress, improve sleep, and help you cope with challenges better.  

        People who practice gratitude are often more optimistic and have stronger relationships.  
        Try writing down three things you’re grateful for each day.  

        Small daily habits can create big changes in your mindset and wellbeing.
        """


    video_query = "nature calm"
    target_duration = 45  # 🎯 set to 45 seconds

    # STEP 2: TTS to voiceover.wav
    audio_path = text_to_speech(input_text)
    audio = AudioFileClip(audio_path)
    target_duration = int(audio.duration)  # sync video length to audio


    # STEP 3: Get stock videos
    video_urls = search_pexels_videos(video_query, PEXELS_API_KEY, it=6, min_dur=5)
    video_paths = [download_video(url) for url in video_urls]

    # STEP 4: Combine clips into vertical video
    combined_video = combine_video_clips(video_paths, target_duration)

    # STEP 5: Generate subtitles
    text, segments = transcribe_audio_locally(audio_path)
    srt_path = "./temp/subtitles.srt"
    whisper_segments_to_srt(segments, srt_path)

    # STEP 6: Add subs + audio to final video
    final_video_path = add_subs_and_audio(combined_video, audio_path, srt_path)
    print(colored(f"[✓] Final video saved at: {final_video_path}", "green"))

if __name__ == "__main__":
    main()
