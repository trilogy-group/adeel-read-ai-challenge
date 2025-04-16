# Interactive Meeting Playback

A simple web interface for synchronized video and transcript playback.

## Setup

1. Place your meeting recording as `meeting.mp4` in this directory
2. Start a local server:
   ```bash
   python -m http.server 8000
   ```
3. Open http://localhost:8000 in your browser

## File Requirements

- `meeting.mp4`: The meeting recording (not included in repo due to size)
  - Download from: [Video demonstration](https://drive.google.com/file/d/1a9P_2lFY4RdZATZoDpjMQAqK_KLrRRpH/view?usp=sharing)
  - Save as `meeting.mp4` in this directory
- `event.json`: Meeting data including transcript and metadata for the above video
- `index.html`: The web interface
