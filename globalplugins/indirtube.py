# -*- coding: utf-8 -*-
import os
import threading
import subprocess
import gui
import wx
import ui
import api
import globalPluginHandler
import scriptHandler
import webbrowser
import addonHandler

addonHandler.initTranslation()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super().__init__()

	def run_download(self, url, format_type):
		addon_dir = os.path.dirname(os.path.dirname(__file__))
		lib_path = os.path.join(addon_dir, "lib")
		ytdlp_exe = os.path.join(lib_path, "yt-dlp.exe")
		download_path = os.path.join(os.path.expandvars("%USERPROFILE%"), "Downloads")
		output_template = os.path.join(download_path, "%(title)s.%(ext)s")
		cmd = [ytdlp_exe, "-o", output_template, "--no-mtime", "--ffmpeg-location", lib_path, url]
		if format_type == "mp3":
			cmd.extend(["--extract-audio", "--audio-format", "mp3"])
		else:
			cmd.extend(["-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"])
		try:
			process = subprocess.Popen(cmd, creationflags=0x00000010)
			process.wait()
			if process.returncode == 0:
				wx.CallAfter(ui.message, _("indirTube: Download completed successfully!"))
			else:
				wx.CallAfter(ui.message, _("indirTube: An error occurred during download."))
		except Exception:
			wx.CallAfter(ui.message, _("indirTube: System error."))

	@scriptHandler.script(description=_("Starts indirTube download dialog"), category=_("indirTube"))
	def script_indirTubeStart(self, gesture):
		try:
			url = api.getClipData().strip()
		except:
			ui.message(_("Clipboard could not be read."))
			return
		if "youtu" not in url.lower():
			ui.message(_("Please copy a valid YouTube link."))
			return
		def show_dialog():
			choices = [_("MP3 (Audio)"), _("MP4 (Video)"), _("Donate (Support Developer)")]
			dlg = wx.SingleChoiceDialog(gui.mainFrame, _("Select format:"), _("indirTube v5.0 - Volkan Ozdemir Software Services"), choices)
			if dlg.ShowModal() == wx.ID_OK:
				choice = dlg.GetSelection()
				if choice == 0:
					ui.message(_("Starting, please wait..."))
					threading.Thread(target=self.run_download, args=(url, "mp3"), daemon=True).start()
				elif choice == 1:
					ui.message(_("Starting, please wait..."))
					threading.Thread(target=self.run_download, args=(url, "mp4"), daemon=True).start()
				elif choice == 2:
					webbrowser.open("https://www.paytr.com/link/N2IAQKm")
			dlg.Destroy()
		wx.CallAfter(show_dialog)