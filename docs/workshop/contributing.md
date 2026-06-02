# Contributing to the Community Repository

The community repository (`fastsuite-e2-community`) contains reference downloaders and examples that benefit all FASTSUITE E2 users. If you've built something useful — a new vendor downloader, a bug fix, an improvement — you can contribute it back.

## Important: This Is a Separate Workflow

Contributing to the community is **not done from within your starter repository**. The `community/` folder in your repo is read-only. To contribute, you work with a **separate fork** of the community repository.

---

## Prerequisites

- A GitHub account
- Git installed on your machine
- Familiarity with the basics in [Git Essentials](git-essentials.md)

---

## Step-by-Step: Contributing a Change

### 1. Fork the Community Repository

A "fork" is your own copy of the community repo on GitHub.

1. Go to https://github.com/cenit-dfs/fastsuite-e2-community
2. Click the **Fork** button (top right)
3. Select your account as the destination
4. You now have `https://github.com/<your-account>/fastsuite-e2-community`

### 2. Clone Your Fork Locally

Clone your fork to a **separate folder** (not inside your starter repo):

```powershell
cd C:\Projects
git clone https://github.com/<your-account>/fastsuite-e2-community.git
cd fastsuite-e2-community
```

### 3. Create a Branch for Your Change

```powershell
git checkout -b feature/add-staeubli-downloader
```

Use a descriptive branch name that explains what you're contributing.

### 4. Make Your Changes

Edit the files in your fork. Follow these conventions:

- **New downloaders:** Place in `OLPTranslators/<VENDOR>/<VendorName>.py`
- **Bug fixes:** Edit the existing file and describe the fix clearly
- **Examples:** Place in `examples/`
- Follow the coding style of existing files (indentation, naming, structure)

### 5. Test Your Changes

- Test the downloader in FASTSUITE E2 with real workcells
- Verify the output is correct for different motion types, events, and configurations
- Generated output should be deterministic (no timestamps or usernames unless guarded)

### 6. Commit and Push

```powershell
git add .
git commit -m "Add Stäubli VAL3 base downloader

- Supports LIN/PTP/CIRC motion
- Handles speed and tool events
- Outputs .pgx files"

git push -u origin feature/add-staeubli-downloader
```

Write a clear commit message. The first line is a short summary; add details below after a blank line.

### 7. Create a Pull Request

1. Go to your fork on GitHub: `https://github.com/<your-account>/fastsuite-e2-community`
2. GitHub will show a banner: *"Compare & pull request"* — click it
3. Fill in:
   - **Title:** Clear summary (e.g., "Add Stäubli VAL3 base downloader")
   - **Description:** What you added/changed, how to test it, any limitations
4. Click **"Create pull request"**

CENIT will review your contribution and either merge it, request changes, or discuss it with you.

---

## What Makes a Good Contribution?

- **Works out of the box** — Someone should be able to use your downloader with minimal setup
- **Clear code** — Use meaningful variable names, follow existing patterns
- **No customer-specific logic** — Contributions should be general-purpose; keep customer customizations in your own repo
- **Tested** — Verify with at least one E2 workcell before submitting
- **Documented** — Add inline comments for non-obvious logic

---

## Keeping Your Fork Up to Date

Over time, the original community repo gets new commits. To sync your fork:

```powershell
# Add the original repo as "upstream" (one-time setup)
git remote add upstream https://github.com/cenit-dfs/fastsuite-copilot-starter.git
git remote add upstream https://github.com/cenit-dfs/fastsuite-e2-community.git

# Fetch the latest changes
git fetch upstream

# Switch to your master branch
git checkout master

# Merge upstream changes
git merge upstream/master

# Push the updated master to your fork
git push
```

---

## After Your PR Is Merged

Once your contribution is merged into the community repo, you (and everyone else) can pull it into their starter repos:

```powershell
# In your starter repo
cd community
git pull origin master
cd ..
git add community
git commit -m "Update community: includes my Stäubli downloader"
git push
```

Your contribution is now available to everyone who uses the community reference code.
