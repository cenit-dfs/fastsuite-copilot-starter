"""User interface utility created by CENIT AG.

The tkinter package (“Tk interface”) is the standard Python interface to the Tcl/Tk GUI toolkit.
For more information please visit: https://docs.python.org/3/library/tkinter.html

Tkinter (tk) widgets are recommended for beginners because they are easy to learn. On the other hand, 
Tkinter.ttk (tkk) is a module designed to make Tkinter widgets look really nice, although it is difficult to customize.

   Typical usage example:

   ui = UserInterface("Create Log", 620, 200)
   CreateUIContent(ui)
   ui.focus_force()  # make window active
   ui.mainloop()  # listen for events and wait for the window to close
   def CreateUIContent(window):
      # Configure the main frame and grid
      mainFrame = window.AddFrame(window)
      window.grid_rowconfigure(0, weight=1)
      window.grid_columnconfigure(0, weight=1)
      mainFrame.grid(row=0, column=0, sticky=E+W+N+S, **window.PADDINGS)
      # Create the variables
      window.user = StringVar()
      window.comment = StringVar()
      # Create the widgets
      window.AddLabel(mainFrame, "Windows-Benutzer", 120, 25, None).grid(row=0, column=0, sticky=E+W, **window.PADDINGS)
      ..
      window.AddTextBox(mainFrame, window.user, True).grid(row=0, column=1, columnspan=2, sticky=E+W+N+S, **window.PADDINGS)
      ..
      dDList = window.AddDropDownList(mainFrame, window.reason, reasonsList[1], reasonsList, 1, 1, None)
      dDList.grid(row=2, column=1, columnspan=2, sticky=E+W+N+S, **window.PADDINGS)
      ..
      multiTextBox = window.AddMultilineTextBox(mainFrame, "", 1, 3)
      multiTextBox.grid(row=3, column=1, columnspan=2, sticky=E+W+N+S, **window.PADDINGS)
      multiTextBox.focus()
      def AcceptClicked():
         global AcceptButtonClicked
         AcceptButtonClicked = True
         window.comment.set(multiTextBox.get("1.0","end-1c"))
         window.destroy()
      window.AddButton(mainFrame, "AKZEPTIEREN", 200, 60, AcceptClicked).grid(row=4, column=1, **window.PADDINGS)
      window.AddButton(mainFrame, "STORNIEREN", 200, 60, window.destroy).grid(row=4, column=2, **window.PADDINGS)

COPYRIGHT Cenit AG 2022
"""

import sys
import os
import inspect
import ctypes
import tkinter.ttk as tkk
from tkinter import *
from pathlib import Path


