# Daily Workflow — Creating and Managing Customizations

This guide covers the day-to-day work of creating E2 downloaders, uploaders, and technology plugins.

## Which Workflow Is Right for You?

This guide describes two different approaches. Read the table below and follow the one that matches your situation:

| Workflow | Who is it for? | How it works |
|----------|---------------|--------------|
| **Workflows 1–4** (this page) | **End users** — project engineers who maintain their own E2 plugins in a single repository | You clone the starter once, create your vendor code, commit, push. One repo holds everything. Branches separate parallel tasks. |
| **Workflow 5** (bottom of this page) | **CENIT internal developers**, **integrators**, and **power users** who deliver plugins to multiple customers *and* improve the starter/skills for production releases | Each customer gets its own repo. Skill improvements are cherry-picked back to the starter. Agent updates flow downstream via `git merge`. |

> **Not sure?** Start with Workflows 1–4. You can always migrate to the multi-repo approach later — your commit history carries over.

> **All workflows:** Don't forget to [pull updates from the starter repo](#pulling-updates-from-the-starter-repo) periodically to get the latest Copilot skills and docs.

---

## Understanding the Repository Structure

Your repository has two distinct areas:

```
your-repo/
├── OLPTranslators/          ← YOUR code goes here (you edit this)
│   └── MYVENDOR/
│       └── MyDownloader.py
├── Technologies/             ← YOUR tech plugins go here (you edit this)
├── community/                ← Reference code (READ-ONLY, don't edit)
│   └── OLPTranslators/
│       ├── KUKA/KUKA_KRC5.py    ← Example to learn from
│       └── ABB/ABB_IRC5.py      ← Advanced example
├── skills/                   ← Copilot skills (rarely need to edit)
├── docs/                     ← Documentation (rarely need to edit)
└── .github/                  ← Copilot instructions (rarely need to edit)
```

**Key rule:** You create your own files in `OLPTranslators/` and `Technologies/`. The `community/` folder is a reference library — Copilot reads it to understand how E2 downloaders work, but you never edit those files directly.

---

## Workflow 1 — Create a New Downloader

### Step 1: Tell Copilot What You Need

Open Copilot Chat and describe what you want:

> *"Create a new FANUC R-30iB downloader that outputs .LS files with motion commands, tool/base frames, and signal I/O"*

Or switch to the **E2Downloader** agent mode for more focused help:
1. Click the agent mode selector in the Chat panel
2. Choose **E2Downloader**
3. Ask your question

Copilot will generate a downloader based on the reference code in `community/` and the skill files.

### Step 2: Save the Generated Code

1. Create a vendor folder: Right-click `OLPTranslators/` → **New Folder** → e.g., `FANUC`
2. Create the file: Right-click the new folder → **New File** → e.g., `FANUC_R30iB.py`
3. Paste or let Copilot write the code directly into the file

### Step 3: Iterate with Copilot

Ask follow-up questions to refine the downloader:

- *"Add CIRC motion support"*
- *"Handle the speed event to output OVERRIDE commands"*
- *"Add a FOLD structure for the WAIT instruction"*

Copilot understands E2's callback lifecycle, position formats, and event handling because of the skills and reference code.

### Step 4: Test in FASTSUITE E2

1. Copy your `.py` file to E2's translator folder (or configure E2 to point to your repo folder)
2. Create the corresponding `.xml` configuration file (Copilot can help with this too)
3. Run a download in FASTSUITE E2
4. Check the generated robot program output

### Step 5: Save Your Work (Commit)

After you're happy with your changes:

1. Open the **Source Control** panel in VS Code (click the branch icon in the left sidebar, or press `Ctrl+Shift+G`)
2. You'll see your changed files listed
3. Type a short message describing what you did, e.g., *"Add FANUC R-30iB base downloader"*
4. Click the **✓ Commit** button
5. Click **Sync Changes** to push to GitHub

See [Git Essentials](git-essentials.md) for more details on commits and branches.

---

## Workflow 2 — Modify an Existing Downloader

If you need to customize an existing downloader for a specific customer:

1. **Copy** the reference file from `community/` to your `OLPTranslators/` folder:
   - Right-click the file in `community/OLPTranslators/KUKA/KUKA_KRC5.py`
   - Copy it to `OLPTranslators/KUKA/KUKA_KRC5_CustomerName.py`
