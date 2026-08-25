---
name: setup
description: Run initial setup — install dependencies, configure optional features, verify environment
allowed-tools: ["Bash", "Read", "Write", "Edit"]
---

# 10x Content Expert — Setup

Run the complete environment setup for this skill.

## User Request

$ARGUMENTS

## Instructions

Follow these steps in order. Skip steps the user has already completed.

### Step 1: Run environment check

```bash
node scripts/setup-check.js
```

If Node.js is not installed, guide the user with OS-specific commands:
- **Windows**: `winget install OpenJS.NodeJS.LTS`
- **macOS**: `brew install node@18`
- **Linux**: `curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - && sudo apt-get install -y nodejs`

### Step 2: Run Python setup wizard

```bash
python setup.py
```

This creates the `.venv` virtual environment and installs all core dependencies.
If setup.py prompts for optional features, let the user decide.

### Step 3: Install TLDraw canvas (if Node.js is available)

```bash
cd tldraw-canvas && npm install
```

### Step 4: Check optional features

Detect what's already installed on the user's system:

| Feature | Check Command | Purpose |
|---------|--------------|---------|
| Docker | `docker info` | Container-based Whisper transcription |
| FFmpeg | `ffmpeg -version` | Audio/video processing |
| Whisper | `python -c "import whisper"` | Local transcription |
| OpenAI API | Check `.env` for `OPENAI_API_KEY` | Cloud transcription |
| Canva API | Check `.env` for `CANVA_CLIENT_ID` | Design automation |
| MEGA CMD | `mega-version` or `mega-cmd-server --version` | Cloud file access |

### Step 5: Configure optional transcription

If the user wants transcription, offer three options:

**Option A — OpenAI API (easiest, cloud-based):**
- Set `OPENAI_API_KEY=sk-...` in `.env`
- No local install needed
- Uses OpenAI Whisper API

**Option B — Local Whisper (offline, private):**
- Requires FFmpeg installed on PATH
- Install: `.venv/Scripts/pip install openai-whisper torch` (Windows) or `.venv/bin/pip install openai-whisper torch` (Mac/Linux)
- Models: tiny (~1GB RAM), base (~1GB), small (~2GB), medium (~5GB), large (~10GB)
- Set `WHISPER_MODEL=base` in `.env`

**Option C — Docker Whisper (no Python deps):**
- Requires Docker Desktop running
- Set `USE_DOCKER_WHISPER=true` in `.env`
- Claude will handle docker run commands automatically

### Step 6: Configure Canva API (if user wants design features)

1. Go to https://www.canva.com/developers/
2. Create an app
3. Set redirect URI to `http://127.0.0.1:3001/oauth/redirect`
4. Copy Client ID and Secret to `.env`
5. Run OAuth flow: `python scripts/oauth_flow.py`

### Step 7: Verify everything

Run the setup check again to confirm:
```bash
node scripts/setup-check.js
```

### Step 8: Summary

After setup, tell the user what's available:

```
✅ Core Setup
  - Python venv with all editing packages
  - PDF, PPTX, DOCX, XLSX editing ready
  - Content creation (emails, social, blogs, presentations)
  - Brand voice analysis

📦 Optional Features
  - [✓/✗] Transcription: [method]
  - [✓/✗] TLDraw Canvas: http://localhost:5173
  - [✓/✗] Canva API: Design automation
  - [✓/✗] MEGA CMD: Cloud file access

🚀 Quick Start Commands
  /content    — Create any type of content
  /canva      — Canva design operations
  /mega       — MEGA cloud storage
```
