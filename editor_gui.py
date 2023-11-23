#!/usr/bin/env python3
#Created by: Ioannes Cruxibulum
#Date Created: 11-23-23

import os
import gi
import time
import subprocess
from moviepy.editor import AudioFileClip, VideoFileClip
from moviepy.audio.fx.all import volumex
from moviepy.editor import concatenate_videoclips
from moviepy.editor import concatenate_audioclips
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GLib

class FileChooserWindow_Stitch_Audio(Gtk.Window):
    def __init__(self, treeview_window):
        Gtk.Window.__init__(self, title="Stitch Audio")
        self.set_default_size(400, 200)

        #This is to destroy the treeview when x is pressed.
        self.treeview_window = treeview_window
        # Connect the delete-event signal to the on_delete_event function
        self.connect("delete-event", self.on_delete_event)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(box)

        button1 = Gtk.Button(label="Choose First Audio")
        button1.connect("clicked", self.on_file_clicked, os.path.expanduser('~/Music'))
        box.add(button1)

        button2 = Gtk.Button(label="Choose Second Audio")
        button2.connect("clicked", self.on_file_clicked, os.path.expanduser('~/Music'))
        box.add(button2)

        self.entry = Gtk.Entry()
        self.entry.set_text("output.mp3")
        box.add(self.entry)

        self.button3 = Gtk.Button(label="Stitch Audios")
        self.button3.connect("clicked", self.on_stitch_clicked)
        box.add(self.button3)
        self.button3.set_sensitive(False)

        self.label = Gtk.Label()
        box.add(self.label)

        self.audio_files = []

    def on_delete_event(self, widget, event):
        # Destroy the FileChooserWindow
        self.destroy()
        GLib.timeout_add_seconds(1, self.destroy)  # 5 seconds delay
        # Make the treeview window visible
        #self.treeview_window.destroy()
        self.treeview_window.show_all()
        # Return False to propagate the event further (this is needed for the window to actually close)
        return False

    def on_file_clicked(self, widget, path):
        dialog = Gtk.FileChooserDialog(
            title="Please choose a file", parent=self,
            action=Gtk.FileChooserAction.OPEN
        )
        dialog.set_current_folder(path)
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK
        )

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.audio_files.append(dialog.get_filename())
            if len(self.audio_files) == 2:
                self.button3.set_sensitive(True)

        dialog.destroy()

    def on_stitch_clicked(self, widget):
        output_filename = self.entry.get_text()
        if not output_filename.endswith('.mp3'):
            self.label.set_text("Filename must end with .mp3")
            return

        try:
            clips = [AudioFileClip(f) for f in self.audio_files]
            final_clip = concatenate_audioclips(clips)
            os.chdir(os.path.expanduser('~/Desktop'))
            final_clip.write_audiofile(output_filename)

            self.audio_files = []
            self.button3.set_sensitive(False)
            self.label.set_text("Audio stitching completed successfully!")
            GLib.timeout_add_seconds(1, self.destroy)  # 5 seconds delay
            # Make the treeview window visible
            #self.treeview_window.destroy()
            self.treeview_window.show_all()
        except Exception as e:
            self.label.set_text(str(e))

