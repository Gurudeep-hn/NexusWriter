# Deploying NexusWriter to Hugging Face Spaces 🚀

Hugging Face Spaces is the best free way to host Streamlit/Python AI demos.

## 1. Prepare Your Repo
1.  Initialize a Git repository (if you haven't already):
    ```bash
    git init
    git add .
    git commit -m "Initial commit for NexusWriter"
    ```

## 2. Create a Space
1.  Go to [Hugging Face Spaces](https://huggingface.co/spaces).
2.  Click **Create new Space**.
3.  **Space Name**: `nexus-writer-demo` (or similar).
4.  **License**: `MIT`.
5.  **SDK**: Select **Docker** (Blank).
6.  Click **Create Space**.

## 3. Upload Code
You can push directly from your terminal if you have `git` configured, or upload files via the website.

**Option A: Git Push (Recommended)**
```bash
# Replace 'username' with your HF username
git remote add space https://huggingface.co/spaces/username/nexus-writer-demo
git push space master:main
```

## 4. Set Environment Variables (Secrets)
**CRITICAL:** Your API keys are NOT in the code (they are in `.env`, which is ignored). You must add them to Hugging Face.

1.  Go to your Space's **Settings** tab.
2.  Scroll to **Variables and secrets**.
3.  Click **New Secret** for each key:
    *   Name: `GROQ_API_KEY`, Value: `gsk_...`
    *   Name: `TAVILY_API_KEY`, Value: `tvly-...`
    *   Name: `GOOGLE_API_KEY`, Value: `AIza...`

## 5. Build & Launch
*   Hugging Face will detect the `Dockerfile` and start building automatically.
*   The build logs will appear in the **Container** tab.
*   Once finished (approx. 2-3 mins), your App will be live! 🟢

## 6. Add to Resume
*   **Link**: `https://huggingface.co/spaces/YOUR_USERNAME/nexus-writer-demo`
*   **Title**: "NexusWriter: Autonomous AI Blogging Agent (FastAPI/LangGraph)"
