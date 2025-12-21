import os
import threading
import subprocess
import gui
import wx
import ui
import api
import globalPluginHandler

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

    def run_download(self, url, format_type):
        # Dosya yollarını ayarla
        addon_dir = os.path.dirname(os.path.dirname(__file__))
        lib_path = os.path.join(addon_dir, "lib")
        ytdlp_exe = os.path.join(lib_path, "yt-dlp.exe")
        ffmpeg_exe = os.path.join(lib_path, "ffmpeg.exe")
        
        # İndirilecek yer: İndirilenler klasörü
        download_path = os.path.join(os.path.expandvars("%USERPROFILE%"), "Downloads")
        output_template = os.path.join(download_path, "%(title)s.%(ext)s")
        
        # Ana komut
        cmd = [ytdlp_exe, "-o", output_template, "--no-mtime", "--ffmpeg-location", lib_path, url]
        
        # Formata göre ek parametreler
        if format_type == "mp3":
            cmd.extend(["--extract-audio", "--audio-format", "mp3"])
        else:
            cmd.extend(["-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"])

        try:
            # Siyah pencereyi göstererek işlemi başlat (0x00000010 pencereyi odağa alır)
            process = subprocess.Popen(cmd, creationflags=0x00000010)
            process.wait()
            
            if process.returncode == 0:
                wx.CallAfter(ui.message, "IndirTube: İndirme başarıyla tamamlandı!")
            else:
                wx.CallAfter(ui.message, "IndirTube: İndirme sırasında bir sorun oluştu.")
        except Exception as e:
            wx.CallAfter(ui.message, "IndirTube: Sistem hatası.")

    def script_indirTubeStart(self, gesture):
        # Panodaki linki al
        try:
            url = api.getClipData().strip()
        except:
            ui.message("Pano okunamadı.")
            return

        if "youtu" not in url.lower():
            ui.message("Lütfen geçerli bir YouTube linki kopyalayın.")
            return

        # Format seçme diyaloğu
        def show_dialog():
            dlg = wx.SingleChoiceDialog(
                gui.mainFrame, 
                f"Video bulundu. Hangi formatta indirilsin?", 
                "IndirTube - Volkan Özdemir", 
                ["MP3 (Ses)", "MP4 (Video)"]
            )
            
            if dlg.ShowModal() == wx.ID_OK:
                choice = dlg.GetSelection()
                fmt = "mp3" if choice == 0 else "mp4"
                ui.message("İşlem başlatıldı, lütfen bekleyin...")
                # İndirmeyi arka planda başlat (NVDA donmasın diye)
                threading.Thread(target=self.run_download, args=(url, fmt), daemon=True).start()
            dlg.Destroy()

        wx.CallAfter(show_dialog)

    # Kısayol Tuşu: NVDA + Shift + 1
    __gestures={"kb:nvda+shift+1": "indirTubeStart"}