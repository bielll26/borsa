#!/usr/bin/env node
/**
 * 10x Content Expert — Pre-install environment checker
 * Validates Python, Node, pip packages, and creates required directories.
 * Run: node scripts/setup-check.js
 */

import { execSync } from 'child_process';
import { existsSync, mkdirSync, copyFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const ROOT = join(__dirname, '..');

let errors = 0;
let warnings = 0;

function ok(msg) { console.log(`  ✓ ${msg}`); }
function warn(msg) { warnings++; console.log(`  ⚠ ${msg}`); }
function fail(msg) { errors++; console.log(`  ✗ ${msg}`); }

function getVersion(cmd) {
  try {
    return execSync(cmd, { encoding: 'utf8', stdio: ['pipe', 'pipe', 'pipe'] }).trim();
  } catch { return null; }
}

function getOsHint(tool) {
  const p = process.platform;
  const hints = {
    python: {
      win32: 'winget install Python.Python.3.12',
      darwin: 'brew install python@3.12',
      linux: 'sudo apt-get install -y python3 python3-pip python3-venv',
    },
    node: {
      win32: 'winget install OpenJS.NodeJS.LTS',
      darwin: 'brew install node@18',
      linux: 'curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - && sudo apt-get install -y nodejs',
    },
  };
  return (hints[tool] && hints[tool][p]) || `Install ${tool} from its official website`;
}

console.log('\n🔍 10x Content Expert — Environment Check\n');

// --- Python ---
console.log('Python:');
let pyCmd = null;
for (const cmd of ['python3 --version', 'python --version']) {
  const v = getVersion(cmd);
  if (v) {
    const ver = v.replace(/Python\s*/i, '');
    const [major, minor] = ver.split('.').map(Number);
    if (major >= 3 && minor >= 9) {
      ok(`Python ${ver} (>= 3.9)`);
      pyCmd = cmd.split(' ')[0];
      break;
    }
  }
}
if (!pyCmd) {
  fail('Python 3.9+ not found');
  console.log(`    → ${getOsHint('python')}`);
}

// --- pip ---
if (pyCmd) {
  const pipV = getVersion(`${pyCmd} -m pip --version`);
  if (pipV) ok(`pip available`);
  else warn('pip not found — install: python -m ensurepip --upgrade');
}

// --- Node.js ---
console.log('Node.js:');
const nodeV = getVersion('node -v');
if (nodeV) {
  ok(`Node ${nodeV.replace('v', '')} (for tldraw-canvas)`);
} else {
  warn('Node.js not found (needed for tldraw-canvas)');
  console.log(`    → ${getOsHint('node')}`);
}

// --- Virtual Environment ---
console.log('Python venv:');
const venvPath = join(ROOT, '.venv');
if (existsSync(venvPath)) {
  ok('.venv exists');
} else {
  warn('.venv not found — run: python setup.py');
}

// --- Core Python packages ---
if (pyCmd) {
  console.log('Python packages:');
  const required = [
    ['dotenv', 'python-dotenv'],
    ['pptx', 'python-pptx'],
    ['docx', 'python-docx'],
    ['openpyxl', 'openpyxl'],
    ['PyPDF2', 'PyPDF2'],
    ['pdfplumber', 'pdfplumber'],
    ['PIL', 'Pillow'],
    ['rich', 'rich'],
    ['requests', 'requests'],
  ];
  for (const [mod, pkg] of required) {
    const check = getVersion(`${pyCmd} -c "import ${mod}; print('ok')" 2>&1`);
    if (check && check.includes('ok')) {
      ok(pkg);
    } else {
      warn(`${pkg} not installed — pip install ${pkg}`);
    }
  }
}

// --- Directories ---
console.log('Directories:');
const dirs = [
  'input/presentations', 'input/documents', 'input/pdfs', 'input/spreadsheets',
  'output/content/emails', 'output/content/social', 'output/content/presentations',
  'output/content/blogs', 'output/content/sequences', 'output/content/hooks',
  'output/content/campaigns', 'output/analysis', 'output/plans', 'output/working',
  'output/pdf', 'output/pptx', 'output/docx', 'output/xlsx',
  'output/mega-downloads', 'output/transcripts', 'output/canvas', 'output/logs',
  'references/transcripts', 'references/examples', 'references/brand-voice', 'references/templates',
  'samples/images', 'samples/presentations', 'samples/videos', 'samples/brand-kits',
];
let created = 0;
for (const d of dirs) {
  const full = join(ROOT, d);
  if (!existsSync(full)) { mkdirSync(full, { recursive: true }); created++; }
}
if (created > 0) ok(`Created ${created} missing directories`);
else ok('All directories exist');

// --- .env ---
console.log('Environment:');
const envFile = join(ROOT, '.env');
const envExample = join(ROOT, '.env.example');
if (!existsSync(envFile) && existsSync(envExample)) {
  copyFileSync(envExample, envFile);
  ok('Created .env from .env.example');
} else if (existsSync(envFile)) {
  ok('.env exists');
} else {
  warn('No .env or .env.example found');
}

// --- Canvas ---
console.log('Canvas:');
const canvasPkg = join(ROOT, 'tldraw-canvas', 'package.json');
const canvasModules = join(ROOT, 'tldraw-canvas', 'node_modules');
if (existsSync(canvasPkg)) {
  ok('tldraw-canvas/package.json found');
  if (!existsSync(canvasModules)) {
    warn('tldraw-canvas/node_modules missing — run: cd tldraw-canvas && npm install');
  } else {
    ok('tldraw-canvas dependencies installed');
  }
} else {
  fail('tldraw-canvas/package.json not found');
}

// --- Optional Tools ---
console.log('Optional tools:');

// Docker
const dockerV = getVersion('docker --version 2>&1');
if (dockerV && dockerV.includes('Docker')) {
  ok(`Docker (${dockerV.replace('Docker version ', '').split(',')[0]})`);
  // Check if running
  const dockerInfo = getVersion('docker info 2>&1');
  if (dockerInfo && !dockerInfo.includes('error')) {
    ok('Docker daemon running — can use Docker Whisper');
  } else {
    console.log('    ℹ Docker installed but not running — start Docker Desktop to use Docker Whisper');
  }
} else {
  console.log('  – Docker not found (optional — for container-based Whisper)');
}

// FFmpeg
const ffmpegV = getVersion('ffmpeg -version 2>&1');
if (ffmpegV && ffmpegV.includes('ffmpeg version')) {
  ok(`FFmpeg (${ffmpegV.split('\n')[0].replace('ffmpeg version ', '').split(' ')[0]})`);
} else {
  console.log('  – FFmpeg not found (optional — needed for local Whisper transcription)');
  const p = process.platform;
  if (p === 'win32') console.log('    → winget install Gyan.FFmpeg');
  else if (p === 'darwin') console.log('    → brew install ffmpeg');
  else console.log('    → sudo apt-get install -y ffmpeg');
}

// Whisper (local)
if (pyCmd) {
  const whisperCheck = getVersion(`${pyCmd} -c "import whisper; print(whisper.__version__)" 2>&1`);
  if (whisperCheck && !whisperCheck.includes('Error') && !whisperCheck.includes('No module')) {
    ok(`Whisper ${whisperCheck} (local transcription ready)`);
  } else {
    console.log('  – Whisper not installed (optional — pip install openai-whisper torch)');
  }
}

// OpenAI API key
import { readFileSync } from 'fs';
try {
  const envContent = readFileSync(join(ROOT, '.env'), 'utf8');
  if (envContent.includes('OPENAI_API_KEY=sk-')) {
    ok('OpenAI API key configured (cloud transcription ready)');
  } else {
    console.log('  – OpenAI API key not set (optional — for cloud transcription)');
  }
  if (envContent.includes('CANVA_CLIENT_ID=') && !envContent.includes('your_client_id_here')) {
    ok('Canva API configured');
  } else {
    console.log('  – Canva API not configured (optional — for design automation)');
  }
} catch {
  console.log('  – .env not found — optional features not configured');
}

// MEGA CMD
const megaV = getVersion('mega-version 2>&1') || getVersion('mega-cmd-server --version 2>&1');
if (megaV && !megaV.includes('not found') && !megaV.includes('not recognized')) {
  ok(`MEGA CMD available`);
} else {
  console.log('  – MEGA CMD not found (optional — https://mega.io/cmd)');
}

// --- Summary ---
console.log('\n' + '─'.repeat(50));
if (errors > 0) {
  console.log(`\n❌ ${errors} critical issue(s). Fix before continuing.\n`);
  process.exit(1);
} else if (warnings > 0) {
  console.log(`\n⚠ ${warnings} warning(s). Core setup can proceed.\n`);
  console.log('Next steps:');
  console.log('  1. python setup.py          # Install Python deps in .venv');
  console.log('  2. cd tldraw-canvas && npm install  # Install canvas deps');
  console.log('  3. /setup in Claude Code    # Full guided setup\n');
} else {
  console.log('\n✅ Environment ready.\n');
}