class UserInterface(Tk):
   """User interface utility.

   Args:
       Tk (Tk): tkinter interface.

   Returns:
       Tk: tkinter interface instance.
   """

   # Default variables shared by all instances
   WINDOW_BACKGROUND = '#2F2F2F'
   BUTTON_BACKGROUND = '#2F2F2F'
   BUTTON_BACKGROUND_HIGHLIGHTED = '#ACC334'
   BUTTON_BACKGROUND_ACTIVE = '#ACC334'
   BUTTON_FOREGROUND = '#EDEDED'
   BUTTON_FOREGROUND_ACTIVE = '#2F2F2F'
   ENUM_BACKGROUND = '#2F2F2F'
   ENUM_BACKGROUND_ACTIVE = '#ACC334'
   ENUM_FOREGROUND = '#EDEDED'
   ENUM_FOREGROUND_ACTIVE = '#EDEDED'
   LABEL_BACKGROUND = '#2F2F2F'
   LABEL_FOREGROUND = '#EDEDED'
   ENTRY_BACKGROUND = '#2F2F2F'
   ENTRY_BACKGROUND_READONLY = '#2F2F2F'
   ENTRY_BACKGROUND_SELECTED = '#ACC334'
   ENTRY_FOREGROUND = '#EDEDED'
   ENTRY_BORDER = '#636363'
   ENTRY_BORDER_ACTIVE = '#ACC334'
   ENTRY_CURSOR = '#EDEDED'
   TEXT_BACKGROUND = '#2F2F2F'
   TEXT_BACKGROUND_SELECTED = '#ACC334'
   TEXT_FOREGROUND = '#EDEDED'
   TEXT_BORDER = '#636363'
   TEXT_BORDER_ACTIVE = '#ACC334'
   TEXT_CURSOR = '#EDEDED'
   SCROLLBAR_BACKGROUND = '#2F2F2F'
   SCROLLBAR_BACKGROUND_ACTIVE = '#ACC334'
   SCROLLBAR_FOREGROUND = '#ACC334'
   SCROLLBAR_BORDER = '#636363'
   SCROLLBAR_BORDER_ACTIVE = '#ACC334'
   SCROLLBAR_TROUGH = '#2F2F2F'
   SCROLLBAR_ARROW = '#ACC334'
   SCROLLBAR_LIGHT = '#ACC334'
   SCROLLBAR_DARK = '#ACC334'
   PADDINGS = {'padx': 5, 'pady': 5}
   __currentFilePath = Path(os.path.abspath(inspect.getfile(inspect.currentframe())))
   ICON = os.path.join(__currentFilePath.parent, "images", "Fastsuite_E2_Icon.ico")

   def __init__(self, title, width, height, resizeWidth = False, resizeHeight = False):
      """Construct a new 'Tk' object. 
      
      Create an empty UI window with the given title and parameters in E2 style.

      Args:
          title (str): the window's titel.
          width (int): the window's width in pixels.
          height (int): the window's height in pixels.
      """
      sys.argv  = ['']
      super().__init__()
      # Calculates the X and Y coordinates for the window to be centered on the screen
      centerX = int((self.winfo_screenwidth() / 2) - (width / 2))
      centerY = int((self.winfo_screenheight() / 2) - (height / 2))
      self.geometry(f"{width}x{height}+{centerX}+{centerY}")
      self.title(title)
      self.resizable(resizeWidth, resizeHeight)
      if self.ICON:
         self.iconbitmap(self.ICON)
      self.configure(bg=self.WINDOW_BACKGROUND)
      self._virtualPixel = PhotoImage(width=1, height=1)
      
   def AddFrame(self, window):
      """Add a Frame to the given window.

      Args:
          window (tk): instance of tkinter window.

      Returns:
          tk.Frame: frame instance.
      """
      frame = Frame(window, bg=self.WINDOW_BACKGROUND, **self.PADDINGS)
      return frame

   def AddButton(self, window, text, width, height, function):
      """Add a Button to the given window with the specified parameters.

      Args:
          window (tk): instance of tkinter window.
          text (str): text of the button to display.
          width (int): window's height in pixels.
          height (int): window's height in pixels.
          function (def): callback function on button click.

      Returns:
          tk.Button: button instance.
      """
      buttont = Button(window, text=text, width=width, height=height, command=function,
                       image=self._virtualPixel, relief=RIDGE, font=("Arial", 10), compound="c",
                       fg=self.BUTTON_FOREGROUND, bg=self.BUTTON_BACKGROUND, 
                       activebackground=self.BUTTON_BACKGROUND_ACTIVE, 
                       activeforeground=self.BUTTON_FOREGROUND_ACTIVE)
      def on_enter(e):
         buttont['background'] = self.BUTTON_BACKGROUND_HIGHLIGHTED
      def on_leave(e):
         buttont['background'] = self.BUTTON_BACKGROUND
      buttont.bind("<Enter>", on_enter)
      buttont.bind("<Leave>", on_leave)
      return buttont

   def AddDropDownList(self, window, variable, default, listValues, width, height, function):
      """Add a drop-down list to the given window with the specified parameters.

      Args:
          window (tk): instance of tkinter window.
          variable (tk.StringVar): currently selected list value.
          default (list value): default list value.
          listValues (list): list of values.
          width (int): window's width in pixels.
          height (int): window's height in pixels.
          function (def): callback function on enum changed.

      Returns:
          tk.OptionMenu: drop-down list instance.
      """
      enum = OptionMenu(window, variable, *listValues, command=function)
      variable.set(default)
      enum.configure(width=width, height=height, 
                     highlightthickness=0, justify=LEFT, font=("Arial", 10), 
                     bg=self.ENUM_BACKGROUND, fg=self.ENUM_FOREGROUND, 
                     activebackground=self.ENUM_BACKGROUND_ACTIVE, 
                     activeforeground=self.ENUM_FOREGROUND_ACTIVE)
      enum["menu"].configure(bg=self.ENUM_BACKGROUND, fg=self.ENUM_FOREGROUND, 
                             activebackground=self.ENUM_BACKGROUND_ACTIVE, 
                             activeforeground=self.ENUM_FOREGROUND_ACTIVE)
      return enum

   def AddLabel(self, window, text, width, height, function):
      """Add a Label to the given window with the specified parameters.

      Args:
          window (tk): instance of tkinter window.
          text (str): text to display.
          width (int): window's width in pixels.
          height (int): window's height in pixels.
          function (def): callback function on label changed.

      Returns:
          tk.Label: label instance.
      """
      label = Label(window, text=text, width=width, height=height, command=function,
                 image=self._virtualPixel, font=("Arial", 10), compound="c", anchor='w',
                 bg=self.LABEL_BACKGROUND, fg=self.LABEL_FOREGROUND)
      return label

   def AddTextBox(self, window, variable, readonly=False):
      """Add a simple TextBox entry to the given window with the specified parameters.

      Args:
          window (tk): instance of tkinter window.
          variable (tk.StringVar): TextBox value holder.
          readonly (bool, optional): readonly flag. Defaults to False.

      Returns:
          tk.Entry: TextBox instance.
      """
      entry = Entry(window, textvariable=variable,
                    justify=LEFT, font=("Arial", 10),
                    bg=self.ENTRY_BACKGROUND, fg=self.ENTRY_FOREGROUND,
                    insertbackground=self.ENTRY_CURSOR, selectbackground=self.ENTRY_BACKGROUND_SELECTED,
                    highlightthickness=1, 
                    highlightcolor=self.ENTRY_BORDER_ACTIVE, highlightbackground=self.ENTRY_BORDER)
      if readonly:
         entry.configure(state='readonly', readonlybackground=self.ENTRY_BACKGROUND_READONLY)
      return entry

   def AddMultilineTextBox(self, window, text, width, height, readonly=False):
      """Add a multiline TextBox entry to the given window with the specified parameters.

      Args:
          window (tk): instance of tkinter window.
          text (_type_): text to display.
          width (int): number of characters.
          height (int): number of rows.
          readonly (bool, optional): readonly flag. Defaults to False.

      Returns:
          tk.Text: TextBox instance.
      """
      textBox = Text(window, height=height, width=width, font=("Arial",10),
                     fg=self.TEXT_FOREGROUND, bg=self.TEXT_BACKGROUND,
                     insertbackground=self.TEXT_CURSOR, selectbackground=self.TEXT_BACKGROUND_SELECTED,
                     highlightthickness=1, 
                     highlightcolor=self.TEXT_BORDER_ACTIVE, highlightbackground=self.TEXT_BORDER)
      textBox.insert(END, text)
      if readonly:
         textBox.configure(state=DISABLED)
      return textBox

   def AddScrollbar(self, window, orient, function):
      """Add a Scrollbar to the given window witht the specified parameters.

      Args:
          window (tk): instance of tkinter window.
          orient (str): use 'horizontal' for a horizontal scrollbar and 'vertical' for a vertical one.
          function (def): callback function on scrollbar changed.

      Returns:
          tkk.Scrollbar: Scrollbar instance.

      Typical usage example:
          comment = window.AddMultilineTextBox(mainFrame, "", 1, 3)
          comment.grid(row=3, column=1, columnspan=2, sticky=E+W+N+S, padx=(5, 20), pady=5)
          scrollbar = window.AddScrollbar(mainFrame, "vertical", comment.yview)
          scrollbar.grid(row=3, column=2, sticky=N+S+E, **window.PADDINGS)
          comment.configure(yscrollcommand=scrollbar.set)
      """
      style=tkk.Style()
      style.theme_use('clam')
      style.configure("Vertical.TScrollbar", arrowcolor=self.SCROLLBAR_ARROW,
                      background=self.SCROLLBAR_BACKGROUND, foreground=self.SCROLLBAR_FOREGROUND,
                      bordercolor=self.SCROLLBAR_BORDER, troughcolor=self.SCROLLBAR_TROUGH,
                      darkcolor=self.SCROLLBAR_DARK, lightcolor=self.SCROLLBAR_LIGHT)
      style.configure("Horizontal.TScrollbar", arrowcolor=self.SCROLLBAR_ARROW,
                      background=self.SCROLLBAR_BACKGROUND, foreground=self.SCROLLBAR_FOREGROUND,
                      bordercolor=self.SCROLLBAR_BORDER, troughcolor=self.SCROLLBAR_TROUGH,
                      darkcolor=self.SCROLLBAR_DARK, lightcolor=self.SCROLLBAR_LIGHT)
      scrollbar = tkk.Scrollbar(window, orient=orient, command=function)
      return scrollbar

