#!/usr/bin/env python2
# Ubuntu 10 compatible

import gtk
import gobject
import subprocess
import os

DIR = os.path.dirname(os.path.abspath(__file__))
MEMORY = os.path.join(DIR, "memory.txt")
BRAIN = os.path.join(DIR, "brain.sh")
IMAGE = os.path.join(DIR, "dragon.png")

class Dragon:
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_decorated(False)
        self.window.set_keep_above(True)
        self.window.set_skip_taskbar_hint(True)
        self.window.set_skip_pager_hint(True)
        self.window.set_app_paintable(True)
        self.window.connect("destroy", gtk.main_quit)

        self.window.set_default_size(200, 200)

        self.image = gtk.Image()
        self.image.set_from_file(IMAGE)
        self.window.add(self.image)

        self.window.add_events(
            gtk.gdk.BUTTON_PRESS_MASK |
            gtk.gdk.BUTTON1_MOTION_MASK
        )

        self.window.connect("button-press-event", self.on_click)
        self.window.connect("motion-notify-event", self.on_drag)

        self.drag_x = 0
        self.drag_y = 0

        self.window.show_all()

    def on_drag(self, widget, event):
        if event.state & gtk.gdk.BUTTON1_MASK:
            self.window.move(
                int(event.x_root - self.drag_x),
                int(event.y_root - self.drag_y)
            )

    def on_click(self, widget, event):
        if event.button == 1:
            self.drag_x = event.x
            self.drag_y = event.y
        elif event.button == 3:
            self.popup_menu(event)

    def popup_menu(self, event):
        menu = gtk.Menu()

        talk = gtk.MenuItem("Speak")
        talk.connect("activate", self.speak)
        menu.append(talk)

        memory = gtk.MenuItem("Memory")
        memory.connect("activate", self.show_memory)
        menu.append(memory)

        quit = gtk.MenuItem("Dismiss Dragon")
        quit.connect("activate", lambda x: gtk.main_quit())
        menu.append(quit)

        menu.show_all()
        menu.popup(None, None, None, event.button, event.time)

    def speak(self, widget):
        dialog = gtk.Dialog(
            "Dragon",
            self.window,
            gtk.DIALOG_MODAL,
            (gtk.STOCK_OK, gtk.RESPONSE_OK)
        )

        entry = gtk.Entry()
        dialog.vbox.pack_start(entry)
        entry.show()

        response = dialog.run()
        text = entry.get_text()
        dialog.destroy()

        if text:
            with open(MEMORY, "a") as f:
                f.write("User: " + text + "\n")

            reply = subprocess.check_output([BRAIN, text])
            self.say(reply)

    def say(self, text):
        with open(MEMORY, "a") as f:
            f.write("Blaze: " + text + "\n")

        subprocess.Popen(["espeak", text])

        md = gtk.MessageDialog(
            self.window,
            gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.MESSAGE_INFO,
            gtk.BUTTONS_OK,
            text
        )
        md.run()
        md.destroy()

    def show_memory(self, widget):
        md = gtk.MessageDialog(
            self.window,
            gtk.DIALOG_MODAL,
            gtk.MESSAGE_INFO,
            gtk.BUTTONS_OK,
            open(MEMORY).read()[-2000:]
        )
        md.run()
        md.destroy()

Dragon()
gtk.main()
