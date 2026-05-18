"""COPYRIGHT Cenit AG 2022"""

import subprocess


class NetworkUtility:
   """Network utility functions designed for analyzing and configuring various aspects of computer networks."""

   def Login(self, remoteLocation, username, password, persistent=False, timeoutSec=None):
      """Login to the remote location using username and passowrd.
      If the login successful, the new entry will be added to the network connections list.
      To see the available network connections run CMD command 'net use'.

      Args:
          remoteLocation (str): address to the remote directory (for example: '\\\\192.168.32.128\\FolderName').
          username (str): username to use for login.
          password (str): password to use for login.
          persistent (bool, optional): 'Yes' saves the connections and restores them at next logon.
          timeoutSec (int, optional): timeout in seconds. Defaults to None.

      Returns:
          bool: True if no error occurred, otherwise False.
      """
      persistentStr = "no"
      if persistent:
         persistentStr = "yes"
      result = subprocess.run(f"net use {remoteLocation} /persistent:{persistentStr} /user:{username} {password}",
                              universal_newlines=True, stdout=subprocess.PIPE, timeout=timeoutSec)
      if result.returncode == 0:
         return True
      return False

   def Disconnect(self, remoteLocation):
      """Remove the network address from the connections list.
      To see the available network connections run CMD command 'net use'.

      Args:
          remoteLocation (str): address to the remote directory (for example: '\\\\192.168.32.128\\FolderName').

      Returns:
          bool: True if no error occurred, otherwise False.
      """
      result = subprocess.run(f"net use {remoteLocation} /delete", 
                              universal_newlines = True, stdout = subprocess.PIPE)
      if result.returncode == 0:
         return True
      return False
