# Interactive Meeting Playback

A web interface for synchronized video and transcript playback with interactive features.

## Features

- **Auto Mode**:
  - Shows meeting details when paused
  - Displays synchronized transcript during playback
  - Auto-scrolls to current speaker
  - Highlights current segment

- **Fixed Mode** (toggle in transcript header):
  - Always shows full transcript
  - Search functionality
  - Click any segment to jump to that timestamp
  - Orange highlights for search matches

- **General Features**:
  - Responsive layout
  - Pause indicator
  - Smooth transitions
  - Meeting details view

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

## Demonstration

Demonstration video: https://drive.google.com/file/d/1fNEkfHcHxHSL-p903BYlzYxQplfkV87B/view?usp=sharing
