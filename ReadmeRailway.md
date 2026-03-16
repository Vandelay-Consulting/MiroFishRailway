# MiroFish on Railway

> **Deploy MiroFish to Railway in minutes with one click!**

## 🚀 Quick Deploy

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new?template=https://github.com/Vandelay-Consulting/MiroFishRailway)

Click the button above to deploy MiroFish to Railway. Railway will prompt you for required API keys.

---

## 📋 Prerequisites

Before deploying, you'll need two free API keys:

### 1. LLM API Key (Choose One)

**Option A: Aliyun Qwen (Recommended)**
- Go to: https://bailian.console.aliyun.com/
- Sign up or log in
- Create API key in dashboard
- Copy the key value

**Option B: OpenAI**
- Go to: https://platform.openai.com/api-keys
- Create API key
- Copy the key value

**Option C: Any OpenAI-Compatible API**
- Use your provider's API key
- Update `LLM_BASE_URL` and `LLM_MODEL_NAME` accordingly

### 2. Zep Cloud API Key

- Go to: https://app.getzep.com/
- Sign up (free tier available)
- Create a new project
- Copy your API key

---

## 🎯 Deployment Options

### Option 1: One-Click Deploy (Easiest)

Click the deploy button above. Railway will:
1. Show you the configuration
2. Prompt for `LLM_API_KEY` and `ZEP_API_KEY`
3. Pre-fill `LLM_BASE_URL` and `LLM_MODEL_NAME`
4. Deploy automatically

**Time**: ~10 minutes, zero manual config needed

### Option 2: Manual Deploy on Railway

1. Create a [Railway](https://railway.com) account
2. Create a new project
3. Add service from GitHub: `Vandelay-Consulting/MiroFishRailway`
4. Add environment variables (see below)
5. Click Deploy

### Option 3: Local Development

```bash
# Clone this repo
git clone https://github.com/Vandelay-Consulting/MiroFishRailway.git
cd MiroFishRailway

# Copy environment template
cp .env.example .env

# Edit .env with your API keys
nano .env

# Install dependencies
npm run setup:all

# Start development server
npm run dev