class FileChooserWindow_Stitch_Vid(Gtk.Window):

    def __init__(self, treeview_window):
        Gtk.Window.__init__(self, title="Stitch Videos")
        self.set_default_size(400, 200)

        #This is to destroy the treeview when x is pressed.
        self.treeview_window = treeview_window
        # Connect the delete-event signal to the on_delete_event function
        self.connect("delete-event", self.on_delete_event)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(box)

        button1 = Gtk.Button(label="Choose First Video")
        button1.connect("clicked", self.on_file_clicked, os.path.expanduser('~/Videos'))
        box.add(button1)

        button2 = Gtk.Button(label="Choose Second Video")
        button2.connect("clicked", self.on_file_clicked, os.path.expanduser('~/Videos'))
        box.add(button2)

        self.entry = Gtk.Entry()
        self.entry.set_text("output.mp4")
        box.add(self.entry)

        self.button3 = Gtk.Button(label="Stitch Videos")
        self.button3.connect("clicked", self.on_stitch_clicked)
        box.add(self.button3)
        self.button3.set_sensitive(False)

        self.label = Gtk.Label()
        box.add(self.label)

        self.video_files = []

    def on_delete_event(self, widget, event):
        # Destroy the FileChooserWindow
        self.destroy()
        GLib.timeout_add_seconds(1, self.destroy)  # 5 seconds delay
        # Make the treeview window visible
        #self.treeview_window.destroy()
        self.treeview_window.show_all()
        # Return False to propagate the event further (this is needed for the window to actually close)
        return False

    def on_file_clicked(self, widget, path):
        dialog = Gtk.FileChooserDialog(
            title="Please choose a file", parent=self,
            action=Gtk.FileChooserAction.OPEN
        )
        dialog.set_current_folder(path)
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK
        )

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.video_files.append(dialog.get_filename())
            if len(self.video_files) == 2:
                self.button3.set_sensitive(True)

        dialog.destroy()

    def on_stitch_clicked(self, widget):
        output_filename = self.entry.get_text()
        if not output_filename.endswith('.mp4'):
            self.label.set_text("Filename must end with .mp4")
            return

        try:
            clips = [VideoFileClip(f) for f in self.video_files]
            final_clip = concatenate_videoclips(clips)
            os.chdir(os.path.expanduser('~/Desktop'))
            final_clip.write_videofile(output_filename)

            self.video_files = []
            self.button3.set_sensitive(False)
            self.label.set_text("Video stitching completed successfully!")
            GLib.timeout_add_seconds(1, self.destroy)  # 5 seconds delay
            # Make the treeview window visible
            #self.treeview_window.destroy()
            self.treeview_window.show_all()
        except Exception as e:
            self.label.set_text(str(e))

class FileChooserWindow_Adjust_Vol(Gtk.Window):
    def __init__(self, treeview_window):
        Gtk.Window.__init__(self, title="Adjust Volume")
        self.set_default_size(400, 200)

        #This is to destroy the treeview when x is pressed.
        self.treeview_window = treeview_window
        # Connect the delete-event signal to the on_delete_event function
        self.connect("delete-event", self.on_delete_event)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(box)

        button1 = Gtk.Button(label="Choose Audio")
        button1.connect("clicked", self.on_file_clicked, os.path.expanduser('~/Music'))
        box.add(button1)

        self.entry_filename = Gtk.Entry()
        self.entry_filename.set_text("output.mp3")
        box.add(self.entry_filename)

        self.entry_volume = Gtk.Entry()
        self.entry_volume.set_text("1.0")
        box.add(self.entry_volume)

        self.button2 = Gtk.Button(label="Adjust Volume")
        self.button2.connect("clicked", self.on_adjust_clicked)
        box.add(self.button2)
        self.button2.set_sensitive(False)

        self.label = Gtk.Label()
        box.add(self.label)

        self.audio_file = None

    def on_delete_event(self, widget, event):
        # Destroy the FileChooserWindow
        self.destroy()
        GLib.timeout_add_seconds(1, self.destroy)  # 5 seconds delay
        # Make the treeview window visible
        #self.treeview_window.destroy()
        self.treeview_window.show_all()
        # Return False to propagate the event further (this is needed for the window to actually close)
        return False

    def on_file_clicked(self, widget, path):
        dialog = Gtk.FileChooserDialog(
            title="Please choose a file", parent=self,
            action=Gtk.FileChooserAction.OPEN
        )
        dialog.set_current_folder(path)
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK
        )

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.audio_file = dialog.get_filename()
            self.button2.set_sensitive(True)

        dialog.destroy()

    def on_adjust_clicked(self, widget):
        output_filename = self.entry_filename.get_text()
        if not output_filename.endswith('.mp3'):
            self.label.set_text("Filename must end with .mp3")
            return

        try:
            volume_level = float(self.entry_volume.get_text())
        except ValueError:
            self.label.set_text("Volume level must be a number")
            return

        try:
            audio = AudioFileClip(self.audio_file)
            audio = audio.fx(volumex, volume_level)
            os.chdir(os.path.expanduser('~/Desktop'))
            audio.write_audiofile(output_filename)

            self.audio_file = None
            self.button2.set_sensitive(False)
            self.label.set_text("Volume adjustment completed successfully!")
            GLib.timeout_add_seconds(1, self.destroy)  # 5 seconds delay
            # Make the treeview window visible
            #self.treeview_window.destroy()
            self.treeview_window.show_all()
        except Exception as e:
            self.label.set_text(str(e))

