# Git Essentials — Only What You Need for E2 Work

This is not a Git tutorial. This is a practical cheat sheet for the Git operations you'll actually use when working with E2 customizations.

## Concept: What Git Does for You

Git tracks every change you make to your files. You can:
- **Go back** to any previous version if something breaks
- **Share** your work with colleagues via GitHub
- **Work on multiple things** at once using branches
- **Get updates** from the community reference code

---

## The Three Steps: Edit → Commit → Push

Everything you do follows this pattern:

1. **Edit** files in VS Code (Git tracks all changes automatically)
2. **Commit** — save a snapshot with a message ("Add KUKA speed handling")
3. **Push** — upload your commits to GitHub

### Using VS Code (recommended for beginners)

1. Make your changes to files
2. Open **Source Control** panel (`Ctrl+Shift+G`)
3. Review changed files in the list
4. Click **+** next to each file to **stage** it (or **+** at the top to stage all)
5. Type a commit message
6. Click **✓ Commit**
7. Click **Sync Changes** (this pushes to GitHub)

### Using the Terminal

```powershell
# See what changed
git status

# Stage all changes
git add .

# Commit with a message
git commit -m "Add FANUC R-30iB base downloader"

# Push to GitHub
git push
```

---

## Branches — Working on Multiple Things

Branches let you work on different tasks without them interfering with each other.

```
main ─────────────────────── your stable code
  \
   └─ customer-a/project ── work for Customer A
  \
   └─ feature/new-motion ── experimental changes
```

### Common Branch Operations

```powershell
# See which branch you're on
git branch

# Create a new branch and switch to it
git checkout -b customer-a/arc-welding

# Switch back to main
git checkout main

# Switch to an existing branch
git checkout customer-a/arc-welding

# Push a new branch to GitHub
git push -u origin customer-a/arc-welding
```

### When You're Done with a Branch

Merge it into main:

```powershell
# Switch to main
git checkout main

# Merge your branch
git merge customer-a/arc-welding

# Push the updated main
git push

# Delete the branch (optional)
git branch -d customer-a/arc-welding
```

---

## The community/ Submodule

The `community/` folder is special — it's a link to the reference code repository. Think of it as a "read-only library" embedded in your project.

### Update to Latest Reference Code

When CENIT publishes new reference downloaders or fixes:

```powershell
cd community
git pull origin master
cd ..
git add community
git commit -m "Update community reference to latest"
git push
```

### If community/ Is Empty After Cloning

This happens if you forgot the submodule step during setup:

```powershell
git submodule update --init
```

### Important

- **Never edit files inside `community/`** from your main repo
- If you want to contribute improvements, see [Contributing](contributing.md)

---

## Common Situations

### "I made a mess and want to start over on a file"

```powershell
# Discard all changes to a specific file
git checkout -- OLPTranslators/KUKA/MyDownloader.py
```

### "I want to see what I changed"

```powershell
# See a summary of changed files
git status

# See exact changes (line by line)
git diff
```

Or use the **Source Control** panel in VS Code — click any file to see a visual diff.

### "I committed but haven't pushed yet — I want to undo"

```powershell
# Undo the last commit but keep the changes
git reset --soft HEAD~1
```

### "I need to pull my colleague's changes"

```powershell
git pull
```

### "Git says there's a conflict"

This happens when you and a colleague changed the same lines. VS Code will highlight the conflict:

```
<<<<<<< HEAD
your version of the code
=======
their version of the code
>>>>>>> other-branch
```

Choose which version to keep (or combine them), save, then:

```powershell
git add .
git commit -m "Resolve merge conflict in MyDownloader.py"
```

---

## .gitignore — Files Git Should Ignore

The `.gitignore` file tells Git to skip certain files. The template already includes sensible defaults:

- `__pycache__/` — Python cache files
- `*.pyc` — Compiled Python files
- `.vs/` — Visual Studio files

If E2 generates output files in your repo folder, add them to `.gitignore`:

```
# E2 output files
*.ls
*.src
*.dat
*.mod
```

---

## Advanced: Cherry-Picking & Moving Commits Between Repos