class MessageBox:
   """Message window, also known as a dialog box, presents a message to the user. 
   It is a modal window, blocking other actions in the application until the user closes it.

   Please see for more information:
   https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-messagebox?redirectedfrom=MSDN
   
   """
   # Button IDs
   OK = 0x0
   OKCANCEL = 0x01
   ABORTRETRYIGNORE = 0x02
   YESNOCANCEL = 0x03
   YESNO = 0x04
   RETRYCANCEL = 0x05
   CANCELTRYCONTINUE = 0x06
   
   # Icon IDs
   ICON_ERROR = 0x10
   ICON_QUESTION = 0x20
   ICON_WARNING=0x30
   ICON_INFO = 0x40
   
   # Result IDs
   IDERROR = 0  #The function fails
   IDOK = 1  #The OK button was selected
   IDCANCEL = 2  #The Cancel button was selected
   IDABORT = 3  #The Abort button was selected
   IDRETRY = 4  #The Retry button was selected
   IDIGNORE = 5  #The Ignore button was selected
   IDYES = 6  #The Yes button was selected
   IDNO = 7  #The No button was selected
   IDTRYAGAIN = 10  #The Try Again button was selected
   IDCONTINUE = 11  #The Continue button was selected
   
   def Show(self, title, message, buttonStyle, icon):
      """Display a simple MessageBox that displays a modal dialog box with a system icon, 
      a set of buttons, and a brief application-specific message, such as status or error information.

      Args:
          title (str): dialog box title
          message (str): message to be displayed.
          buttonStyle (int): buttons style flag
          icon (int): icon flag

      Returns:
          int: integer value that indicates which button the user clicked
      """
      return ctypes.windll.user32.MessageBoxW(0, message, title, buttonStyle | icon)
