# VideoSlide

A very simple video player, with no UI whatsoever. Created in order to play sequence of videos created with [manim](https://github.com/ManimCommunity/manim) as a slideshow.
The code is a (shameless) adaptation of [this code](https://git.videolan.org/?p=vlc/bindings/python.git;a=blob;f=examples/tkvlc.py;h=9984138afa37132ad1279e55d66eb7b705e21b98;hb=HEAD).

# How to use

You have the following modules installed:
- python-vlc
- tkinter

To run it, put your videos in a folder and call the following command:
```bash
python play.py <folderName>
```

Once started, you can use to following keyboard commands:
| Key        | Action           |
| ------------- |:-------------:|
| Space      | Pause |
| Escape| Quit |
| f | Toggle Fullscreen |
| Right | Play Next Video |
| Left | Play Previous Video |
| d | Go 1 second forward |
| a | Go 1 second back |