2. Edit your copy — never the original in `community/`
3. Ask Copilot: *"In my KUKA_KRC5_CustomerName.py, add support for analog outputs using $ANOUT"*

---

## Workflow 3 — Technology Plugin Customization

Technology plugins customize the E2 UI (tabs, attributes, events).

1. Switch to **E2Technology** agent mode in Copilot Chat
2. Create your plugin folder: `Technologies/ArcWeldingTechnology/MYVENDOR/Standard/Scripts/`
3. Ask Copilot: *"Create a PostTechInitAttributes callback that adds a custom 'WireSpeed' attribute"*
4. Test in E2 by assigning the technology to a controller

---

## Workflow 4 — Working on Multiple Projects (End Users)

> **Audience:** End users / project engineers who work in a single repository and need to separate work for different customers or tasks.

Use **Git branches** to keep changes isolated inside the same repository. Each branch is like a separate workspace — you switch between them without losing work:

```powershell
# Create a branch for Customer A
git checkout -b customer-a/arc-welding

# ... do your work, commit ...

# Switch to main branch
git checkout main

# Create a branch for Customer B
git checkout -b customer-b/handling
```

When you're done with a customer's work, merge the branch into `main` (see [Git Essentials](git-essentials.md)).

**This approach is simple and works well when:**
- You maintain one set of plugins for yourself or a small number of customers
- You don't need independent release tags per customer
- You don't need to push skill/agent improvements back to the starter repo

---

## The community/ Folder — Updating Reference Code

The `community/` folder is a **Git submodule** — a pointer to a specific version of the community repository. To get the latest reference code:

```powershell
cd community
git pull origin master
cd ..
git add community
git commit -m "Update community reference code"
git push
```

You typically only need to do this when CENIT publishes new reference downloaders or fixes.

---

## Pulling Updates from the Starter Repo

> **Important for all end users:** The starter repo receives improvements over time — better Copilot skills, updated API docs, new templates, and bug fixes. You should pull these updates into your repository periodically.

### One-Time Setup: Add the Starter as `upstream`

When you created your repo from the template, GitHub did **not** keep a link back to the original. You need to add it manually (once):

```powershell
git remote add upstream https://github.com/cenit-dfs/fastsuite-copilot-starter.git
```

Verify it's set up:

```powershell
git remote -v
# origin    https://github.com/<you>/<your-repo>.git (fetch)
# origin    https://github.com/<you>/<your-repo>.git (push)
# upstream  https://github.com/cenit-dfs/fastsuite-copilot-starter.git (fetch)
# upstream  https://github.com/cenit-dfs/fastsuite-copilot-starter.git (push)
```

### Pulling Updates (anytime)

```powershell
git fetch upstream
git merge upstream/main
```

**Why this works without conflicts:** Your code lives in `OLPTranslators/<VENDOR>/` and `Technologies/<VENDOR>/` — directories that are never modified in the starter. Updates from the starter land in `skills/`, `docs/`, `.github/`, `.vscode/`, etc. The two sets of files don't overlap.

After merging, push the updated state to your own remote:

```powershell
git push
```

### What if I see a conflict?

This is rare but can happen if you edited a file that the starter also changed (e.g., you customized `.github/copilot-instructions.md`). VS Code will highlight the conflict — resolve it, then:

```powershell
git add .
git commit -m "Merge upstream starter updates"
git push
```

