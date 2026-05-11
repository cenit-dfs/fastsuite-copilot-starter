# Daily Workflow — Creating and Managing Customizations

This guide covers the day-to-day work of creating E2 downloaders, uploaders, and technology plugins.

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

## Workflow 4 — Working on Multiple Projects

If you work on customizations for different customers, use **Git branches**:

```powershell
# Create a branch for Customer A
git checkout -b customer-a/arc-welding

# ... do your work, commit ...

# Switch to main branch
git checkout main

# Create a branch for Customer B
git checkout -b customer-b/handling
```

Each branch keeps its changes isolated. See [Git Essentials](git-essentials.md) for details.

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
