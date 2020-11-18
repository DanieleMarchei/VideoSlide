import vlc
import sys
import tkinter as Tk
from tkinter import ttk
from os.path import expanduser, isfile
import os
libtk = "N/A"
C_Key = "Control-"

class Player(Tk.Frame):
    _geometry = ''
    _stopped  = None

    def __init__(self, parent, folder):
        Tk.Frame.__init__(self, parent)

        pad = 3
        self.parent = parent
        self.parent.title(folder)
        self.parent.bind("<Key>", self.KeyPressed)
        self.parent.attributes('-fullscreen', True)
        
        self.videos = [f"{folder}/{video}" for video in os.listdir(folder)]
        self.n_videos = len(self.videos)
        self.index = 0

        self.video = self.videos[self.index]
        
        self.videopanel = ttk.Frame(self.parent)
        self.canvas = Tk.Canvas(self.videopanel)
        self.videopanel.pack(fill=Tk.BOTH, expand=1)
        self.canvas.pack(fill=Tk.BOTH, expand=1)

        # VLC player
        args = []

        self.Instance = vlc.Instance(args)
        self.player = self.Instance.media_player_new()

        self.parent.update()


        self.parent.minsize(width=720, height=405)
        self.OnPlay()

    def KeyPressed(self, event):
        key = event.keysym
        if key == "space":
            self.OnPause()
        elif key == "Escape":
            self.OnClose()
        elif key == "f":
            isFullscreen = self.parent.attributes('-fullscreen')
            self.parent.attributes('-fullscreen', not isFullscreen)
        elif key == "Right":
            if self.index == self.n_videos - 1:
                return

            self.OnPause()
            self.player.set_media(None)
            self.index += 1
            self.video = self.videos[self.index]
            self.OnPlay()
        elif key == "Left":
            if self.index == 0:
                return

            self.OnPause()
            self.player.set_media(None)
            self.index -= 1
            self.video = self.videos[self.index]
            self.OnPlay()
        elif key == "d":
            t = self.player.get_time()
            self.player.set_time(int(t + 1e3))
        elif key == "a":
            t = self.player.get_time()
            self.player.set_time(int(t - 1e3))

    def OnClose(self, *unused):
        self.parent.quit()  # stops mainloop
        self.parent.destroy()  # this is necessary on Windows to avoid
        # ... Fatal Python Error: PyEval_RestoreThread: NULL tstate
    
    def _Pause_Play(self, playing):
        c = self.OnPlay if playing is None else self.OnPause
        self._stopped = False
    
    def _Play(self, video):
        # helper for OnOpen and OnPlay
        if isfile(video):  # Creation
            m = self.Instance.media_new(str(video))  # Path, unicode
            self.player.set_media(m)

            # set the window id where to render VLC's video output
            h = self.videopanel.winfo_id()  # .winfo_visualid()?
            self.player.set_hwnd(h)
            # FIXME: this should be made cross-platform
            self.OnPlay()

    def OnPause(self, *unused):
        """Toggle between Pause and Play.
        """
        if self.player.get_media():
            self._Pause_Play(not self.player.is_playing())
            self.player.pause()  # toggles

    def OnPlay(self, *unused):
        """Play video, if none is loaded, open the dialog window.
        """
        # if there's no video to play or playing,
        # open a Tk.FileDialog to select a file
        if not self.player.get_media():
            if self.video:
                self._Play(expanduser(self.video))
                self.video = ''
        # Try to play, if this fails display an error message
        elif self.player.play():  # == -1
            self.showError("Unable to play the video.")
        else:
            self._Pause_Play(True)

if __name__ == "__main__":

    folder = ''

    while len(sys.argv) > 1:
        arg = sys.argv.pop(1)
        folder = expanduser(arg)

    root = Tk.Tk()
    player = Player(root, folder)
    root.protocol("WM_DELETE_WINDOW", player.OnClose)
    root.mainloop()
