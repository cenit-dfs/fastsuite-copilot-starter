# -------------------------------------------------------------------------------------------
# Name: Dev Loop Watcher (TEMPLATE)
# Description: Generic AuxiliaryCommands/OlpProgram tool for the agentic downloader dev loop.
#              Start it once manually on the active program; it then keeps running and
#              auto-retriggers a download whenever a watched translator file changes on disk
#              (or an explicit trigger file is written), reporting results to a status file
#              so a coding agent can read them without a human re-clicking Download in E2.
#              Copy this file + a sibling "devloop_config.json" into a
#              Technologies/<Tech>/<Vendor>/Standard/AuxiliaryCommands/OlpProgram/ folder and
#              generate a fresh GetCommandUuId() for the copy.
# Debugg info: E2@localhost:5254
# Author: CENIT AG
# Changelog:
#     Version: 1.0
#        Changed by:
#        Date: 2026-08-31
# -------------------------------------------------------------------------------------------

# Import libraries
from centypes import *
from cenpylib import *
import sys, os, json, shutil, inspect, time
import tkinter as tk
sys.dont_write_bytecode = True

CONFIG_FILE_NAME = "devloop_config.json"
ACTIVE_PROGRAM_SENTINEL = "<active>"
DEFAULT_POLL_INTERVAL_MS = 1000
LOG_RING_BUFFER_SIZE = 200
REQUIRED_CONFIG_KEYS = ["workspace_root", "watch_files", "program_names", "trigger_file", "status_file", "output_copy_dir"]

def GetCommandName():
   return "DevLoopWatcher"

def GetCommandUuId():
   # Regenerate this per copy/instance so E2 does not see duplicate command IDs.
   return "962EF838-6B9F-4346-A863-6D25A3B27DBF"

def GetIconName():
   return "COM_ScriptsRun"

# -------------------------------------------------------------------------------------------
def _ScriptDir():
   return os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

def _LoadConfig():
   configPath = os.path.join(_ScriptDir(), CONFIG_FILE_NAME)
   with open(configPath, "r", encoding="utf-8") as f:
      config = json.load(f)
   missing = [key for key in REQUIRED_CONFIG_KEYS if key not in config]
   if missing:
      raise ValueError(f"{CONFIG_FILE_NAME} is missing required key(s): {missing}")
   config.setdefault("poll_interval_ms", DEFAULT_POLL_INTERVAL_MS)
   return config

def _AbsPath(workspaceRoot, relativePath):
   return os.path.normpath(os.path.join(workspaceRoot, relativePath))

def _AtomicWriteJson(path, data):
   os.makedirs(os.path.dirname(path), exist_ok=True)
   tmpPath = path + ".tmp"
   with open(tmpPath, "w", encoding="utf-8") as f:
      json.dump(data, f, indent=2)
   os.replace(tmpPath, path)


class _RingLog:
   """Fixed-size in-memory tail shared by the Operator logger, the Tk widget, and status.json."""

   def __init__(self, maxLines=LOG_RING_BUFFER_SIZE):
      self._lines = []
      self._maxLines = maxLines

   def Add(self, line):
      self._lines.append(line)
      if len(self._lines) > self._maxLines:
         self._lines.pop(0)

   def Tail(self):
      return list(self._lines)