class FileChooserWindow_Extract(Gtk.Window):
    def __init__(self, treeview_window):
        Gtk.Window.__init__(self, title="Extract Audio")
        self.set_default_size(400, 200)

        #This is to destroy the treeview when x is pressed.
        self.treeview_window = treeview_window
        # Connect the delete-event signal to the on_delete_event function
        self.connect("delete-event", self.on_delete_event)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(box)

        button1 = Gtk.Button(label="Choose Video")
        button1.connect("clicked", self.on_file_clicked, os.path.expanduser('~/Videos'))
        box.add(button1)

        self.entry = Gtk.Entry()
        self.entry.set_text("output.mp3")
        box.add(self.entry)

        self.button2 = Gtk.Button(label="Extract Audio")
        self.button2.connect("clicked", self.on_extract_clicked)
        box.add(self.button2)
        self.button2.set_sensitive(False)

        self.label = Gtk.Label()
        box.add(self.label)

        self.video_file = None

    def on_delete_event(self, widget, event):
        # Destroy the FileChooserWindow
        self.destroy()
        GLib.timeout_add_seconds(1, self.destroy)  # 5 seconds delay
        # Make the treeview window visible
        #self.treeview_window.destroy()
        self.treeview_window.show_all()
        # Return False to propagate the event further (this is needed for the window to actually close)
        return False

    def on_file_clicked(self, widget, path):
        dialog = Gtk.FileChooserDialog(
            title="Please choose a file", parent=self,
            action=Gtk.FileChooserAction.OPEN
        )
        dialog.set_current_folder(path)
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK
        )

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.video_file = dialog.get_filename()
            self.button2.set_sensitive(True)

        dialog.destroy()

    def on_extract_clicked(self, widget):
        output_filename = self.entry.get_text()
        if not output_filename.endswith('.mp3'):
            self.label.set_text("Filename must end with .mp3")
            return

        try:
            video = VideoFileClip(self.video_file)
            audio = video.audio
            os.chdir(os.path.expanduser('~/Desktop'))
            audio.write_audiofile(output_filename)

            self.video_file = None
            self.button2.set_sensitive(False)
            self.label.set_text("Audio extraction completed successfully!")
            GLib.timeout_add_seconds(1, self.destroy)  # 5 seconds delay
            # Make the treeview window visible
            #self.treeview_window.destroy()
            self.treeview_window.show_all()
        except Exception as e:
            self.label.set_text(str(e))

class FileChooserWindow_Merge(Gtk.Window):
    def __init__(self, treeview_window):
        Gtk.Window.__init__(self, title="Merge Audio/Video")
        self.set_default_size(400, 200)

        #This is to destroy the treeview when x is pressed.
        self.treeview_window = treeview_window
        # Connect the delete-event signal to the on_delete_event function
        self.connect("delete-event", self.on_delete_event)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(box)

        button1 = Gtk.Button(label="Choose Video")
        button1.connect("clicked", self.on_file_clicked, os.path.expanduser('~/Videos'))
        box.add(button1)

        button2 = Gtk.Button(label="Choose Audio")
        button2.connect("clicked", self.on_file_clicked, os.path.expanduser('~/Music'))
        box.add(button2)

        self.entry = Gtk.Entry()
        self.entry.set_text("output.mp4")
        box.add(self.entry)

        self.button3 = Gtk.Button(label="Merge Audio and Video")
        self.button3.connect("clicked", self.on_merge_clicked)
        box.add(self.button3)
        self.button3.set_sensitive(False)

        self.label = Gtk.Label()
        box.add(self.label)

        self.video_file = None
        self.audio_file = None

    def on_delete_event(self, widget, event):
        # Destroy the FileChooserWindow
        self.destroy()
        GLib.timeout_add_seconds(1, self.destroy)  # 5 seconds delay
        # Make the treeview window visible
        #self.treeview_window.destroy()
        self.treeview_window.show_all()
        # Return False to propagate the event further (this is needed for the window to actually close)
        return False

    def on_file_clicked(self, widget, path):
        dialog = Gtk.FileChooserDialog(
            title="Please choose a file", parent=self,
            action=Gtk.FileChooserAction.OPEN
        )
        dialog.set_current_folder(path)
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK
        )

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            if widget.get_label() == 'Choose Video':
                self.video_file = dialog.get_filename()
            else:
                self.audio_file = dialog.get_filename()

            if self.video_file and self.audio_file:
                self.button3.set_sensitive(True)

        dialog.destroy()

    def on_merge_clicked(self, widget):
        try:
            video = VideoFileClip(self.video_file)
            audio = AudioFileClip(self.audio_file)
            final_clip = video.set_audio(audio)
            output_filename = self.entry.get_text()
            if not output_filename.endswith('.mp4'):
                output_filename += '.mp4'
            os.chdir(os.path.expanduser('~/Desktop'))
            final_clip.write_videofile(output_filename)

            self.video_file = None
            self.audio_file = None
            self.button3.set_sensitive(False)
            self.label.set_text("Merge completed successfully!")
            GLib.timeout_add_seconds(1, self.destroy)  # 5 seconds delay
            # Make the treeview window visible
            #self.treeview_window.destroy()
            self.treeview_window.show_all()
        except Exception as e:
            self.label.set_text(str(e))