See [Git Essentials — conflicts](git-essentials.md#git-says-theres-a-conflict) for details.

---

## Workflow 5 — Multi-Repo Setup (CENIT Internal / Integrators / Power Users)

> **Audience:** CENIT developers who improve the starter repo and skills for production releases, system integrators delivering to multiple customers, and power users who need independent release cycles.

**When to use this instead of branches (Workflow 4):**
- You maintain the **starter repo itself** (skills, agent files, docs) *and* deliver customer plugins
- Customers need **independent repositories** with their own release tags (v1.0, v2.0 …)
- You want to **cherry-pick skill improvements** back to the starter so all customers benefit
- Different customers have different release cadences or access restrictions

**How it differs from Workflow 4:**

| | Workflow 4 (Branches) | Workflow 5 (Multi-Repo) |
|-|----------------------|------------------------|
| Repos | 1 repo, multiple branches | 1 starter + 1 repo per customer |
| Releases | Tags on `main` | Independent tags per customer repo |
| Skill fixes | Stay in your repo | Cherry-picked back to starter, flow to all customers |
| Complexity | Low | Medium — requires commit discipline |

The idea: each customer gets a **separate clone** of the starter. The starter repo is added as an `upstream` remote so you can pull agent/skill updates into any customer repo at any time. Because customer code (`OLPTranslators/<VENDOR>/`, `Technologies/`) and agent files (`skills/`, `docs/`, `.github/`) live in non-overlapping directories, merges from upstream are conflict-free.

### One-Time Setup for a New Customer

```powershell
# Clone the starter as customer A's project
git clone <starter-url> customer-a
cd customer-a
git submodule update --init

# Rename origin → upstream, add customer's own remote as origin
git remote rename origin upstream
git remote add origin <customer-a-repo-url>
git push -u origin main
```

Now `upstream` = starter repo, `origin` = customer A's repo.

### Daily Commit Discipline

Keep **two kinds of commits separate** — this is the key discipline that makes everything else work.

**Plugin commits** — customer-specific code:
```powershell
git add OLPTranslators/KUKA/ Technologies/ docs/KUKA/
git commit -m "feat(KUKA): add CIR motion support for customer A"
```

**Skill/agent commits** — improvements to skills, docs, or Copilot instructions:
```powershell
git add skills/ docs/API_Python/ .github/
git commit -m "skill: clarify event read-ahead pattern in downloader skill"
```

### Backporting Skill Improvements to the Starter

When you fix or improve a skill while working in a customer repo, cherry-pick those commits back to the starter:

```powershell
# In the starter repo
cd ../fastsuite-copilot-starter

# Add customer repo as a local remote (one-time)
git remote add customer-a ../customer-a

# Fetch and cherry-pick the skill commit(s)
git fetch customer-a
git cherry-pick <commit-hash>
git push origin main
```

See [Git Essentials — Cherry-Picking](git-essentials.md#cherry-picking--moving-commits-between-repos) for step-by-step details.

### Pulling Starter Updates into a Customer Repo

When the starter gets new skills or docs:

```powershell
cd ../customer-a
git fetch upstream
git merge upstream/main
# Typically no conflicts — different directories
git push origin main
```

### Releasing a Customer Version

Tag releases in the customer repo:

```powershell
git tag -a v1.0.0 -m "Customer A: KUKA KRC5 + ABB IRC5 release"
git push origin v1.0.0
```

### Summary — The Rhythm

| Step | Where | Command |
|------|-------|---------|
| Daily coding | `customer-a/` | Commit plugin code and skill fixes **separately** |
| Push customer work | `customer-a/` | `git push` |
| Backport skill fixes | `starter/` | `git cherry-pick <hash>` from customer remote |
| Pull latest agent files | `customer-a/` | `git fetch upstream && git merge upstream/main` |
| Release customer version | `customer-a/` | `git tag v1.x.x && git push origin v1.x.x` |

---

## Quick Reference — VS Code Shortcuts

| Action | Shortcut |
|--------|----------|
| Open Copilot Chat | `Ctrl+Shift+I` |
| Open Source Control | `Ctrl+Shift+G` |
| Open Terminal | `` Ctrl+` `` |
| Save file | `Ctrl+S` |
| Search in files | `Ctrl+Shift+F` |
| Open file by name | `Ctrl+P` |
| Toggle sidebar | `Ctrl+B` |

---

## Tips for Working with Copilot

1. **Be specific** — *"Add a KUKA FOLD comment with PE marker"* works better than *"add a comment"*
2. **Reference existing code** — *"Use the same pattern as LogicPortEvent in KUKA_KRC5.py"*
3. **Use agent modes** — Switch to E2Downloader when working on downloaders
4. **Open reference files** — Having `community/OLPTranslators/KUKA/KUKA_KRC5.py` open in a tab gives Copilot more context
5. **Use the tree dumper** — Download with `Simple_Python_Translator.py` first to see the E2 object tree, then share the output with Copilot
