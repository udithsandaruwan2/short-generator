### 🔹 Project Description

> This Python-based video automation tool generates **engaging AI-powered storytelling videos**. It uses Pexels stock footage, Whisper for audio transcription, gTTS for voiceovers, and MoviePy for video editing. The result is a **vertical or horizontal YouTube-ready video** with voice and subtitles — created entirely from a text input.

---

# AI Video Generator 🎬🤖

This project automatically creates engaging videos with subtitles and voiceovers from input text. It uses:
- 🧠 Whisper (OpenAI) for audio transcription
- 🗣️ gTTS (Google Text-to-Speech) for voiceover
- 🎞️ Pexels stock videos as visuals
- 🛠️ MoviePy for video processing and overlaying subtitles

---

## 📌 Features

- Generate professional-quality videos from plain text
- Voiceover using `gTTS`
- Subtitles using Whisper + SRT
- Smart stock video search and cropping (16:9 or 9:16)
- Centered subtitle overlays with wrapping support
- Transparent mask background for clear readability

---

## 📸 Output Example

| Feature              | Format   |
|----------------------|----------|
| Resolution           | 1080x1920 (Shorts) or 1920x1080 (YouTube) |
| Audio                | AI-generated from `gTTS` |
| Subtitles            | Auto-generated with Whisper |
| Source videos        | Fetched from [Pexels](https://www.pexels.com/) |



## ⚙️ Setup Instructions

1. **Clone the repo**:
   ```bash
   git clone https://github.com/your-username/ai-video-generator.git
   cd ai-video-generator
   ```
2. **Install Python 3.11.1** and create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file** with your Pexels API key:

   ```env
   PEXELS_API_KEY=your_pexels_api_key_here
   ```

5. **Install ImageMagick** (with legacy utilities enabled):

   * Download: [https://imagemagick.org/script/download.php](https://imagemagick.org/script/download.php)
   * During installation, make sure to check:

     > ✅ “Install legacy utilities (e.g., convert)”

6. **Run the script**:

   ```bash
   python main.py
   ```

---

## 📦 Dependencies

Python version: `3.11.1`

Install with:

```bash
pip install -r requirements.txt
```

<details>
<summary>📜 Click to view <code>requirements.txt</code> contents</summary>

```
certifi==2025.6.15
charset-normalizer==3.4.2
click==8.1.8
colorama==0.4.6
decorator==4.4.2
filelock==3.18.0
fsspec==2025.5.1
gTTS==2.5.4
idna==3.10
imageio==2.37.0
imageio-ffmpeg==0.6.0
Jinja2==3.1.6
llvmlite==0.44.0
MarkupSafe==3.0.2
more-itertools==10.7.0
moviepy==1.0.3
mpmath==1.3.0
networkx==3.5
numba==0.61.2
numpy==2.2.6
openai-whisper @ git+https://github.com/openai/whisper.git@c0d2f624c09dc18e709e37c2ad90c039a4eb72a2
pillow==11.2.1
proglog==0.1.12
python-dotenv==1.1.1
regex==2024.11.6
requests==2.32.4
setuptools==80.9.0
srt==3.5.3
sympy==1.14.0
termcolor==3.1.0
tiktoken==0.9.0
torch==2.7.1
tqdm==4.67.1
typing_extensions==4.14.0
urllib3==2.5.0
wheel==0.45.1
```

</details>

---

## 🧠 Powered By

* [Whisper (OpenAI)](https://github.com/openai/whisper)
* [gTTS (Google Text-to-Speech)](https://pypi.org/project/gTTS/)
* [MoviePy](https://zulko.github.io/moviepy/)
* [Pexels Video API](https://www.pexels.com/api/)

---

## 📄 License

This project is licensed under the Apache License 2.0

---

## 🙋‍♂️ Author

**Udith Sandaruwan**
🌐 [udithsandaruwan.me](https://udithsandaruwan.me)

```

