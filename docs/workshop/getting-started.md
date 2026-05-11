# Getting Started — From Zero to Working

This guide walks you through setting up everything you need to customize FASTSUITE E2 with AI-assisted development. No prior Git or VS Code experience required.

## What You Will Set Up

1. A **GitHub account** (free)
2. **Git** on your machine
3. **VS Code** with Copilot
4. Your own **customization repository** (based on this template)
5. A local **working copy** connected to FASTSUITE E2

## Prerequisites

- **FASTSUITE E2 R2026.1** (or later) installed on your machine
- **Windows 10/11**
- **Internet access** (for GitHub and Copilot)
- A **GitHub Copilot license** (ask your company admin or sign up at https://github.com/features/copilot)

---

## Step 1 — Create a GitHub Account

If you already have a GitHub account, skip to Step 2.

1. Go to https://github.com/signup
2. Follow the registration process
3. Verify your email address

> **Company accounts:** If your company uses GitHub Enterprise, ask your admin whether to use your enterprise account or a personal one for this work.

---

## Step 2 — Install Git

Git is the version control system that tracks your changes.

1. Download Git from https://git-scm.com/download/win
2. Run the installer — **accept all defaults** (they are fine for our use case)
3. Verify the installation:
   - Open **PowerShell** (search for it in the Start menu)
   - Type: `git --version`
   - You should see something like: `git version 2.45.0.windows.1`

### Configure Your Identity

Git needs to know who you are (for commit messages). Run these two commands in PowerShell, replacing with your name and email:

```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@company.com"
```

---

## Step 3 — Install VS Code

1. Download VS Code from https://code.visualstudio.com/
2. Run the installer
3. During installation, check:
   - ☑ Add "Open with Code" action to Windows Explorer context menu
   - ☑ Add to PATH

---

## Step 4 — Install VS Code Extensions

Open VS Code and install these extensions:

1. **Python** (by Microsoft) — `ms-python.python`
2. **GitHub Copilot** (by GitHub) — `GitHub.copilot`
3. **GitHub Copilot Chat** (by GitHub) — `GitHub.copilot-chat`

To install an extension:
1. Click the Extensions icon in the left sidebar (or press `Ctrl+Shift+X`)
2. Search for the extension name
3. Click **Install**

After installing Copilot, you'll be prompted to sign in with your GitHub account. Follow the prompts.

---

## Step 5 — Create Your Repository from the Template

This is where you get your own copy of the starter project.

1. Go to https://github.com/cenit-dfs/fastsuite-copilot-starter
2. Click the green **"Use this template"** button
3. Click **"Create a new repository"**
4. Fill in:
   - **Owner:** Your GitHub account (or your company's organization)
   - **Repository name:** Something descriptive, e.g. `e2-customizations` or `mycompany-e2-plugins`
   - **Visibility:** Private (recommended for company work) or Public
5. Click **"Create repository"**

You now have your own repository at `https://github.com/<your-account>/<your-repo-name>`.

---

## Step 6 — Clone Your Repository Locally

"Cloning" downloads your repository to your machine so you can work on it.

1. Open **PowerShell**
2. Navigate to where you want your project folder:
   ```powershell
   cd C:\Projects
   ```
3. Clone your repository (replace the URL with yours):
   ```powershell
   git clone https://github.com/<your-account>/<your-repo-name>.git
   ```
4. Enter the project folder:
   ```powershell
   cd <your-repo-name>
   ```
5. Initialize the community reference code:
   ```powershell
   git submodule update --init
   ```
   This downloads the reference downloaders into the `community/` folder.

---

## Step 7 — Configure for Your E2 Installation

1. Open the project in VS Code:
   ```powershell
   code .
   ```
   VS Code will ask to install recommended extensions — click **Yes**.

2. Open `.vscode/settings.json` (click it in the Explorer sidebar)

3. Find the line with `python.defaultInterpreterPath` and update it to match your E2 installation:
   ```json
   "python.defaultInterpreterPath": "c:\\Programs\\FASTSUITE_Edition_2_R2026.1\\python.exe"
   ```
   
4. Update all lines marked with `// TODO:` comments to match your E2 installation path.

5. Save the file (`Ctrl+S`).

---

## Step 8 — Verify Everything Works

1. In VS Code, open the Copilot Chat panel (`Ctrl+Shift+I` or click the chat icon)
2. Type: *"What agent modes are available?"*
3. Copilot should mention **E2Downloader**, **E2Technology**, and **E2Uploader**
4. Type: *"Show me the KUKA base downloader structure"*
5. Copilot should reference `community/OLPTranslators/KUKA/KUKA_KRC5.py`

If Copilot responds with relevant E2 context, you're set up correctly.

---

## What's Next?

- Read [Daily Workflow](daily-workflow.md) to learn how to create and manage your customizations
- Read [Git Essentials](git-essentials.md) if you're new to version control

---

## Troubleshooting

### "git is not recognized"
Git wasn't added to your PATH. Restart PowerShell, or reinstall Git and check "Add to PATH" during setup.

### Copilot doesn't respond with E2 context
Make sure `community/` folder is populated (run `git submodule update --init`). Check that `.github/copilot-instructions.md` exists in your project.

### Python errors in VS Code
The Python path in `.vscode/settings.json` must point to your actual E2 installation. Check that the folder and `python.exe` exist at the specified path.

### "Permission denied" when cloning
If your repository is private, Git will ask for your GitHub credentials. Enter your GitHub username and a **Personal Access Token** (not your password). Create a token at https://github.com/settings/tokens.
