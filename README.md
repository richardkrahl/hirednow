# HiredNow

> Apply to jobs automatically. **$79 once, not $600/year.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Local AI](https://img.shields.io/badge/AI-Ollama-green.svg)](https://ollama.com)

**HiredNow** is a local-first job application automation tool. Find jobs on LinkedIn & Indeed, optimize your resume with AI, and track applications — all on your own machine. No cloud. No subscriptions. No data mining.

![Dashboard](https://hirednow.app/screenshot.png)

---

## 🚀 Quick Start

```bash
# Install with one command
curl -fsSL https://hirednow.app/install.sh | bash

# Or clone manually
git clone https://github.com/richardkrahl/hirednow.git
cd hirednow
pip install -r requirements.txt

# Start the dashboard
python dashboard.py
# Open http://localhost:5000
```

---

## ✨ Features

- **🔍 Auto Job Search** - Scrapes LinkedIn & Indeed automatically
- **✨ AI Resume Optimization** - Tailors resume per job using local Ollama (no API costs)
- **🤖 One-Click Apply** - Browser extension auto-fills applications
- **📊 Application Tracker** - Visual dashboard shows your pipeline
- **📝 Cover Letter Generator** - AI writes personalized cover letters
- **🔒 100% Local** - Your resume never leaves your machine

---

## 🎯 Why HiredNow?

|  | Competitors | HiredNow |
|---|---|---|
| **Price** | $588/year | **$79 once** |
| **Privacy** | Cloud-based | **100% local** |
| **AI** | OpenAI API ($$$) | **Local Ollama (free)** |
| **Data** | Their servers | **Your machine** |
| **Lock-in** | Subscription | **Own it forever** |

---

## 📦 Installation

### Requirements
- Python 3.11+
- macOS or Linux
- Chrome browser
- [Ollama](https://ollama.com) (free, for AI features)

### One-Line Install
```bash
curl -fsSL https://hirednow.app/install.sh | bash
```

### Manual Install
```bash
# Clone repo
git clone https://github.com/richardkrahl/hirednow.git
cd hirednow

# Install dependencies
pip install -r requirements.txt

# Install Ollama (for AI)
curl -fsSL https://ollama.com/install.sh | sh
ollama pull hoangquan456/qwen3-nothink:8b

# Start dashboard
python dashboard.py
```

---

## 🖥️ Usage

### Web Dashboard
```bash
python dashboard.py
# Open http://localhost:5000 in browser
```

### Command Line
```bash
# Search for jobs
python scraper/job_scraper.py "Hospitality Manager" "Nashville, TN"

# Optimize resume for a job
python optimizer/smart_optimizer.py "Manager" "Company" job_description.txt

# Track applications
python tracker/application_tracker.py dashboard
```

### Chrome Extension
1. Go to `chrome://extensions`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select the `extension/` folder
5. 🤖 HiredNow button appears on job sites

---

## 🛠️ Tech Stack

- **Python 3.11+** - Core automation
- **Flask + Bootstrap** - Web dashboard
- **Playwright** - Browser automation
- **Ollama** - Local AI (LLaMA/Qwen)
- **SQLite** - Local database
- **Chrome Extension** - Form auto-fill

---

## 💰 Pricing

**$79 one-time purchase**

- Lifetime access
- All features included
- Free updates
- No subscriptions
- No hidden fees

[Buy Now](https://buy.stripe.com/...) • [View on GitHub](https://github.com/richardkrahl/hirednow)

---

## 🔒 Privacy

- ✅ All data stays on your machine
- ✅ No cloud storage
- ✅ No data mining
- ✅ No "we updated our privacy policy"
- ✅ Open source (MIT license)

---

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 License

MIT License - see [LICENSE](LICENSE)

**Built with ❤️ in Nashville, TN**