> **Who needs this?** CENIT internal developers, integrators, and power users following [Workflow 5](daily-workflow.md#workflow-5--multi-repo-setup-cenit-internal--integrators--power-users). If you use a single repository with branches (Workflow 4), you can skip this section entirely.

These operations let you move individual commits between repositories — typically to backport a skill improvement from a customer repo to the starter.

### Cherry-Picking — What It Does

`git cherry-pick` copies a **single commit** from one branch (or repo) and replays it on your current branch. The original commit stays where it is — you get a new commit with the same changes and a new hash.

```
starter/main:       A ─ B ─ C ─ D'     ← D' is the cherry-picked copy
customer-a/main:    A ─ B ─ X ─ D ─ Y  ← D is the original skill fix
```

### Step-by-Step: Cherry-Pick a Commit from Another Repo

**1. Find the commit hash you want to move**

In the source repo (e.g., customer-a):

```powershell
# Show recent commits — look for your skill fix
git log --oneline -20
```

Output:
```
f3a1b2c  feat(KUKA): add CIR motion for customer A
9d4e5f6  skill: clarify event read-ahead pattern      ← this one
a1b2c3d  feat(ABB): add signal handling
```

Copy the hash (`9d4e5f6`).

**2. Switch to the target repo and add a remote**

```powershell
cd ../fastsuite-copilot-starter

# Add the customer repo as a remote (one-time)
git remote add customer-a ../customer-a

# Fetch its commits
git fetch customer-a
```

**3. Cherry-pick the commit**

```powershell
git cherry-pick 9d4e5f6
```

If there are **no conflicts**, Git creates a new commit automatically. You're done — push it:

```powershell
git push origin main
```

**4. If there are conflicts**

Git will tell you which files conflict. Open them in VS Code — look for the conflict markers:

```
<<<<<<< HEAD
your version
=======
their version
>>>>>>> 9d4e5f6
```

Resolve each file, then:

```powershell
git add .
git cherry-pick --continue
```

To **abort** a cherry-pick that went wrong:

```powershell
git cherry-pick --abort
```

### Cherry-Picking Multiple Commits

```powershell
# Pick a range (oldest..newest, oldest is EXCLUDED)
git cherry-pick abc1234..def5678

# Pick specific commits (listed in order)
git cherry-pick abc1234 def5678 ghi9012
```

### Working with Remotes — Quick Reference

Remotes are named links to other repositories. You can have as many as you need.

```powershell
# List all remotes
git remote -v

# Add a remote (local path or URL)
git remote add customer-a ../customer-a
git remote add customer-b https://github.com/company/customer-b.git

# Fetch all branches from a remote (does NOT change your files)
git fetch customer-a

# Remove a remote you no longer need
git remote remove customer-a
```

### Tagging Releases

Tags mark specific commits as release points.

```powershell
# Create an annotated tag
git tag -a v1.0.0 -m "Customer A: initial KUKA + ABB release"

# Push the tag to the remote
git push origin v1.0.0

# Push all tags
git push origin --tags

# List existing tags
git tag -l

# Check out a tag (read-only, detached HEAD)
git checkout v1.0.0
```

### Stashing — Temporarily Shelve Changes

When you need to switch branches but have uncommitted work:

```powershell
# Save current changes to a stash
git stash

# Switch branches, do other work, come back...
git checkout main

# Restore stashed changes
git stash pop
```

---

## Glossary

| Term | What It Means |
|------|---------------|
| **Repository (repo)** | Your project folder, tracked by Git |
| **Clone** | Download a repo from GitHub to your machine |
| **Commit** | A saved snapshot of your changes |
| **Push** | Upload commits from your machine to GitHub |
| **Pull** | Download commits from GitHub to your machine |
| **Branch** | A parallel line of work |
| **Merge** | Combine two branches |
| **Cherry-pick** | Copy a single commit onto your current branch |
| **Remote** | A named link to another repository (URL or local path) |
| **Tag** | A named marker on a specific commit (used for releases) |
| **Stash** | Temporarily shelve uncommitted changes |
| **Stage** | Mark files to include in the next commit |
| **Submodule** | An embedded link to another repository |
| **Diff** | The difference between two versions of a file |