class FileChooserWindow_Audio(Gtk.Window):
    def __init__(self, treeview_window):
        Gtk.Window.__init__(self, title="Cut Audio")
        # Create a FileChooserDialog
        self.dialog = Gtk.FileChooserDialog(
            title="Please choose a file", parent=self,
            action=Gtk.FileChooserAction.OPEN
        )

        #This is to destroy the treeview when x is pressed.
        self.treeview_window = treeview_window
        # Connect the delete-event signal to the on_delete_event function
        self.connect("delete-event", self.on_delete_event)
        
        self.set_default_size(375, 275)
        box = Gtk.Box(spacing=6)
        box.set_border_width(10)  # Creates a 10-pixel buffer around the box
        fixed = Gtk.Fixed()
        self.add(fixed)

        button1 = Gtk.Button(label="Choose File")
        button1.set_size_request(40, 20)  # Set the width to 20 and the height to 20
        button1.connect("clicked", self.on_file_clicked)
        fixed.put(button1, 10, 50)  # Position the button at (10,10) instead of (0,0)

        # Add another button
        button2 = Gtk.Button(label="Cut Audio")
        button2.set_size_request(60, 20)  # Set the width to 20 and the height to 20
        button2.connect("clicked", self.on_button2_clicked)
        fixed.put(button2, 10, 90)  # Position the button at (40,10)

        # Add a textbox for start time
        self.start_time_textbox = Gtk.Entry()
        self.start_time_textbox.set_text("start time")  # Set the initial text
        self.start_time_textbox.set_size_request(200, 20)  # Set the width to 200 and the height to 20
        fixed.put(self.start_time_textbox, 150, 50)  # Position the textbox at (150,50)

        # Add a textbox for end time
        self.end_time_textbox = Gtk.Entry()
        self.end_time_textbox.set_text("end time")  # Set the initial text
        self.end_time_textbox.set_size_request(200, 20)  # Set the width to 200 and the height to 20
        fixed.put(self.end_time_textbox, 150, 90)  # Position the textbox at (150,80)
        self.treeview_window = treeview_window

        # Add a textbox for filename
        self.filename_textbox = Gtk.Entry()
        self.filename_textbox.set_text("filename.mp3")  # Set the initial text
        self.filename_textbox.set_size_request(200, 20)  # Set the width to 200 and the height to 20
        fixed.put(self.filename_textbox, 150, 130)  # Position the textbox at (150,130)

        #create the label
        self.label = Gtk.Label(label="Please choose a file, a start time,\n          end time and filename")
        fixed.put(self.label, 70, 200)

    def on_delete_event(self, widget, event):
        # Destroy the FileChooserWindow
        self.destroy()
        GLib.timeout_add_seconds(1, self.destroy)  # 5 seconds delay
        # Make the treeview window visible
        #self.treeview_window.destroy()
        self.treeview_window.show_all()
        # Return False to propagate the event further (this is needed for the window to actually close)
        return False

    def on_file_clicked(self, widget):
        self.dialog = Gtk.FileChooserDialog(
            title="Please choose a file", parent=self,
            action=Gtk.FileChooserAction.OPEN
        )
        self.dialog.set_current_folder(os.path.expanduser('~/Music'))
        self.dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK,
        )

        filter_mp4 = Gtk.FileFilter()
        filter_mp4.set_name("MP3 files")
        filter_mp4.add_mime_type("audio/mpeg")
        self.dialog.add_filter(filter_mp4)

        response = self.dialog.run()
        #if response == Gtk.ResponseType.OK:
            #print("You selected %s" % self.dialog.get_filename())
            # Here you can add your video cutting function

        self.dialog.hide()

    def on_button2_clicked(self, widget):
        try:
            start_time_str = self.start_time_textbox.get_text()  # Get the text from the start time textbox
            end_time_str = self.end_time_textbox.get_text()  # Get the text from the end time textbox
            start_time = int(start_time_str)  # Try to convert the start time to an integer
            end_time = int(end_time_str)  # Try to convert the end time to an integer
            filename_str = self.filename_textbox.get_text()  # Get the text from the filename textbox
            if not filename_str.endswith('.mp3'):
                self.label.set_text("The filename must end with .mp3")
                return
            # Here you can add your video cutting function
            filename = self.dialog.get_filename()
            if self.dialog is None:
                self.label.set_text("Please select a file first.")
                return
            if filename is not None:
                self.label.set_text("The user entered the start time: %d\n            and end time: %d" % (start_time, end_time))
                clip = AudioFileClip(filename).subclip(start_time, end_time)
                os.chdir(os.path.expanduser('~/Desktop'))
                clip.write_audiofile(filename_str)
                GLib.timeout_add_seconds(1, self.destroy)  # 5 seconds delay
                # Make the treeview window visible
                #self.treeview_window.destroy()
                self.treeview_window.show_all()
            else:
                self.label.set_text("No file was selected.")
        except ValueError:
            self.label.set_text("The user must enter a valid integer")

