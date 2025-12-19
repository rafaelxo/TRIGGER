import ctypes
import time
import argparse
import os
import threading
import sys
try:
    import keyboard
except ImportError:
    print("⚠️  Módulo 'keyboard' não encontrado. Instalando...")
    os.system('pip install keyboard')
    import keyboard

try:
    import pyautogui
except ImportError:
    os.system('pip install pyautogui')
    import pyautogui

pyautogui.FAILSAFE = False

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

trigger_ativo = False

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

SM_CXSCREEN = 0
SM_CYSCREEN = 1
SRCCOPY = 0x00CC0020
BI_RGB = 0
INPUT_MOUSE = 0
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [
        ("biSize", ctypes.c_uint32),
        ("biWidth", ctypes.c_int32),
        ("biHeight", ctypes.c_int32),
        ("biPlanes", ctypes.c_uint16),
        ("biBitCount", ctypes.c_uint16),
        ("biCompression", ctypes.c_uint32),
        ("biSizeImage", ctypes.c_uint32),
        ("biXPelsPerMeter", ctypes.c_int32),
        ("biYPelsPerMeter", ctypes.c_int32),
        ("biClrUsed", ctypes.c_uint32),
        ("biClrImportant", ctypes.c_uint32),
    ]


class BITMAPINFO(ctypes.Structure):
    _fields_ = [("bmiHeader", BITMAPINFOHEADER), ("bmiColors", ctypes.c_uint32 * 3)]


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_uint32),
        ("dwFlags", ctypes.c_uint32),
        ("time", ctypes.c_uint32),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
    ]


class INPUT(ctypes.Structure):
    class _I(ctypes.Union):
        _fields_ = [("mi", MOUSEINPUT)]

    _anonymous_ = ("i",)
    _fields_ = [("type", ctypes.c_uint32), ("i", _I)]


def get_screen_size():
    w = user32.GetSystemMetrics(SM_CXSCREEN)
    h = user32.GetSystemMetrics(SM_CYSCREEN)
    return w, h


def get_cursor_pos():
    p = POINT()
    user32.GetCursorPos(ctypes.byref(p))
    return p.x, p.y


def click_left():
    pyautogui.click()


def capture_roi_to_buffer(x, y, roi):
    w, h = get_screen_size()
    half = roi // 2
    left = max(0, x - half)
    top = max(0, y - half)
    right = min(w, left + roi)
    bottom = min(h, top + roi)
    width = right - left
    height = bottom - top

    hdc_screen = user32.GetDC(0)
    hdc_mem = gdi32.CreateCompatibleDC(hdc_screen)
    hbm = gdi32.CreateCompatibleBitmap(hdc_screen, width, height)
    gdi32.SelectObject(hdc_mem, hbm)

    gdi32.BitBlt(hdc_mem, 0, 0, width, height, hdc_screen, left, top, SRCCOPY)

    bmi = BITMAPINFO()
    bmi.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
    bmi.bmiHeader.biWidth = width
    bmi.bmiHeader.biHeight = -height
    bmi.bmiHeader.biPlanes = 1
    bmi.bmiHeader.biBitCount = 32
    bmi.bmiHeader.biCompression = BI_RGB
    bmi.bmiHeader.biSizeImage = width * height * 4

    buf = ctypes.create_string_buffer(bmi.bmiHeader.biSizeImage)
    gdi32.GetDIBits(hdc_mem, hbm, 0, height, buf, ctypes.byref(bmi), 0)

    gdi32.DeleteObject(hbm)
    gdi32.DeleteDC(hdc_mem)
    user32.ReleaseDC(0, hdc_screen)

    return buf, width, height


def contains_yellow(buf, width, height, r_min, g_min, b_max):
    data = bytes(buf)
    for i in range(0, width * height * 4, 4):
        b = data[i]
        g = data[i + 1]
        r = data[i + 2]
        if r >= r_min and g >= g_min and b <= b_max:
            return True
    return False


def toggle_trigger():
    global trigger_ativo
    trigger_ativo = not trigger_ativo
    status = "🟢 ATIVADO" if trigger_ativo else "🔴 DESATIVADO"
    print(f"\n{status}")


def main():
    global trigger_ativo

    ap = argparse.ArgumentParser(
        description="� Trigger Bot - Detecta amarelo e clica automaticamente",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Exemplos de uso:
  python red_trigger_clicker.py              (modo normal - clica ao detectar)
  python red_trigger_clicker.py --teste      (modo teste - só detecta, não clica)
  python red_trigger_clicker.py --sensibilidade 180  (mais sensível ao amarelo)
  python red_trigger_clicker.py --tecla f7   (usa F7 para ativar/desativar)
        """)

    ap.add_argument("--area", type=int, default=100,
                    help="Tamanho da área de detecção ao redor do cursor (padrão: 100px)")
    ap.add_argument("--sensibilidade", type=int, default=200,
                    help="Sensibilidade ao amarelo: 150=alta, 200=média, 230=baixa (padrão: 200)")
    ap.add_argument("--intervalo", type=float, default=0.01,
                    help="Intervalo mínimo entre cliques em segundos (padrão: 0.01)")
    ap.add_argument("--fps", type=int, default=100,
                    help="Taxa de verificação por segundo (padrão: 100)")
    ap.add_argument("--tecla", type=str, default="caps lock",
                    help="Tecla para ativar/desativar o trigger (padrão: caps lock)")
    ap.add_argument("--teste", action="store_true",
                    help="Modo teste: detecta mas não clica (bom para testar configurações)")
    ap.add_argument("--verbose", "-v", action="store_true",
                    help="Mostra cada detecção de amarelo")

    args = ap.parse_args()
    frame_delay = 1.0 / max(1, args.fps)

    r_min = args.sensibilidade
    g_min = args.sensibilidade
    b_max = max(30, 255 - args.sensibilidade - 50)

    keyboard.add_hotkey(args.tecla, toggle_trigger)

    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*60)
    print("� TRIGGER BOT - DETECTOR DE COR AMARELA")
    print("="*60)
    print(f"📍 Área de detecção: {args.area}x{args.area} pixels ao redor do cursor")
    print(f"🎯 Sensibilidade: {args.sensibilidade} (amarelo: R>={args.sensibilidade}, G>={args.sensibilidade})")
    print(f"⚡ Taxa de verificação: {args.fps} FPS")
    print(f"⏱️  Intervalo entre cliques: {args.intervalo}s")
    print(f"⌨️  Tecla de ativação: {args.tecla.upper()}")
    print("="*60)

    try:
        last_click = 0.0
        click_count = 0
        detection_count = 0

        while True:
            x, y = get_cursor_pos()
            buf, w, h = capture_roi_to_buffer(x, y, args.area)

            if contains_yellow(buf, w, h, r_min, g_min, b_max):
                detection_count += 1

                if args.teste:
                    if args.verbose:
                        print(f"🟡 Amarelo detectado! (posição: {x}, {y})")
                elif trigger_ativo:
                    for i in range(3):
                        click_left()
                        click_count += 1
                        time.sleep(0.05)
                    print(f"🖱️  3 cliques realizados em ({x}, {y}) - Total: {click_count}")

            time.sleep(frame_delay)

    except KeyboardInterrupt:
        print("\n" + "="*60)
        print("🛑 TRIGGER BOT ENCERRADO")
        print("="*60)
        if not args.teste:
            print(f"📊 Total de cliques realizados: {click_count}")
        print(f"📊 Total de detecções: {detection_count}")
        print("\n✅ Finalizado com sucesso!\n")


if __name__ == "__main__":
    main()
