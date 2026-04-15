import sys
import time
from rich.live import Live
from rich.console import Console

from themes import TEMALAR
from sensors import SistemDurumu
from ui import ekran_olustur, tema_secim_menusu

console = Console()

def ana_motor():
    secilen_tema = None
    
    if len(sys.argv) > 1:
        istenen = sys.argv[1].lower()
        if istenen in TEMALAR:
            secilen_tema = istenen
        elif istenen == "matrix":
            secilen_tema = "matrix"
            
    if secilen_tema is None:
        secilen_tema = tema_secim_menusu()

    aktif_tema = TEMALAR[secilen_tema]
    durum_yoneticisi = SistemDurumu()
    
    console.clear()
    try:
        with Live(ekran_olustur(durum_yoneticisi, aktif_tema), refresh_per_second=1) as live:
            while True:
                time.sleep(1)
                live.update(ekran_olustur(durum_yoneticisi, aktif_tema))
    except KeyboardInterrupt:
        console.print(f"\n[{aktif_tema['ANA']}]DISCONNECTED.[/{aktif_tema['ANA']}]")

if __name__ == '__main__':
    ana_motor()