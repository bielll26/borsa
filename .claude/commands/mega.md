---
name: mega
description: |
  MEGA cloud file management. Browse, download, search, and transcribe files from MEGA storage.
  Requires MEGA CMD installed and logged in.
---

# /mega Command

Manage MEGA cloud storage files.

## Usage

```
/mega [action] [options]
```

## Available Actions

| Command | Description | Routes To |
|---------|-------------|-----------|
| `/mega browse` | List files in MEGA | mega-manager |
| `/mega download` | Download files from MEGA | mega-manager |
| `/mega find` | Search for files in MEGA | mega-manager |
| `/mega info` | Show account/storage info | mega-manager |
| `/mega transcribe` | Download + transcribe media | mega-manager → mega-transcriber |
| `/mega pipeline` | Download → Transcribe → Analyze → Canvas | mega-manager → mega-transcriber → content-analyzer → tldraw-canvas |

## Examples

### Browse root folder
```
/mega browse
> "Show me what's in my MEGA root"
```

### Download a file
```
/mega download
> "Download /Videos/webinar-2024.mp4"
```

### Find videos
```
/mega find
> "Find all .mp4 files in /Recordings"
```

### Full pipeline
```
/mega pipeline
> "Download my latest webinar, transcribe it, analyze for content, and create a visual plan"
```

---

## Setup Guide (Windows)

### Step 1: Install MEGA CMD

**Option A: Using winget (Recommended if available)**
```bash
winget install Mega.MEGAcmd
```

**Option B: Manual Download**
1. Download from: https://mega.io/cmd
2. Run the installer: `MEGAcmdSetup64.exe`
3. Follow installation prompts
4. Restart your terminal after installation

### Step 2: Verify Installation

MEGA CMD installs to: `C:\Users\[USERNAME]\AppData\Local\MEGAcmd\`

Check installation:
```bash
# If MEGA CMD is in PATH:
mega-version

# If not in PATH, use full path:
"C:\Users\[USERNAME]\AppData\Local\MEGAcmd\mega-version.bat"
```

### Step 3: Login to MEGA Account

```bash
# Interactive login (password hidden):
mega-login your-email@example.com

# Or with password (for scripts):
mega-login your-email@example.com "YourPassword"
```

**First login takes time** - MEGA syncs your account data (can be 100MB+ for large accounts). Wait for it to complete.

### Step 4: Verify Login

```bash
mega-whoami
```

Should display your account email and storage info.

---

## MEGA CMD Commands Reference

### Account & Session
| Command | Description |
|---------|-------------|
| `mega-whoami` | Show current logged-in account |
| `mega-logout` | Logout from current session |
| `mega-df` | Show disk usage/storage quota |
| `mega-version` | Show MEGA CMD version |

### Navigation & Listing
| Command | Description |
|---------|-------------|
| `mega-ls /path` | List folder contents |
| `mega-ls -l /path` | Detailed listing with sizes |
| `mega-pwd` | Show current MEGA directory |
| `mega-cd /path` | Change directory |
| `mega-tree /path` | Show folder tree structure |

### Search
| Command | Description |
|---------|-------------|
| `mega-find / --pattern "*.mp4"` | Find files by pattern |
| `mega-find /path --pattern "keyword"` | Search in specific path |

### Download & Upload
| Command | Description |
|---------|-------------|
| `mega-get /remote/file local/` | Download file |
| `mega-get /remote/folder/ local/` | Download folder |
| `mega-put local/file /remote/` | Upload file |

### Shared Links
| Command | Description |
|---------|-------------|
| `mega-import "mega-link" /destination` | Import shared folder/file |
| `mega-export /path` | Create share link |

---

## Claude Integration

### Running MEGA Commands from Claude

Since MEGA CMD may not be in system PATH, use full paths:

```bash
# Windows PowerShell method (recommended):
powershell -Command "& 'C:\Users\[USERNAME]\AppData\Local\MEGAcmd\MEGAclient.exe' ls -l /"

# Windows batch method:
"C:\Users\[USERNAME]\AppData\Local\MEGAcmd\mega-ls.bat" /
```

### Output Paths

All MEGA downloads go to: `output/mega-downloads/`

---

## Troubleshooting

### "Command not found"
MEGA CMD not in PATH. Use full path:
```bash
"C:\Users\[USERNAME]\AppData\Local\MEGAcmd\mega-version.bat"
```

### "Not logged in"
Run login command and wait for sync:
```bash
"C:\Users\[USERNAME]\AppData\Local\MEGAcmd\mega-login.bat" email@example.com
```

### Login takes forever
First login syncs account metadata. For large accounts (100GB+), this can take several minutes. Be patient.

### "Invalid destiny" error
Path resolution issue with Git Bash. Use PowerShell or CMD instead:
```bash
powershell -Command "& 'C:\Users\[USERNAME]\AppData\Local\MEGAcmd\MEGAclient.exe' ls /"
```

### Server not running
MEGA CMD server starts automatically. If issues:
```bash
# Start server manually:
"C:\Users\[USERNAME]\AppData\Local\MEGAcmd\MEGAcmdServer.exe"
```

---

## Prerequisites Summary

1. **MEGA CMD**: Download from https://mega.io/cmd
2. **Login**: Run `mega-login your@email.com` in terminal
3. **Wait for sync**: First login syncs account data
4. **For transcription**: `pip install openai-whisper torch`
