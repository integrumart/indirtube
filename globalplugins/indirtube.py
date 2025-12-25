import os
import threading
import subprocess
import gui
import wx
import ui
import api
import globalPluginHandler
import webbrowser

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    scriptCategory = "İndirTube v3.0"

    def run_download(self, url, format_type):
        # Orijinal dosya yolları ve kütüphane mantığı
        addon_dir = os.path.dirname(os.path.dirname(__file__))
        lib_path = os.path.join(addon_dir, "lib")
        ytdlp_exe = os.path.join(lib_path, "yt-dlp.exe")
        
        # İndirilecek yer: İndirilenler klasörü
        download_path = os.path.join(os.path.expandvars("%USERPROFILE%"), "Downloads")
        output_template = os.path.join(download_path, "%(title)s.%(ext)s")
        
        # Orijinal komut yapısı
        cmd = [ytdlp_exe, "-o", output_template, "--no-mtime", "--ffmpeg-location", lib_path, url]
        
        if format_type == "mp3":
            cmd.extend(["--extract-audio", "--audio-format", "mp3"])
        else:
            cmd.extend(["-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"])

        try:
            # Siyah pencereyi odaklayan orijinal creationflags
            process = subprocess.Popen(cmd, creationflags=0x00000010)
            process.wait()
            
            if process.returncode == 0:
                wx.CallAfter(ui.message, "IndirTube: İndirme başarıyla tamamlandı! / Download completed!")
            else:
                wx.CallAfter(ui.message, "IndirTube: İndirme sırasında bir sorun oluştu. / Download error.")
        except Exception as e:
            wx.CallAfter(ui.message, "IndirTube: Sistem hatası. / System error.")

    def script_indirTubeStart(self, gesture):
        try:
            url = api.getClipData().strip()
        except:
            ui.message("Pano okunamadı. / Clipboard error.")
            return

        if "youtu" not in url.lower():
            ui.message("Lütfen geçerli bir YouTube linki kopyalayın. / Please copy a valid YouTube link.")
            return

        def show_dialog():
            # Format seçimine Bağış Linki eklendi
            choices = [
                "MP3 (Ses / Audio)", 
                "MP4 (Video)", 
                "Bağış Yap / Donate (Support Developer)"
            ]
            
            dlg = wx.SingleChoiceDialog(
                gui.mainFrame, 
                "Format seçiniz / Select format:", 
                "İndirTube v3.0 - Volkan Özdemir Yazılım", 
                choices
            )
            
            if dlg.ShowModal() == wx.ID_OK:
                choice = dlg.GetSelection()
                if choice == 0:
                    ui.message("İşlem başlatıldı, lütfen bekleyin... / Starting, please wait...")
                    threading.Thread(target=self.run_download, args=(url, "mp3"), daemon=True).start()
                elif choice == 1:
                    ui.message("İşlem başlatıldı, lütfen bekleyin... / Starting, please wait...")
                    threading.Thread(target=self.run_download, args=(url, "mp4"), daemon=True).start()
                elif choice == 2:
                    # İşte beklenen bağış linki yönlendirmesi
                    webbrowser.open("https://www.paytr.com/link/N2IAQKm")
            dlg.Destroy()

        wx.CallAfter(show_dialog)

    # Senin orijinal kısayolun: NVDA + Shift + 1
    __gestures={"kb:nvda+shift+1": "indirTubeStart"}