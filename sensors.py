import psutil
import time
import subprocess
import platform
from collections import deque

def isi_bilgisi_al(tema):
    mimari = platform.machine()
    if mimari == 'arm64':
        try:
            ciktisi = subprocess.check_output(['sudo', '-n', 'powermetrics', '--samplers', 'smc', '-n', '1'], stderr=subprocess.DEVNULL).decode('utf-8')
            for satir in ciktisi.split('\n'):
                if 'CPU die temperature' in satir:
                    derece = float(satir.split(':')[1].replace('C', '').strip())
                    renk = tema["ALARM"] if derece > 80 else "bold yellow" if derece > 65 else tema["ANA"]
                    return f"[{renk}]{derece:.1f}°C[/{renk}]"
            return f"[{tema['SILIK']}]N/A[/{tema['SILIK']}]"
        except subprocess.CalledProcessError:
            return f"[{tema['SILIK']}]SUDO REQ.[/{tema['SILIK']}]"
        except Exception:
            return f"[{tema['SILIK']}]LOCKED[/{tema['SILIK']}]"
    try:
        isi = subprocess.check_output(['osx-cpu-temp'], stderr=subprocess.DEVNULL).decode('utf-8').strip()
        derece = float(isi.replace('°C', '').strip())
        renk = tema["ALARM"] if derece > 80 else "bold yellow" if derece > 65 else tema["ANA"]
        return f"[{renk}]{isi}[/{renk}]"
    except FileNotFoundError:
        return f"[{tema['SILIK']}]TOOL MISSING[/{tema['SILIK']}]"
    except Exception:
        return f"[{tema['SILIK']}]N/A[/{tema['SILIK']}]"

def muzik_bilgisi_al(tema):
    try:
        spotify_script = 'tell application "System Events" to if exists process "Spotify" then tell application "Spotify" to if player state is playing then return artist of current track & " - " & name of current track'
        sonuc = subprocess.check_output(['osascript', '-e', spotify_script], stderr=subprocess.DEVNULL).decode('utf-8').strip()
        if sonuc and sonuc != "false": 
            return f"[{tema['ANA']}]🎵 AUDIO.STREAM: {sonuc}[/{tema['ANA']}]"
        music_script = 'tell application "System Events" to if exists process "Music" then tell application "Music" to if player state is playing then return artist of current track & " - " & name of current track'
        sonuc = subprocess.check_output(['osascript', '-e', music_script], stderr=subprocess.DEVNULL).decode('utf-8').strip()
        if sonuc and sonuc != "false":
            return f"[{tema['ANA']}]🎵 AUDIO.STREAM: {sonuc}[/{tema['ANA']}]"
    except Exception:
        pass
    return f"[{tema['SILIK']}]🎵 AUDIO.STREAM: OFFLINE[/{tema['SILIK']}]"

def batarya_bilgisi_al(tema):
    try:
        pil = psutil.sensors_battery()
        if not pil:
            return "🔌 AC POWER (DESKTOP)", "CYCLE: N/A", "100%", tema["ANA"]
        yuzde = pil.percent
        prizde_mi = pil.power_plugged
        durum_metni = "🔌 AC POWER" if prizde_mi else "🔋 BATT"
        renk = tema["ALARM"] if yuzde < 20 and not prizde_mi else tema["ANA"]
        try:
            devir_ciktisi = subprocess.check_output("ioreg -r -c AppleSmartBattery | grep '\"CycleCount\" =' | awk '{print $3}'", shell=True, stderr=subprocess.DEVNULL).decode('utf-8').strip()
            devir_bilgisi = f"CYCLE: {devir_ciktisi}" if devir_ciktisi else "CYCLE: N/A"
        except Exception:
            devir_bilgisi = "CYCLE: ERR"
        return durum_metni, devir_bilgisi, f"%{yuzde:.0f}", renk
    except Exception:
        return "ERR", "", "", tema["SILIK"]
    
def ping_bilgisi_al(tema):
    try:
        ciktisi = subprocess.check_output(
            ['ping', '-c', '1', '1.1.1.1'], 
            stderr=subprocess.DEVNULL, 
            timeout=0.8
        ).decode('utf-8')
        
        if 'time=' in ciktisi:
            zaman_str = ciktisi.split('time=')[1].split(' ms')[0]
            gecikme = float(zaman_str)
            
            # Gecikmeye göre renk ve durum tespiti
            renk = tema["ANA"] if gecikme < 30 else "bold yellow" if gecikme < 80 else tema["ALARM"]
            durum = "STABLE" if gecikme < 30 else "WARN" if gecikme < 80 else "CRITICAL"
            
            return f"[{renk}]{gecikme:.1f}ms[/{renk}]", f"[{renk}]{durum}[/{renk}]"
    except Exception:
        pass
        
    # İnternet koptuysa veya cevap yoksa:
    return f"[{tema['ALARM']}]ERR[/{tema['ALARM']}]", f"[{tema['ALARM']}]OFFLINE[/{tema['ALARM']}]"    

class SistemDurumu:
    def __init__(self):
        self.cpu_gecmis = deque([0] * 15, maxlen=15)
        self.ram_gecmis = deque([0] * 15, maxlen=15)
        self.son_ag = psutil.net_io_counters()
        self.son_disk = psutil.disk_io_counters()
        self.son_zaman = time.time()
        self.ag_indirme_hizi = 0
        self.ag_yukleme_hizi = 0
        self.disk_okuma_hizi = 0
        self.disk_yazma_hizi = 0

    def guncelle(self):
        su_an = time.time()
        gecen_sure = su_an - self.son_zaman
        if gecen_sure <= 0: gecen_sure = 0.001 
        suanki_ag = psutil.net_io_counters()
        suanki_disk = psutil.disk_io_counters()
        if suanki_ag and self.son_ag:
            self.ag_indirme_hizi = (suanki_ag.bytes_recv - self.son_ag.bytes_recv) / gecen_sure
            self.ag_yukleme_hizi = (suanki_ag.bytes_sent - self.son_ag.bytes_sent) / gecen_sure
        if suanki_disk and self.son_disk:
            self.disk_okuma_hizi = (suanki_disk.read_bytes - self.son_disk.read_bytes) / gecen_sure
            self.disk_yazma_hizi = (suanki_disk.write_bytes - self.son_disk.write_bytes) / gecen_sure
        self.son_ag = suanki_ag
        self.son_disk = suanki_disk
        self.son_zaman = su_an
        self.cpu_gecmis.append(psutil.cpu_percent())
        
        if platform.system() == 'Darwin':
            try:
                vm_stat = subprocess.check_output(['vm_stat']).decode('utf-8')
                lines = vm_stat.split('\n')
                pages = {}
                for line in lines:
                    if ':' in line:
                        key, val = line.split(':')
                        pages[key.strip()] = int(val.strip().replace('.', ''))
                wired = pages.get('Pages wired down', 0)
                active = pages.get('Pages active', 0)
                compressed = pages.get('Pages occupied by compressor', 0)
                free = pages.get('Pages free', 0)
                inactive = pages.get('Pages inactive', 0)
                kullanilan_sayfalar = wired + active + compressed
                toplam_sayfalar = kullanilan_sayfalar + free + inactive
                ram_yuzdesi = (kullanilan_sayfalar / toplam_sayfalar) * 100 if toplam_sayfalar > 0 else 0
            except Exception:
                ram_yuzdesi = psutil.virtual_memory().percent
        else:
            ram_yuzdesi = psutil.virtual_memory().percent
            
        self.ram_gecmis.append(ram_yuzdesi)