import time
import psutil
import sys
from rich.table import Table
from rich.panel import Panel
from rich.console import Console
from rich.layout import Layout
from rich import box
from rich.align import Align
from sensors import isi_bilgisi_al, muzik_bilgisi_al, batarya_bilgisi_al, ping_bilgisi_al

console = Console()
SPARK_KARAKTERLER = [" ", "▂", "▃", "▄", "▅", "▆", "▇", "█"]

def sparkline_uret(gecmis_veriler):
    grafik = ""
    for deger in gecmis_veriler:
        indeks = min(int((deger / 100) * 8), 7)
        grafik += SPARK_KARAKTERLER[indeks]
    return grafik

def hiz_formatla(bayt_hizi):
    if bayt_hizi < 1024:
        return f"{bayt_hizi:.1f} B/s"
    elif bayt_hizi < 1024 * 1024:
        return f"{bayt_hizi / 1024:.1f} KB/s"
    else:
        return f"{bayt_hizi / (1024 * 1024):.2f} MB/s"

def tema_secim_menusu():
    console.clear()
    
    # Başlık ve Alt Başlık 
    console.print(Panel(Align.center("[bold cyan]MATRIX SYSTEM BOOTLOADER[/bold cyan]\n[dim]Awaiting Protocol Selection...[/dim]"), border_style="cyan"))
    
    # Seçenekler (Açıklama yok, sadece saf protokol isimleri)
    console.print("\n[1] [bold spring_green1]SYS.PROTOCOL: MATRIX[/bold spring_green1]")
    console.print("[2] [bold purple]SYS.PROTOCOL: AMETHYST[/bold purple]")
    console.print("[Q] [bold red]TERMINATE_CONNECTION[/bold red]\n")

    while True:
        # Girdi bekleme ekranı
        secim = console.input("[bold white]INPUT (1/2/Q): [/bold white]").lower()
        
        if secim == '1':
            return "matrix"
        elif secim == '2':
            return "purple" # (Bu kelime ekranda görünmez, sadece motorun içindeki renk kodunu çağırır)
        elif secim == 'q':
            sys.exit()
        else:
            # Hata mesajı bile sistem dilinde
            console.print("[red]ERR: UNKNOWN COMMAND[/red]")

def ekran_olustur(durum, tema):
    durum.guncelle()
    cpu_suan = durum.cpu_gecmis[-1]
    ram_suan = durum.ram_gecmis[-1]
    cpu_renk = tema["ALARM"] if cpu_suan > 85 else tema["ANA"]
    ram_renk = tema["ALARM"] if ram_suan > 90 else tema["ANA"]

    sistem_tablosu = Table(show_header=False, expand=True, box=None)
    sistem_tablosu.add_column("COMPONENT", style=tema["ALT"])
    sistem_tablosu.add_column("GRAPH", style=tema["ANA"], width=15)
    sistem_tablosu.add_column("RATIO", justify="right")
    
    sistem_tablosu.add_row("CPU", f"[{cpu_renk}]{sparkline_uret(durum.cpu_gecmis)}[/{cpu_renk}]", f"[{cpu_renk}]{cpu_suan:.1f}%[/{cpu_renk}]")
    sistem_tablosu.add_row("", "", "") 
    sistem_tablosu.add_row("RAM", f"[{ram_renk}]{sparkline_uret(durum.ram_gecmis)}[/{ram_renk}]", f"[{ram_renk}]{ram_suan:.1f}%[/{ram_renk}]")
    sistem_tablosu.add_row("", "", "") 
    sistem_tablosu.add_row("TEMP", f"[{tema['SILIK']}]---------------[/{tema['SILIK']}]", isi_bilgisi_al(tema))

    io_tablosu = Table(show_header=True, expand=True, box=box.SIMPLE, header_style=tema["ANA"])
    io_tablosu.add_column("SENSOR", style=tema["ALT"])
    io_tablosu.add_column("RX / READ", style=tema["ANA"], justify="right")
    io_tablosu.add_column("TX / WRITE", style=tema["ANA"], justify="right")
    
    io_tablosu.add_row("NET", hiz_formatla(durum.ag_indirme_hizi), hiz_formatla(durum.ag_yukleme_hizi))
    io_tablosu.add_row("SSD", hiz_formatla(durum.disk_okuma_hizi), hiz_formatla(durum.disk_yazma_hizi))

    ping_ms, ping_durum = ping_bilgisi_al(tema)
    io_tablosu.add_row("PING", ping_durum, ping_ms)

    surecler_tablosu = Table(show_header=True, header_style=tema["ANA"], expand=True, box=box.MINIMAL)
    surecler_tablosu.add_column("PID", style=tema["SILIK"], width=8)
    surecler_tablosu.add_column("PROCESS NAME", style=tema["ALT"])
    surecler_tablosu.add_column("CPU %", justify="right", style=tema["ANA"])
    surecler_tablosu.add_column("MEM %", justify="right", style=tema["SILIK"])

    surecler = []
    for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            surecler.append((p.info, p.info['cpu_percent'] or 0.0))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    en_agir_surecler = sorted(surecler, key=lambda x: x[1], reverse=True)[:10]
    for p_info, cpu in en_agir_surecler:
        surecler_tablosu.add_row(str(p_info['pid']), str(p_info['name'])[:20], f"{cpu:.1f}%", f"{(p_info['memory_percent'] or 0.0):.1f}%")

    ust_kisim = Layout()
    ust_kisim.split_row(
        Panel(Align(sistem_tablosu, vertical="middle"), title=f"[{tema['ANA']}]SYS.PULSE[/{tema['ANA']}]", border_style=tema["ALT"], box=box.SQUARE, padding=(0, 2)),
        Panel(Align(io_tablosu, vertical="middle"), title=f"[{tema['ANA']}]SYS.IO_STREAM[/{tema['ANA']}]", border_style=tema["ALT"], box=box.SQUARE, padding=(0, 2))
    )
    
    ana_duzen = Layout()
    header = Align.center(f"[{tema['ANA']}]=== WAKE UP, NEO. SYSTEM UPTIME: {(time.time() - psutil.boot_time()) / 3600:.1f}H ===[/{tema['ANA']}]")
    
    footer_tablosu = Table(show_header=False, expand=True, box=None)
    footer_tablosu.add_column("Music", justify="left")  
    footer_tablosu.add_column("Battery", justify="right")   
    
    durum_metni, devir_bilgisi, yuzde_metni, pil_renk = batarya_bilgisi_al(tema)
    pil_durumu = f"[{pil_renk}]{durum_metni} {yuzde_metni}  |  {devir_bilgisi}[/{pil_renk}]"
    
    footer_tablosu.add_row(muzik_bilgisi_al(tema), pil_durumu)
    
    ana_duzen.split_column(
        Layout(header, size=2),
        Layout(ust_kisim, size=10),
        Layout(Panel(surecler_tablosu, title=f"[{tema['ANA']}]SYS.PROCESS_LIST[/{tema['ANA']}]", border_style=tema["ALT"], box=box.SQUARE)),
        Layout(footer_tablosu, size=2) 
    )
    
    return ana_duzen