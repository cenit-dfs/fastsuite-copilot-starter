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
| **Stage** | Mark files to include in the next commit |
| **Submodule** | An embedded link to another repository |
| **Diff** | The difference between two versions of a file |