class DevLoopWatcher:
   """Owns the Tk status window, poll loop, and download/status/output plumbing for one run."""

   def __init__(self, operator: CENPyOlpProgramModifyOperator, config: dict):
      self.operator = operator
      self.config = config
      self.logging = operator.GetLoggerOperator()
      self.workspaceRoot = config["workspace_root"]
      self.watchFiles = [_AbsPath(self.workspaceRoot, p) for p in config["watch_files"]]
      self.programNames = config["program_names"]
      self.pollIntervalMs = config["poll_interval_ms"]
      self.triggerFile = _AbsPath(self.workspaceRoot, config["trigger_file"])
      self.statusFile = _AbsPath(self.workspaceRoot, config["status_file"])
      self.outputCopyDir = _AbsPath(self.workspaceRoot, config["output_copy_dir"])
      self.ringLog = _RingLog()
      self.mtimeSnapshot = self._SnapshotMtimes()
      self.stopRequested = False
      # Dispatch table so "upload" (or other actions) can be added later without reshaping the poll loop.
      self.actionDispatch = {
         "download": self._DoDownload,
      }
      self._logWidget = None
      self._BuildUi()

   # ---------------- logging fan-out (Operator logger + Tk widget + ring buffer) ----------------
   def _Log(self, message, level="info"):
      if level == "error":
         self.logging.LogError(message)
      elif level == "warn":
         self.logging.LogWarn(message)
      else:
         self.logging.LogInfo(message)
      self.ringLog.Add(message)
      if self._logWidget is not None:
         self._logWidget.configure(state="normal")
         self._logWidget.insert("end", message + "\n")
         self._logWidget.see("end")
         self._logWidget.configure(state="disabled")

   # ---------------- mtime watch ----------------
   def _SnapshotMtimes(self):
      snapshot = {}
      for path in self.watchFiles:
         try:
            snapshot[path] = os.path.getmtime(path)
         except OSError:
            snapshot[path] = None
      return snapshot

   def _MtimesChanged(self):
      changed = False
      for path in self.watchFiles:
         try:
            current = os.path.getmtime(path)
         except OSError:
            current = None
         if current != self.mtimeSnapshot.get(path):
            self.mtimeSnapshot[path] = current
            changed = True
      return changed

   # ---------------- explicit trigger file ----------------
   def _ConsumeTriggerFile(self):
      if not os.path.isfile(self.triggerFile):
         return None
      try:
         with open(self.triggerFile, "r", encoding="utf-8") as f:
            trigger = json.load(f)
      except (OSError, json.JSONDecodeError) as e:
         self._Log(f"DevLoopWatcher: failed to read trigger file, ignoring: {e}", "warn")
         trigger = None
      try:
         os.remove(self.triggerFile)
      except OSError:
         pass
      return trigger

   # ---------------- Tk UI ----------------
   def _BuildUi(self):
      self.root = tk.Tk()
      self.root.title("Downloader Dev Loop Watcher")
      self.root.attributes("-topmost", True)
      self.root.protocol("WM_DELETE_WINDOW", self._RequestStop)

      self.stateVar = tk.StringVar(value="Watching")
      self.triggerVar = tk.StringVar(value="(none yet)")
      self.resultVar = tk.StringVar(value="(none yet)")

      tk.Label(self.root, text="State:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
      tk.Label(self.root, textvariable=self.stateVar).grid(row=0, column=1, sticky="w", padx=5, pady=2)
      tk.Label(self.root, text="Last Trigger:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
      tk.Label(self.root, textvariable=self.triggerVar).grid(row=1, column=1, sticky="w", padx=5, pady=2)
      tk.Label(self.root, text="Last Result:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
      tk.Label(self.root, textvariable=self.resultVar).grid(row=2, column=1, sticky="w", padx=5, pady=2)

      self._logWidget = tk.Text(self.root, height=12, width=80, state="disabled")
      self._logWidget.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

      tk.Button(self.root, text="Stop", command=self._RequestStop).grid(row=4, column=0, columnspan=2, pady=5)

   def _RequestStop(self):
      self.stopRequested = True

   # ---------------- main poll loop ----------------
   def Run(self):
      self._Log(f"DevLoopWatcher started. Watching: {self.watchFiles}")
      self.root.after(self.pollIntervalMs, self._Poll)
      self.root.mainloop()

   def _Poll(self):
      if self.stopRequested:
         self._Log("DevLoopWatcher: stop requested, closing.")
         self.root.destroy()
         return

      trigger = self._ConsumeTriggerFile()
      if trigger is not None:
         action = trigger.get("action", "download")
         if action == "stop":
            self._Log("DevLoopWatcher: stop trigger received, closing.")
            self.root.destroy()
            return
         self.triggerVar.set("explicit trigger file")
         self._RunAction(action, trigger.get("program_names", self.programNames))
      elif self._MtimesChanged():
         self.triggerVar.set("watched file changed")
         self._RunAction("download", self.programNames)

      self.root.after(self.pollIntervalMs, self._Poll)

   # ---------------- action dispatch ----------------
   def _RunAction(self, action, programNames):
      handler = self.actionDispatch.get(action)
      if handler is None:
         self._Log(f"DevLoopWatcher: action '{action}' is not implemented.", "error")
         self._WriteStatus(action, programNames, success=False, error=f"action '{action}' not implemented")
         return
      self.stateVar.set("Running")
      try:
         handler(programNames)
      except Exception as e:
         self._Log(f"DevLoopWatcher: '{action}' failed: {e}", "error")
         self._WriteStatus(action, programNames, success=False, error=str(e))
      finally:
         self.stateVar.set("Watching")

   def _ResolveProgramNames(self, programNames):
      resolved = []
      for name in programNames:
         if name == ACTIVE_PROGRAM_SENTINEL:
            activeProgram = self.operator.GetActiveProgram()
            if activeProgram is None:
               raise RuntimeError("No active program to resolve '<active>'.")
            resolved.append(activeProgram.GetName())
         else:
            resolved.append(name)
      return resolved

   def _DoDownload(self, programNames):
      controller = self.operator.GetController()
      resolvedNames = self._ResolveProgramNames(programNames)
      returnCodes = {}
      for name in resolvedNames:
         returnCodes[name] = controller.DownloadProgramByName(name)
      generatedFiles = controller.GetLastGeneratedFilePathsFromDownload() or []

      copiedFiles = []
      os.makedirs(self.outputCopyDir, exist_ok=True)
      for filePath in generatedFiles:
         try:
            destPath = os.path.join(self.outputCopyDir, os.path.basename(filePath))
            shutil.copy2(filePath, destPath)
            copiedFiles.append(destPath)
         except OSError as e:
            self._Log(f"DevLoopWatcher: failed to copy '{filePath}': {e}", "warn")

      success = all(code == 0 for code in returnCodes.values())
      self._Log(f"DevLoopWatcher: download {'succeeded' if success else 'failed'} for {resolvedNames} -> {returnCodes}")
      self.resultVar.set("OK" if success else "FAILED")
      self._WriteStatus("download", resolvedNames, success=success, returnCodes=returnCodes,
                         generatedFiles=generatedFiles, copiedFiles=copiedFiles)

   # ---------------- status file ----------------
   def _WriteStatus(self, action, programNames, success, returnCodes=None, generatedFiles=None,
                     copiedFiles=None, error=None):
      status = {
         "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
         "action": action,
         "program_names": programNames,
         "success": success,
         "return_codes": returnCodes or {},
         "generated_files": generatedFiles or [],
         "copied_files": copiedFiles or [],
         "error": error,
         "log_tail": self.ringLog.Tail(),
      }
      _AtomicWriteJson(self.statusFile, status)


# -------------------------------------------------------------------------------------------
def ModifyActiveProgram(Operator: CENPyOlpProgramModifyOperator):
   logging = Operator.GetLoggerOperator()
   try:
      config = _LoadConfig()
   except Exception as e:
      logging.LogError(f"DevLoopWatcher: failed to load {CONFIG_FILE_NAME}: {e}")
      raise

   watcher = DevLoopWatcher(Operator, config)
   watcher.Run()
