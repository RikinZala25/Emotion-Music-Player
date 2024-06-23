# Python Gunicorn Flask Backend

# Initial Setup

## Environment Variables

Create a .env file and structure it like this.

```python
export ASSEMBLYAI_API_KEY=your_key
export MUSICMATCH_API_KEY=your_key
export REPLICATE_API_TOKEN=your_key
export SPOTIFY_CLIENT_ID=your_key
export SPOTIFY_CLIENT_SECRET=your_key
```

- Replace `your_key` to respective keys
- Assembly Key [assemblyai.com](https://www.assemblyai.com/dashboard/signup)
- MusicMatch API Key [developer.musixmatch.com](https://developer.musixmatch.com/login)
- Replicate API Key [replicate.com](https://replicate.com/signin?next=/)
- Spotify API Key [developer.spotify.com](https://developer.spotify.com/dashboard)

## How to run?

- Create a virtual environment, refer the docs [python.org/venv](https://docs.python.org/3/library/venv.html)
- Activate the venv
- run `pip install -r requirements.txt`
- run `Flask run` or `python app.py`
- If any error regarding modules - try to upgrade the packages installed to the latest version

You will get the Backend-URL, use this in Front-End, read the Readme.md.
