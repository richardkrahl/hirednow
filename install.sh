#!/bin/bash
#
# HiredNow One-Click Installer
# Usage: curl -fsSL https://hirednow.app/install.sh | bash
#

set -e

echo "🚀 HiredNow Installer"
echo "===================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
    echo "✅ macOS detected"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    echo "✅ Linux detected"
else
    echo "${RED}❌ Unsupported OS: $OSTYPE${NC}"
    echo "HiredNow supports macOS and Linux only."
    exit 1
fi

# Check for required tools
echo ""
echo "📋 Checking requirements..."

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ Python found: $PYTHON_VERSION"
else
    echo "${RED}❌ Python 3 not found${NC}"
    echo "Please install Python 3.11+ from https://python.org"
    exit 1
fi

# Check pip
if command -v pip3 &> /dev/null; then
    echo "✅ pip3 found"
else
    echo "${YELLOW}⚠️  pip3 not found, attempting to install...${NC}"
    python3 -m ensurepip --upgrade || true
fi

# Check Chrome
if [[ "$OS" == "macos" ]]; then
    if [ -d "/Applications/Google Chrome.app" ]; then
        echo "✅ Google Chrome found"
    else
        echo "${YELLOW}⚠️  Google Chrome not found${NC}"
        echo "Please install Chrome from https://google.com/chrome"
    fi
else
    if command -v google-chrome &> /dev/null || command -v chromium &> /dev/null; then
        echo "✅ Chrome/Chromium found"
    else
        echo "${YELLOW}⚠️  Chrome not found${NC}"
        echo "Please install Chrome from https://google.com/chrome"
    fi
fi

# Download HiredNow
echo ""
echo "📥 Downloading HiredNow..."
INSTALL_DIR="$HOME/.hirednow"

if [ -d "$INSTALL_DIR" ]; then
    echo "📝 Updating existing installation..."
    cd "$INSTALL_DIR"
    git pull origin main 2>/dev/null || echo "⚠️  Could not update via git"
else
    echo "📝 Cloning repository..."
    git clone https://github.com/richardkrahl/hirednow.git "$INSTALL_DIR" 2>/dev/null || {
        echo "⚠️  Git clone failed, downloading manually..."
        mkdir -p "$INSTALL_DIR"
        cd "$INSTALL_DIR"
        curl -fsSL https://github.com/richardkrahl/hirednow/archive/main.tar.gz | tar -xz --strip-components=1
    }
fi

cd "$INSTALL_DIR"

# Install Python dependencies
echo ""
echo "📦 Installing dependencies..."
pip3 install -q -r requirements.txt || {
    echo "${YELLOW}⚠️  Some packages failed to install. This is usually OK.${NC}"
}

# Install Playwright browsers
echo ""
echo "🎭 Installing Playwright browsers..."
python3 -m playwright install firefox || echo "⚠️  Playwright install may need manual completion"

# Check for Ollama
echo ""
echo "🤖 Checking Ollama..."
if command -v ollama &> /dev/null; then
    echo "✅ Ollama found"
    echo "📝 Pulling AI model (this may take a few minutes)..."
    ollama pull hoangquan456/qwen3-nothink:8b || echo "⚠️  Model download may need to be completed manually"
else
    echo "${YELLOW}⚠️  Ollama not found${NC}"
    echo ""
    echo "Ollama is required for AI resume optimization."
    echo "Install it with:"
    echo "  curl -fsSL https://ollama.com/install.sh | bash"
    echo ""
    echo "Or visit: https://ollama.com/download"
fi

# Create command shortcut
echo ""
echo "🔗 Creating command shortcuts..."
mkdir -p "$HOME/.local/bin"

cat > "$HOME/.local/bin/hirednow" << 'EOF'
#!/bin/bash
# HiredNow launcher

cd "$HOME/.hirednow"

if [ $# -eq 0 ]; then
    echo "HiredNow - Job Application Automation"
    echo ""
    echo "Commands:"
    echo "  hirednow scrape 'Job Title' 'Location'  - Find jobs"
    echo "  hirednow optimize 'Job' 'Company' file  - Optimize resume"
    echo "  hirednow tracker                          - Open tracker"
    echo "  hirednow profile                          - Edit profile"
    echo ""
    echo "Or run directly from $HOME/.hirednow"
    exit 0
fi

python3 "job_hunter.py" "$@"
EOF

chmod +x "$HOME/.local/bin/hirednow"

# Add to PATH if needed
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo ""
    echo "📝 Adding to PATH..."
    if [[ "$SHELL" == *"zsh"* ]]; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc"
        echo "✅ Added to ~/.zshrc"
    else
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
        echo "✅ Added to ~/.bashrc"
    fi
fi

# Create desktop shortcut (macOS)
if [[ "$OS" == "macos" ]]; then
    echo ""
    echo "🍎 Creating macOS shortcut..."
    
    cat > "$HOME/Desktop/HiredNow.command" << 'EOF'
#!/bin/bash
cd "$HOME/.hirednow"
open -a Terminal . || python3 job_hunter.py
EOF
    
    chmod +x "$HOME/Desktop/HiredNow.command"
    echo "✅ Created Desktop shortcut"
fi

# Setup wizard
echo ""
echo "⚙️  Initial Setup..."
echo ""

if [ ! -f "$HOME/.hirednow/data/profile.json" ]; then
    echo "📝 Let's set up your profile (1 minute)..."
    echo ""
    
    read -p "First Name: " firstname
    read -p "Last Name: " lastname
    read -p "Email: " email
    read -p "Phone: " phone
    read -p "City: " city
    read -p "State: " state
    
    cat > "$HOME/.hirednow/data/profile.json" << EOF
{
  "personal": {
    "firstName": "$firstname",
    "lastName": "$lastname",
    "email": "$email",
    "phone": "$phone",
    "city": "$city",
    "state": "$state",
    "linkedin": "",
    "github": ""
  },
  "experience": [],
  "education": [],
  "skills": []
}
EOF
    
    echo "✅ Profile created!"
else
    echo "✅ Profile already exists"
fi

# Final instructions
echo ""
echo "${GREEN}✅ HiredNow installed successfully!${NC}"
echo ""
echo "📍 Installation: $HOME/.hirednow"
echo ""
echo "🚀 Quick Start:"
echo ""
echo "1. Find jobs:"
echo "   cd ~/.hirednow"
echo "   python3 scraper/job_scraper.py 'Hospitality Manager' 'Nashville, TN'"
echo ""
echo "2. Optimize resume:"
echo "   python3 optimizer/smart_optimizer.py 'Manager' 'Company' job_description.txt"
echo ""
echo "3. Track applications:"
echo "   python3 tracker/application_tracker.py dashboard"
echo ""
echo "📖 Full docs: https://hirednow.app/docs"
echo "🐛 Issues: https://github.com/richardkrahl/hirednow/issues"
echo ""
echo "Happy job hunting! 🎯"