class DownloaderWindow(Gtk.Window):
    def __init__(self, treeview_window):
        Gtk.Window.__init__(self, title="YouTube Downloader")
        # This is to destroy the treeview when x is pressed.
        self.treeview_window = treeview_window
        # Connect the delete-event signal to the on_delete_event function
        self.connect("delete-event", self.on_delete_event)
        self.set_border_width(10)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self.url_entry = Gtk.Entry()
        self.url_entry.set_text("Enter YouTube URL here")
        vbox.pack_start(self.url_entry, True, True, 0)

        self.button = Gtk.Button(label="Fetch Formats")
        self.button.connect("clicked", self.on_button_clicked)
        vbox.pack_start(self.button, True, True, 0)

        self.label = Gtk.Label()
        vbox.pack_start(self.label, True, True, 0)

        self.format_entry = Gtk.Entry()
        self.format_entry.set_text("Enter format code here")
        vbox.pack_start(self.format_entry, True, True, 0)

        self.download_button = Gtk.Button(label="Download")
        self.download_button.connect("clicked", self.on_download_button_clicked)
        vbox.pack_start(self.download_button, True, True, 0)
    
    # This is to destroy the treeview when x is pressed.
    def on_delete_event(self, widget, event):
        # Destroy the Downloader Window
        self.destroy()
        GLib.timeout_add_seconds(1, self.destroy)  # 5 seconds delay
        # Make the treeview window visible
        #self.treeview_window.destroy()
        self.treeview_window.show_all()
        # Return False to propagate the event further (this is needed for the window to actually close)
        return False

    def on_button_clicked(self, widget):
        url = self.url_entry.get_text()
        self.update_formats(url)

    def on_download_button_clicked(self, widget):
        url = self.url_entry.get_text()
        format_code = self.format_entry.get_text()
        os.chdir(os.path.expanduser('~/Desktop'))
        subprocess.run(["yt-dlp", "-f", format_code, url])
        GLib.timeout_add_seconds(1, self.destroy)  # 5 seconds delay
        # Make the treeview window visible
        #self.treeview_window.destroy()
        self.treeview_window.show_all()

    def update_formats(self, url):
        result = subprocess.run(["yt-dlp", "-F", url], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        formats = [line for line in lines if ("mp4" in line)]
        self.label.set_text('\n'.join(formats))

class FileChooserWindow(Gtk.Window):
    def __init__(self, treeview_window):
        Gtk.Window.__init__(self, title="Cut Video")
        # Create a FileChooserDialog
        self.dialog = Gtk.FileChooserDialog(
            title="Please choose a file", parent=self,
            action=Gtk.FileChooserAction.OPEN
        )

        #This is to destroy the treeview when x is pressed.
        self.treeview_window = treeview_window
        # Connect the delete-event signal to the on_delete_event function
        self.connect("delete-event", self.on_delete_event)
        
        self.set_default_size(375, 275)
        box = Gtk.Box(spacing=6)
        box.set_border_width(10)  # Creates a 10-pixel buffer around the box
        fixed = Gtk.Fixed()
        self.add(fixed)

        button1 = Gtk.Button(label="Choose File")
        button1.set_size_request(40, 20)  # Set the width to 20 and the height to 20
        button1.connect("clicked", self.on_file_clicked)
        fixed.put(button1, 10, 50)  # Position the button at (10,10) instead of (0,0)

        # Add another button
        button2 = Gtk.Button(label="Cut Video")
        button2.set_size_request(60, 20)  # Set the width to 20 and the height to 20
        button2.connect("clicked", self.on_button2_clicked)
        fixed.put(button2, 10, 90)  # Position the button at (40,10)

        # Add a textbox for start time
        self.start_time_textbox = Gtk.Entry()
        self.start_time_textbox.set_text("start time")  # Set the initial text
        self.start_time_textbox.set_size_request(200, 20)  # Set the width to 200 and the height to 20
        fixed.put(self.start_time_textbox, 150, 50)  # Position the textbox at (150,50)

        # Add a textbox for end time
        self.end_time_textbox = Gtk.Entry()
        self.end_time_textbox.set_text("end time")  # Set the initial text
        self.end_time_textbox.set_size_request(200, 20)  # Set the width to 200 and the height to 20
        fixed.put(self.end_time_textbox, 150, 90)  # Position the textbox at (150,80)
        self.treeview_window = treeview_window

        # Add a textbox for filename
        self.filename_textbox = Gtk.Entry()
        self.filename_textbox.set_text("filename.mp4")  # Set the initial text
        self.filename_textbox.set_size_request(200, 20)  # Set the width to 200 and the height to 20
        fixed.put(self.filename_textbox, 150, 130)  # Position the textbox at (150,130)

        #create the label
        self.label = Gtk.Label(label="Please choose a file, a start time,\n          end time and filename")
        fixed.put(self.label, 70, 200)

    def on_delete_event(self, widget, event):
        # Destroy the FileChooserWindow
        self.destroy()
        GLib.timeout_add_seconds(1, self.destroy)  # 5 seconds delay
        # Make the treeview window visible
        #self.treeview_window.destroy()
        self.treeview_window.show_all()
        # Return False to propagate the event further (this is needed for the window to actually close)
        return False

    def on_file_clicked(self, widget):
        self.dialog = Gtk.FileChooserDialog(
            title="Please choose a file", parent=self,
            action=Gtk.FileChooserAction.OPEN
        )
        self.dialog.set_current_folder(os.path.expanduser('~/Videos'))
        self.dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK,
        )

        filter_mp4 = Gtk.FileFilter()
        filter_mp4.set_name("MP4 files")
        filter_mp4.add_mime_type("video/mp4")
        self.dialog.add_filter(filter_mp4)

        response = self.dialog.run()
        #if response == Gtk.ResponseType.OK:
            #print("You selected %s" % self.dialog.get_filename())
            # Here you can add your video cutting function

        self.dialog.hide()

    def on_button2_clicked(self, widget):
        try:
            start_time_str = self.start_time_textbox.get_text()  # Get the text from the start time textbox
            end_time_str = self.end_time_textbox.get_text()  # Get the text from the end time textbox
            start_time = int(start_time_str)  # Try to convert the start time to an integer
            end_time = int(end_time_str)  # Try to convert the end time to an integer
            filename_str = self.filename_textbox.get_text()  # Get the text from the filename textbox
            if not filename_str.endswith('.mp4'):
                self.label.set_text("The filename must end with .mp4")
                return
            # Here you can add your video cutting function
            filename = self.dialog.get_filename()
            if self.dialog is None:
                self.label.set_text("Please select a file first.")
                return
            if filename is not None:
                self.label.set_text("The user entered the start time: %d\n and end time: %d" % (start_time, end_time))
                clip = VideoFileClip(filename).subclip(start_time, end_time)
                os.chdir(os.path.expanduser('~/Desktop'))
                clip.write_videofile(filename_str)
                GLib.timeout_add_seconds(1, self.destroy)  # 5 seconds delay
                # Make the treeview window visible
                #self.treeview_window.destroy()
                self.treeview_window.show_all()
            else:
                self.label.set_text("No file was selected.")
        except ValueError:
            self.label.set_text("The user must enter a valid integer")

class TreeViewFilterWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Pyra Editor Function")

        # Set the window size here
        self.set_default_size(300, 300)

        # Setting up the self.grid in which the elements are to be positionned
        self.grid = Gtk.Grid()
        self.add(self.grid)

        # Creating the ListStore model
        self.func_liststore = Gtk.ListStore(str)
        for main_functions in ["YT Downloader", "Cut Video", "Cut Audio", "Merge Audio Video", "Extract Audio", "Adjust Volume", "Stitch Video", "Stitch Audio"]:
            self.func_liststore.append([main_functions])

        # Creating the treeview and adding the columns
        self.treeview = Gtk.TreeView.new_with_model(self.func_liststore)
        for i, column_title in enumerate(["Editing Functions"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)

        # Connect the row-activated signal to the on_row_activated function
        self.treeview.connect("row-activated", self.on_row_activated)

        # Setting up the layout, putting the treeview in a scrollwindow
        self.scrollable_treelist = Gtk.ScrolledWindow()
        # Makes the treeview expand the height of the window
        self.scrollable_treelist.set_vexpand(True)
        # Makes the treeview expand the width of the window
        self.scrollable_treelist.set_hexpand(True)
        self.grid.attach(self.scrollable_treelist, 0, 0, 8, 10)
        self.scrollable_treelist.add(self.treeview)

        self.show_all()

    def on_row_activated(self, treeview, path, column):
        # Get the selected fruit
        model = treeview.get_model()
        iter = model.get_iter(path)
        main_functions = model.get_value(iter, 0)

        # Perform an action based on the selected fruit
        if main_functions == "YT Downloader":
            self.yt_downloader_func()
        elif main_functions == "Cut Video":
            self.cut_vid_func()
        elif main_functions == "Cut Audio":
            self.cut_audio_func()
        elif main_functions == "Merge Audio Video":
            self.merge_av_func()
        elif main_functions == "Extract Audio":
            self.extract_audio_func()
        elif main_functions == "Adjust Volume":
            self.adjust_vol_func()
        elif main_functions == "Stitch Video":
            self.stitch_video()
        elif main_functions == "Stitch Audio":
            self.stitch_audio()

    def yt_downloader_func(self):
        ytd_win = DownloaderWindow(self)
        ytd_win.show_all()
        self.hide()

    def cut_vid_func(self):
        # Create a new instance of FileChooserWindow
        file_chooser = FileChooserWindow(self)
        # Show the file chooser window
        file_chooser.show_all()
        self.hide()

    def cut_audio_func(self):
        # Create a new instance of FileChooserWindow
        file_chooser_audio = FileChooserWindow_Audio(self)
        # Show the file chooser window
        file_chooser_audio.show_all()
        self.hide()
    def merge_av_func(self):
        # Create a new instance of FileChooserWindow
        file_chooser = FileChooserWindow_Merge(self)
        # Show the file chooser window
        file_chooser.show_all()
        self.hide()
    def extract_audio_func(self):
        # Create a new instance of FileChooserWindow
        file_chooser = FileChooserWindow_Extract(self)
        # Show the file chooser window
        file_chooser.show_all()
        self.hide()
    def adjust_vol_func(self):
        # Create a new instance of FileChooserWindow
        file_chooser = FileChooserWindow_Adjust_Vol(self)
        # Show the file chooser window
        file_chooser.show_all()
        self.hide()
    def stitch_video(self):
        # Create a new instance of FileChooserWindow
        file_chooser = FileChooserWindow_Stitch_Vid(self)
        # Show the file chooser window
        file_chooser.show_all()
        self.hide()
    def stitch_audio(self):
        # Create a new instance of FileChooserWindow
        file_chooser = FileChooserWindow_Stitch_Audio(self)
        # Show the file chooser window
        file_chooser.show_all()
        self.hide()

win = TreeViewFilterWindow()
win.connect("destroy", Gtk.main_quit)
Gtk.main()
