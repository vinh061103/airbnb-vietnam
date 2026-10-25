from ctypes import wintypes
import ctypes
import psutil
import os
import sys
import time
import keyboard 
import math 
import json 
import random 
import threading
from PIL import Image
import mss 
import tkinter as tk 
import tkinter.font as tkFont
from tkinter import messagebox
try:
    import customtkinter as ctk
    CTK_AVAILABLE = True
except ImportError:
    CTK_AVAILABLE = False
    # Fallback to regular tkinter if customtkinter not available
import pyautogui  # Thư viện click chuột
import requests
import datetime
from datetime import datetime as dt
import string
import tempfile
import shutil
import subprocess
from io import BytesIO
from PIL import ImageDraw, ImageFont
import base64
import traceback
try:
    import cv2
    import numpy as np
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    cv2 = None
    np = None

# ====================================================================
# SCRIPT DIRECTORY - Đường dẫn tuyệt đối cho compiled version
# ====================================================================
if getattr(sys, 'frozen', False):
    # Nếu chạy từ .exe (compiled)
    if hasattr(sys, "_MEIPASS") and os.path.exists(os.path.join(sys._MEIPASS, "templates")):
        SCRIPT_DIR = sys._MEIPASS
    else:
        SCRIPT_DIR = os.path.dirname(sys.executable)
else:
    # Nếu chạy từ Python script
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# ====================================================================
# 🛡️ CONTINUOUS PROTECTION - Quét Liên Tục Debug Tools (5 lần/giây)
# ====================================================================
try:
    from continuous_protection import start_continuous_protection
    # Quét mỗi 0.2 giây (5 lần/giây) - Phát hiện debugger trong 0.2-0.4s
    # Thread sẽ LUÔN LUÔN quét: x64dbg, IDA, OllyDbg, CheatEngine, etc.
    start_continuous_protection(check_interval=0.2, check_vm=False)
except ImportError:
    # Nếu không có module, bỏ qua (để dev mode vẫn chạy được)
    pass

pyautogui.FAILSAFE = False  # Tắt fail-safe để tránh lỗi khi click

# ====================================================================
# ENHANCED ANTI-DETECTION SYSTEM
# ====================================================================
def get_random_system_exe():
    """Tạo tên file ngẫu nhiên với ký tự đặc biệt"""
    allowed_chars = string.ascii_letters + string.digits + '!@#$%&_'
    length = random.randint(8, 16)
    random_name = ''.join(random.choice(allowed_chars) for _ in range(length))
    return random_name + ".exe"

def inject_random_delays():
    """Thêm delay ngẫu nhiên giữa các hành động để tránh pattern detection"""
    delay = random.uniform(0.05, 0.15)
    time.sleep(delay)

# def spoof_process_name():
#     """Thay đổi tên process trong memory (Windows only)"""
#     try:
#         kernel32 = ctypes.windll.kernel32
        
#         # Định nghĩa cấu trúc PROCESS_BASIC_INFORMATION
#         class PROCESS_BASIC_INFORMATION(ctypes.Structure):
#             _fields_ = [
#                 ("Reserved1", ctypes.c_void_p),
#                 ("PebBaseAddress", ctypes.c_void_p),
#                 ("Reserved2", ctypes.c_void_p * 2),
#                 ("UniqueProcessId", ctypes.c_void_p),
#                 ("Reserved3", ctypes.c_void_p),
#             ]
        
#         # Lấy handle của process hiện tại
#         current_process = kernel32.GetCurrentProcess()
        
#         # Tạo tên process giả mạo (giống Windows system process)
#         fake_names = [
#             "svchost.exe", "dwm.exe", "explorer.exe", 
#             "RuntimeBroker.exe", "taskhostw.exe", "ctfmon.exe",
#             "Windows.Service.exe", "System.Update.exe"
#         ]
#         fake_name = random.choice(fake_names)
        
#         # Ghi đè tên process trong PEB (Process Environment Block)
#         # Lưu ý: Kỹ thuật này chỉ hoạt động trên một số phiên bản Windows
#         ntdll = ctypes.windll.ntdll
#         pbi = PROCESS_BASIC_INFORMATION()
        
#         # Query thông tin process
#         ntdll.NtQueryInformationProcess(
#             current_process, 0, ctypes.byref(pbi), 
#             ctypes.sizeof(pbi), None
#         )
        
#         # Không thực hiện ghi đè trực tiếp để tránh crash
#         # Chỉ log để biết đã cố gắng spoof
#         pass
        
#     except Exception as e:
#         # Nếu fail thì bỏ qua (vẫn chạy được nhưng không spoof)
#         pass
        

# def self_rename():
#     """Tự động clone file sang thư mục temp với tên Windows hợp lệ và chạy bản copy"""
#     # Nếu đã chạy từ bản copy thì bỏ qua
#     if "--cloned" in sys.argv:
#         spoof_process_name()
#         return

#     # Tạo tên file giống process hệ thống
#     new_exe_name = get_random_system_exe()
#     base_name = new_exe_name.replace(".exe", "")
    
#     # Chọn thư mục temp của Windows (ẩn hơn)
#     temp_dirs = [
#         os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Temp'),
#         os.path.join(os.environ.get('APPDATA', ''), 'Local', 'Temp'),
#         tempfile.gettempdir()
#     ]
    
#     # Thử từng thư mục cho đến khi thành công
#     for temp_dir in temp_dirs:
#         try:
#             if not os.path.exists(temp_dir):
#                 continue
                
#             new_path = os.path.join(temp_dir, new_exe_name)
            
#             # Copy file với tên mới
#             shutil.copy2(sys.executable, new_path)
            
#             # Chạy bản copy với flag --cloned
#             startupinfo = subprocess.STARTUPINFO()
#             startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
#             startupinfo.wShowWindow = subprocess.SW_HIDE
            
#             subprocess.Popen(
#                 [new_path, "--cloned"],
#                 startupinfo=startupinfo,
#                 creationflags=subprocess.CREATE_NO_WINDOW
#             )
            
#             # Thoát bản gốc
#             sys.exit(0)
#         except Exception as e:
#             # Nếu fail, thử thư mục tiếp theo
#             continue
    
#     # Nếu tất cả thất bại, tiếp tục chạy bản gốc
#     spoof_process_name()

# # Chạy self_rename ngay khi khởi động (với random delay để tránh pattern)
# self_rename()

# Tạo tên cửa sổ ngẫu nhiên (dùng cho title GUI)
RANDOM_WINDOW_NAME = get_random_system_exe().replace(".exe", "")

# ====================================================================
# ANTI-DETECTION: HUMANIZED INPUT SIMULATION
# ====================================================================
class HumanizedInput:
    """Wrapper cho keyboard/mouse để tránh pattern detection"""
    
    @staticmethod
    def press_key(key, duration=None):
        """Nhấn phím với timing ngẫu nhiên"""
        inject_random_delays()
        keyboard.press(key)
        time.sleep(duration or random.uniform(0.05, 0.15))
        keyboard.release(key)
    
    @staticmethod
    def click_mouse(x, y):
        """Click chuột với movement tự nhiên"""
        # Di chuyển chuột với đường cong tự nhiên
        current_x, current_y = pyautogui.position()
        duration = random.uniform(0.1, 0.3)
        pyautogui.moveTo(x, y, duration=duration, tween=pyautogui.easeInOutQuad)
        inject_random_delays()
        pyautogui.click()
    
    @staticmethod
    def type_text(text, interval=None):
        """Gõ text với timing tự nhiên"""
        for char in text:
            inject_random_delays()
            keyboard.write(char)
    
    @staticmethod
    def hold_key(key, duration):
        """Giữ phím với timing chính xác"""
        keyboard.press(key)
        time.sleep(duration)
        keyboard.release(key)
    
    @staticmethod
    def random_mouse_jitter():
        """Tạo chuyển động chuột ngẫu nhiên nhỏ (giống người thật)"""
        if random.random() < 0.1:  # 10% chance
            current_x, current_y = pyautogui.position()
            jitter_x = random.randint(-5, 5)
            jitter_y = random.randint(-5, 5)
            pyautogui.moveTo(current_x + jitter_x, current_y + jitter_y, duration=0.1)


# Tạo instance global để dùng trong code
humanized = HumanizedInput()

# Helper function to get resource path (for Nuitka onefile compatibility)
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for Nuitka onefile"""
    try:
        # Nếu chạy từ onefile bundle (Nuitka hoặc PyInstaller)
        base_path = sys._MEIPASS
    except AttributeError:
        # Nếu chạy từ Python script hoặc dev mode
        try:
            base_path = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
        except Exception:
            base_path = os.path.dirname(os.path.abspath(__file__))
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    full_path = os.path.join(base_path, relative_path)
    return full_path

# ====================================================================
# ANTI-MEMORY SCANNING
# ====================================================================
# Encode các string nhạy cảm để tránh signature scanning
def decode_str(encoded):
    """Decode base64 string"""
    return base64.b64decode(encoded).decode('utf-8')

# Thay vì hardcode string "bot", "cheat", "hack"... ta encode chúng
# Anti-cheat sẽ không tìm thấy signature trong memory
OBFUSCATED_STRINGS = {
    'bot': decode_str('Ym90'),  # "bot"
    'active': decode_str('YWN0aXZl'),  # "active"
    'mining': decode_str('bWluaW5n'),  # "mining"
}

# Randomize timing để tránh pattern detection
class AntiPatternTimer:
    """Quản lý timing để tránh bị phát hiện pattern"""
    def __init__(self):
        self.last_action_time = 0
        self.action_intervals = []
    
    def should_act(self, min_interval=0.1, max_interval=0.5):
        """Kiểm tra có nên thực hiện action không (với timing ngẫu nhiên)"""
        current_time = time.time()
        if current_time - self.last_action_time < min_interval:
            return False
        
        # Random delay để tránh pattern
        if random.random() < 0.3:  # 30% chance thêm delay
            time.sleep(random.uniform(0.05, 0.2))
        
        self.last_action_time = current_time
        return True
    
    def record_action(self):
        """Ghi lại thời gian action"""
        current_time = time.time()
        if self.last_action_time > 0:
            interval = current_time - self.last_action_time
            self.action_intervals.append(interval)
            # Giữ tối đa 100 intervals
            if len(self.action_intervals) > 100:
                self.action_intervals.pop(0)
        self.last_action_time = current_time

# Global timer instance
anti_pattern_timer = AntiPatternTimer()

# ====================================================================
# ANTI-DEBUGGING & VM DETECTION
# ====================================================================
def is_debugger_present():
    """Kiểm tra debugger có đang attach không"""
    try:
        return ctypes.windll.kernel32.IsDebuggerPresent() != 0
    except:
        return False

def check_vm_artifacts():
    """Kiểm tra các dấu hiệu của VM"""
    vm_indicators = [
        'vmware', 'virtualbox', 'vbox', 'qemu', 
        'virtual', 'vmtoolsd', 'vboxservice'
    ]
    
    try:
        for proc in psutil.process_iter(['name']):
            proc_name = proc.info['name'].lower()
            if any(indicator in proc_name for indicator in vm_indicators):
                return True
    except:
        pass
    
    return False

def anti_cheat_checks():
    """Chạy các kiểm tra anti-cheat"""
    detected = False
    
    # Kiểm tra debugger
    if is_debugger_present():
        print("[WARNING] Debugger detected!")
        detected = True
    
    # Kiểm tra VM (tùy chọn)
    # if check_vm_artifacts():
    #     print("[WARNING] Virtual Machine detected!")
    #     # Không block VM vì nhiều người dùng bình thường cũng dùng VM
    
    # Kiểm tra process nghi ngờ
    suspicious_processes = [
        'ollydbg', 'x64dbg', 'x32dbg', 'ida', 'ida64',
        'windbg', 'immunitydebugger', 'cheatengine',
        'processhacker', 'procmon', 'wireshark'
    ]
    
    try:
        for proc in psutil.process_iter(['name']):
            proc_name = proc.info['name'].lower()
            if any(suspicious in proc_name for suspicious in suspicious_processes):
                print(f"[WARNING] Suspicious process detected: {proc.info['name']}")
                detected = True
    except:
        pass
    
    return detected

# Chạy check khi khởi động
DETECTED_ANTI_CHEAT = anti_cheat_checks()

# Nếu phát hiện anti-cheat, tăng delay và randomization
if DETECTED_ANTI_CHEAT:
    print("[Anti-Detection] Enhanced protection mode enabled")
    inject_random_delays()
else:
    pass

# ========== OVERLAY HIỂN THỊ SỐ GỖ ĐÃ CHẶT ==========
import threading
import tkinter as tk

overlay_window = None
overlay_label = None
def show_wood_overlay():
    global overlay_window, overlay_label
    if overlay_window is not None:
        return
    overlay_window = tk.Toplevel()
    overlay_window.title(RANDOM_WINDOW_NAME)
    overlay_window.geometry('160x60+20+40')
    overlay_window.attributes('-topmost', False)
    overlay_window.overrideredirect(True)
    overlay_window.configure(bg='#222222')
    overlay_label = tk.Label(overlay_window, text='', font=('Segoe UI', 22, 'bold'), fg='#7ED320', bg='#222222')
    overlay_label.pack(expand=True, fill='both')
    update_wood_overlay()

def update_wood_overlay():
    global overlay_label, total_trees_chopped
    if overlay_label is not None:
        overlay_label.config(text=f'Đã chặt: {total_trees_chopped}')
    # Cập nhật mỗi 0.5s
    if overlay_label and overlay_label.winfo_exists():
        overlay_label.after(500, update_wood_overlay)

def start_overlay_thread():
    t = threading.Thread(target=show_wood_overlay, daemon=True)
    t.start()


# Khởi động overlay sau khi GUI chính đã khởi tạo (gọi sau setup_gui)
# (Trong hàm setup_gui hoặc sau khi root Tk() đã tồn tại, hãy gọi show_wood_overlay())

# ====================================================================
# KEY VERIFICATION SETUP (Sao chép từ guibase.py)
# ==================================================================== "AAABAAEAICAAAAEAIACoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAAABAAAMMOAADDDgAAAAAAAAAAAAAWFRf/FhUX/xYVF/8XFhf/FxYY/xcWGP8XFhj/GBYY/xgWGf8ZFhn/GRYZ/xkWGf8ZFxr/GRca/xkXGv8ZFxr/GRca/xkXGf8ZFhn/GRYZ/xkWGf8YFhn/GBYY/xcWGP8XFhj/FxYX/xcWF/8WFRf/FhUX/xYVF/8WFhf/FhYX/xYVF/8WFRf/FxYX/xcWGP8XFhj/GBYY/xgWGf8ZFhn/GRcZ/xoXGv8aFxr/Ghca/xsXG/8bFxv/Gxcb/xsXG/8bFxv/Ghcb/xoXGv8aFxr/GRca/xkWGf8ZFhn/GBYZ/xcWGP8XFhj/FxYX/xcWF/8WFRf/FhUX/xYVF/8WFhf/FhUX/xcWF/8XFhj/FxYY/xgWGf8ZFhn/GRcZ/xoXGv8aFxv/Gxcb/xsXHP8cGBz/HBgc/xwYHP8cGBz/HBgc/xwYHP8cGBz/Gxcc/xsXG/8aFxv/Ghca/xkXGv8ZFhn/GBYZ/xgWGP8XFhj/FxYX/xYVF/8WFRf/FhUX/xYWF/8XFhf/FxYY/xcWGP8YFhn/GRYZ/xkXGv8aFxr/Gxcb/xwXHP8cGBz/HRgd/x0YHf8eGB7/Hhge/x4YHv8eGB7/Hhgd/x0YHf8dGB3/HBcc/xwXHP8bFxv/Ghca/xkXGv8ZFhn/GBYZ/xcWGP8XFhj/FxYX/xYVF/8WFRf/FhUX/xcWGP8XFhj/GBYZ/xkWGf8ZFxr/Gxca/xsXHP8cFxz/HRcd/x4YHv8eGB7/Hxgf/x8YH/8fGB//Hxgf/x8YH/8fGB//Hxgf/x8YH/8fGB//Hhge/x0YHf8cFxz/GxYa/xkWGv8ZFhn/GBYZ/xcWGP8XFhj/FxYX/xYVF/8WFRf/FxYY/xgWGP8ZFhn/GRca/xoXGv8bFxz/HBcc/x4YHv8fGB//IRgg/yIZIf8jGSL/JBki/yQZIv8kGSP/JBoj/yUaI/8mGST/Jhkk/yYZJP8lGSP/Ihgh/x8XH/8dFh3/GxYa/xkVGv8ZFhn/GBYY/xcWGP8XFhf/FhUX/xYVF/8XFhj/GBYZ/xkWGf8aFxr/Gxcb/xwXHP8eGB7/IBgf/yMZIv8oGyb/LB4q/y0eK/8tHCr/LBwp/ywcKv8tHCr/Lhwr/zAe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if+oibP/hmKU/zkVSP8rETb/Z090/0k3Uv8cEx//HRgf/xoWG/8YFhn/FxUX/xYVF/8XFhf/FxYY/xgWGf8ZFhn/Ghca/xwYHP8dGB3/Hxkf/yAYH/8hGSD/JBoj/ysbKP83HzL/QyM9/2UlWP/36vb/17TR/2EKUf/Sqsz/upG4/zgDO/86G0D/NyE7/y8fM/8fESP/HxUj/yAZIv8bFh3/GRYb/xcVGP8XFRf/FhUX/xYVF/8XFhj/FxYY/xkWGf8aFxr/Gxcb/xwYHP8eGB7/Hxkf/yAYH/8iGSL/KRsn/zQeMP9DJD3/Xh1R/+jQ5P/t1+n/ZRhW/6Nrmf/dv9j/RhhA/zgjOP8tGy7/JRkn/yQaJv8hGSP/HRce/xsXHP8ZFhr/FxUY/xcVF/8WFRf/FhUX/xcWF/8XFhj/GBYY/xkWGf8aFxr/Gxcc/x0YHf8eGR7/Hxgf/yEYIP8nGib/Mh8v/zwdNf+KTn3/7tLp//fs9f9mFFX/soGo/8imwv85ETP/MyEy/yobKv8jGST/IBki/x4YH/8cFx3/GhYb/xgVGf8XFRj/FxYX/xYVF/8WFRf/FhUX/xcWGP8XFhj/GRYZ/xkXGv8bFxv/HBgc/x0YHf8fGR7/Hxgf/yUaI/8vHiz/NBsv/3A6ZP/98vr/+vT5/7Vzp//Em7z/YTJY/zMbMP8uHS3/Jhol/yEYIf8eGB//HBcd/xsXG/8ZFhr/GBUY/xcWGP8WFhf/FhUX/xYVF/8WFRf/FxYX/xcWGP8YFhj/GRYZ/xoXGv8bFxv/HBgc/x4YHf8fGB7/Ihkh/yobJ/80ITD/OhIy/7KNqv/dw9f/fEhx/0kgQf80GzD/MB4u/ycaJv8hGCH/Hhgf/xwXHf8bFxv/GRYa/xkVGf8XFhj/FxYY/xYVF/8WFRf/FhYX/xYVF/8WFRf/FxYX/xcWGP8YFhn/GRYZ/xoXGv8bFxv/HBgc/x0XHf8fGB//JRoj/ywcKf8yHi//PRs2/0IZOv8yFSz/Mx4w/y8dLP8nGiX/IRgh/x4XHv8cFh3/GxYb/xoWGv8ZFhn/GBYZ/xcWGP8XFhf/FhUX/xYVF/8WFhf/FhUX/xYVF/8XFhf/FxYY/xcWGP8ZFhn/GRca/xoXGv8bFxz/HBgc/x0YHf8gGB//JBoj/yobJ/8sHSr/LR4q/y4eLP8qGyj/JRok/yEYIP8eFx7/HBcc/xsXHP8bFxr/GRca/xkWGf8YFhj/FxYY/xcWF/8WFRf/FhUX/xYWF/8WFhf/FhUX/xYVF/8XFhf/FxYY/xgWGP8ZFhn/GRca/xoXGv8bFxv/HBcc/x0YHf8fGB//IRgg/yMZIv8kGSP/Ixki/yEYIP8fGB//Hhgd/xwXHP8bFxz/Gxcb/xkXGv8ZFhn/GBYZ/xcWGP8XFhf/FhUX/xYVF/8WFhf/FhYX/xYWF/8WFRf/FhUX/xYVF/8XFhj/FxYY/xgWGP8ZFhn/GRca/xoXGv8bFxv/Gxcc/xwXHP8dGB3/HRgd/x4YHv8dGB3/HRgd/xwXHP8cFxz/Gxcb/xsXGv8ZFxr/GRYZ/xgWGf8XFhj/FxYY/xcWF/8WFRf/FhUX/xYWF/8WFhf/FhYX/xYWF/8WFRf/FhUX/xcWF/8XFhj/FxYY/xgWGP8ZFhn/GRYZ/xoXGv8aFxr/Gxcb/xsXG/8bFxv/Gxcc/xsXHP8bFxv/Gxcb/xsXG/8aFxr/GRca/xkWGf8YFhn/FxYY/xcWGP8XFhf/FhUX/xYVF/8WFRf/FhYX/xYWF/8WFhf/FhYX/xYVF/8WFRf/FhUX/xcWF/8XFhj/FxYY/xgWGP8YFhn/GRYZ/xkXGf8aFxr/Ghca/xoXGv8aFxr/Ghca/xoXGv8aFxr/GRca/xkWGf8ZFhn/GBYZ/xgWGP8XFhj/FxYX/xYVF/8WFRf/FhUX/xYWF/8WFhf/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA="  # Điền base64 của L.ico vào đây
LOGO_BASE64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAfQAAAH0CAIAAABEtEjdAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAEx2lUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSfvu78nIGlkPSdXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQnPz4KPHg6eG1wbWV0YSB4bWxuczp4PSdhZG9iZTpuczptZXRhLyc+CjxyZGY6UkRGIHhtbG5zOnJkZj0naHR0cDovL3d3dy53My5vcmcvMTk5OS8wMi8yMi1yZGYtc3ludGF4LW5zIyc+CgogPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9JycKICB4bWxuczpBdHRyaWI9J2h0dHA6Ly9ucy5hdHRyaWJ1dGlvbi5jb20vYWRzLzEuMC8nPgogIDxBdHRyaWI6QWRzPgogICA8cmRmOlNlcT4KICAgIDxyZGY6bGkgcmRmOnBhcnNlVHlwZT0nUmVzb3VyY2UnPgogICAgIDxBdHRyaWI6Q3JlYXRlZD4yMDI1LTA4LTE2PC9BdHRyaWI6Q3JlYXRlZD4KICAgICA8QXR0cmliOkV4dElkPmUyNDljMWY1LWQwMDctNDRhZi1hOGEzLTNkYzVjYzk5MTQ0NjwvQXR0cmliOkV4dElkPgogICAgIDxBdHRyaWI6RmJJZD41MjUyNjU5MTQxNzk1ODA8L0F0dHJpYjpGYklkPgogICAgIDxBdHRyaWI6VG91Y2hUeXBlPjI8L0F0dHJpYjpUb3VjaFR5cGU+CiAgICA8L3JkZjpsaT4KICAgPC9yZGY6U2VxPgogIDwvQXR0cmliOkFkcz4KIDwvcmRmOkRlc2NyaXB0aW9uPgoKIDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PScnCiAgeG1sbnM6ZGM9J2h0dHA6Ly9wdXJsLm9yZy9kYy9lbGVtZW50cy8xLjEvJz4KICA8ZGM6dGl0bGU+CiAgIDxyZGY6QWx0PgogICAgPHJkZjpsaSB4bWw6bGFuZz0neC1kZWZhdWx0Jz5MIC0gMTwvcmRmOmxpPgogICA8L3JkZjpBbHQ+CiAgPC9kYzp0aXRsZT4KIDwvcmRmOkRlc2NyaXB0aW9uPgoKIDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PScn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"  # Điền base64 của L.png vào đây

def get_resource_path(resource_data, extension):
    """
    Trả về đường dẫn tới file resource.
    Nếu chạy từ .exe (Nuitka), tạo temp file.
    Nếu chạy từ .py, tìm file trong thư mục hiện tại.
    """
    # Thử tìm file trong thư mục hiện tại trước
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = f"L{extension}"
    file_path = os.path.join(current_dir, file_name)
    
    if os.path.exists(file_path):
        return file_path
    
    # Nếu không tìm thấy và có base64 data, tạo temp file
    if resource_data:
        try:
            data = base64.b64decode(resource_data)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=extension)
            temp_file.write(data)
            temp_file.close()
            return temp_file.name
        except:
            pass
    
    return None

# ====================================================================
# KEY VERIFICATION SETUP
# ====================================================================

def _decode_api_url():
    """Giải mã API URL (chống reverse engineering)"""
    # URL đã mã hóa bằng XOR và base64
    encrypted = "Ql5eWlkQBQVZSVhDWl4ETUVFTUZPBElFRwVHS0lYRVkFWQVrYUxTSUhdcEtzblJJcGUcRFp5XBpcQHllY3hNGh8TQmhTG3VTZWAccEIHHX5fQ3waaHJSRGYTUnJffgcbfRN1RGxgQnBoZU0FT1JPSQ=="
    decoded_bytes = base64.b64decode(encrypted)
    xor_key = 42
    url = ''.join(chr(b ^ xor_key) for b in decoded_bytes)
    return url
def _check_malicious_processes():
    """
    Kiểm tra các tiến trình proxy/debug đang chạy
    Returns: (is_detected, process_name)
    """
    # Danh sách các tiến trình nguy hiểm (proxy/MITM tools)
    dangerous_processes = [
        # MITM Proxy Tools
        'mitmproxy.exe', 'mitmdump.exe', 'mitmweb.exe',
        'fiddler.exe', 'fiddlereverywhere.exe',
        'charles.exe', 'charlesproxy.exe',
        'burpsuite.exe', 'burp.exe',
        'proxifier.exe', 'proxycap.exe',
        'wireshark.exe', 'tshark.exe',
        
        # Network Analysis Tools
        'httpanalyzer.exe', 'httpdebugger.exe',
        'telerik.fiddler.exe',
        
        # Additional Debug/Reverse Tools
        'processhacker.exe', 'processhacker2.exe',
        'dnspy.exe', 'ilspy.exe',
        'httpdebugpro.exe', 'httpwatch.exe',
    ]
    
    # print(f"[DEBUG] Bắt đầu quét {len(dangerous_processes)} tiến trình nguy hiểm...")
    
    try:
        # Quét tất cả tiến trình đang chạy
        process_count = 0
        for proc in psutil.process_iter(['name']):
            try:
                process_count += 1
                proc_name = proc.info['name'].lower()
                # So sánh với danh sách (đã lowercase)
                if proc_name in dangerous_processes:
                    # print(f"[SECURITY] ⚠️ PHÁT HIỆN: {proc.info['name']}")
                    return True, proc.info['name']
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        # print(f"[DEBUG] Đã quét {process_count} tiến trình - Không phát hiện mối đe dọa")
    except Exception as e:
        # print(f"[ERROR] Lỗi khi quét tiến trình: {e}")
        pass
    
    return False, None

API_URL = _decode_api_url()
INI_FILE = os.path.join(os.getcwd(), "config.ini")

GLOBAL_KEY_INFO = {
    "is_lifetime": False,
    "expire_time_ms": None,
    "hwid_mismatch": False,
    "initial_check_done": False,
    "expiry": None
}
def move_mouse_down_smooth(pixels, steps):
    # Dùng mouse_event với MOUSEEVENTF_MOVE (relative movement)
    MOUSEEVENTF_MOVE = 0x0001
    pixels_per_step = pixels // steps
    
    for i in range(steps):
        # mouse_event: dx=0 (không di chuyển ngang), dy=pixels_per_step (di chuyển xuống)
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_MOVE, 0, pixels_per_step, 0, 0)
        time.sleep(0.02)
def get_hwid():
    return os.environ.get("COMPUTERNAME", "UNKNOWN")

def get_resource_path(filename: str) -> str:
    if getattr(sys, "frozen", False):
        if hasattr(sys, "_MEIPASS"):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, filename)

def circularize_image(img):
    size = min(img.size)
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    img = img.resize((size, size), Image.LANCZOS).convert("RGBA")
    result = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    result.paste(img, (0, 0), mask)
    return result

def _make_image(text, size=(300,80), bg=(20,20,20), fg=(200,200,200), logo=False):
    img = Image.new("RGBA", size, bg + (255,))
    draw = ImageDraw.Draw(img)
    try:
        f = ImageFont.truetype("arial.ttf", 18)
    except Exception:
        f = ImageFont.load_default()
    if logo:
        r = 28
        draw.ellipse((10, (size[1]//2)-r, 10+2*r, (size[1]//2)+r), fill=(50,150,255))
        draw.text((10+2*r+10, 10), text, font=f, fill=fg)
    else:
        draw.text((10, 10), text, font=f, fill=fg)
    bio = BytesIO()
    img.save(bio, format="PNG")
    bio.seek(0)
    return bio

def _open_url(url):
    import webbrowser
    webbrowser.open(url, new=1)

def make_rounded_image(text, size=(160,40), bg="#2e7d32", fg="white",
                       border="#1b5e20", radius=12, font_name="Segoe UI", font_size=12):
    w, h = size
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle([(0, 0), (w-1, h-1)], radius=radius, fill=border)
    inset = 2
    draw.rounded_rectangle([(inset, inset), (w-1-inset, h-1-inset)], radius=max(0, radius-inset), fill=bg)

    try:
        f = ImageFont.truetype("segoeui.ttf", font_size)
    except Exception:
        try:
            f = ImageFont.truetype("arial.ttf", font_size)
        except Exception:
            f = ImageFont.load_default()

    try:
        bbox = draw.textbbox((0, 0), text, font=f)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    except AttributeError:
        tw, th = draw.textsize(text, font=f)

    draw.text(((w-tw)//2, (h-th)//2), text, font=f, fill=fg)
    from PIL import ImageTk
    return ImageTk.PhotoImage(img)

def format_remaining_time(timestamp_ms):
    if timestamp_ms is None:
        return "00:00 (Lỗi/Hết hạn)", True

    expire_dt = dt.fromtimestamp(timestamp_ms / 1000)
    now = dt.now()
    remaining = expire_dt - now

    total_seconds = int(remaining.total_seconds())

    if total_seconds <= 0:
        return "00:00 (Hết hạn)", True

    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    if days > 0:
        return f"{days} ngày {hours} giờ", False
    elif hours > 0:
        return f"{hours:02d} giờ {minutes:02d} phút", False
    else:
        return f"{minutes:02d} phút {seconds:02d} giây", False

def save_key_to_ini(key, hwid, expiry_date_str=None):
    """Lưu key, hwid và ngày hết hạn (nếu có) vào file config."""
    content = f"[Auth]\nKey={key}\nHWID={hwid}\n"
    content += f"ExpiryDate={expiry_date_str}\n" 
    with open(INI_FILE, "w", encoding="utf-8") as f:
        f.write(content)

def read_key_from_ini():
    if not os.path.exists(INI_FILE):
        return None, None
    key, hwid = None, None
    with open(INI_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("Key="):
                key = line.strip().split("=")[1]
            elif line.startswith("HWID="):
                hwid = line.strip().split("=")[1]
    return key, hwid

def check_key(key, hwid):
    """Kiểm tra key qua API với process detection"""
    try:
        # 🛡️ SECURITY CHECK: Kiểm tra tiến trình proxy/debug
        is_malicious, proc_name = _check_malicious_processes()
        # print(f"[DEBUG] Process check: is_malicious={is_malicious}, proc_name={proc_name}")
        if is_malicious:
            # print(f"[SECURITY] Phát hiện tiến trình nguy hiểm: {proc_name}")
            return "proxy_detected", proc_name, False
        
        # print(f"[DEBUG] Đang gửi request đến API: {API_URL}")
        # print(f"[DEBUG] Key: {key}, HWID: {hwid}")
        
        resp = requests.get(API_URL, params={"key": key, "hwid": hwid}, timeout=30, verify=True)
        
        # print(f"[DEBUG] Status Code: {resp.status_code}")
        # print(f"[DEBUG] Response Text: {resp.text}")
        
        try:
            data = resp.json()
            # print(f"[DEBUG] JSON Response: {data}")
            
            status = data.get("status", "invalid_key")
            is_lifetime = data.get("is_lifetime", False)
            expire_time_ms = data.get("expireTime")
            
            # print(f"[DEBUG] Status: {status}, Lifetime: {is_lifetime}")
            
            if is_lifetime:
                return status, None, True
            else:
                return status, expire_time_ms, False
                
        except ValueError:
            response_text = resp.text.strip()
            # print(f"[DEBUG] Non-JSON Response: {response_text}")
            
            if response_text == "invalid_key":
                return "invalid_key", None, False
            elif response_text == "missing_params":
                return "api_error", None, False
            elif response_text == "sheet_not_found":
                return "api_error", None, False
            elif response_text == "invalid_time_duration":
                return "invalid_key", None, False
            elif resp.status_code >= 400:
                print(f"[DEBUG] HTTP Error {resp.status_code}")
                return "api_error", None, False
            else:
                return "api_error", None, False
    
    except requests.exceptions.Timeout:
        # print("[DEBUG] Lỗi: Timeout khi gọi API (>30 giây)")
        return "timeout_error", None, False
    except requests.exceptions.ConnectionError as e:
        # print(f"[DEBUG] Lỗi: Connection Error - {e}")
        return "network_error", None, False
    except requests.exceptions.RequestException as e:
        # print(f"[DEBUG] Lỗi: Request Exception - {e}")
        return "network_error", None, False
    except Exception as e:
        # print(f"[DEBUG] Lỗi: Không xác định - {e}")
        return "network_error", None, False

def activation_gui_and_wait(hwid):
    width, height = 420, 600
    win = tk.Tk()
    win.title(RANDOM_WINDOW_NAME)  # Đặt tên ngẫu nhiên (mặc dù không hiển thị do overrideredirect)
    
    # Thiết lập icon
    icon_path = get_resource_path("L.ico")
    if icon_path and os.path.exists(icon_path):
        try:
            win.iconbitmap(icon_path)
        except:
            pass
    
    win.overrideredirect(True)
    win.resizable(False, False)
    win.attributes("-topmost", False)
    win.configure(bg="#0b0b0b")
    WIN_BG = "#0f0820"
    ACCENT = "#8A2BE2"
    ACCENT_LIGHT = "#B794FF"
    TEXT = "#F5EEFF"
    win.deiconify()
    BTN_BG = "#2e7d32"
    BTN_BORDER = "#1b5e20"
    BTN_ACTIVE = "#4caf50"
    BTN_FONT = ("Segoe UI", 10, "bold")
    PANEL_BG = "#0b0b0b"

    win.update_idletasks()
    x = (win.winfo_screenwidth() - width) // 2
    y = (win.winfo_screenheight() - height) // 2
    win.geometry(f"{width}x{height}+{x}+{y}")

    try:
        logo_path = get_resource_path("L.png")
        if logo_path and os.path.exists(logo_path):
            logo_img = Image.open(logo_path).convert("RGBA")
            logo_img = circularize_image(logo_img)
        else:
            raise FileNotFoundError("Logo not found")
    except Exception:
        logo_bio = _make_image("GTA5VN", size=(380,90), logo=True)
        logo_img = Image.open(logo_bio)
        logo_img = circularize_image(logo_img) 

    max_w, max_h = 100, 100
    try:
        logo_img = logo_img.convert("RGBA")
        logo_img.thumbnail((max_w, max_h), Image.LANCZOS)
    except Exception:
        pass

    from PIL import ImageTk
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_frame = tk.Frame(win, bg=PANEL_BG)
    logo_frame.pack(pady=(12,6))
    logo_lbl = tk.Label(logo_frame, image=logo_photo, bg=PANEL_BG)
    logo_lbl.image = logo_photo
    logo_lbl.pack(side="left")
    brand_lbl = tk.Label(logo_frame, text="Chặt Gỗ SVIP", fg=ACCENT_LIGHT, bg=PANEL_BG,
                         font=("Segoe UI", 25, "italic"))
    brand_lbl.pack(side="left", padx=(12,0), pady=8)

    frm = tk.Frame(win, bg=WIN_BG)
    frm.pack(fill="both", expand=True, padx=18, pady=(4,8))

    title = tk.Label(frm, text="Kích hoạt Tool", fg="white", bg=WIN_BG,
                     font=("Consolas", 14, "bold"))
    title.pack(pady=(0,8))

    inner = tk.Frame(frm, bg="#121212")
    inner.pack(padx=6, pady=6, fill="x")

    tk.Label(inner, text="Nhập Key", fg="#ddd", bg="#121212", anchor="w",
             font=("Consolas", 10)).pack(fill="x", padx=8, pady=(8,0))
    key_var = tk.StringVar()
    entry = tk.Entry(inner, textvariable=key_var, width=36, font=("Consolas", 11),
                     relief="flat", bg="#1a1a1a", fg="#fff", insertbackground="#fff")
    entry.pack(padx=8, pady=(6,10))
    entry.focus_set()

    msg_var = tk.StringVar(value="")
    msg_lbl = tk.Label(inner, textvariable=msg_var, fg="#ffcc00", bg="#121212",
                       font=("Consolas", 9))
    msg_lbl.pack(anchor="w", padx=8, pady=(0,8))
    current_key, saved_hwid = read_key_from_ini()
    
    def update_key_info_gui(status, expire_time_ms, is_lifetime):
        expiry_str = "N/A"
        msg = "Đã kiểm tra. Trạng thái không xác định." 
        color = "black"
        
        GLOBAL_KEY_INFO["is_lifetime"] = is_lifetime
        GLOBAL_KEY_INFO["expire_time_ms"] = expire_time_ms
        GLOBAL_KEY_INFO["hwid_mismatch"] = (status == "hwid_mismatch")
        GLOBAL_KEY_INFO["initial_check_done"] = True
        
        remaining_time_str = format_remaining_time(expire_time_ms)[0]
        
        if status == "active":
            msg = "✅ Kích hoạt thành công!"
            color = "green"
            
            if is_lifetime:
                expiry_lbl.config(text="Thời hạn sử dụng: KHÔNG THỜI HẠN", fg=color)
                remaining_lbl.config(text="Còn lại: Vĩnh viễn", fg=color)
                expiry_str = None
            else:
                expiry_dt = dt.fromtimestamp(expire_time_ms / 1000)
                expiry_dt_str = expiry_dt.strftime('%Y-%m-%d %H:%M:%S')
                expiry_str = expiry_dt.strftime('%Y-%m-%d %H:%M:%S')
                GLOBAL_KEY_INFO['expiry'] = expiry_dt_str
                expiry_dt_lbl = dt.fromtimestamp(expire_time_ms / 1000).strftime('%Y-%m-%d %H:%M')
                expiry_lbl.config(text=f"Thời gian hết hạn: {expiry_dt_lbl}", fg=color)
                remaining_lbl.config(text=f"Còn lại: {remaining_time_str}", fg=color)
            
            save_key_to_ini(current_key if 'current_key' in locals() else key_var.get(), hwid, expiry_str)
            if expiry_str:
                GLOBAL_KEY_INFO['expiry'] = expiry_str
            
            set_buttons_state(True)
            
        elif status == "expired":
            msg = "❌ Key hết hạn rồi, nhắn Lazy mua key mới đê"
            color = "red"
            expiry_lbl.config(text="Trạng thái: Key đã hết hạn", fg=color)
            remaining_lbl.config(text="Vui lòng nhập key mới", fg=color)
            entry.delete(0, tk.END)
            entry.focus()
            set_buttons_state(True)
            
        elif status == "hwid_mismatch":
            msg = "❌ Key này ở trên máy khác rồi ba"
            color = "red"
            expiry_lbl.config(text="Trạng thái: Key đang bị khóa HWID.", fg=color)
            remaining_lbl.config(text="Còn lại: N/A", fg=color)
            set_buttons_state(True)
        
        elif status == "invalid_key":
            msg = "❌ Sai mẹ key rồi ní ơi"
            color = "red"
            expiry_lbl.config(text="Trạng thái: Key không hợp lệ", fg=color)
            remaining_lbl.config(text="Còn lại: N/A", fg=color)
            entry.delete(0, tk.END)
            entry.focus()
            set_buttons_state(True)
        
        elif status == "security_error":
            msg = "🚨 PHÁT HIỆN TẤN CÔNG MITM! Connection không an toàn. Tool sẽ thoát."
            color = "red"
            expiry_lbl.config(text="Trạng thái: ⚠️ BẢO MẬT BỊ XÂM PHẠM", fg=color)
            remaining_lbl.config(text="Phát hiện MITM Proxy/Certificate Fake", fg=color)
            msg_var.set(msg)
            msg_lbl.config(fg=color)
            # Thoát sau 3 giây
            win.after(3000, lambda: os._exit(1))
            return
        
        elif status == "timeout_error":
            msg = "⚠️ Lỗi timeout! Không thể kết nối đến server. Vui lòng kiểm tra internet."
            color = "orange"
            expiry_lbl.config(text="Trạng thái: Timeout khi kết nối", fg=color)
            remaining_lbl.config(text="Vui lòng thử lại", fg=color)
            set_buttons_state(True)
        
        elif status == "network_error":
            msg = "⚠️ Lỗi mạng! Không thể kết nối internet. Vui lòng kiểm tra kết nối."
            color = "orange"
            expiry_lbl.config(text="Trạng thái: Lỗi kết nối mạng", fg=color)
            remaining_lbl.config(text="Vui lòng thử lại", fg=color)
            set_buttons_state(True)
        
        elif status == "api_error":
            msg = "❌ Lỗi API! Server trả về lỗi. Vui lòng thử lại sau."
            color = "red"
            expiry_lbl.config(text="Trạng thái: Lỗi từ server", fg=color)
            remaining_lbl.config(text="Vui lòng thử lại sau", fg=color)
            set_buttons_state(True)
        
        elif status == "unknown_error":
            msg = "❌ Lỗi không xác định. Vui lòng thử lại."
            color = "red"
            expiry_lbl.config(text="Trạng thái: Lỗi không xác định", fg=color)
            remaining_lbl.config(text="Vui lòng thử lại", fg=color)
            set_buttons_state(True)
        
        else:
            # Các status không xác định khác
            msg = f"❌ Trạng thái không xác định: {status}. Vui lòng liên hệ hỗ trợ."
            color = "#ffcc00"
            expiry_lbl.config(text=f"Trạng thái: {status}", fg=color)
            remaining_lbl.config(text="Vui lòng liên hệ hỗ trợ", fg=color)
            set_buttons_state(True)
            
        msg_var.set(msg)

    def initial_check():
        if current_key and saved_hwid == hwid:
            key_var.set(current_key)
            status, expire_time_ms, is_lifetime = check_key(current_key, hwid)
            
            if not is_lifetime and expire_time_ms:
                expire_dt = dt.fromtimestamp(expire_time_ms / 1000)
                if dt.now() > expire_dt:
                    status = "expired"
                    
            update_key_info_gui(status, expire_time_ms, is_lifetime)
            
            if status == "active":
                win.after(1000, win.destroy)
                
        else:
            if not current_key:
                msg_var.set("Vui lòng nhập Key để kích hoạt.")
            elif saved_hwid != hwid:
                msg_var.set(f"Key được lưu cho HWID khác ({saved_hwid}). Vui lòng nhập Key mới.")

            expiry_lbl.config(text="Thời hạn sử dụng: N/A")
            remaining_lbl.config(text="Còn lại: N/A")

    win.after(100, initial_check)

    info_frame = tk.Frame(frm, bg=WIN_BG)
    info_frame.pack(fill="x", padx=6, pady=(10,6))
    
    key_info_lbl = tk.Label(info_frame, text="Key Info:", fg="#4CAF50", bg=WIN_BG, 
                            font=("Consolas", 12, "bold"), anchor="w")
    key_info_lbl.pack(fill="x", padx=8, pady=(4,0))
    
    expiry_lbl = tk.Label(info_frame, text="Hết hạn: Đang kiểm tra...", fg="#F5EEFF", bg=WIN_BG, 
                          font=("Consolas", 10), anchor="w")
    expiry_lbl.pack(fill="x", padx=8)

    remaining_lbl = tk.Label(info_frame, text="Còn lại: --:--", fg="#F5EEFF", bg=WIN_BG, 
                             font=("Consolas", 10), anchor="w")
    remaining_lbl.pack(fill="x", padx=8, pady=(0,4))
    
    btn_frame = tk.Frame(frm, bg=WIN_BG)
    btn_frame.pack(fill="x", pady=6)
    btn_frame.columnconfigure(0, weight=1)
    btn_frame.columnconfigure(1, weight=1)

    sec_frame = tk.Frame(frm, bg=WIN_BG)
    sec_frame.pack(fill="x", pady=(6,0))
    sec_frame.columnconfigure(0, weight=1)
    sec_frame.columnconfigure(1, weight=1)
    sec_frame.columnconfigure(2, weight=1)
    
    img_confirm = make_rounded_image("Xác nhận", size=(160,40), bg="#2e7d32", fg="white", border="#1b5e20", radius=10)
    img_confirm_h = make_rounded_image("Xác nhận", size=(160,40), bg="#4caf50", fg="white", border="#2e7d20", radius=10)
    img_exit = make_rounded_image("Thoát", size=(160,40), bg="#2e7d32", fg="white", border="#1b5e20", radius=10)
    img_exit_h = make_rounded_image("Thoát", size=(160,40), bg="#e53935", fg="white", border="#b71c1c", radius=10)
    img_help = make_rounded_image("Hướng dẫn (YouTube)", size=(220,40), bg="#2e7d32", fg="white", border="#1b5e20", radius=10)
    img_help_h = make_rounded_image("Hướng dẫn (YouTube)", size=(220,40), bg="#4caf50", fg="white", border="#2e7d20", radius=10)
    img_price = make_rounded_image("Bảng giá", size=(120,36), bg="#2e7d32", fg="white", border="#1b5e20", radius=10)
    img_price_h = make_rounded_image("Bảng giá", size=(120,36), bg="#4caf50", fg="white", border="#2e7d20", radius=10)
    img_discord = make_rounded_image("Discord", size=(120,36), bg="#2e7d32", fg="white", border="#1b5e20", radius=10)
    img_discord_h = make_rounded_image("Discord", size=(120,36), bg="#4caf50", fg="white", border="#2e7d20", radius=10)

    def set_buttons_state(state: bool):
        for w in (b1, b3, b4, b5):
            try:
                w.config(state="normal" if state else "disabled")
            except Exception:
                pass

    def on_confirm():
        k = key_var.get().strip()
        if not k:
            msg_var.set("Vui lòng nhập key.")
            return
        
        msg_var.set("Đang kiểm tra key... Vui lòng chờ 15 giây.")
        set_buttons_state(False)
        
        # Khai báo biến ở scope của on_confirm
        status = None
        expire_time_ms = None
        is_lifetime = False
        
        def worker_check():
            nonlocal status, expire_time_ms, is_lifetime
            try:
                status, expire_time_ms, is_lifetime = check_key(k, hwid)
                
                if not is_lifetime and expire_time_ms:
                    expire_dt = dt.fromtimestamp(expire_time_ms / 1000)
                    if dt.now() > expire_dt:
                        status = "expired"
                        
            except Exception as ex:
                status = "unknown_error"
                expire_time_ms, is_lifetime = None, False
            
            def after_check():
                nonlocal status
                # Xử lý tất cả status thông qua update_key_info_gui
                update_key_info_gui(status, expire_time_ms, is_lifetime)

                if status == "active":
                    save_key_to_ini(k, hwid)
                    win.after(1000, win.destroy)
                else:
                    set_buttons_state(True)
                    
            win.after(0, after_check)
            
        threading.Thread(target=worker_check, daemon=True).start()

    def on_exit():
        win.destroy()
        raise SystemExit()
    
    def on_close():
        win.destroy()
        raise SystemExit()
    
    win.protocol("WM_DELETE_WINDOW", on_close)
    
    def on_help():
        _open_url("https://youtu.be/rKnKr7BI3FA")

    def on_pricing():
        bio = _make_image("Bảng giá:\n1 giờ: 3k\n2 giờ: 5k\n1 ngày: 29k\n1 tuần: 89k\n1 tháng: 179k", size=(380,160))
        img = Image.open(bio)
        top = tk.Toplevel(win)
        top.title(RANDOM_WINDOW_NAME)
        top.geometry("420x220")
        top.attributes("-topmost", False)
        top.update_idletasks()
        tx = (top.winfo_screenwidth() - 420) // 2
        ty = (top.winfo_screenheight() - 220) // 2
        top.geometry(f"420x220+{tx}+{ty}")
        from PIL import ImageTk
        p = ImageTk.PhotoImage(img)
        lbl = tk.Label(top, image=p, bg=WIN_BG)
        lbl.image = p
        lbl.pack(padx=8, pady=8)

    def on_discord():
        _open_url("https://discord.gg/nhmegjSa")

    b1 = tk.Button(btn_frame, image=img_confirm, command=on_confirm, bd=0, bg=WIN_BG, activebackground=WIN_BG)
    b1.image = img_confirm
    b1.grid(row=0, column=0, padx=6, pady=6, sticky="ew")
    b1.bind("<Enter>", lambda e: b1.config(image=img_confirm_h))
    b1.bind("<Leave>", lambda e: b1.config(image=img_confirm))

    b2 = tk.Button(btn_frame, image=img_exit, command=on_exit, bd=0, bg=WIN_BG, activebackground=WIN_BG)
    b2.image = img_exit
    b2.grid(row=0, column=1, padx=6, pady=6, sticky="ew")
    b2.bind("<Enter>", lambda e: b2.config(image=img_exit_h))
    b2.bind("<Leave>", lambda e: b2.config(image=img_exit))

    b3 = tk.Button(sec_frame, image=img_help, command=on_help, bd=0, bg=WIN_BG, activebackground=WIN_BG)
    b3.image = img_help
    b3.grid(row=0, column=0, columnspan=3, padx=6, pady=(8,6), sticky="ew")
    b3.bind("<Enter>", lambda e: b3.config(image=img_help_h))
    b3.bind("<Leave>", lambda e: b3.config(image=img_help))

    b4 = tk.Button(sec_frame, image=img_price, command=on_pricing, bd=0, bg=WIN_BG, activebackground=WIN_BG)
    b4.image = img_price
    b4.grid(row=1, column=0, padx=6, pady=6, sticky="ew")
    b4.bind("<Enter>", lambda e: b4.config(image=img_price_h))
    b4.bind("<Leave>", lambda e: b4.config(image=img_price))

    b5 = tk.Button(sec_frame, image=img_discord, command=on_discord, bd=0, bg=WIN_BG, activebackground=WIN_BG)
    b5.image = img_discord
    b5.grid(row=1, column=2, padx=6, pady=6, sticky="ew")
    b5.bind("<Enter>", lambda e: b5.config(image=img_discord_h))
    b5.bind("<Leave>", lambda e: b5.config(image=img_discord))

    footer = tk.Label(win, text="Liên hệ hỗ trợ: Discord: Yutoasagi / ZL: 0812144227", fg="#CFC6FF",
                      bg=WIN_BG, font=("Segoe UI", 9))
    footer.pack(side="bottom", pady=8)

    win.mainloop()
    cur, hw = read_key_from_ini()
    return cur is not None and hw == hwid
    
    win.update_idletasks()
    x = (win.winfo_screenwidth() - width) // 2
    y = (win.winfo_screenheight() - height) // 2
    win.geometry(f"{width}x{height}+{x}+{y}")
    
    # Title
    title = tk.Label(win, text="🔐 Xác Minh Key", fg="white", bg=WIN_BG,
                     font=("Consolas", 16, "bold"))
    title.pack(pady=(20,10))
    
    # Input Frame
    frm = tk.Frame(win, bg=WIN_BG)
    frm.pack(fill="both", expand=True, padx=20, pady=(0,20))
    
    inner = tk.Frame(frm, bg="#121212")
    inner.pack(padx=6, pady=6, fill="x")
    
    tk.Label(inner, text="Nhập Key", fg="#ddd", bg="#121212", anchor="w",
             font=("Consolas", 10)).pack(fill="x", padx=8, pady=(8,0))
    
    key_var = tk.StringVar()
    entry = tk.Entry(inner, textvariable=key_var, width=36, font=("Consolas", 11),
                     relief="flat", bg="#1a1a1a", fg="#fff", insertbackground="#fff")
    entry.pack(padx=8, pady=(6,10))
    entry.focus_set()
    
    msg_var = tk.StringVar(value="")
    msg_lbl = tk.Label(inner, textvariable=msg_var, fg="#ffcc00", bg="#121212",
                       font=("Consolas", 9))
    msg_lbl.pack(anchor="w", padx=8, pady=(0,8))
    
    status_var = tk.StringVar(value="Sẵn sàng")
    status_lbl = tk.Label(frm, textvariable=status_var, fg="#0F0", bg=WIN_BG,
                          font=("Consolas", 9))
    status_lbl.pack(anchor="w", pady=(0,10))
    
    key_verified = [False]
    
    def verify_key_onclick():
        key = key_var.get().strip()
        if not key:
            msg_var.set("Vui lòng nhập key!")
            return
        
        hwid = get_hwid()
        msg_var.set("Đang kiểm tra...")
        status_var.set("🔄 Kiểm tra")
        msg_lbl.update()
        
        status, expire_time_ms, is_lifetime = check_key(key, hwid)
        
        if status == "active":
            msg_var.set("✅ Kích hoạt thành công!")
            status_var.set("✅ Hợp lệ")
            msg_lbl.config(fg="#0F0")
            status_lbl.config(fg="#0F0")
            save_key_to_ini(key, hwid)
            key_verified[0] = True
            win.after(1500, win.destroy)
        elif status == "expired":
            msg_var.set("❌ Key đã hết hạn")
            status_var.set("❌ Hết hạn")
            msg_lbl.config(fg="#FF0000")
            status_lbl.config(fg="#FF0000")
        elif status == "hwid_mismatch":
            msg_var.set("❌ Key bị khóa HWID")
            status_var.set("❌ Không khớp HWID")
            msg_lbl.config(fg="#FF0000")
            status_lbl.config(fg="#FF0000")
        else:
            msg_var.set(f"❌ Lỗi: {status}")
            status_var.set("❌ Lỗi")
            msg_lbl.config(fg="#FF0000")
            status_lbl.config(fg="#FF0000")
    
    # Button
    btn_frame = tk.Frame(frm, bg=WIN_BG)
    btn_frame.pack(fill="x", pady=(10,0))
    
    verify_btn = tk.Button(btn_frame, text="✓ Xác Minh", bg="#2e7d32", fg="white",
                          font=("Consolas", 11, "bold"), relief="flat",
                          command=verify_key_onclick, cursor="hand2")
    verify_btn.pack(side="left", padx=(0,5))
    
    entry.bind("<Return>", lambda e: verify_key_onclick())
    
    win.mainloop()
    return key_verified[0]

def auto_detect_GTA5VN_path():
    """
    Tự động phát hiện subprocess_dir - Logic GIỐNG journey_bot 100%
    Quét TẤT CẢ tiến trình hệ thống, tìm có 'subprocess' trong path
    """
    print("[AUTO-DETECT] 🔍 Quét toàn bộ hệ thống tìm GTA5VN...")
    
    try:
        for proc in psutil.process_iter(['exe', 'name']):
            try:
                exe_path = proc.info.get('exe')
                if exe_path and 'subprocess' in exe_path.lower():
                    subprocess_dir = os.path.dirname(exe_path)
                    if os.path.exists(subprocess_dir):
                        print(f"[AUTO-DETECT] ✅ Tìm thấy: {subprocess_dir}")
                        return subprocess_dir
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
    except Exception as e:
        print(f"[AUTO-DETECT] ⚠️ Lỗi: {e}")
    
    print("[AUTO-DETECT] ❌ Không tìm thấy subprocess")
    return None


def wait_for_game_process(subprocess_dir):
    """Cửa sổ chờ tìm tiến trình game với 3 bước quét"""
    
    game_data = {
        'pid': None,
        'process_path': None,
        'module_name': None,
        'base_address': None,
        'step': 1,  # Bước hiện tại: 1, 2, 3
        'completed': False
    }
    
    # Tạo cửa sổ chờ
    wait_win = tk.Tk()
    wait_win.title(RANDOM_WINDOW_NAME)
    wait_win.geometry("600x400")
    wait_win.resizable(False, False)
    
    # Center window
    wait_win.update_idletasks()
    x = (wait_win.winfo_screenwidth() // 2) - (600 // 2)
    y = (wait_win.winfo_screenheight() // 2) - (400 // 2)
    wait_win.geometry(f"600x400+{x}+{y}")
    
    # Set icon
    icon_path = get_resource_path("L.ico")
    if icon_path and os.path.exists(icon_path):
        try:
            wait_win.iconbitmap(icon_path)
        except:
            pass
    
    wait_win.configure(bg="#1a1a2e")
    
    # Main container
    main_frame = tk.Frame(wait_win, bg="#16213e", relief=tk.RIDGE, bd=2)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Title
    title_label = tk.Label(main_frame, text="🎮 ĐANG KHỞI ĐỘNG TOOL", 
                           font=("Segoe UI", 18, "bold"),
                           fg="#4ecca3", bg="#16213e")
    title_label.pack(pady=(15, 10))
    
    # Separator
    sep = tk.Frame(main_frame, height=2, bg="#4ecca3")
    sep.pack(fill=tk.X, padx=20, pady=(0, 15))
    
    # Steps frame - Container để add bước động
    steps_frame = tk.Frame(main_frame, bg="#16213e")
    steps_frame.pack(pady=15, fill=tk.BOTH, expand=True)
    
    # Dictionary để lưu các bước đã tạo
    step_widgets = {}
    
    def create_step(step_num, text, status='loading'):
        """Tạo bước mới và thêm vào giao diện
        status: 'loading', 'success', 'error'
        """
        if step_num in step_widgets:
            return  # Đã tạo rồi thì không tạo nữa
        
        # Chọn màu background theo status
        if status == 'loading':
            bg_color = "#1e3a5f"
            icon = "🔄"
            fg_color = "#4ecca3"
        elif status == 'success':
            bg_color = "#1e5f3f"
            icon = "✅"
            fg_color = "#00ff88"
        else:  # error
            bg_color = "#5f1e1e"
            icon = "❌"
            fg_color = "#e74c3c"
        
        step_container = tk.Frame(steps_frame, bg=bg_color, relief=tk.FLAT, bd=1)
        step_container.pack(fill=tk.X, pady=8, padx=15)
        
        inner_frame = tk.Frame(step_container, bg=bg_color)
        inner_frame.pack(fill=tk.X, padx=10, pady=8)
        
        # Icon
        icon_label = tk.Label(inner_frame, text=icon, 
                             font=("Arial", 16),
                             fg=fg_color, bg=bg_color, width=2)
        icon_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Text
        text_label = tk.Label(inner_frame, text=text,
                             font=("Segoe UI", 12),
                             fg=fg_color, bg=bg_color,
                             anchor=tk.W)
        text_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        step_widgets[step_num] = {
            'container': step_container,
            'inner_frame': inner_frame,
            'icon': icon_label,
            'text': text_label
        }
    
    def update_step(step_num, status, detail=""):
        """Cập nhật trạng thái của bước đã tạo"""
        if step_num not in step_widgets:
            return
        
        widgets = step_widgets[step_num]
        
        if status == 'loading':
            bg_color = "#1e3a5f"
            icon = "🔄"
            fg_color = "#4ecca3"
        elif status == 'success':
            bg_color = "#1e5f3f"
            icon = "✅"
            fg_color = "#00ff88"
        else:  # error
            bg_color = "#5f1e1e"
            icon = "❌"
            fg_color = "#e74c3c"
        
        widgets['container'].config(bg=bg_color)
        widgets['inner_frame'].config(bg=bg_color)
        widgets['icon'].config(text=icon, fg=fg_color, bg=bg_color)
        widgets['text'].config(fg=fg_color, bg=bg_color)
        
        if detail:
            original_text = widgets['text'].cget('text').split(' - ')[0]
            widgets['text'].config(text=f"{original_text} - {detail}")
    
    # Progress indicator
    progress_label = tk.Label(main_frame, text="●", 
                             font=("Arial", 24),
                             fg="#4ecca3", bg="#16213e")
    progress_label.pack(pady=12)
    
    # Info label
    info_label = tk.Label(main_frame, 
                         text="Vui lòng đảm bảo GTA5VN đang chạy và bạn đã vào server...", 
                         font=("Segoe UI", 10),
                         fg="#5a6c7d", bg="#16213e",
                         justify=tk.CENTER, wraplength=500)
    info_label.pack(pady=(5, 15))
    
    # Scan counter
    scan_count = [0]
    
    def animate_progress():
        """Animate loading dots"""
        current = progress_label.cget("text")
        if len(current) >= 5:
            progress_label.config(text="●")
        else:
            progress_label.config(text=current + "●")
        
        if not game_data['completed']:
            wait_win.after(300, animate_progress)
    
    def scan_step_1():
        """Bước 1: Tìm tiến trình GTA5VN"""
        scan_count[0] += 1
        
        # Tạo bước 1 nếu chưa có
        if 1 not in step_widgets:
            create_step(1, "Tìm tiến trình GTA5VN", 'loading')
        else:
            update_step(1, 'loading')
        
        info_label.config(text=f"Đang quét tiến trình... (Lần {scan_count[0]})")
        
        pid, process_path, module_name = find_running_GTA5VN_subprocess(subprocess_dir)
        
        if pid is not None:
            # Tìm thấy process!
            game_data['pid'] = pid
            game_data['process_path'] = process_path
            game_data['module_name'] = module_name
            game_data['step'] = 2
            
            update_step(1, 'success')
            info_label.config(text=f"✅ Bước 1 hoàn thành! Đang chuyển sang bước 2...")
            
            # Chuyển sang bước 2 sau 800ms
            wait_win.after(800, scan_step_2)
        else:
            # Chưa tìm thấy, quét lại sau 2 giây
            update_step(1, 'loading')
            info_label.config(text=f"⏳ Chưa tìm thấy GTA5VN... Đang quét lại... (Lần {scan_count[0]})")
            wait_win.after(2000, scan_step_1)
    
    def scan_step_2():
        """Bước 2: Lấy Base Address"""
        # Tạo bước 2 lần đầu hiển thị
        if 2 not in step_widgets:
            create_step(2, "Lấy Base Address", 'loading')
        else:
            update_step(2, 'loading')
        info_label.config(text="🔄 Đang lấy Base Address từ module...")
        
        try:
            base_address = get_base_address_of_module(game_data['pid'], game_data['module_name'])
            
            if base_address and base_address != 0:
                game_data['base_address'] = base_address
                game_data['step'] = 3
                
                update_step(2, 'success')
                info_label.config(text=f"✅ Bước 2 hoàn thành! Đang chuyển sang bước 3...")
                
                # Chuyển sang bước 3 sau 800ms
                wait_win.after(800, scan_step_3)
            else:
                # Không lấy được base address
                update_step(2, 'error')
                info_label.config(text="❌ Không thể lấy Base Address! Thử lại sau 2s...")
                wait_win.after(2000, scan_step_2)
        except Exception as e:
            update_step(2, 'error')
            info_label.config(text=f"❌ Lỗi: {str(e)[:50]}... Thử lại sau 2s...")
            wait_win.after(2000, scan_step_2)
    
    step_3_retry = [0]
    def scan_step_3():
        """Bước 3: Kiểm tra kết nối game"""
        step_3_retry[0] += 1
        # Tạo bước 3 lần đầu hiển thị
        if 3 not in step_widgets:
            create_step(3, "Bước 3: Kiểm tra kết nối game", 'loading')
        else:
            update_step(3, 'loading')
        info_label.config(text=f"🔄 Đang kiểm tra kết nối với game... (Lần {step_3_retry[0]})")
        
        try:
            # Thử đọc dữ liệu từ game
            world_offset = BUILD_OFFSETS.get("b2189", {}).get("world_ptr")
            if world_offset:
                ped_address = get_local_player_ped_address(
                    game_data['pid'], 
                    game_data['base_address'], 
                    world_offset
                )
                
                if ped_address and ped_address > 0:
                    # Kết nối thành công!
                    update_step(3, 'success', "Kết nối OK")
                    info_label.config(text="✅ Hoàn thành tất cả 3 bước!\nĐang khởi động giao diện chính...")
                    progress_label.config(text="✓", fg="#00ff88")
                    
                    game_data['completed'] = True
                    
                    # Đóng cửa sổ sau 1.2 giây
                    wait_win.after(1200, wait_win.quit)
                else:
                    if step_3_retry[0] >= 5:
                        # Thử 5 lần không thấy dữ liệu ped -> có thể chọn nhầm PID, quay lại bước 1 quét lại
                        step_3_retry[0] = 0
                        info_label.config(text="⏳ Đang quét lại tiến trình game...")
                        wait_win.after(1000, scan_step_1)
                    else:
                        update_step(3, 'loading')
                        info_label.config(text=f"⏳ Chưa phát hiện dữ liệu game... Vui lòng vào server! ({step_3_retry[0]}/5)")
                        wait_win.after(2000, scan_step_3)
            else:
                update_step(3, 'error')
                info_label.config(text="❌ Không tìm thấy offset game!")
                wait_win.after(2000, scan_step_3)
        except Exception as e:
            update_step(3, 'error')
            info_label.config(text=f"❌ Lỗi: {str(e)[:50]}... Thử lại sau 2s...")
            wait_win.after(2000, scan_step_3)
    
    # Bắt đầu animation và quét từ bước 1
    animate_progress()
    scan_step_1()
    
    # Xử lý đóng cửa sổ - Chỉ cho phép đóng khi hoàn thành
    def on_closing():
        if not game_data['completed']:
            # Chưa hoàn thành 3 bước → Thoát tool
            print("[GAME] ❌ Người dùng đóng cửa sổ. Thoát tool...")
            sys.exit(0)
        else:
            # Đã hoàn thành → Tiếp tục
            wait_win.quit()
    
    wait_win.protocol("WM_DELETE_WINDOW", on_closing)
    
    try:
        wait_win.mainloop()
        wait_win.destroy()
    except:
        pass
    
    # Kiểm tra BẮT BUỘC - CHỈ return khi hoàn thành đủ 3 bước
    if not game_data['completed']:
        print("[GAME] ❌ Không hoàn thành 3 bước quét! Thoát tool...")
        sys.exit(1)
    
    # Kiểm tra dữ liệu trả về
    if (game_data['pid'] is None or 
        game_data['base_address'] is None or 
        game_data['base_address'] == 0):
        print("[GAME] ❌ Dữ liệu không đầy đủ! Thoát tool...")
        sys.exit(1)
    
    return game_data['pid'], game_data['process_path'], game_data['module_name'], game_data['base_address']

# ====================================================================
# I. CẤU HÌNH NGƯỜI DÙNG & BIẾN TOÀN CỤC
# ====================================================================

# 📁 KHÔNG CÒN DÙNG config.json - Tool sẽ tự động detect mỗi lần khởi động
SUBPROCESS_DIR = None  # Sẽ được detect hoặc hỏi khi khởi động

# 🎯 ĐỊNH NGHĨA BUILD ID MỤC TIÊU (Hardcode - không thay đổi)
TARGET_BUILD_ID = "b2189" 
PLAYER_PED_OFFSET = 0x8 

# MOUSE/KEY SIMULATION SETUP
user32 = ctypes.windll.user32
MOUSEEVENTF_MOVE = 0x0001
KEY_TOGGLE = '='
KEY_FORWARD = 'w'
KEY_AUTORUN = '.'
KEY_SPACE = 'space' 
AIM_TOLERANCE_DEGREES = 2 
MOVE_DISTANCE_THRESHOLD = 10
CHOP_COOLDOWN_SECONDS = 45 
SPACE_PRESS_INTERVAL_SECONDS = 2.0 
AIM_SMOOTHING_FACTOR = 0.3  # 🔧 Tăng từ 0.3 → 0.7 để fix khựng chuột (aim mượt + nhanh, 0.8-1.0 = quá nhanh)

# GUI/RADAR SETUP
RADAR_SIZE = 250        
RADAR_RANGE = 60.0      
READ_INTERVAL_MS = 10  # Giảm từ 100 để bot phản ứng nhanh hơn (ai mượt hơn)
TRIANGLE_SIZE = 6       

# BOT STATUS
is_bot_active = False 
is_moving = False 
g_tree_cooldowns = {} 
g_last_space_time = 0.0

# CHOP STATUS (để hiển thị trên GUI)
chop_state = "IDLE"
spam_e_count = 0
spam_key = "None"
is_chopping = False  # Flag để biết đang trong quá trình chặt cây
keys_pressed = ""  # Hiển thị phím đang được bấm 

# TREE COUNT & LIMIT
total_trees_chopped = 0  # Số cây đã chặt
tree_chop_limit = 20  # Số cây muốn chặt (0 = unlimited)
should_stop_bot = False  # Flag để dừng bot khi đạt limit

# SELL FEATURE
auto_sell_enabled = True  # Bật/tắt chức năng bán gỗ
is_selling = False  # Đang trong quá trình bán gỗ
is_returning = False  # Đang quay về sau khi bán
is_going_to_random_start = False  # Đang đi đến random start point sau khi quay về
random_start_target = None  # Tọa độ random start point được chọn

# JUMPING FEATURE (Nhảy khi đi bán/quay về)
auto_jumping_enabled = False  # Bật/tắt nhảy tự động khi đi bán/quay về
jumping_thread = None  # Thread quản lý nhảy
last_jump_time = 0.0  # Thời điểm nhảy cuối cùng
JUMP_INTERVAL_SECONDS = random.uniform(2.0, 5.0)  # Nhảy mỗi 1 giây
JUMP_PRESS_DURATION = 0.25  # Nhấn space 0.25 giây
sell_point_index = 0  # Chỉ số điểm bán hiện tại (dùng cho cả bán lẫn quay về)
is_bot_paused = False  # ⏸️ PAUSE BOT (nhấn PAUSE để tạm dừng mà không reset)

# ====================================================================
# AUTO RELOGIN LAUNCHER CONFIG & GLOBALS
# ====================================================================
ACCOUNT_FILE = os.path.join(SCRIPT_DIR, "login_account.json")

def load_account_info():
    default_info = {"username": "frost35912", "password": "frost35912", "auto_relogin": 1}
    if os.path.exists(ACCOUNT_FILE):
        try:
            with open(ACCOUNT_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {**default_info, **data}
        except Exception:
            pass
    return default_info

def save_account_info(username, password, auto_relogin=1):
    try:
        with open(ACCOUNT_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "username": username,
                "password": password,
                "auto_relogin": 1 if auto_relogin else 0
            }, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

login_account_data = load_account_info()
login_username = login_account_data.get("username", "frost35912")
login_password = login_account_data.get("password", "frost35912")
auto_relogin_enabled = bool(login_account_data.get("auto_relogin", 1))
last_launcher_action_time = 0.0
connecting_stuck_start_time = 0.0
last_auto_launch_time = 0.0


# ========== MULTIPLE SELL ROUTES (RANDOM SELECT MỖI LẦN BÁN) ==========
# Mỗi route là 1 tập hợp special_locations khác nhau
# sell_sequence và return_sequence CỐ ĐỊNH (không đổi theo route)

SELL_ROUTES = [
    {
        "name": "Route 1",
        "special_locations": [
            (-564.02, 5355.9),
            (-556.99, 5433.75),
            (-550.78, 5418.73),
            (-553.61, 5408.15),
            (-557.51, 5383.63),
            (-577.39, 5343.53),
            (-573.8, 5314.94),
        ]
    },
    {
        "name": "Route 2",
        "special_locations": [
            (-555.28, 5436.15),
            (-552.95, 5429.27),
            (-550.79, 5414.0),
            (-555.43, 5390.0),
            (-565.88, 5363.38),
            (-577.29, 5326.97),
            (-573.8, 5314.94),
        ]
    },
    {
        "name": "Route 3",
        "special_locations": [
            (-560.11, 5432.1),
            (-560.11, 5432.1),
            (-553.19, 5414.47),
            (-552.53, 5400.51),
            (-555.46, 5387.21),
            (-575.30, 5320.86),
            (-573.8, 5314.94),
        ]
    },
    {
        "name": "Route 4",
        "special_locations": [
            (-549.52, 5426.93),
            (-549.52, 5426.93),
            (-547.13, 5412.73),
            (-551.56, 5390.88),
            (-565.14, 5374.29),
            (-581.37, 5334.29),
            (-573.8, 5314.94),
        ]
    },
    {
        "name": "Route 5",
        "special_locations": [
            (-557.91, 5427.45),
            (-558.12, 5427.71),
            (-555.17, 5419.69),
            (-553.13, 5402.80),
            (-557.17, 5383.80),
            (-577.38, 5325.54),
            (-573.8, 5314.94),
        ]
    },
    {
        "name": "Route 6",
        "special_locations": [
            (-557.91, 5427.45),
            (-558.12, 5427.71),
            (-555.17, 5419.69),
            (-553.13, 5402.80),
            (-557.17, 5383.80),
            (-577.38, 5325.54),
            (-573.8, 5314.94),
        ]
    },
    {
        "name": "Route 7",
        "special_locations": [
            (-564.02, 5355.9),      # Index 0
            (-556.99, 5433.75),     # Index 1
            (-552.45, 5416.44),     # Index 2
            (-550.88, 5405.19),     # Index 3
            (-555.14, 5386.55),     # Index 4
            (-581.99, 5323.05),     # Index 5
            (-573.8, 5314.94),     # Index 6 (NPC)
        ]
    }
]

# CỐ ĐỊNH - Chuỗi chỉ số không đổi theo route
# Đường bán: Đi từ điểm 1 → 1 → 3 → 4 → 5 → 6(NPC)
sell_sequence = [1, 1, 3, 4, 5, 6]

# Đường quay về: Quay từ điểm 5 → 4 → 3 → 2 → 1 (quay ngược lại từ NPC)
return_sequence = [5, 4, 3, 2, 1]

# Biến hiện tại (sẽ được load từ route được chọn)
current_route = SELL_ROUTES[0]
current_special_locations = current_route["special_locations"]
current_route_name = current_route["name"]  # Tên route hiện tại

# sell_click_positions = [
#     (621, 889),   # Vị trí 1
#     (724, 206),   # Vị trí 2
#     (512, 562)    # Vị trí 3 (nhấn nhiều lần bằng số cây chặt)
# ]
sell_click_positions = [
    (302, 531),   # Vị trí 1
    (400, 29),   # Vị trí 2
    (420, 383)    # Vị trí 3 (nhấn nhiều lần bằng số cây chặt)
]
sell_click_count = 0  # Số lần nhấn vị trí 3
random_start_locations = []  # Danh sách random start locations (load từ HARDCODED_LOCATIONS)

# WOODCUTTING FEATURE (CƯA GỖ - chức năng riêng biệt từ bán gỗ)
enable_woodcutting = True  # Bật/tắt chức năng cưa gỗ
sawmill_locations = [
    {"x": -574.53, "y": 5364.5, "z": 70.23, "yaw": -1.4856, "type": "sawmill", "aiming_at": {"x": -576.52, "y": 5364.67}},
    {"x": -576.19, "y": 5358.68, "z": 70.22, "yaw": -1.2366, "type": "sawmill", "aiming_at": {"x": -578.08, "y": 5359.33}},
    {"x": -577.91, "y": 5353.04, "z": 70.21, "yaw": -1.2545, "type": "sawmill", "aiming_at": {"x": -579.81, "y": 5353.67}},
    {"x": -579.66, "y": 5346.3, "z": 70.24, "yaw": -1.209, "type": "sawmill", "aiming_at": {"x": -581.53, "y": 5347.0}},
    {"x": -581.74, "y": 5339.37, "z": 70.21, "yaw": -1.2326, "type": "sawmill", "aiming_at": {"x": -583.63, "y": 5340.03}},
    {"x": -579.15, "y": 5365.97, "z": 70.26, "yaw": -1.2215, "type": "sawmill", "aiming_at": {"x": -581.03, "y": 5366.66}},
    {"x": -581.02, "y": 5360.0, "z": 70.24, "yaw": -1.2801, "type": "sawmill", "aiming_at": {"x": -582.94, "y": 5360.57}},
    {"x": -582.65, "y": 5354.12, "z": 70.26, "yaw": -1.2026, "type": "sawmill", "aiming_at": {"x": -584.52, "y": 5354.84}},
    {"x": -584.51, "y": 5347.32, "z": 70.3, "yaw": -1.1896, "type": "sawmill", "aiming_at": {"x": -586.36, "y": 5348.06}},
    {"x": -586.2, "y": 5340.69, "z": 70.21, "yaw": -1.1841, "type": "sawmill", "aiming_at": {"x": -588.05, "y": 5341.45}},
]  # Danh sách máy cưa - hardcode để tránh đọc file
current_sawmill = None  # Máy cưa hiện tại để cưa
is_woodcutting = False  # Đang trong quá trình cưa gỗ
is_plank_sell = False  # Flag để bán plank (ván gỗ) thay vì wood khi sau cưa
woodcut_state = "IDLE"  # Trạng thái: IDLE, AIMING, WAITING_FOR_UI, CUTTING
woodcut_wood_selected = False  # Đã chọn ván gỗ chưa
woodcut_last_right_click_time = 0  # Thời gian spam right-click lần cuối
woodcut_template_lost_time = 0  # Thời điểm go.png biến mất (để chờ 20s rồi ESC)

# ===== BACKGROUND THREAD DETECTION REALTIME (MSS) =====
template_detection_thread = None  # Background thread
template_detection_running = True  # Flag để dừng thread
template_detection_lock = threading.Lock()  # Lock để thread-safe
cached_go_detected = False  # Cache: đã detect go.png?
cached_vango_detected = False  # Cache: đã detect vango.png?
TEMPLATE_DETECT_INTERVAL = 30  # Detect mỗi 30ms (nhanh hơn, ~33 FPS)

# Template detection (converted to 1280x720)
# Vị trí chính xác tìm được từ debug tool: (633, 458) - (718, 544)
# Size: 85×86 pixels
TEMPLATE_REGION_X1 = 633  # Left
TEMPLATE_REGION_Y1 = 458  # Top
TEMPLATE_REGION_X2 = 806  # Right
TEMPLATE_REGION_Y2 = 544  # Bottom

# Woodcut click coordinates
# Woodcut click coordinates (1280x720)
WOODCUT_WOOD_CLICK_X = 676  # Chọn ván gỗ (676 - 320)
WOODCUT_WOOD_CLICK_Y = 275  # Chọn ván gỗ (275 - 180)
WOODCUT_RIGHT_CLICK_X = 389  # Spam right-click (389 - 320)
WOODCUT_RIGHT_CLICK_Y = 511 # Spam right-click (511 - 180)

# PROCESS & ERROR RECOVERY
read_error_count = 0  # Đếm số lần lỗi đọc dữ liệu liên tiếp
last_rescan_time = 0.0  # Thời điểm quét lần cuối
RESCAN_INTERVAL = 2.0  # Quét lại sau 2 giây nếu lỗi liên tục
MAX_ERROR_BEFORE_RESCAN = 3  # Lỗi 3 lần liên tiếp thì quét lại

# ANTI-STUCK STATUS
last_player_pos = (0, 0)  # Vị trí trước đó để kiểm tra di chuyển
last_distance = None  # Khoảng cách cuối cùng đến target
last_change_time = None  # Thời điểm cuối có thay đổi khoảng cách
last_anti_stuck_time = 0.0  # Thời điểm cuối thực hiện anti-stuck
anti_stuck_active = False  # Đang thực hiện hành động chống kẹt
DISTANCE_CHANGE_THRESHOLD = 0.15  # Ngưỡng thay đổi khoảng cách (0.15m)

# NEW ANTI-STUCK LOGIC - Track 20s per target
stuck_check_start_time = 0.0  # Thời điểm bắt đầu track target hiện tại
stuck_check_target_coord = None  # Tọa độ target hiện tại (để detect khi thay đổi)

# ========== SELL SEQUENCE BYPASS LOGIC (Tránh obstacles) ==========
sell_bypass_waypoints = [(-548.57, 5406.9), (-533.39, 5412.46), (-536.69, 5416.86), (-545.11, 5419.41), (-551.40, 5409.86)]  # 3 điểm bypass
sell_bypass_mode = False  # Đang trong chế độ bypass
sell_bypass_index = 0  # Chỉ số điểm bypass hiện tại (0-2)
sell_bypass_original_point_index = None  # Lưu sell_point_index trước khi vào bypass


# CẤU HÌNH SPAM CỦA NGƯỜI DÙNG
# ====================================================================
# CHUYỂN ĐỔI TỌA ĐỘ: 1920x1080 → 1280x720 (game ở giữa màn hình)
# Offset: X = (1920-1280)/2 = 320, Y = (1080-720)/2 = 180
# Công thức: new_coord = old_coord - offset
# ====================================================================

# --- TỌA ĐỘ CŨ (1920x1080 - FULLSCREEN) ---
# CHECK_X, CHECK_Y = 779, 496  # Cũ hơn
# CHECK_X, CHECK_Y = 765, 500  # Đang dùng
# POINT_BASE = (960, 570)
# POINT_MATCH1 = (962, 560)
# POINT_MATCH2 = (960, 580)

# --- TỌA ĐỘ MỚI (1280x720 - WINDOWED MODE Ở GIỮA MÀN 1920x1080) ---
CHECK_X, CHECK_Y = 445, 320  # 765 - 320 = 445, 500 - 180 = 320
POINT_BASE = (640, 390)       # 960 - 320 = 640, 570 - 180 = 390
POINT_MATCH1 = (642, 380)     # 962 - 320 = 642, 560 - 180 = 380
POINT_MATCH2 = (640, 400)     # 960 - 320 = 640, 580 - 180 = 400

EXPECTED_COLOR = 0x7ED320
EXPECTED_TOLERANCE = 10

REGION_MIN_X = min(CHECK_X, POINT_BASE[0], POINT_MATCH1[0], POINT_MATCH2[0])
REGION_MIN_Y = min(CHECK_Y, POINT_BASE[1], POINT_MATCH1[1], POINT_MATCH2[1])
REGION_MAX_X = max(CHECK_X, POINT_BASE[0], POINT_MATCH1[0], POINT_MATCH2[0])
REGION_MAX_Y = max(CHECK_Y, POINT_BASE[1], POINT_MATCH1[1], POINT_MATCH2[1])
REGION_WIDTH = REGION_MAX_X - REGION_MIN_X + 1
REGION_HEIGHT = REGION_MAX_Y - REGION_MIN_Y + 1

# ====================================================================
# HARDCODED LOCATIONS (Ẩn logic - không đọc từ file)
# ====================================================================
HARDCODED_LOCATIONS = [
    # SPECIAL LOCATIONS (Bán hàng + Quay về)
    {"x": -564.02,"y": 5355.9,"type": "special"},
    {"x": -556.99,"y": 5433.75,"type": "special"},
    {"x": -552.45,"y": 5416.44,"type": "special"},
    {"x": -550.88,"y": 5405.19,"type": "special"},
    {"x": -555.14,"y": 5386.55,"type": "special"},
    # {"x": -580.37,"y": 5317.74,"type": "special"},
    {"x": -581.99,"y": 5323.05,"type": "special"},
    {"x": -573.76,"y": 5314.34,"type": "special"},
    
    # RANDOM START LOCATIONS (Sau khi bán xong quay về, random 1 điểm này)
    {"x": -577.60, "y": 5427.10, "type": "random_start"},
    {"x": -586.84, "y": 5446.84, "type": "random_start"},
    {"x": -592.19, "y": 5447.92, "type": "random_start"},
    {"x": -594.11, "y": 5450.96, "type": "random_start"},
    {"x": -596.84, "y": 5473.53, "type": "random_start"},
    {"x": -589.14, "y": 5493.65, "type": "random_start"},
    {"x": -584.47, "y": 5492.91, "type": "random_start"},
    {"x": -572.59, "y": 5507.65, "type": "random_start"},
    {"x": -566.36, "y": 5504.28, "type": "random_start"},
    {"x": -555.74, "y": 5511.14, "type": "random_start"},
    {"x": -541.56, "y": 5492.16, "type": "random_start"},
    {"x": -537.72, "y": 5490.34, "type": "random_start"},
    {"x": -539.19, "y": 5484.06, "type": "random_start"},
    {"x": -561.66, "y": 5461.37, "type": "random_start"},
    {"x": -565.07, "y": 5458.14, "type": "random_start"},
    {"x": -518.10, "y": 5510.49, "type": "random_start"},
    {"x": -534.64, "y": 5538.33, "type": "random_start"},
    {"x": -537.71, "y": 5548.10, "type": "random_start"},
    {"x": -537.24, "y": 5553.58, "type": "random_start"},
    {"x": -525.29, "y": 5560.00, "type": "random_start"},
    {"x": -523.80, "y": 5569.12, "type": "random_start"},
    {"x": -507.74, "y": 5563.14, "type": "random_start"},
    {"x": -487.31, "y": 5544.93, "type": "random_start"},
    
    # NORMAL LOCATIONS (Chặt cây)

    {"x": -577.6, "y": 5427.1, "type": "normal"},
    {"x": -586.84, "y": 5446.84, "type": "normal"},
    {"x": -592.19, "y": 5447.92, "type": "normal"},
    {"x": -594.11, "y": 5450.96, "type": "normal"},
    {"x": -596.84, "y": 5473.53, "type": "normal"},
    {"x": -589.14, "y": 5493.65, "type": "normal"},
    {"x": -584.47, "y": 5492.91, "type": "normal"},
    {"x": -572.59, "y": 5507.65, "type": "normal"},
    {"x": -566.36, "y": 5504.28, "type": "normal"},
    {"x": -555.74, "y": 5511.14, "type": "normal"},
    {"x": -541.56, "y": 5492.16, "type": "normal"},
    {"x": -537.72, "y": 5490.34, "type": "normal"},
    {"x": -539.19, "y": 5484.06, "type": "normal"},
    {"x": -561.66, "y": 5461.37, "type": "normal"},
    {"x": -565.07, "y": 5458.14, "type": "normal"},
    {"x": -518.1, "y": 5510.49, "type": "normal"},
    {"x": -534.64, "y": 5538.33, "type": "normal"},
    {"x": -537.71, "y": 5548.1, "type": "normal"},
    {"x": -537.24, "y": 5553.58, "type": "normal"},
    {"x": -525.29, "y": 5560.0, "type": "normal"},
    {"x": -523.8, "y": 5569.12, "type": "normal"},
    {"x": -507.74, "y": 5563.14, "type": "normal"},
    {"x": -487.31, "y": 5544.93, "type": "normal"},
]

# TÊN FILE CHỨA TẤT CẢ TỌA ĐỘ (NORMAL VÀ SPECIAL)
# LOCATION_FILE = "location.json" 

# Cấu trúc Offset Tĩnh (Static)
BUILD_OFFSETS = {
    "b2189": {
        "world_ptr": 0x24E6D90,                 
        "CamGameplayDirector_ptr": 0x1F89768,   
        "Coords_X": 0x90,                       
        "Ped_Forward_X": 0x80,                  
        "Ped_Forward_Y": 0x84,                  
        "Camera_Struct_Offset": 0x2C0,          
        "View_Angles_X": 0x40,                  
    }
}

# GUI Globals
root = None
canvas = None
info_labels = {}
log_text = None  # Text widget để hiển thị log
toggle_btn = None  # Nút bật/tắt bot
tree_limit_entry = None  # Entry field cho số cây muốn chặt

# ====================================================================
# II. ĐỊNH NGHĨA API VÀ CÁC HÀM HỖ TRỢ ĐỌC BỘ NHỚ & TẢI DATA
# ====================================================================
PROCESS_VM_READ = 0x0010
PROCESS_QUERY_INFORMATION = 0x0400

kernel32 = ctypes.windll.kernel32
OpenProcess = kernel32.OpenProcess
ReadProcessMemory = kernel32.ReadProcessMemory
CloseHandle = kernel32.CloseHandle
psapi = ctypes.windll.psapi

try:
    OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    OpenProcess.restype = wintypes.HANDLE
    ReadProcessMemory.argtypes = [wintypes.HANDLE, wintypes.LPCVOID, wintypes.LPVOID, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]
    ReadProcessMemory.restype = wintypes.BOOL
    psapi.EnumProcessModulesEx.argtypes = [wintypes.HANDLE, wintypes.LPVOID, wintypes.DWORD, ctypes.POINTER(wintypes.DWORD), wintypes.DWORD]
    psapi.EnumProcessModulesEx.restype = wintypes.DWORD
    psapi.GetModuleBaseNameW.argtypes = [wintypes.HANDLE, wintypes.HMODULE, wintypes.LPWSTR, wintypes.DWORD]
    psapi.GetModuleBaseNameW.restype = wintypes.DWORD
except AttributeError:
    pass

def read_memory(hProcess, address, size=8, is_float=False, is_int32=False): 
    buffer = (ctypes.c_byte * size)()
    bytes_read = ctypes.c_size_t(0)
    if ReadProcessMemory(hProcess, wintypes.LPCVOID(address), buffer, size, ctypes.byref(bytes_read)):
        data = bytes(buffer)
        if is_float:
            return ctypes.c_float.from_buffer_copy(buffer).value if size == 4 else ctypes.c_double.from_buffer_copy(buffer).value
        return int.from_bytes(data, byteorder='little')
    return None

def read_pointer_chain(pid, base_address, offsets, size=8, is_float=False):
    hProcess = OpenProcess(PROCESS_VM_READ, False, pid) 
    if not hProcess: return None
    current_address = base_address
    for offset in offsets[:-1]:
        read_addr = current_address + offset
        next_ptr = read_memory(hProcess, read_addr, size=8)
        if next_ptr is None or next_ptr == 0:
            CloseHandle(hProcess)
            return None
        current_address = next_ptr
    final_offset = offsets[-1] if offsets else 0
    final_read_addr = current_address + final_offset
    final_value = read_memory(hProcess, final_read_addr, size=size, is_float=is_float)
    CloseHandle(hProcess)
    return final_value

def find_running_GTA5VN_subprocess(subprocess_dir):
    """
    Tìm tiến trình game GTA5VN
    Quét TẤT CẢ tiến trình hệ thống, tìm có 'subprocess' trong path
    Loại trừ launcher/service và ưu tiên tiến trình game thật
    """
    print("[GAME] 🔍 Quét toàn bộ hệ thống tìm tiến trình game...")
    
    candidates = []
    
    try:
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                exe_path = proc.info.get('exe')
                proc_name = proc.info.get('name') or ''
                
                if not exe_path or 'subprocess' not in exe_path.lower():
                    continue
                
                # Loại trừ service files và launcher (ROSLauncher, Launcher, etc.)
                if any(x in proc_name.lower() for x in ['dumpserver', 'rosservice', 'chrome', 'steam', 'launcher', 'crashpad', 'helper', 'updater']):
                    continue
                
                candidates.append({
                    'pid': proc.info['pid'],
                    'name': proc_name,
                    'exe': exe_path,
                    'name_length': len(proc_name)
                })
                print(f"[GAME]   ✓ {proc_name} (PID: {proc.info['pid']})")
                        
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
    except Exception as e:
        print(f"[GAME] ⚠️ Lỗi: {e}")
    
    if candidates:
        def sort_priority(item):
            n = item['name'].lower()
            if 'gameprocess' in n:
                return (0, item['name_length'])
            elif 'gta' in n:
                return (1, item['name_length'])
            else:
                return (2, item['name_length'])

        candidates.sort(key=sort_priority)
        best = candidates[0]
        print(f"[GAME] ✅ Chọn: {best['name']} (PID: {best['pid']})")
        return best['pid'], best['exe'], best['name']
    
    print("[GAME] ❌ Không tìm thấy")
    return None, None, None

def get_base_address_of_module(pid, module_name):
    """
    Lấy base address của module game.
    Với game bị spoof name, module_name sẽ là tên exe thật.
    """
    permissions = PROCESS_QUERY_INFORMATION | PROCESS_VM_READ 
    hProcess = OpenProcess(permissions, False, pid)
    if not hProcess: 
        return 0
    
    hModules = (wintypes.HMODULE * 1024)()
    cb = ctypes.sizeof(hModules)
    cbNeeded = wintypes.DWORD()
    
    if psapi.EnumProcessModulesEx(hProcess, hModules, cb, ctypes.byref(cbNeeded), 0x03):
        module_count = cbNeeded.value // ctypes.sizeof(wintypes.HMODULE)
        
        # Duyệt qua tất cả modules để tìm module game
        for i in range(module_count):
            hModule = hModules[i]
            module_name_buf = ctypes.create_unicode_buffer(260)
            
            # Lấy tên module
            if psapi.GetModuleBaseNameW(hProcess, hModule, module_name_buf, 260):
                current_module_name = module_name_buf.value
                
                # So sánh tên module (case-insensitive)
                if current_module_name.lower() == module_name.lower():
                    CloseHandle(hProcess)
                    return hModule
        
        # Nếu không tìm thấy module phù hợp, trả về module đầu tiên (main exe)
        # Đây thường là module game thật với các game bị spoof
        if module_count > 0:
            CloseHandle(hProcess)
            return hModules[0]
    
    CloseHandle(hProcess)
    return 0

def get_game_build_offsets(build_id):
    if build_id.lower() not in BUILD_OFFSETS:
        log_message(f"\n!!! LỖI QUAN TRỌNG !!! Build ID '{build_id}' không tồn tại trong cấu hình BUILD_OFFSETS.")
        return None, None
    return build_id, BUILD_OFFSETS.get(build_id.lower())

def get_local_player_ped_address(pid, base_address, world_offset):
    return read_pointer_chain(pid, base_address, [world_offset, PLAYER_PED_OFFSET], size=8)

def read_player_data(pid, ped_address, offsets):
    if ped_address is None or ped_address == 0: return None
    data = {}
    hProcess = OpenProcess(PROCESS_VM_READ, False, pid)
    if not hProcess: return None
    
    coords_offset = offsets.get("Coords_X")
    if coords_offset:
        data['X'] = read_memory(hProcess, ped_address + coords_offset, size=4, is_float=True)
        data['Y'] = read_memory(hProcess, ped_address + coords_offset + 0x4, size=4, is_float=True)
    
    forward_x_offset = offsets.get("Ped_Forward_X")
    forward_y_offset = offsets.get("Ped_Forward_Y")
    
    if forward_x_offset: data['Forward_X'] = read_memory(hProcess, ped_address + forward_x_offset, size=4, is_float=True)
    if forward_y_offset: data['Forward_Y'] = read_memory(hProcess, ped_address + forward_y_offset, size=4, is_float=True)
        
    fx, fy = data.get('Forward_X'), data.get('Forward_Y')
    if fx is not None and fy is not None:
         data['PedYawRad'] = math.atan2(fx, fy) 
         
    CloseHandle(hProcess)
    return data

def read_camera_data(pid, base_address, offsets):
    director_offset = offsets.get("CamGameplayDirector_ptr") 
    cam_struct_offset = offsets.get("Camera_Struct_Offset") 
    view_angles_offset = offsets.get("View_Angles_X") 

    if not all([director_offset, cam_struct_offset, view_angles_offset]): return None

    camera_ptr = read_pointer_chain(pid, base_address, [director_offset, cam_struct_offset], size=8)
    data = {"Camera_Ptr": camera_ptr}

    if camera_ptr and camera_ptr > 0x100000:
        hProcess = OpenProcess(PROCESS_VM_READ, False, pid)
        if not hProcess: return None
        
        data['AngleX_Raw'] = read_memory(hProcess, camera_ptr + view_angles_offset, size=4, is_float=True) 
        data['AngleY_Raw'] = read_memory(hProcess, camera_ptr + view_angles_offset + 0x4, size=4, is_float=True) 
        
        raw_x, raw_y = data.get('AngleX_Raw'), data.get('AngleY_Raw')
        if raw_x is not None and raw_y is not None:
             data['CamYawRad'] = math.atan2(raw_x, raw_y)
        else:
             data['CamYawRad'] = None 
             
        CloseHandle(hProcess)
    
    return data

def load_and_filter_locations():
    """Tải tọa độ từ dữ liệu hardcoded thay vì file JSON"""
    normal_locations = []
    special_locations = []
    random_start_locations = []
    
    try:
        # Sử dụng dữ liệu hardcoded
        all_locations = HARDCODED_LOCATIONS
        
        if not isinstance(all_locations, list):
            log_message(f"[LOAD ERROR] Dữ liệu tọa độ không phải là list hợp lệ.")
            return normal_locations, special_locations, random_start_locations
            
        for item in all_locations:
            if isinstance(item, dict):
                point_type = item.get('type')
                if point_type == "normal":
                    normal_locations.append(item)
                elif point_type == "special":
                    special_locations.append(item)
                elif point_type == "random_start":
                    random_start_locations.append(item)
        
       
    except Exception as e:
        log_message(f"[LOAD ERROR] Lỗi khi tải dữ liệu tọa độ: {e}")
         
    return normal_locations, special_locations, random_start_locations

def select_random_route():
    """Random chọn 1 route để bán gỗ (tránh pattern detection)"""
    global current_route, current_special_locations, current_route_name
    
    current_route = random.choice(SELL_ROUTES)
    current_special_locations = current_route["special_locations"]
    current_route_name = current_route["name"]
    
    log_message(f"[ROUTE] 🗺️ Chọn route ngẫu nhiên: {current_route['name']}")
    return current_special_locations

# ====================================================================
# III. LOGIC AIMING VÀ MOVEMENT (CTYPES/KEYBOARD)
# ====================================================================

def move_mouse_relative(dx, dy):
    user32.mouse_event(MOUSEEVENTF_MOVE, int(dx), int(dy), 0, 0)

def calculate_mouse_movement(delta_yaw_rad):
    YAW_PER_PIXEL = (2 * math.pi) / 10000.0 
    dx = delta_yaw_rad / YAW_PER_PIXEL
    return -dx 

def normalize_angle_rad(angle):
    while angle > math.pi:
        angle -= 2 * math.pi
    while angle <= -math.pi:
        angle += 2 * math.pi
    return angle

def manage_auto_jumping():
    """Thread function để quản lý nhảy tự động mỗi 1 giây. Dùng cho selling/returning."""
    global auto_jumping_enabled, last_jump_time, woodcut_state
    
    while auto_jumping_enabled:
        current_time = time.time()
        
        # Nếu đang aim vào máy cưa (woodcut_state == "AIMING"), không nhảy
        if woodcut_state == "AIMING":
            time.sleep(0.1)
            continue
        
        # Nhảy mỗi JUMP_INTERVAL_SECONDS giây
        if current_time - last_jump_time >= JUMP_INTERVAL_SECONDS:
            try:
                # Nhấn space 0.25 giây để nhảy
                keyboard.press('space')
                time.sleep(JUMP_PRESS_DURATION)
                keyboard.release('space')
                last_jump_time = current_time
                log_message(f"[JUMP] ↑ Nhảy lúc {current_time:.2f}")
            except Exception as e:
                log_message(f"[JUMP] ⚠️ Lỗi nhảy: {e}")
        
        time.sleep(0.05)  # Check mỗi 0.05s để không block CPU
    
    log_message(f"[JUMP] ⏹️ Dừng nhảy tự động")

def start_auto_jumping():
    """Bật nhảy tự động trong một thread riêng."""
    global auto_jumping_enabled, jumping_thread, last_jump_time
    
    if auto_jumping_enabled:
        return  # Đã bật rồi
    
    auto_jumping_enabled = True
    last_jump_time = time.time()
    jumping_thread = threading.Thread(target=manage_auto_jumping, daemon=True)
    jumping_thread.start()
    log_message(f"[JUMP] ▶️ Bắt đầu nhảy tự động (mỗi {JUMP_INTERVAL_SECONDS}s, nhấn {JUMP_PRESS_DURATION}s)")

def stop_auto_jumping():
    """Tắt nhảy tự động."""
    global auto_jumping_enabled
    auto_jumping_enabled = False

def aim_at_target(current_yaw_rad, p_x, p_y, t_x, t_y):
    delta_x = t_x - p_x
    delta_y = t_y - p_y
    
    target_yaw_rad = math.atan2(delta_x, delta_y) 
    delta_yaw_rad = normalize_angle_rad(current_yaw_rad - target_yaw_rad)
    
    delta_yaw_deg = math.degrees(abs(delta_yaw_rad))
    if delta_yaw_deg <= AIM_TOLERANCE_DEGREES:
        return True, delta_yaw_deg
        
    dx = calculate_mouse_movement(delta_yaw_rad)
    dx *= AIM_SMOOTHING_FACTOR 
    
    move_mouse_relative(dx, 0)
    
    return False, delta_yaw_deg

# ====================================================================
# ANTI-STUCK: PHẦN BÁN/CƯA/QUAY VỀ (Thresholds: 1s, 6s, 8s, 10s)
# ====================================================================
def check_and_handle_stuck(player_x, player_y, target_x, target_y):
    """Anti-stuck cho phần BÁN/CƯA/QUAY VỀ - Chỉ trigger nếu 20s chưa tới target"""
    global last_distance, stuck_check_start_time, stuck_check_target_coord, anti_stuck_active, last_anti_stuck_time
    global is_chopping, is_selling, is_returning, sell_bypass_mode, sell_bypass_index, sell_bypass_original_point_index, sell_point_index
    import threading

    # 🔴 AUTO-DISABLE BYPASS KHI ĐÃ TỚI ĐIỂM 4
    if sell_bypass_mode and sell_point_index >= 4:
        log_message(f"[ANTI-STUCK] ✓ Đã tới điểm 4! Tắt bypass mode.")
        sell_bypass_mode = False
    
    # Bỏ qua khi chặt cây
    if is_chopping:
        stuck_check_start_time = 0.0
        stuck_check_target_coord = None
        last_distance = None
        return False

    current_time = time.time()
    current_target = (round(target_x, 1), round(target_y, 1))
    dist = math.hypot(target_x - player_x, target_y - player_y)
    
    # ✅ Kiểm tra nếu target thay đổi
    if stuck_check_target_coord != current_target:
        log_message(f"[ANTI-STUCK] 🎯 Target mới: ({target_x:.1f}, {target_y:.1f}). Reset timer.")
        stuck_check_start_time = current_time
        stuck_check_target_coord = current_target
        last_distance = None
        return False
    
    # ✅ Khởi tạo nếu chưa có timer
    if stuck_check_start_time == 0.0:
        stuck_check_start_time = current_time
        stuck_check_target_coord = current_target
        last_distance = None
        return False
    
    # ✅ Nếu đã tới target → reset tất cả
    if dist < 1.0:
        stuck_check_start_time = 0.0
        stuck_check_target_coord = None
        last_distance = None
        return False
    
    # ✅ Kiểm tra nếu player di chuyển tới target mới → reset timer
    if last_distance is None or abs(dist - last_distance) > DISTANCE_CHANGE_THRESHOLD:
        last_distance = dist
        stuck_check_start_time = current_time  # Reset timer khi detect di chuyển
        return False
    
    last_distance = dist
    elapsed = current_time - stuck_check_start_time
    
    # ⚠️ CHỈ TRIGGER NẾU 20s KHÔNG TIẾN ĐẠT ĐƯỢC
    if elapsed > 10.0:
        log_message(f"[ANTI-STUCK] ⚠️ Kẹt 20s trên target ({target_x:.1f}, {target_y:.1f})!")
        
        if is_selling and sell_point_index < 4:  # CHỈ bypass từ điểm 0→3, KHÔNG bypass ở điểm 4+
            # Bật bypass mode để tránh obstacles (chỉ từ điểm 1 đến 4)
            if not sell_bypass_mode:
                log_message(f"[ANTI-STUCK] 🔄 Kích hoạt BYPASS MODE (điểm {sell_point_index}→4)...")
                sell_bypass_mode = True
                sell_bypass_index = 0
                sell_bypass_original_point_index = sell_point_index
        else:
            # Reset hành động (thả W, pause, bấm W lại)
            log_message(f"[ANTI-STUCK] 🔄 Reset hành động...")
            keyboard.press(KEY_FORWARD)
            keyboard.press(KEY_AUTORUN)
            keyboard.press('space')
            for _ in range(15):
                time.sleep(0.01)
            keyboard.release('space')
            for _ in range(50):
                time.sleep(0.01)
            keyboard.press('space')
            for _ in range(15):
                time.sleep(0.01)
            keyboard.release('space')
            for _ in range(50):
                time.sleep(0.01)
            keyboard.press('a')
            for _ in range(200):
                time.sleep(0.01)
            keyboard.release('a')
            keyboard.press('d')
            for _ in range(200):
                time.sleep(0.01)
            keyboard.release('d')
            
        
        # Reset timer để chờ 20s tiếp theo
        stuck_check_start_time = current_time
        last_distance = None
        return False
    
    return anti_stuck_active

# ====================================================================
# ANTI-STUCK: PHẦN CHẶT GỖ (Thresholds: 2s, 12s, 16s, 20s - Dài hơn)
# ====================================================================
def check_and_handle_stuck_chopping(player_x, player_y, target_x, target_y):
    """Anti-stuck cho phần CHẶT GỖ (thresholds dài: 2s, 12s, 16s, 20s - Kiên nhẫn hơn)"""
    global last_distance, last_change_time, anti_stuck_active, last_anti_stuck_time
    import threading

    dist = math.hypot(target_x - player_x, target_y - player_y)
    current_time = time.time()

    if last_distance is None or abs(dist - last_distance) > DISTANCE_CHANGE_THRESHOLD:
        last_distance = dist
        last_change_time = current_time
        anti_stuck_active = False
        return False

    elapsed = current_time - last_change_time

    if current_time - last_anti_stuck_time < 2.0:
        return anti_stuck_active

    def anti_stuck_action(action_type):
        global anti_stuck_active, last_anti_stuck_time
        anti_stuck_active = True
        last_anti_stuck_time = time.time()
        if action_type == 'reset':
            log_message("[STUCK-CHOP] Kẹt 20s. Thả W để reset...")
            keyboard.release(KEY_FORWARD)
            for _ in range(10):
                time.sleep(0.01)
            keyboard.press(KEY_FORWARD)
            global last_change_time
            last_change_time = time.time()
        elif action_type == 'back_left':
            log_message("[STUCK-CHOP] Kẹt 16s. Lùi + xoay trái (S+A)...")
            keyboard.release(KEY_FORWARD)
            for _ in range(5):
                time.sleep(0.01)
            keyboard.press('s')
            keyboard.press('a')
            for _ in range(100):
                time.sleep(0.01)
            keyboard.release('a')
            keyboard.release('s')
            keyboard.press(KEY_FORWARD)
        elif action_type == 'back_long_turn':
            log_message("[STUCK-CHOP] Kẹt 12s. Lùi 2s + xoay 2s...")
            
            keyboard.release(KEY_FORWARD)
            keyboard.release(KEY_AUTORUN)
            for _ in range(5):
                time.sleep(0.01)
            keyboard.press('s')
            for _ in range(100):
                time.sleep(0.01)
            keyboard.release('s')
            keyboard.press(KEY_AUTORUN)
            if target_x > player_x:
                keyboard.press('d')
                for _ in range(100):
                    time.sleep(0.01)
                keyboard.release('d')
            else:
                keyboard.press('a')
                for _ in range(100):
                    time.sleep(0.01)
                keyboard.release('a')
            keyboard.press(KEY_FORWARD)
        elif action_type == 'turn_jump':
            log_message("[STUCK-CHOP] Phát hiện kẹt nhẹ (4s). Nhảy và chỉnh hướng...")
            keyboard.press('space')
            time.sleep(0.15)
            keyboard.release('space')
            time.sleep(0.1)
            # Nhấp nhẹ né vật cản 0.15s thay vì xoay vòng vòng 4 giây
            turn_key = 'd' if target_x > player_x else 'a'
            keyboard.press(turn_key)
            time.sleep(0.15)
            keyboard.release(turn_key)
            keyboard.press(KEY_FORWARD)
            keyboard.press(KEY_AUTORUN)
        anti_stuck_active = False
        return

    # === 16s: Reset cuối cùng ===
    if elapsed > 16.0:
        t = threading.Thread(target=anti_stuck_action, args=('reset',), daemon=True)
        t.start()
        return False
    # === 12s: Lùi + xoay trái ===
    elif elapsed > 12.0:
        t = threading.Thread(target=anti_stuck_action, args=('back_left',), daemon=True)
        t.start()
        return False
    # === 8s: Lùi dài + né ===
    elif elapsed > 8.0:
        t = threading.Thread(target=anti_stuck_action, args=('back_long_turn',), daemon=True)
        t.start()
        return False
    # === 4s: Nhảy nhẹ + chỉnh hướng (chỉ khi thực sự đứng yên >= 4 giây) ===
    elif elapsed > 4.0:
        t = threading.Thread(target=anti_stuck_action, args=('turn_jump',), daemon=True)
        t.start()
        return False
    return anti_stuck_active

def start_sell_sequence(locations, special_locations, player_x, player_y):
    """Bắt đầu trình tự bán gỗ"""
    global is_selling, sell_point_index, sell_click_count, auto_sell_enabled, tree_chop_limit
    
    if not auto_sell_enabled or is_selling:
        return False
    
    is_selling = True
    sell_point_index = 0
    sell_click_count = 0
    if hasattr(handle_sell_sequence, "retry_npc_count"):
        handle_sell_sequence.retry_npc_count = 0
    log_message(f"[SELL] 🛒 Bắt đầu trình tự bán gỗ ({tree_chop_limit} lần)...")
    return True

BRAD_LABEL_TEMPLATE = None
NPC_BADGE4_TEMPLATE = None
BRAD_TEMPLATES_LOADED = False

def is_brad_tolliver_dialog_open():
    """
    Kiểm tra xem Màn hình 1 (Hội thoại Brad Tolliver) đã mở hay chưa.
    Dùng template matching với nhãn chữ 'BRAD TOLLIVER' và ô số '[4]'.
    """
    global BRAD_LABEL_TEMPLATE, NPC_BADGE4_TEMPLATE, BRAD_TEMPLATES_LOADED
    try:
        if not CV2_AVAILABLE or cv2 is None or np is None:
            return False

        if not BRAD_TEMPLATES_LOADED:
            brad_path = os.path.join(SCRIPT_DIR, "templates", "npc_brad_label_720p.png")
            if not os.path.exists(brad_path) and getattr(sys, 'frozen', False):
                alt = os.path.join(os.path.dirname(sys.executable), "templates", "npc_brad_label_720p.png")
                if os.path.exists(alt):
                    brad_path = alt
            if os.path.exists(brad_path):
                BRAD_LABEL_TEMPLATE = cv2.imread(brad_path)

            badge4_path = os.path.join(SCRIPT_DIR, "templates", "npc_badge4_720p.png")
            if not os.path.exists(badge4_path) and getattr(sys, 'frozen', False):
                alt = os.path.join(os.path.dirname(sys.executable), "templates", "npc_badge4_720p.png")
                if os.path.exists(alt):
                    badge4_path = alt
            if os.path.exists(badge4_path):
                NPC_BADGE4_TEMPLATE = cv2.imread(badge4_path)

            BRAD_TEMPLATES_LOADED = True

        if BRAD_LABEL_TEMPLATE is None and NPC_BADGE4_TEMPLATE is None:
            return False

        with mss.mss() as sct:
            mon = sct.monitors[1]
            img = sct.grab(mon)
            bgr = cv2.cvtColor(np.array(img), cv2.COLOR_BGRA2BGR)

        if bgr.shape[0] != 720 or bgr.shape[1] != 1280:
            bgr = cv2.resize(bgr, (1280, 720))

        score_brad = 0.0
        if BRAD_LABEL_TEMPLATE is not None:
            roi_brad = bgr[520:580, 390:580]
            if roi_brad.shape[0] >= BRAD_LABEL_TEMPLATE.shape[0] and roi_brad.shape[1] >= BRAD_LABEL_TEMPLATE.shape[1]:
                res1 = cv2.matchTemplate(roi_brad, BRAD_LABEL_TEMPLATE, cv2.TM_CCOEFF_NORMED)
                score_brad = float(cv2.minMaxLoc(res1)[1])

        score_badge4 = 0.0
        if NPC_BADGE4_TEMPLATE is not None:
            roi_badge4 = bgr[400:470, 1150:1230]
            if roi_badge4.shape[0] >= NPC_BADGE4_TEMPLATE.shape[0] and roi_badge4.shape[1] >= NPC_BADGE4_TEMPLATE.shape[1]:
                res2 = cv2.matchTemplate(roi_badge4, NPC_BADGE4_TEMPLATE, cv2.TM_CCOEFF_NORMED)
                score_badge4 = float(cv2.minMaxLoc(res2)[1])

        if score_brad >= 0.70 or score_badge4 >= 0.72:
            return True

        # Fallback nhận diện pixel chữ xanh BRAD TOLLIVER (x: 410..560, y: 535..565)
        blue_matches = 0
        for bx in range(410, 560, 6):
            for by in range(535, 565, 4):
                b, g, r = bgr[by, bx]
                if b > 140 and r < 80 and g > 60:
                    blue_matches += 1
        if blue_matches >= 5:
            return True

    except Exception as e:
        pass
    return False

def handle_sell_sequence(player_x, player_y, current_yaw_rad, locations, special_locations):
    """Xử lý từng bước của trình tự bán gỗ"""
    global is_selling, sell_point_index, sell_click_count, sell_sequence, sell_click_positions, tree_chop_limit
    global enable_woodcutting, is_woodcutting, woodcut_state, current_sawmill, sawmill_locations, is_plank_sell
    global sell_bypass_mode, sell_bypass_index, sell_bypass_waypoints, sell_bypass_original_point_index
    global auto_jumping_enabled
    
    if not is_selling:
        # Stop jumping khi không còn bán
        if auto_jumping_enabled:
            stop_auto_jumping()
        return False
    
    # Start jumping khi bắt đầu bán
    if not auto_jumping_enabled:
        start_auto_jumping()
    
    current_time = time.time()
    
    # ========== BYPASS MODE: Tránh obstacles bằng hardcode waypoints ==========
    if sell_bypass_mode:
        if sell_bypass_index < len(sell_bypass_waypoints):
            bypass_wp = sell_bypass_waypoints[sell_bypass_index]
            target_x, target_y = bypass_wp[0], bypass_wp[1]
            distance = math.hypot(target_x - player_x, target_y - player_y)
            
            # Aim tới bypass waypoint
            aimed_at_target, delta_yaw_deg = aim_at_target(current_yaw_rad, player_x, player_y, target_x, target_y)
            start_auto_jumping()  # Đảm bảo bật nhảy khi ở bypass mode
            # Kiểm tra kẹt trong bypass - dùng logic chopping (từng giây) vì bypass chỉ nhảy thẳng có thể bị stuck
            check_and_handle_stuck_chopping(player_x, player_y, target_x, target_y)
            
            if distance > 1.0:
                # Chưa tới, tiếp tục di chuyển
                set_moving(True, f"[SELL-BYPASS] {current_route_name} - Bypass {sell_bypass_index + 1}/3 - còn {distance:.1f}m")
                return True
            else:
                # Đã tới bypass waypoint, chuyển sang điểm tiếp theo
                log_message(f"[SELL-BYPASS] ✓ Đã qua bypass điểm {sell_bypass_index + 1}/3")
                sell_bypass_index += 1
                return True
        else:
            stop_auto_jumping()  # Tắt nhảy khi đã hoàn tất bypass
            # Đã hoàn tất 3 bypass waypoints - quay trở lại sell_sequence từ điểm ban đầu
            log_message(f"[SELL-BYPASS] ✅ Hoàn tất bypass! Quay lại sell_sequence từ điểm {sell_bypass_original_point_index}")
            sell_bypass_mode = False
            sell_bypass_index = 0
            # sell_point_index vẫn giữ nguyên = sell_bypass_original_point_index
            # Tiếp tục logic bình thường ở phía dưới
    
    # ========== NORMAL SELL SEQUENCE (khi không ở bypass mode) ==========
    # Bước 1-4: Điều hướng đến các điểm special (4 -> 1 -> 2 -> 3 ...)
    if sell_point_index < len(sell_sequence) - 1:
        special_idx = sell_sequence[sell_point_index]
        if special_idx < len(special_locations):
            special_loc = special_locations[special_idx]
            
            # Xử lý cả tuple/list lẫn dict
            target_x, target_y = None, None
            if isinstance(special_loc, (tuple, list)) and len(special_loc) >= 2:
                target_x, target_y = special_loc[0], special_loc[1]
            elif isinstance(special_loc, dict) and special_loc.get('x') and special_loc.get('y'):
                target_x, target_y = special_loc['x'], special_loc['y']
            
            if target_x is not None and target_y is not None:
                distance = math.hypot(target_x - player_x, target_y - player_y)

                # Kiểm tra kẹt khi đi bán
                if special_idx >= 4:
                    # Điểm 4+: Dùng logic chống kẹt từng giây (2s, 12s, 16s, 20s)
                    check_and_handle_stuck_chopping(player_x, player_y, target_x, target_y)
                else:
                    # Điểm 1-3: Dùng logic bypass (20s trigger)
                    check_and_handle_stuck(player_x, player_y, target_x, target_y)

                # Aim tới target
                aimed_at_target, delta_yaw_deg = aim_at_target(current_yaw_rad, player_x, player_y, target_x, target_y)

                # Nếu là điểm 6 hoặc 7 thì đi bộ, còn lại chạy
                if special_idx in [6]:
                    if distance > 0.8:
                        set_walking(False, f"[SELL] Đi bộ đến điểm {special_idx} (còn {distance:.1f}m)")
                        return True
                    else:
                        set_walking(False, f"[SELL] Đã tới điểm {special_idx}")
                        log_message(f"[SELL] ✓ Đã tới điểm {special_idx}")
                        sell_point_index += 1
                        return True
                # ===== KIỂM TRA CẦU GỖ TẠI ĐIỂM 4 =====
                elif special_idx == 4:
                    if distance > 0.8:
                        set_moving(True, f"[SELL] {current_route_name} - Điểm {special_idx} - còn {distance:.1f}m")
                        return True
                    else:
                        # Đã tới điểm 4
                        log_message(f"[SELL] ✓ {current_route_name} - Đã tới điểm {special_idx}")
                        
                        # ===== KIỂM TRA ENABLE WOODCUTTING =====
                        if enable_woodcutting and sawmill_locations and len(sawmill_locations) > 0:
                            # Bắt đầu cưa gỗ: chọn ngẫu nhiên 1 máy cưa từ danh sách
                            log_message(f"[WOODCUT] 🏭 Chuẩn bị cưa gỗ - Chọn ngẫu nhiên máy cưa...")
                            is_selling = False  # 🔥 THOÁT khỏi bán để vào cưa gỗ
                            is_woodcutting = True
                            woodcut_state = "MOVING_TO_SAWMILL"
                            current_sawmill = random.choice(sawmill_locations)  # ✅ Chọn ngẫu nhiên
                            log_message(f"[WOODCUT] 🎲 Đã chọn máy cưa: ({current_sawmill['x']:.1f}, {current_sawmill['y']:.1f})")
                            # Không increment sell_point_index, sẽ tiếp tục bán sau cưa xong
                            return True
                        else:
                            # Không cưa, tiếp tục bán
                            sell_point_index += 1
                            return True
                else:
                    if distance > 0.8:
                        set_moving(True, f"[SELL] {current_route_name} - Điểm {special_idx} - còn {distance:.1f}m")
                        return True
                    else:
                        # set_moving(True, f"[SELL] Đã tới điểm {special_idx}")
                        log_message(f"[SELL] ✓ {current_route_name} - Đã tới điểm {special_idx}")
                        sell_point_index += 1
                        return True
    
    # Bước 5: Đi đến điểm cuối (index 0 - NPC bán gỗ) và nhấn E
    elif sell_point_index == len(sell_sequence) - 1:
        special_idx = sell_sequence[sell_point_index]
        start_auto_jumping()
        # Chỉ kéo góc nhìn xuống 1 lần khi bắt đầu đi bộ đến NPC
        if not hasattr(handle_sell_sequence, "camera_moved_down"):
            handle_sell_sequence.camera_moved_down = False
        if not handle_sell_sequence.camera_moved_down:
            move_mouse_down_smooth(600, 6)
            handle_sell_sequence.camera_moved_down = True
        if special_idx < len(special_locations):
            special_loc = special_locations[special_idx]
            
            # Xử lý cả tuple/list lẫn dict
            target_x, target_y = None, None
            if isinstance(special_loc, (tuple, list)) and len(special_loc) >= 2:
                target_x, target_y = special_loc[0], special_loc[1]
            elif isinstance(special_loc, dict) and special_loc.get('x') and special_loc.get('y'):
                target_x, target_y = special_loc['x'], special_loc['y']
            
            if target_x is not None and target_y is not None:
                distance = math.hypot(target_x - player_x, target_y - player_y)

                # Kiểm tra kẹt khi đi tới NPC (dùng logic chopping - từng giây)
                check_and_handle_stuck_chopping(player_x, player_y, target_x, target_y)

                # Aim tới NPC bán gỗ
                aimed_at_target, delta_yaw_deg = aim_at_target(current_yaw_rad, player_x, player_y, target_x, target_y)

                # Nếu còn cách NPC xa (> 2.0m): Tiếp tục di chuyển đến sát NPC
                if distance > 2.0:
                    set_moving(True, f"[SELL] {current_route_name} - Di chuyển tới NPC Brad Tolliver (còn {distance:.1f}m)")
                    return True
                else:
                    # Đã tới sát NPC (<= 2.0m)
                    stop_auto_jumping()  # Tắt nhảy khi đã tới NPC
                    set_moving(False, f"[SELL] {current_route_name} - Đã tới sát Brad Tolliver, tương tác")
                    keyboard.release(KEY_FORWARD)
                    keyboard.release(KEY_AUTORUN)
                    time.sleep(0.2)

                    # 1. Kiểm tra xem hội thoại Brad Tolliver đã mở sẵn chưa
                    if is_brad_tolliver_dialog_open():
                        log_message(f"[SELL] ✅ Hội thoại Brad Tolliver đã mở sẵn -> Chuyển sang bước bấm số 4")
                        if hasattr(handle_sell_sequence, "retry_npc_count"):
                            handle_sell_sequence.retry_npc_count = 0
                        sell_point_index += 1
                        return True
                    
                    # 2. Bấm phím E để tương tác với Brad Tolliver
                    log_message(f"[SELL] 💬 Đã tới sát Brad Tolliver (cách {distance:.1f}m) -> Bấm E mở hội thoại NPC...")
                    keyboard.press('e')
                    time.sleep(0.2)
                    keyboard.release('e')
                    time.sleep(0.4)
                    keyboard.press('e')
                    time.sleep(0.2)
                    keyboard.release('e')
                    time.sleep(1.0)  # Chờ Màn hình 1 (Hội thoại Brad Tolliver) hiện lên
                    
                    # 3. Kiểm tra lại xem hội thoại đã mở hay chưa
                    if is_brad_tolliver_dialog_open():
                        log_message(f"[SELL] ✅ Đã mở hội thoại Brad Tolliver thành công -> Chuyển sang bước bấm số 4")
                        if hasattr(handle_sell_sequence, "retry_npc_count"):
                            handle_sell_sequence.retry_npc_count = 0
                        sell_point_index += 1  # Chuyển sang bước UI bán gỗ
                        return True
                    else:
                        # CHƯA MỞ ĐƯỢC HỘI THOẠI (lệch góc đứng hoặc vướng người chơi khác)
                        # Theo yêu cầu: Quay đầu / chạy lùi ra xa một chút rồi quay lại chạy dô chỗ NPC bấm E tiếp
                        retry_c = getattr(handle_sell_sequence, "retry_npc_count", 0) + 1
                        handle_sell_sequence.retry_npc_count = retry_c
                        log_message(f"[SELL] ⚠️ Chưa mở được hội thoại Brad Tolliver (thử lần {retry_c})! Chạy lùi ra xa và tiếp cận lại...")
                        
                        # Nhả hết phím tiến
                        keyboard.release(KEY_FORWARD)
                        keyboard.release(KEY_AUTORUN)
                        time.sleep(0.1)
                        
                        # Chạy lùi ra xa NPC (nhấn S + autorun + space nhảy nhẹ vượt vật cản)
                        keyboard.press('s')
                        keyboard.press(KEY_AUTORUN)
                        
                        # Đổi góc lùi né nhẹ nếu thử nhiều lần để tránh kẹt
                        side_key = None
                        if retry_c % 3 == 2:
                            side_key = 'a'
                            keyboard.press('a')
                        elif retry_c % 3 == 0:
                            side_key = 'd'
                            keyboard.press('d')
                            
                        time.sleep(0.3)
                        # Nhảy 1 nhịp vượt vật cản/người chơi chắn phía sau
                        keyboard.press('space')
                        time.sleep(0.15)
                        keyboard.release('space')
                        
                        # Tiếp tục chạy lùi ra xa (~4-5m)
                        time.sleep(1.0)
                        
                        keyboard.release('s')
                        if side_key:
                            keyboard.release(side_key)
                        keyboard.release(KEY_AUTORUN)
                        time.sleep(0.2)
                        
                        # Giữ nguyên sell_point_index để ở tick tiếp theo (khoảng cách > 2.0m),
                        # bot sẽ tự động aim lại Brad Tolliver và chạy vào tiếp cận lại!
                        return True
    
    # Bước 5: Thao tác UI bán gỗ
    elif sell_point_index == len(sell_sequence):
        if sell_click_count == 0:
            # Tại Màn hình 1 (Hội thoại NPC): Click chuột trực tiếp vào ô số 4 và bấm phím 4
            opt4_x, opt4_y = 1058, 450      # Giữa thanh "Tôi muốn mua đồ của ông [4]"
            badge4_x, badge4_y = 1195, 450  # Ngay ô số 4 ở mép phải
            log_message(f"[SELL] 🖱 Click chuột vào ô số 4: ({opt4_x}, {opt4_y}) và bấm phím 4...")
            
            # Di chuyển và click vào thanh lựa chọn số 4
            pyautogui.moveTo(opt4_x, opt4_y, duration=0.2)
            pyautogui.click(opt4_x, opt4_y)
            time.sleep(0.25)
            # Click vào ô số 4 bên phải
            pyautogui.click(badge4_x, badge4_y)
            time.sleep(0.2)
            
            # Đồng thời gửi phím 4
            try:
                keyboard.press('4')
                time.sleep(0.15)
                keyboard.release('4')
            except Exception:
                pass
            try:
                pyautogui.press('4')
            except Exception:
                pass
                
            time.sleep(1.5)  # Chờ Màn hình 2 (Cửa hàng Thu mua) xuất hiện
            sell_click_count += 1
            return True
        
        elif sell_click_count == 1:
            # Tại Màn hình 2 (Cửa hàng Tạp Hóa 24/7): Bấm chuyển sang tab "Thu mua"
            tab_thumua_x, tab_thumua_y = 360, 42
            log_message(f"[SELL] 🛒 Click chuyển sang phần 'Thu mua' tại ({tab_thumua_x}, {tab_thumua_y})...")
            pyautogui.moveTo(tab_thumua_x, tab_thumua_y, duration=0.2)
            pyautogui.click(tab_thumua_x, tab_thumua_y)
            time.sleep(0.25)
            pyautogui.click(tab_thumua_x, tab_thumua_y)
            time.sleep(0.8)  # Chờ tab Thu mua hiển thị danh sách vật phẩm
            sell_click_count += 1
            return True
        
        elif sell_click_count == 2:
            # Đang ở tab Thu mua: Nhập số lượng gỗ để bán
            should_sell_plank = enable_woodcutting or is_plank_sell
            
            # Chọn toạ độ dựa trên chế độ bán (plank hay wood)
            if should_sell_plank:
                # Bán PLANK (ván gỗ)
                input_x, input_y = 336, 384  # Ô nhập số
                button_x, button_y = 423, 383  # Nút bán
                log_message(f"[SELL] 🌳 Tại tab Thu mua: Bán PLANK (ván gỗ) -> Ô nhập ({input_x}, {input_y}) → Nút bán ({button_x}, {button_y})")
            else:
                # Bán WOOD (gỗ thô)
                input_x, input_y = 108, 384  # Ô nhập số
                button_x, button_y = 196, 382  # Nút bán
                log_message(f"[SELL] 🪵 Tại tab Thu mua: Bán WOOD (gỗ thô) -> Ô nhập ({input_x}, {input_y}) → Nút bán ({button_x}, {button_y})")
            
            # Bấm vào ô nhập số
            pyautogui.click(input_x, input_y)
            time.sleep(0.3)
            # Nhập số lượng bán
            keyboard.write("38")
            time.sleep(0.5)
            # Bấm nút bán
            pyautogui.click(button_x, button_y)   
            time.sleep(0.3)
            
            # Lần nhập thứ 2 để bán nốt
            pyautogui.click(input_x, input_y)
            time.sleep(0.3)
            keyboard.write("37")
            time.sleep(0.5)
            # Bấm nút bán
            pyautogui.click(button_x, button_y)   
            time.sleep(0.3)
            
            sell_click_count += 1
            return True
        
        else:
            global is_returning
            # Hoàn tất bán gỗ, nhấn ESC để thoát menu, sau đó quay về
            log_message(f"[SELL] ✅ Hoàn tất bán gỗ! Đã bán xong.")
            time.sleep(1.5)
            keyboard.press('esc')
            time.sleep(0.25)
            keyboard.release('esc')
            time.sleep(1.0)
            log_message(f"[SELL] 🚪 Nhấn ESC để thoát menu bán gỗ")
            # Kéo góc nhìn lên lại sau khi bán xong
            move_mouse_down_smooth(-600, 30)
            # Reset flag để lần sau lại kéo xuống đúng 1 lần
            if hasattr(handle_sell_sequence, "camera_moved_down"):
                handle_sell_sequence.camera_moved_down = False
            # Chuyển sang trạng thái quay về
            is_selling = False
            is_returning = True
            sell_point_index = 0  # Reset về 0 để bắt đầu return journey
            log_message(f"[RETURN] 🔙 Bắt đầu quay về khu vực chặt cây...")
            return False
    
    return is_selling

def handle_woodcutting_sequence(player_x, player_y, current_yaw_rad, locations, special_locations):
    """
    Xử lý logic cưa gỗ tại máy cưa
    Quy trình:
    1. Aim đến điểm aiming_at của máy cưa
    2. Spam E cho đến khi phát hiện go.png
    3. Click wood (670, 275)
    4. Spam right-click (389, 511) mỗi 2 giây
    5. Thoát khi go.png biến mất
    """
    global is_woodcutting, woodcut_state, woodcut_wood_selected, woodcut_last_right_click_time, current_sawmill
    global is_selling, sell_point_index, sell_click_count, is_returning, is_plank_sell
    
    if not is_woodcutting or current_sawmill is None:
        return False
    
    current_time = time.time()
    
    # 🔄 OPTION B: Nếu go.png đã hiện ở bất kỳ state nào → Nhảy thẳng CUTTING
    if woodcut_state != "IDLE" and woodcut_state != "CUTTING" and (detect_go_template_cached() or detect_vango_template_cached()):
        log_message(f"[WOODCUT] 🎯 Phát hiện go.png! Nhảy thẳng sang CUTTING...")
        set_walking(False, "[WOODCUT] Dừng - phát hiện UI")
        woodcut_state = "CUTTING"
        woodcut_wood_selected = False
        return True
    
    # ===== PHASE 0: Đi bộ đến máy cưa + SPAM E để kích hoạt UI =====
    if woodcut_state == "MOVING_TO_SAWMILL":
        sawmill_x = current_sawmill.get('x', player_x)
        sawmill_y = current_sawmill.get('y', player_y)
        distance_to_sawmill = math.hypot(sawmill_x - player_x, sawmill_y - player_y)
        
        # ✅ CHỐNG KẸT khi đi từ điểm 4 đến máy cưa
        check_and_handle_stuck(player_x, player_y, sawmill_x, sawmill_y)
        stop_auto_jumping()
        # Chuyển đổi giữa chạy và đi bộ dựa trên khoảng cách
        if distance_to_sawmill > 5.0:
            # > 5m: Chạy (bật W thường) - KHÔNG SPAM E
            set_moving(True, f"[WOODCUT] Chạy đến máy cưa (còn {distance_to_sawmill:.1f}m)")
        elif distance_to_sawmill > 0.5:
            # ≤ 5m: Đi bộ + SPAM E để kích hoạt giao diện
            set_walking(True, f"[WOODCUT] Đi bộ + spam E đến máy cưa (còn {distance_to_sawmill:.1f}m)")
        else:
            # <= 0.5m: Đã tới máy cưa, dừng lại
            set_walking(False, "[WOODCUT] Đã tới máy cưa")
            log_message(f"[WOODCUT] ✓ Đã tới máy cưa, chuẩn bị aim...")
            # Clean up time tracker
            if hasattr(handle_woodcutting_sequence, "last_sawmill_aim_time"):
                delattr(handle_woodcutting_sequence, "last_sawmill_aim_time")
            if hasattr(handle_woodcutting_sequence, "woodcut_moving_spam_e_time"):
                delattr(handle_woodcutting_sequence, "woodcut_moving_spam_e_time")
            woodcut_state = "AIMING"
            return True
        
        # Aim tới máy cưa MỖI FRAME mà không delay để aim liên tục (fix khựng chuột)
        # Không cần check time vì loop chính đã đủ nhanh
        aimed_at_target, delta_yaw_deg = aim_at_target(current_yaw_rad, player_x, player_y, sawmill_x, sawmill_y)
        
        # 🔄 CHỈ SPAM E KHI ≤20m (đang đi bộ)
        if distance_to_sawmill <= 20.0:
            if not hasattr(handle_woodcutting_sequence, "woodcut_moving_spam_e_time"):
                handle_woodcutting_sequence.woodcut_moving_spam_e_time = 0
            
            if current_time - handle_woodcutting_sequence.woodcut_moving_spam_e_time > 0.3:
                keyboard.press('e')
                time.sleep(0.1)
                keyboard.release('e')
                handle_woodcutting_sequence.woodcut_moving_spam_e_time = current_time
        
        return True
    
    # ===== PHASE 1: Aim tới máy cưa =====
    if woodcut_state == "AIMING":
        # Aim trực tiếp vào tọa độ máy cưa
        aiming_x = current_sawmill.get('x')
        aiming_y = current_sawmill.get('y')
        
        distance_to_aim = math.hypot(aiming_x - player_x, aiming_y - player_y)
        
        # Drag mouse down để kéo camera xuống
        if not hasattr(handle_woodcutting_sequence, "woodcut_camera_moved_down"):
            handle_woodcutting_sequence.woodcut_camera_moved_down = False
        
        if not handle_woodcutting_sequence.woodcut_camera_moved_down:
            
            handle_woodcutting_sequence.woodcut_camera_moved_down = True
        
        # Aim tới điểm
        aimed_at_target, delta_yaw_deg = aim_at_target(current_yaw_rad, player_x, player_y, aiming_x, aiming_y)
        
        if aimed_at_target:
            log_message(f"[WOODCUT] ✓ Đã aim chính xác tới máy cưa")
            woodcut_state = "WAITING_FOR_UI"
            woodcut_wood_selected = False
            return True
        
        # Spam E để tương tác với máy cưa (chờ UI hiện ra)
        if not hasattr(handle_woodcutting_sequence, "woodcut_spam_e_time"):
            handle_woodcutting_sequence.woodcut_spam_e_time = 0
        
        if current_time - handle_woodcutting_sequence.woodcut_spam_e_time > 0.3:  # Spam E mỗi 0.3 giây
            keyboard.press('e')
            time.sleep(0.1)
            keyboard.release('e')
            handle_woodcutting_sequence.woodcut_spam_e_time = current_time
        
        return True
    
    # ===== PHASE 2: Chờ phát hiện go.png =====
    elif woodcut_state == "WAITING_FOR_UI":
        # ✅ KIỂM TRA go.png TRƯỚC (gỗ để xẻ) - quét realtime
        if detect_go_template():
            log_message(f"[WOODCUT] � Phát hiện go.png! Bắt đầu cưa gỗ...")
            woodcut_state = "CUTTING"
            woodcut_wood_selected = False
            # Reset spam E time
            if hasattr(handle_woodcutting_sequence, "woodcut_spam_e_time"):
                delattr(handle_woodcutting_sequence, "woodcut_spam_e_time")
            return True
        
        # ⚠️ CHỈ KIỂM TRA vango NẾU CHƯA CÓ go.png (máy cưa không có gỗ) - quét realtime
        if detect_vango_template():
            log_message(f"[WOODCUT] 🌳 Phát hiện chỉ vango.png (không có go.png)! Không có gỗ để xẻ → Bán PLANK!")
            # Bấm ESC để thoát khỏi giao diện máy cưa
            keyboard.press('esc')
            time.sleep(0.25)
            keyboard.release('esc')
            time.sleep(0.5)
            
            # Kéo camera lên lại
            if hasattr(handle_woodcutting_sequence, "woodcut_camera_moved_down"):
                handle_woodcutting_sequence.woodcut_camera_moved_down = False
            
            # Reset trạng thái cưa gỗ - BỎ QUA và BÁN PLANK
            woodcut_state = "IDLE"
            is_woodcutting = False
            current_sawmill = None
            woodcut_wood_selected = False
            
            # ✅ BẬT CHẾ ĐỘ BÁN PLANK (ván gỗ)
            is_plank_sell = True
            is_selling = True
            sell_point_index = 4  # Bắt đầu bán từ điểm 5 (điểm NPC bán)
            log_message(f"[WOODCUT] 🌳 Chuyển sang bán PLANK (ván gỗ)...")
            return False
        
        # Tiếp tục spam E cho đến khi phát hiện UI
        if not hasattr(handle_woodcutting_sequence, "woodcut_spam_e_time"):
            handle_woodcutting_sequence.woodcut_spam_e_time = 0
        
        if current_time - handle_woodcutting_sequence.woodcut_spam_e_time > 0.3:
            keyboard.press('e')
            time.sleep(0.1)
            keyboard.release('e')
            handle_woodcutting_sequence.woodcut_spam_e_time = current_time
            log_message(f"[WOODCUT] ⏳ Chờ UI... spam E")
        
        # Spam E vô hạn cho đến khi phát hiện UI (không có timeout)
        return True
    
    # ===== BACKTRACK: Đi ngược về điểm 4 (nơi vào khu cưa gỗ), rồi chọn máy cưa khác =====
    # elif woodcut_state == "BACKTRACK_FROM_SAWMILL":
    #     # Đi về điểm 4 (special_locations[4])
    #     if special_locations and len(special_locations) > 4:
    #         backtrack_target = special_locations[4]
    #         target_x = backtrack_target['x']
    #         target_y = backtrack_target['y']
    #         distance = math.hypot(target_x - player_x, target_y - player_y)
            
    #         # Aim về điểm 4
    #         aimed_at_target, delta_yaw_deg = aim_at_target(current_yaw_rad, player_x, player_y, target_x, target_y)
            
    #         if distance > 0.5:
    #             # Vẫn còn xa, tiếp tục đi
    #             set_moving(True, f"[WOODCUT] ↩️ Backtrack về điểm 4 (còn {distance:.1f}m)")
    #             return True
    #         else:
    #             # Đã tới điểm 4, chọn máy cưa khác ngẫu nhiên
    #             log_message(f"[WOODCUT] ✓ Đã backtrack về điểm 4! Chọn máy cưa khác...")
    #             set_moving(False, "Backtrack hoàn tất")
                
    #             # Chọn ngẫu nhiên máy cưa khác
    #             if sawmill_locations and len(sawmill_locations) > 0:
    #                 current_sawmill = random.choice(sawmill_locations)
    #                 woodcut_state = "MOVING_TO_SAWMILL"
    #                 woodcut_wood_selected = False
    #                 log_message(f"[WOODCUT] 🎲 Chọn máy cưa mới: ({current_sawmill['x']:.1f}, {current_sawmill['y']:.1f})")
    #                 return True
    #             else:
    #                 # Không có máy cưa, bỏ qua
    #                 log_message(f"[WOODCUT] ⚠️ Không có máy cưa để thử, bỏ qua...")
    #                 is_woodcutting = False
    #                 is_selling = True
    #                 sell_point_index = 4
    #                 return False
    #     else:
    #         # Fallback: không có special_locations[4]
    #         log_message(f"[WOODCUT] ⚠️ Không tìm thấy điểm 4, bỏ qua...")
    #         is_woodcutting = False
    #         is_selling = True
    #         sell_point_index = 4
    #         return False
    
    # ===== PHASE 3: Click wood + Spam right-click =====
    elif woodcut_state == "CUTTING":
        # Click wood (676, 275) - chỉ 1 lần khi mới vào phase
        if not woodcut_wood_selected:
            log_message(f"[WOODCUT] 🪵 Click vào ván gỗ ({WOODCUT_WOOD_CLICK_X}, {WOODCUT_WOOD_CLICK_Y})")
            pyautogui.click(WOODCUT_WOOD_CLICK_X, WOODCUT_WOOD_CLICK_Y)
            time.sleep(0.5)
            woodcut_wood_selected = True
            woodcut_last_right_click_time = current_time
            woodcut_template_lost_time = 0  # Reset timer
            return True
        
        # Kiểm tra go.png còn tồn tại không - quét realtime
        if not detect_go_template():
            # Template biến mất - bấm ESC ngay lập tức
            log_message(f"[WOODCUT] 📉 go.png biến mất! Bấm ESC ngay...")
            time.sleep(20)
            keyboard.press('esc')
            time.sleep(0.25)
            keyboard.release('esc')
            time.sleep(0.5)
            
            # Kéo camera lên lại
            
            if hasattr(handle_woodcutting_sequence, "woodcut_camera_moved_down"):
                handle_woodcutting_sequence.woodcut_camera_moved_down = False
            
            # Reset trạng thái cưa gỗ
            woodcut_state = "IDLE"
            is_woodcutting = False
            current_sawmill = None
            is_plank_sell = False
            woodcut_wood_selected = False
            woodcut_template_lost_time = 0
            
            # Tiếp tục bán từ điểm 5 và BẬT LẠI AUTO_SELL
            sell_point_index = 4
            is_selling = True  # ✅ BẬT LẠI CHẾ ĐỘ BÁN
            log_message(f"[WOODCUT] ✅ Hoàn tất cưa gỗ! Tiếp tục bán gỗ...")
            return False
        else:
            # go.png vẫn còn, reset timer
            woodcut_template_lost_time = 0
        
        # Spam right-click mỗi 2 giây (chỉ spam khi go.png vẫn còn)
        if current_time - woodcut_last_right_click_time >= 1.0:
            log_message(f"[WOODCUT] 🖱 Spam right-click")
            pyautogui.click(WOODCUT_RIGHT_CLICK_X, WOODCUT_RIGHT_CLICK_Y, button='left')
            woodcut_last_right_click_time = current_time
        return True
    
    return is_woodcutting

def handle_return_journey(player_x, player_y, current_yaw_rad, locations, special_locations, random_start_locs):
    """Xử lý đường quay về sau khi bán gỗ"""
    global is_returning, sell_point_index, return_sequence, random_start_locations, auto_jumping_enabled
    random_start_locations = random_start_locs  # Update global variable
    
    if not is_returning:
        # Stop jumping khi không còn quay về
        if auto_jumping_enabled:
            stop_auto_jumping()
        return False
    
    # Start jumping khi bắt đầu quay về
    if not auto_jumping_enabled:
        start_auto_jumping()
    
    # Đi qua tất cả các điểm trong return_sequence
    if sell_point_index < len(return_sequence):
        special_idx = return_sequence[sell_point_index]
        if special_idx < len(special_locations):
            special_loc = special_locations[special_idx]
            
            # Xử lý cả tuple/list lẫn dict
            target_x, target_y = None, None
            if isinstance(special_loc, (tuple, list)) and len(special_loc) >= 2:
                target_x, target_y = special_loc[0], special_loc[1]
            elif isinstance(special_loc, dict) and special_loc.get('x') and special_loc.get('y'):
                target_x, target_y = special_loc['x'], special_loc['y']
            
            if target_x is not None and target_y is not None:
                distance = math.hypot(target_x - player_x, target_y - player_y)
                
                # Aim tới target
                aimed_at_target, delta_yaw_deg = aim_at_target(current_yaw_rad, player_x, player_y, target_x, target_y)
                
                # ✅ CHỐNG KẸT: Kiểm tra và xử lý kẹt
                check_and_handle_stuck_chopping(player_x, player_y, target_x, target_y)
                
                if distance > 3.0:
                    # Chưa tới, tiếp tục di chuyển
                    set_moving(True, f"[RETURN] {current_route_name} - Điểm {special_idx} - còn {distance:.1f}m")
                    return True
                else:
                    # Đã tới, chuyển sang điểm tiếp theo
                    log_message(f"[RETURN] ✓ {current_route_name} - Đã qua điểm {special_idx}")
                    sell_point_index += 1
                    return True
    else:
        # Đã hoàn tất return journey - Chuyển sang random start point
        is_returning = False
        sell_point_index = 0
        
        # ✅ KÍCH HOẠT LOGIC ĐI ĐẾN RANDOM START POINT
        global is_going_to_random_start, random_start_target
        is_going_to_random_start = True
        
        # Random chọn 1 điểm từ random_start_locations
        if random_start_locations and len(random_start_locations) > 0:
            random_start_target = random.choice(random_start_locations)
            # Jumping sẽ được bắt đầu bởi handle_random_start_point
            log_message(f"[RETURN] ✅ Đã về khu vực chặt cây! Đang đi đến random point ({random_start_target['x']:.1f}, {random_start_target['y']:.1f})...")
        else:
            log_message(f"[RETURN] ⚠️ Không tìm thấy random_start locations! Tiếp tục chặt cây ngay...")
            # Stop jumping nếu không có random start point
            stop_auto_jumping()
            is_going_to_random_start = False
            global total_trees_chopped
            total_trees_chopped = 0
        
        return False
    
    return is_returning

def handle_random_start_point(player_x, player_y, current_yaw_rad):
    """Xử lý logic đi đến random start point sau khi quay về"""
    global is_going_to_random_start, random_start_target, total_trees_chopped, auto_jumping_enabled
    
    if not is_going_to_random_start or random_start_target is None:
        # Stop jumping khi không còn đi random start
        if auto_jumping_enabled:
            stop_auto_jumping()
        return False
    
    # Start jumping khi đi random start point
    if not auto_jumping_enabled:
        start_auto_jumping()
    
    target_x = random_start_target['x']
    target_y = random_start_target['y']
    distance = math.hypot(target_x - player_x, target_y - player_y)
    
    # Aim tới target
    aimed_at_target, delta_yaw_deg = aim_at_target(current_yaw_rad, player_x, player_y, target_x, target_y)
    
    # ✅ CHỐNG KẸT
    check_and_handle_stuck(player_x, player_y, target_x, target_y)
    
    if distance > 3.0:
        # Chưa tới, tiếp tục di chuyển
        set_moving(True, f"[RANDOM START] Đi đến điểm xuất phát (còn {distance:.1f}m)")
        return True
    else:
        # Đã tới random start point
        log_message(f"[RANDOM START] ✅ Đã đến điểm xuất phát! Bắt đầu chặt cây...")
        # Stop jumping khi đã tới random start
        stop_auto_jumping()
        is_going_to_random_start = False
        random_start_target = None
        total_trees_chopped = 0  # Reset tree counter để bắt đầu vòng mới
        return False
    
    return is_going_to_random_start

def set_moving(should_move, reason=""):
    global is_moving, keys_pressed
    
    if should_move == is_moving:
        # Đã ở trạng thái mong muốn, không làm gì
        return
    
    if should_move:
        # Bật di chuyển (chạy)
        keyboard.press(KEY_FORWARD)
        keyboard.press(KEY_AUTORUN)
        is_moving = True
        keys_pressed = f"{KEY_FORWARD.upper()} + {KEY_AUTORUN}"
        log_message(f"[MOVE] ▶ Bắt đầu di chuyển - {reason if reason else 'Aimed at target'}")
    else:
        # Tắt di chuyển
        keyboard.release(KEY_FORWARD)
        keyboard.release(KEY_AUTORUN)
        is_moving = False
        keys_pressed = "None"
        log_message(f"[MOVE] ⏸ Dừng di chuyển - {reason if reason else 'Re-aiming'}")

def set_walking(should_walk, reason=""):
    """Đặt trạng thái đi bộ (chỉ W, không chạy). True = bật, False = tắt."""
    global is_moving, keys_pressed
    
    if should_walk:
        # Bật đi bộ (chỉ W)
        keyboard.release(KEY_AUTORUN)  # Thả autorun nếu đang giữ
        keyboard.press(KEY_FORWARD)
        is_moving = True
        keys_pressed = f"{KEY_FORWARD.upper()}"
        log_message(f"[WALK] 🚶 Đi bộ - {reason if reason else 'Walking to target'}")
    else:
        # Tắt đi bộ
        keyboard.press(KEY_FORWARD)
        keyboard.press(KEY_AUTORUN)  # Đảm bảo autorun tắt
        is_moving = False
        keys_pressed = "None"
        log_message(f"[WALK] ⏸ Dừng đi bộ - {reason if reason else 'Arrived'}")

last_toggle_time = 0
def toggle_bot(e=None):
    global is_bot_active, total_trees_chopped, tree_chop_limit, should_stop_bot, tree_limit_entry, toggle_btn, last_toggle_time
    
    current_t = time.time()
    if current_t - last_toggle_time < 0.4:
        return
    last_toggle_time = current_t
    
    if not is_bot_active:
        # Bật bot - Đọc số lượng từ input (KHÔNG reset total_trees_chopped)
        try:
            limit = int(tree_limit_entry.get().strip()) if tree_limit_entry.get().strip() else 0
            tree_chop_limit = limit
            should_stop_bot = False
            
            is_bot_active = True
            log_message(f"[BOT] ✅ Bot BẬT! Sẽ chặt {tree_chop_limit if tree_chop_limit > 0 else 'không giới hạn'} cây.")
            log_message(f"[BOT] 📊 Tiếp tục đếm từ: {total_trees_chopped} cây")
            
            # Cập nhật nút GUI
            if toggle_btn:
                if CTK_AVAILABLE and hasattr(toggle_btn, 'configure'):
                    toggle_btn.configure(text="⏸️ TẠM DỪNG", fg_color="#0f4")
                elif hasattr(toggle_btn, 'config_text'):
                    toggle_btn.config_text("⏸️ TẠM DỪNG", new_bg="#0f4", new_fg="#000")
        except ValueError:
            log_message("[BOT] ❌ Nhập số không hợp lệ! Bot không bật.")
            return
    else:
        # Tạm dừng bot
        is_bot_active = False
        log_message(f"[BOT] ⏸️ Bot TẠM DỪNG. Số cây hiện tại: {total_trees_chopped}/{tree_chop_limit if tree_chop_limit > 0 else '∞'}")
        log_message(f"[BOT] 💡 Bấm '=' hoặc nút TIẾP TỤC để bật lại")
        set_moving(False, "Bot tạm dừng")
        stop_auto_jumping()
        for k in ['w', 's', 'a', 'd', 'space', 'e', KEY_FORWARD, KEY_AUTORUN]:
            try:
                keyboard.release(k)
            except Exception:
                pass
        
        # Cập nhật nút GUI
        if toggle_btn:
            if CTK_AVAILABLE and hasattr(toggle_btn, 'configure'):
                toggle_btn.configure(text="▶️ TIẾP TỤC", fg_color="#f90")
            elif hasattr(toggle_btn, 'config_text'):
                toggle_btn.config_text("▶️ TIẾP TỤC", new_bg="#f90", new_fg="#000")

def reset_counter():
    """Reset số cây đã chặt về 0"""
    global total_trees_chopped, should_stop_bot
    total_trees_chopped = 0
    should_stop_bot = False
    log_message(f"[RESET] 🔄 Đã reset số cây về 0")
    log_message(f"[RESET] 💡 Giới hạn hiện tại: {tree_chop_limit if tree_chop_limit > 0 else '∞'} cây")

def refresh_game_progress():
    """Quét lại tiến trình game - Reset tất cả counter và trạng thái"""
    global total_trees_chopped, should_stop_bot, is_bot_active, is_selling, is_woodcutting, woodcut_state, sell_point_index, sell_click_count
    
    # Reset các counter
    total_trees_chopped = 0
    should_stop_bot = False
    is_selling = False
    is_woodcutting = False
    sell_point_index = 0
    sell_click_count = 0
    woodcut_state = "MOVING_TO_SAWMILL"
    
    # Dừng bot nếu đang chạy
    if is_bot_active:
        is_bot_active = False
        set_moving(False, "Quét lại tiến trình game")
        log_message("[🔄 QUÉT LẠI] Bot dừng để quét lại tiến trình")
    
    log_message("[🔄 QUÉT LẠI] ✅ Đã quét lại tiến trình game thành công!")
    log_message("[🔄 QUÉT LẠI] 💡 Các trạng thái đã được đặt lại:")
    log_message(f"  • Số cây đã chặt: 0/{tree_chop_limit if tree_chop_limit > 0 else '∞'}")
    log_message(f"  • Trạng thái Bot: TẮT")
    log_message(f"  • Trạng thái Bán: CHƯA KÍCH HOẠT")
    log_message(f"  • Trạng thái Cưa: CHƯA KÍCH HOẠT")

keyboard.on_release_key(KEY_TOGGLE, toggle_bot)

# ====================================================================
# IV. LOGIC GUI VÀ RADAR
# ====================================================================

class ToggleSwitch(tk.Canvas):
    """Custom Toggle Switch Widget - Kiểu gạt trái phải"""
    def __init__(self, parent, width=50, height=26, bg_on="#0F0", bg_off="#555", command=None, **kwargs):
        tk.Canvas.__init__(self, parent, width=width, height=height, bg="#3D2645", highlightthickness=0, **kwargs)
        self.width = width
        self.height = height
        self.bg_on = bg_on
        self.bg_off = bg_off
        self.command = command
        self.is_on = False
        self.circle_diameter = height - 4
        self.circle_radius = self.circle_diameter // 2
        
        self.bind("<Button-1>", self.toggle)
        self.pack_propagate(False)
        self.draw()
    
    def draw(self):
        self.delete("all")
        
        # Vẽ nền với góc bo tròn
        bg_color = self.bg_on if self.is_on else self.bg_off
        
        # Vẽ nền với các góc bo tròn (sử dụng oval + rectangle)
        radius = self.height // 2 - 2
        
        # Vẽ hình chữ nhật giữa
        self.create_rectangle(2 + radius, 2, self.width - 2 - radius, self.height - 2,
                             fill=bg_color, outline=bg_color, tags="bg_rect")
        
        # Vẽ các góc bo tròn (4 phần oval)
        # Góc trái
        self.create_arc(2, 2, 2 + radius * 2, 2 + radius * 2,
                       start=90, extent=90, fill=bg_color, outline=bg_color, tags="bg")
        # Góc phải
        self.create_arc(self.width - 2 - radius * 2, 2, self.width - 2, 2 + radius * 2,
                       start=0, extent=90, fill=bg_color, outline=bg_color, tags="bg")
        # Góc trái dưới
        self.create_arc(2, self.height - 2 - radius * 2, 2 + radius * 2, self.height - 2,
                       start=180, extent=90, fill=bg_color, outline=bg_color, tags="bg")
        # Góc phải dưới
        self.create_arc(self.width - 2 - radius * 2, self.height - 2 - radius * 2, 
                       self.width - 2, self.height - 2,
                       start=270, extent=90, fill=bg_color, outline=bg_color, tags="bg")
        
        # Vị trí của hình tròn
        if self.is_on:
            circle_x = self.width - 2 - self.circle_radius
        else:
            circle_x = 2 + self.circle_radius
        
        circle_y = self.height / 2
        
        # Vẽ hình tròn
        self.create_oval(circle_x - self.circle_radius, circle_y - self.circle_radius,
                        circle_x + self.circle_radius, circle_y + self.circle_radius,
                        fill="white", outline="white", tags="circle")
        
        # Hiệu ứng bóng nhẹ
        self.tag_raise("circle")
    
    def toggle(self, event=None):
        self.is_on = not self.is_on
        self.draw()
        if self.command:
            self.command(self.is_on)
    
    def get_state(self):
        return self.is_on
    
    def set_state(self, state):
        self.is_on = state
        self.draw()


def map_to_radar(game_x, game_y, player_x, player_y, player_yaw):

    rel_x = game_x - player_x
    rel_y = game_y - player_y
    
    cos_yaw = math.cos(player_yaw) 
    sin_yaw = math.sin(player_yaw)
    
    rotated_x = rel_x * cos_yaw - rel_y * sin_yaw
    rotated_y = rel_x * sin_yaw + rel_y * cos_yaw
    
    scale = RADAR_SIZE / (2 * RADAR_RANGE)
    
    canvas_x = (RADAR_SIZE / 2) + rotated_x * scale
    canvas_y = (RADAR_SIZE / 2) - rotated_y * scale 
    
    return canvas_x, canvas_y, rotated_x, rotated_y 


def log_message(message):
    global log_text, root
    # Chỉ log khi GUI đã load xong (root và log_text tồn tại)
    if root is not None and log_text is not None:
        try:
            log_text.insert(tk.END, f"{message}\n")
            log_text.see(tk.END)  # Auto-scroll to bottom
        except:
            pass


def on_pause_key(event):
    """Xử lý phím PAUSE để tạm dừng/tiếp tục bot"""
    global is_bot_paused
    is_bot_paused = not is_bot_paused
    
    if is_bot_paused:
        log_message("⏸️  BOT PAUSED - Nhấn PAUSE lại để tiếp tục")
        set_moving(False, "Bot Paused")
    else:
        log_message("▶️  BOT RESUMED - Tiếp tục hoạt động")


class RoundedButton(tk.Canvas):
    """Tạo nút bo tròn góc bằng Canvas"""
    def __init__(self, parent, text, command, bg_color, fg_color, width=200, height=40, 
                 active_bg_color=None, radius=15, font=None):
        tk.Canvas.__init__(self, parent, width=width, height=height, bg=parent["bg"], 
                          highlightthickness=0, relief=tk.FLAT, bd=0)
        self.parent_bg = parent["bg"]
        self.command = command
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.active_bg_color = active_bg_color or bg_color
        self.text = text
        self.radius = radius
        self.font = font or tkFont.Font(family="Arial", size=10, weight="bold")
        self.is_active = False
        self.current_bg = bg_color
        self.button_width = width
        self.button_height = height
        
        self.draw_button()
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
    
    def draw_button(self, bg_color=None):
        """Vẽ nút với các giá trị hiện tại"""
        if bg_color is None:
            bg_color = self.bg_color
        
        self.delete("all")
        self.create_rounded_rect(0, 0, self.button_width, self.button_height, 
                                radius=self.radius, fill=bg_color, outline="")
        self.create_text(self.button_width//2, self.button_height//2, text=self.text, 
                        fill=self.fg_color, font=self.font, anchor="center")
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius=15, **kwargs):
        """Vẽ hình chữ nhật bo tròn"""
        points = [
            x1+radius, y1,
            x1+radius, y1,
            x2-radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1+radius,
            x1, y1
        ]
        return self.create_polygon(points, **kwargs, smooth=True)
    
    def on_enter(self, event):
        self.draw_button(bg_color=self.active_bg_color)
    
    def on_leave(self, event):
        self.draw_button(bg_color=self.bg_color)
    
    def on_click(self, event):
        if self.command:
            self.command()
    
    def config_text(self, new_text, new_bg=None, new_fg=None):
        """Cập nhật text và màu nút"""
        self.text = new_text
        if new_bg:
            self.bg_color = new_bg
            self.current_bg = new_bg
        if new_fg:
            self.fg_color = new_fg
        
        self.draw_button(bg_color=self.bg_color)


def setup_gui():
    global root, canvas, info_labels, log_text, tree_limit_entry, toggle_btn
    
    # Sử dụng CustomTkinter nếu có, không thì dùng Tkinter thường
    if CTK_AVAILABLE:
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        root = ctk.CTk()
    else:
        root = tk.Tk()
    
    root.title(RANDOM_WINDOW_NAME)
    root.geometry("700x560")
    
    if not CTK_AVAILABLE:
        root.configure(bg="#1a1a2e")
    
    root.resizable(False, False)
    
    # Thiết lập icon
    icon_path = get_resource_path("L.ico")
    if icon_path and os.path.exists(icon_path):
        try:
            root.iconbitmap(icon_path)
        except:
            pass
    
    root.attributes('-topmost', False)
    
    # ⏸️ Gắn phím PAUSE để tạm dừng bot
    root.bind('<Pause>', on_pause_key)

    # Main container với gradient effect
    if CTK_AVAILABLE:
        main_container = ctk.CTkFrame(root, fg_color=("#1a1a2e", "#1a1a2e"))
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
    else:
        main_container = tk.Frame(root, bg="#1a1a2e")
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

    # Header với logo và title  
    if CTK_AVAILABLE:
        header = ctk.CTkFrame(main_container, fg_color=("#16213e", "#16213e"), corner_radius=15, height=120)
    else:
        header = tk.Frame(main_container, bg="#16213e", relief=tk.RIDGE, bd=2)
    header.pack(fill=tk.X, pady=(0, 15))
    header.pack_propagate(False)
    
    # Title với gradient text effect
    if CTK_AVAILABLE:
        title_label = ctk.CTkLabel(header, text="🌲 Tiều Phu SVIP 🌲",
                                    font=("Segoe UI", 24, "bold"),
                                    text_color="#4ecca3")
        title_label.pack(pady=(15, 2))
        
        subtitle1 = ctk.CTkLabel(header, text="⚡Thực hiện và phát triển bới Lazy tool⚡",
                               font=("Consolas", 10), text_color="#93a8c1")
        subtitle1.pack(pady=(0, 2))
        
        subtitle2 = ctk.CTkLabel(header, text="⚡Mọi Tool Crack bán bên ngoài đều không chính thống và nguy hiểm⚡",
                               font=("Consolas", 10), text_color="#93a8c1")
        subtitle2.pack(pady=(0, 8))
    else:
        title_label = tk.Label(header, text="🌲 Tiều Phu SVIP 🌲", 
                              font=("Segoe UI", 24, "bold"),
                              fg="#4ecca3", bg="#16213e")
        title_label.pack(pady=(15, 2))
        
        subtitle1 = tk.Label(header, text="⚡Thực hiện và phát triển bới Lazy tool⚡",
                           font=("Consolas", 10), fg="#93a8c1", bg="#16213e")
        subtitle1.pack(pady=(0, 2))
        
        subtitle2 = tk.Label(header, text="⚡Mọi Tool Crack bán bên ngoài đều không chính thống và nguy hiểm⚡",
                           font=("Consolas", 10), fg="#93a8c1", bg="#16213e")
        subtitle2.pack(pady=(0, 8))

    # Content container (2 columns)
    if CTK_AVAILABLE:
        content = ctk.CTkFrame(main_container, fg_color="transparent")
    else:
        content = tk.Frame(main_container, bg="#1a1a2e")
    content.pack(fill=tk.BOTH, expand=True)

    # ============ LEFT PANEL - Controls ============
    if CTK_AVAILABLE:
        left_panel = ctk.CTkFrame(content, fg_color=("#1a1f3a", "#1a1f3a"), corner_radius=15, width=410)
    else:
        left_panel = tk.Frame(content, bg="#1a1f3a", relief=tk.RIDGE, bd=3, width=350)
    left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 8))
    left_panel.pack_propagate(False)

    # Control header
    if CTK_AVAILABLE:
        ctrl_header = ctk.CTkLabel(left_panel, text="⚙️ ĐIỀU KHIỂN",
                                   font=("Segoe UI", 16, "bold"), text_color="#4ecca3")
    else:
        ctrl_header = tk.Label(left_panel, text="⚙️ ĐIỀU KHIỂN",
                              font=("Segoe UI", 16, "bold"), fg="#4ecca3", bg="#1a1f3a")
    ctrl_header.pack(pady=(10, 8))

    # Separator line
    if CTK_AVAILABLE:
        sep1 = ctk.CTkFrame(left_panel, height=2, fg_color="#4ecca3")
    else:
        sep1 = tk.Frame(left_panel, height=2, bg="#4ecca3")
    sep1.pack(fill=tk.X, padx=18, pady=(0, 10))

    # Input section với card design - TẤT CẢ TRÊN 1 DÒNG
    if CTK_AVAILABLE:
        input_card = ctk.CTkFrame(left_panel, fg_color=("#1e3a5f", "#1e3a5f"), corner_radius=12)
    else:
        input_card = tk.Frame(left_panel, bg="#1e3a5f", relief=tk.FLAT, bd=1)
    input_card.pack(fill=tk.X, padx=12, pady=(0, 10))
    
    # Single row: Mục tiêu + Đã chặt + Bán gỗ
    if CTK_AVAILABLE:
        single_row = ctk.CTkFrame(input_card, fg_color="transparent")
    else:
        single_row = tk.Frame(input_card, bg="#1e3a5f")
    single_row.pack(fill=tk.X, padx=12, pady=10)
    
    # Function: Chỉ cho phép nhập số cho mục tiêu
    def validate_number_input(event=None):
        """Xóa ký tự không phải số khỏi Entry field"""
        current_text = tree_limit_entry.get()
        # Chỉ giữ lại ký tự số
        filtered_text = ''.join(c for c in current_text if c.isdigit())
        if filtered_text != current_text:
            tree_limit_entry.delete(0, tk.END)
            tree_limit_entry.insert(0, filtered_text)
    
    # Mục tiêu
    if CTK_AVAILABLE:
        ctk.CTkLabel(single_row, text="Mục tiêu:", 
                    font=("Segoe UI", 11, "bold"), text_color="#b8c5d6").pack(side=tk.LEFT, padx=(0, 6))
        tree_limit_entry = ctk.CTkEntry(single_row, width=70, height=32,
                                        font=("Consolas", 12, "bold"), placeholder_text="0",
                                        fg_color="#0d1b2a", text_color="#4ecca3",
                                        border_color="#4ecca3", border_width=2, corner_radius=8)
        tree_limit_entry.bind("<KeyRelease>", validate_number_input)
    else:
        tk.Label(single_row, text="Mục tiêu:", 
                font=("Segoe UI", 10, "bold"), fg="#b8c5d6", bg="#1e3a5f").pack(side=tk.LEFT, padx=(0, 6))
        tree_limit_entry = tk.Entry(single_row, width=8, font=("Consolas", 11, "bold"),
                                    bg="#0d1b2a", fg="#4ecca3", insertbackground="#4ecca3",
                                    relief=tk.SOLID, bd=2)
        tree_limit_entry.bind("<KeyRelease>", validate_number_input)
    tree_limit_entry.pack(side=tk.LEFT, padx=(0, 15))
    tree_limit_entry.insert(0, "20")
    
    # Đã chặt
    if CTK_AVAILABLE:
        ctk.CTkLabel(single_row, text="Đã chặt:", 
                    font=("Segoe UI", 11, "bold"), text_color="#b8c5d6").pack(side=tk.LEFT, padx=(0, 6))
    else:
        tk.Label(single_row, text="Đã chặt:",
                font=("Segoe UI", 10, "bold"), fg="#b8c5d6", bg="#1e3a5f").pack(side=tk.LEFT, padx=(0, 6))
    
    trees_chopped_label = tk.StringVar(value="0/∞")
    if CTK_AVAILABLE:
        progress_label = ctk.CTkLabel(single_row, textvariable=trees_chopped_label,
                                     font=("Consolas", 11, "bold"), text_color="#4ecca3",
                                     width=70, height=32, corner_radius=8,
                                     fg_color="#0d1b2a")
    else:
        progress_label = tk.Label(single_row, textvariable=trees_chopped_label,
                                 font=("Consolas", 10, "bold"), fg="#4ecca3", bg="#0d1b2a",
                                 width=8, relief=tk.FLAT, bd=2)
    progress_label.pack(side=tk.LEFT, padx=(0, 15))
    info_labels["_trees_chopped_label"] = trees_chopped_label
    
    # Bán gỗ (cùng dòng)
    def toggle_sell(state=None):
        global auto_sell_enabled, is_selling
        if CTK_AVAILABLE and state is None:
            auto_sell_enabled = sell_switch.get()
        else:
            auto_sell_enabled = state
        if auto_sell_enabled:
            log_message("[💰 BÁN] Chức năng bán gỗ BẬT!")
        else:
            log_message("[💰 BÁN] Chức năng bán gỗ TẮT!")
            # Reset is_selling nếu tắt chức năng bán
            is_selling = False
    
    if CTK_AVAILABLE:
        ctk.CTkLabel(single_row, text="Bán gỗ:", 
                    font=("Segoe UI", 11, "bold"), text_color="#b8c5d6").pack(side=tk.LEFT, padx=(0, 8))
        sell_switch = ctk.CTkSwitch(single_row, text="", command=toggle_sell, width=45, height=24,
                    fg_color="#e74c3c", progress_color="#4ecca3",
                                    button_color="#ffffff", button_hover_color="#d5dde8")
        sell_switch.pack(side=tk.LEFT)
        sell_switch.select()  # Set bán gỗ mặc định là ON
        info_labels["_sell_switch"] = sell_switch
        toggle_sell(True)  # Khởi tạo auto_sell_enabled = True
    else:
        tk.Label(single_row, text="Bán gỗ:",
                font=("Segoe UI", 10, "bold"), fg="#b8c5d6", bg="#1e3a5f").pack(side=tk.LEFT, padx=(0, 8))
        sell_switch = ToggleSwitch(single_row, width=45, height=24,
                                   bg_on="#00ff88", bg_off="#ff3333", command=toggle_sell)
        sell_switch.pack(side=tk.LEFT)
        sell_switch.on()  # Set bán gỗ mặc định là ON
        info_labels["_sell_switch"] = sell_switch
        toggle_sell(True)  # Khởi tạo auto_sell_enabled = True
    
    # === CƯA GỖ (WOODCUTTING) - DÒNG MỚI ===
    woodcut_row = tk.Frame(input_card, bg="#1e3a5f")
    if CTK_AVAILABLE:
        woodcut_row = ctk.CTkFrame(input_card, fg_color="transparent")
    woodcut_row.pack(fill=tk.X, padx=12, pady=10)
    
    def toggle_woodcut(state=None):
        global enable_woodcutting, sawmill_locations, is_woodcutting
        if CTK_AVAILABLE and state is None:
            enable_woodcutting = woodcut_switch.get()
        else:
            enable_woodcutting = state
        
        if enable_woodcutting:
            # Load sawmill locations nếu chưa load
            if not sawmill_locations:
                if load_sawmill_locations():
                    if sawmill_locations:
                        log_message(f"[🏭 CƯA GỖ] Chức năng cưa gỗ BẬT! Đã tìm {len(sawmill_locations)} máy cưa")
                    else:
                        log_message("[🏭 CƯA GỖ] ⚠️ Không tìm thấy máy cưa nào trong location.json!")
                        enable_woodcutting = False
                        if CTK_AVAILABLE:
                            woodcut_switch.set(False)
                        else:
                            woodcut_switch.set(False)
                else:
                    log_message("[🏭 CƯA GỖ] ⚠️ Lỗi load location.json!")
                    enable_woodcutting = False
                    if CTK_AVAILABLE:
                        woodcut_switch.set(False)
                    else:
                        woodcut_switch.set(False)
            else:
                log_message(f"[🏭 CƯA GỖ] Chức năng cưa gỗ BẬT! ({len(sawmill_locations)} máy cưa sẵn sàng)")
        else:
            log_message("[🏭 CƯA GỖ] Chức năng cưa gỗ TẮT!")
            # Reset is_woodcutting nếu tắt chức năng cưa
            is_woodcutting = False
    
    if CTK_AVAILABLE:
        ctk.CTkLabel(woodcut_row, text="Cưa gỗ:", 
                    font=("Segoe UI", 11, "bold"), text_color="#b8c5d6").pack(side=tk.LEFT, padx=(0, 8))
        woodcut_switch = ctk.CTkSwitch(woodcut_row, text="", command=toggle_woodcut, width=45, height=24,
                    fg_color="#3498db", progress_color="#4ecca3",
                                    button_color="#ffffff", button_hover_color="#d5dde8")
        woodcut_switch.pack(side=tk.LEFT)
        woodcut_switch.select()  # Set cưa gỗ mặc định là ON
        toggle_woodcut(True)  # Khởi tạo load sawmill locations
        info_labels["_woodcut_switch"] = woodcut_switch
    else:
        tk.Label(woodcut_row, text="Cưa gỗ:",
                font=("Segoe UI", 10, "bold"), fg="#b8c5d6", bg="#1e3a5f").pack(side=tk.LEFT, padx=(0, 8))
        woodcut_switch = ToggleSwitch(woodcut_row, width=45, height=24,
                                   bg_on="#00ff88", bg_off="#3333ff", command=toggle_woodcut)
        woodcut_switch.pack(side=tk.LEFT)
        woodcut_switch.on()  # Set cưa gỗ mặc định là ON
        toggle_woodcut(True)  # Khởi tạo load sawmill locations
        info_labels["_woodcut_switch"] = woodcut_switch

    # === TỰ VÀO LẠI GAME KHI VĂNG (AUTO RE-LOGIN) ===
    def toggle_relogin(state=None):
        global auto_relogin_enabled
        if CTK_AVAILABLE and state is None:
            auto_relogin_enabled = relogin_switch.get()
        else:
            auto_relogin_enabled = state
        if auto_relogin_enabled:
            log_message("[🔄 RE-LOGIN] Tự động vào lại game khi văng: BẬT!")
        else:
            log_message("[🔄 RE-LOGIN] Tự động vào lại game khi văng: TẮT!")
        save_account_info(login_username, login_password, auto_relogin_enabled)

    if CTK_AVAILABLE:
        ctk.CTkLabel(woodcut_row, text="Tự vào lại:", 
                    font=("Segoe UI", 11, "bold"), text_color="#b8c5d6").pack(side=tk.LEFT, padx=(15, 8))
        relogin_switch = ctk.CTkSwitch(woodcut_row, text="", command=toggle_relogin, width=45, height=24,
                    fg_color="#34495e", progress_color="#4ecca3",
                    button_color="#ffffff", button_hover_color="#d5dde8")
        relogin_switch.pack(side=tk.LEFT)
        if auto_relogin_enabled:
            relogin_switch.select()
        else:
            relogin_switch.deselect()
        info_labels["_relogin_switch"] = relogin_switch
    else:
        tk.Label(woodcut_row, text="Tự vào lại:",
                font=("Segoe UI", 10, "bold"), fg="#b8c5d6", bg="#1e3a5f").pack(side=tk.LEFT, padx=(15, 8))
        relogin_switch = ToggleSwitch(woodcut_row, width=45, height=24,
                                   bg_on="#00ff88", bg_off="#555555", command=toggle_relogin)
        relogin_switch.pack(side=tk.LEFT)
        if auto_relogin_enabled:
            relogin_switch.on()
        else:
            relogin_switch.off()
        info_labels["_relogin_switch"] = relogin_switch

    # Activity Log section
    if CTK_AVAILABLE:
        ctk.CTkLabel(left_panel, text="📋 NHẬT KÝ",
                    font=("Segoe UI", 12, "bold"), text_color="#93a8c1").pack(pady=(6, 5))
    else:
        tk.Label(left_panel, text="📋 NHẬT KÝ",
                font=("Segoe UI", 11, "bold"), fg="#93a8c1", bg="#1a1f3a").pack(pady=(6, 5))
    
    if CTK_AVAILABLE:
        log_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
    else:
        log_frame = tk.Frame(left_panel, bg="#16213e")
    log_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=(0, 10))
    
    log_scroll = tk.Scrollbar(log_frame, bg="#2a3f5f", troughcolor="#0d1b2a")
    log_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    
    log_text = tk.Text(log_frame, height=12, bg="#0d1b2a", fg="#4ecca3",
                      font=("Consolas", 9), yscrollcommand=log_scroll.set,
                      wrap=tk.WORD, relief=tk.FLAT, bd=0, padx=8, pady=8,
                      insertbackground="#4ecca3")
    log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    log_scroll.config(command=log_text.yview)

    # ============ RIGHT PANEL - Info & Controls ============
    if CTK_AVAILABLE:
        right_panel = ctk.CTkFrame(content, fg_color=("#16213e", "#16213e"), corner_radius=15, width=280)
    else:
        right_panel = tk.Frame(content, bg="#16213e", relief=tk.RAISED, bd=2)
    right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
    right_panel.pack_propagate(False)

    # Info header
    if CTK_AVAILABLE:
        info_header = ctk.CTkLabel(right_panel, text="📊 THÔNG TIN",
                                   font=("Segoe UI", 16, "bold"), text_color="#4ecca3")
    else:
        info_header = tk.Label(right_panel, text="📊 THÔNG TIN",
                              font=("Segoe UI", 16, "bold"), fg="#4ecca3", bg="#16213e")
    info_header.pack(pady=(10, 8))

    # Separator
    if CTK_AVAILABLE:
        sep2 = ctk.CTkFrame(right_panel, height=2, fg_color="#4ecca3")
    else:
        sep2 = tk.Frame(right_panel, height=2, bg="#4ecca3")
    sep2.pack(fill=tk.X, padx=15, pady=(0, 10))

    # Info labels with icons
    labels_config = [
        ("🔑 Key:", "Đang kiểm tra..."),
        ("📅 Hết hạn:", "N/A"),
        ("⏰ Còn lại:", "N/A"),
        ("🤖 Bot:", "TẮT"),
        ("🎯 Cây:", "N/A"),
    ]
    
    for key, default_value in labels_config:
        # Label container - CÙNG 1 DÒNG NGANG
        if CTK_AVAILABLE:
            label_container = ctk.CTkFrame(right_panel, fg_color="#1e3a5f", corner_radius=8)
        else:
            label_container = tk.Frame(right_panel, bg="#1e3a5f")
        label_container.pack(fill="x", padx=2, pady=2)
        
        # Label và Value cùng 1 hàng
        if CTK_AVAILABLE:
            inner_row = ctk.CTkFrame(label_container, fg_color="transparent")
        else:
            inner_row = tk.Frame(label_container, bg="#1e3a5f")
        inner_row.pack(fill="x", padx=8, pady=4)
        
        # Key label (bên trái)
        if CTK_AVAILABLE:
            ctk.CTkLabel(inner_row, text=key, font=("Segoe UI", 10),
                        text_color="#b8c5d6", anchor="w", width=80).pack(side=tk.LEFT)
        else:
            tk.Label(inner_row, text=key, font=("Segoe UI", 9),
                    fg="#b8c5d6", bg="#1e3a5f", anchor="w", width=10).pack(side=tk.LEFT)
        
        # Value label (bên phải)
        var = tk.StringVar(value=default_value)
        if CTK_AVAILABLE:
            value_label = ctk.CTkLabel(inner_row, textvariable=var,
                                      font=("Consolas", 10, "bold"), text_color="#4ecca3",
                                      anchor="w", fg_color="transparent")
        else:
            value_label = tk.Label(inner_row, textvariable=var,
                                  font=("Consolas", 9, "bold"), fg="#4ecca3",
                                  bg="#1e3a5f", anchor="w", relief=tk.FLAT)
        value_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        info_labels[key] = var

    # Control buttons section
    if CTK_AVAILABLE:
        btn_container = ctk.CTkFrame(right_panel, fg_color="transparent")
    else:
        btn_container = tk.Frame(right_panel, bg="#16213e")
    btn_container.pack(fill="x", padx=12, pady=2)

    # Toggle button (BẬT/TẠM DỪNG tool)
    if CTK_AVAILABLE:
        toggle_btn = ctk.CTkButton(btn_container, text="▶️ BẬT TOOL", command=toggle_bot,
                                   font=("Segoe UI", 14, "bold"), fg_color="#e74c3c",
                                   hover_color="#c0392b", height=30, corner_radius=12)
        toggle_btn.pack(fill="x", pady=2)
    else:
        toggle_btn = RoundedButton(btn_container, text="▶️ BẬT TOOL", command=toggle_bot,
                                   bg_color="#e74c3c", fg_color="#000000", active_bg_color="#c0392b",
                                   width=240, height=30, radius=12,
                                   font=("Segoe UI", 14, "bold"))
        toggle_btn.pack(fill="x", pady=2)

    # Reset button (RESET số cây về 0)
    if CTK_AVAILABLE:
        reset_btn = ctk.CTkButton(btn_container, text="🔄 RESET SỐ CÂY", command=reset_counter,
                                   font=("Segoe UI", 12, "bold"), fg_color="#9b59b6",
                                   hover_color="#8e44ad", height=25, corner_radius=10)
        reset_btn.pack(fill="x", pady=2)
    else:
        reset_btn = RoundedButton(btn_container, text="🔄 RESET SỐ CÂY", command=reset_counter,
                                   bg_color="#9b59b6", fg_color="#ffffff", active_bg_color="#8e44ad",
                                   width=240, height=25, radius=10,
                                   font=("Segoe UI", 12, "bold"))
        reset_btn.pack(fill="x", pady=2)

    # Refresh game progress button (QUÉT LẠI TIẾN TRÌNH)
    if CTK_AVAILABLE:
        refresh_btn = ctk.CTkButton(btn_container, text="🔍 QUÉT LẠI TIẾN TRÌNH", command=refresh_game_progress,
                                    font=("Segoe UI", 12, "bold"), fg_color="#f39c12",
                                    hover_color="#e67e22", height=25, corner_radius=10)
        refresh_btn.pack(fill="x", pady=2)
    else:
        refresh_btn = RoundedButton(btn_container, text="🔍 QUÉT LẠI TIẾN TRÌNH", command=refresh_game_progress,
                                    bg_color="#f39c12", fg_color="#ffffff", active_bg_color="#e67e22",
                                    width=240, height=25, radius=10,
                                    font=("Segoe UI", 12, "bold"))
        refresh_btn.pack(fill="x", pady=2)

    # Exit button
    def exit_tool():
        global is_bot_active
        is_bot_active = False
        log_message("[🚪 THOÁT] Đang thoát tool...")
        root.after(500, root.quit)
    
    if CTK_AVAILABLE:
        exit_btn = ctk.CTkButton(btn_container, text="🚪 THOÁT", command=exit_tool,
                                font=("Segoe UI", 14, "bold"), fg_color="#34495e",
                                hover_color="#2c3e50", height=30, corner_radius=12)
        exit_btn.pack(fill="x")
    else:
        exit_btn = RoundedButton(btn_container, text="🚪 THOÁT", command=exit_tool,
                                bg_color="#34495e", fg_color="#000000", active_bg_color="#2c3e50",
                                width=240, height=30, radius=12,
                                font=("Segoe UI", 14, "bold"))
        exit_btn.pack(fill="x")

    # Footer
    if CTK_AVAILABLE:
        footer = ctk.CTkLabel(right_panel, text="⚡ AI Technology v2.0 ⚡",
                             font=("Segoe UI", 9), text_color="#5a6c7d")
    else:
        footer = tk.Label(right_panel, text="⚡ AI v2.0 ⚡",
                         font=("Segoe UI", 9), fg="#5a6c7d", bg="#16213e")
    footer.pack(side=tk.BOTTOM, pady=(12, 10))
    
    log_message("✅ Giao diện khởi tạo thành công!")


def update_gui_info(player_data, target_info, bot_status, delta_yaw_deg, is_moving, g_tree_cooldowns):
    global total_trees_chopped, tree_chop_limit, GLOBAL_KEY_INFO
    
    # 🔑 Hiển thị thông tin Key
    if GLOBAL_KEY_INFO.get("is_lifetime"):
        info_labels["🔑 Key:"].set("✅ VĨNH VIỄN")
        info_labels["📅 Hết hạn:"].set("Vĩnh viễn")
        info_labels["⏰ Còn lại:"].set("Vĩnh viễn")
    elif GLOBAL_KEY_INFO.get("expiry"):
        info_labels["🔑 Key:"].set("✅ CÓ HIỆU LỰC")
        info_labels["📅 Hết hạn:"].set(GLOBAL_KEY_INFO["expiry"])
        
        # Tính toán thời gian còn lại
        if GLOBAL_KEY_INFO.get("expire_time_ms"):
            expire_ms = GLOBAL_KEY_INFO["expire_time_ms"]
            current_ms = time.time() * 1000
            remaining_ms = expire_ms - current_ms
            
            if remaining_ms > 0:
                remaining_days = int(remaining_ms // (1000 * 60 * 60 * 24))
                remaining_hours = int((remaining_ms % (1000 * 60 * 60 * 24)) // (1000 * 60 * 60))
                remaining_mins = int((remaining_ms % (1000 * 60 * 60)) // (1000 * 60))
                
                if remaining_days > 0:
                    time_str = f"{remaining_days} ngày {remaining_hours} giờ {remaining_mins} phút"
                elif remaining_hours > 0:
                    time_str = f"{remaining_hours} giờ {remaining_mins} phút"
                else:
                    time_str = f"{remaining_mins} phút"
                
                info_labels["⏰ Còn lại:"].set(time_str)
            else:
                info_labels["⏰ Còn lại:"].set("❌ Hết hạn")
        else:
            info_labels["⏰ Còn lại:"].set("N/A")
    elif GLOBAL_KEY_INFO.get("hwid_mismatch"):
        info_labels["🔑 Key:"].set("❌ HWID KHÔNG MATCH")
        info_labels["📅 Hết hạn:"].set("N/A")
        info_labels["⏰ Còn lại:"].set("N/A")
    else:
        info_labels["🔑 Key:"].set("⚠️ CHƯA KIỂM TRA")
        info_labels["📅 Hết hạn:"].set("N/A")
        info_labels["⏰ Còn lại:"].set("N/A")
    info_labels["🤖 Bot:"].set("BẬT" if bot_status else "TẮT")
    limit_str = str(tree_chop_limit) if tree_chop_limit > 0 else "∞"
    if "_trees_chopped_label" in info_labels:
        info_labels["_trees_chopped_label"].set(f"{total_trees_chopped}/{limit_str}")

    if target_info:
        distance, target_index, t_x, t_y = target_info
        info_labels["🎯 Cây:"].set(f"Index: {target_index} (Cây)")
    else:
        info_labels["🎯 Cây:"].set("N/A")

def rgb_to_int(r, g, b):
    return (r << 16) | (g << 8) | b

def color_within_tolerance(c1, c2, tol):
    r1, g1, b1 = (c1 >> 16) & 0xFF, (c1 >> 8) & 0xFF, c1 & 0xFF
    r2, g2, b2 = (c2 >> 16) & 0xFF, (c2 >> 8) & 0xFF, c2 & 0xFF
    return abs(r1 - r2) <= tol and abs(g1 - g2) <= tol and abs(b1 - b2) <= tol

def get_pixel(image, x, y):
    px = image.load()
    return rgb_to_int(*px[x - REGION_MIN_X, y - REGION_MIN_Y])

def is_color_in_area(image, base_color, cx, cy, tolerance):
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            rel_x = cx + dx - REGION_MIN_X
            rel_y = cy + dy - REGION_MIN_Y
            
            if 0 <= rel_x < REGION_WIDTH and 0 <= rel_y < REGION_HEIGHT:
                try:
                    check_color = get_pixel(image, cx + dx, cy + dy)
                    if color_within_tolerance(base_color, check_color, tolerance):
                        return True
                except IndexError:
                    continue
    return False

def load_sawmill_locations():
    """Các máy cưa đã được hardcode - không cần đọc file"""
    global sawmill_locations
    # Dữ liệu sawmill_locations đã được hardcode ở trên
    if sawmill_locations and len(sawmill_locations) > 0:
        log_message(f"[WOODCUT] 🏭 Đã có sẵn {len(sawmill_locations)} máy cưa (hardcode)")
        return True
    return False

def template_detection_realtime_thread():
    """
    Background thread để detect template realtime từ màn hình bằng mss
    Dùng cv2.matchTemplate() giống như hàm detect gốc (chỉ khác là chạy riêng)
    """
    global template_detection_running, cached_go_detected, cached_vango_detected, template_detection_lock, TEMPLATE_DETECT_INTERVAL
    
    log_message(f"[WOODCUT] 🧵 Realtime template detection thread started (mss + cv2.matchTemplate)")
    
    # Load template files một lần duy nhất (không load lại mỗi frame)
    template_go = None
    template_vango = None
    
    try:
        template_go_path = os.path.join(SCRIPT_DIR, "templates", "go.png")
        template_vango_path = os.path.join(SCRIPT_DIR, "templates", "vango.png")
        
        if os.path.exists(template_go_path):
            template_go = cv2.imread(template_go_path)
            log_message(f"[WOODCUT] ✅ Loaded go.png template")
        
        if os.path.exists(template_vango_path):
            template_vango = cv2.imread(template_vango_path)
            log_message(f"[WOODCUT] ✅ Loaded vango.png template")
    except Exception as e:
        log_message(f"[WOODCUT] ⚠️ Error loading templates: {e}")
    
    MATCH_THRESHOLD = 0.70  # 70% match = detect
    
    while template_detection_running:
        try:
            # Capture vùng template từ màn hình realtime
            with mss.mss() as sct:
                monitor = sct.monitors[1]
                screenshot = sct.grab(monitor)
                screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGBA2BGR)
            
            # Crop search region
            search_region = screenshot_cv[TEMPLATE_REGION_Y1:TEMPLATE_REGION_Y2+1, TEMPLATE_REGION_X1:TEMPLATE_REGION_X2+1]
            
            go_detected = False
            vango_detected = False
            
            # Detect go.png
            if template_go is not None:
                try:
                    result = cv2.matchTemplate(search_region, template_go, cv2.TM_CCOEFF_NORMED)
                    _, max_val, _, _ = cv2.minMaxLoc(result)
                    go_detected = max_val >= MATCH_THRESHOLD
                except:
                    pass
            
            # Detect vango.png (chỉ nếu chưa detect go.png)
            if not go_detected and template_vango is not None:
                try:
                    result = cv2.matchTemplate(search_region, template_vango, cv2.TM_CCOEFF_NORMED)
                    _, max_val, _, _ = cv2.minMaxLoc(result)
                    vango_detected = max_val >= MATCH_THRESHOLD
                except:
                    pass
            
            # Update cache thread-safe
            with template_detection_lock:
                cached_go_detected = go_detected
                cached_vango_detected = vango_detected
            
            # Sleep để không spam
            time.sleep(TEMPLATE_DETECT_INTERVAL / 1000.0)
            
        except Exception as e:
            # Log error nhẹ
            # log_message(f"[WOODCUT] ⚠️ Error in realtime detection: {e}")
            time.sleep(0.1)
    
    log_message(f"[WOODCUT] 🧵 Realtime template detection thread stopped")

def detect_go_template_cached():
    """Get cached go.png detection result (thread-safe)"""
    global cached_go_detected, template_detection_lock
    
    with template_detection_lock:
        return cached_go_detected

def detect_vango_template_cached():
    """Get cached vango.png detection result (thread-safe)"""
    global cached_vango_detected, template_detection_lock
    
    with template_detection_lock:
        return cached_vango_detected

def start_template_detection_thread():
    """Khởi động background thread detection realtime"""
    global template_detection_thread, template_detection_running
    
    if template_detection_thread is None or not template_detection_thread.is_alive():
        template_detection_running = True
        template_detection_thread = threading.Thread(target=template_detection_realtime_thread, daemon=True)
        template_detection_thread.start()
        log_message(f"[WOODCUT] ✅ Realtime template detection thread started")

def stop_template_detection_thread():
    """Dừng background thread"""
    global template_detection_running, template_detection_thread
    
    template_detection_running = False
    if template_detection_thread:
        try:
            template_detection_thread.join(timeout=2)
        except:
            pass
    log_message(f"[WOODCUT] ✅ Realtime template detection thread stopped")

def detect_go_template():
    """
    Phát hiện template go.png bằng pixel color matching.
    Region: (TEMPLATE_REGION_X1, TEMPLATE_REGION_Y1) to (TEMPLATE_REGION_X2, TEMPLATE_REGION_Y2)
    
    Logic: So sánh màu pixel template với screenshot, dùng tolerance 0.9 (90% match)
    """
    try:
        if not CV2_AVAILABLE or cv2 is None or np is None:
            log_message(f"[WOODCUT] ⚠️ cv2/numpy không khả dụng, bỏ qua template detection")
            return False
        
        # Load template file
        template_path = os.path.join(SCRIPT_DIR, "templates", "go.png")
        log_message(f"[WOODCUT] 📁 Template path: {template_path}")
        
        if not os.path.exists(template_path):
            log_message(f"[WOODCUT] ⚠️ Template file không tìm thấy: {template_path}")
            return False
        
        log_message(f"[WOODCUT] ✅ Template file tìm thấy")
        
        # Load template image
        template = cv2.imread(template_path)
        if template is None:
            log_message(f"[WOODCUT] ⚠️ Không thể load template: {template_path}")
            return False
        
        log_message(f"[WOODCUT] ✅ Template loaded: {template.shape}")
        
        # Screenshot với mss (nhanh hơn pyautogui)
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            screenshot = sct.grab(monitor)
            screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGBA2BGR)
        
        # Crop vùng tìm kiếm từ screenshot (lớn hơn template để search)
        search_region = screenshot_cv[TEMPLATE_REGION_Y1:TEMPLATE_REGION_Y2+1, TEMPLATE_REGION_X1:TEMPLATE_REGION_X2+1]
        log_message(f"[WOODCUT] 📸 Search region: {search_region.shape} from ({TEMPLATE_REGION_X1},{TEMPLATE_REGION_Y1}) to ({TEMPLATE_REGION_X2},{TEMPLATE_REGION_Y2})")
        log_message(f"[WOODCUT] 📋 Template size: {template.shape}")
        
        # Kiểm tra template có nhỏ hơn search region không
        if template.shape[0] > search_region.shape[0] or template.shape[1] > search_region.shape[1]:
            log_message(f"[WOODCUT] ⚠️ Template lớn hơn search region, không thể tìm kiếm")
            return False
        
        # Dùng cv2.matchTemplate để tìm template bên trong search_region
        # Method: TM_CCOEFF_NORMED (normalized, -1 to 1 scale)
        result = cv2.matchTemplate(search_region, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        # max_val là độ match cao nhất (0 to 1 scale)
        match_percentage = max_val
        
        # Threshold: nếu max_val >= 0.7 thì coi là tìm thấy
        MATCH_THRESHOLD = 0.7  # 70% match là đủ
        is_detected = match_percentage >= MATCH_THRESHOLD
        
        # 📝 LUÔN LOG kết quả
        log_message(f"[WOODCUT] 🎯 Template Match: {match_percentage*100:.1f}% | Detect: {is_detected} | (threshold={MATCH_THRESHOLD*100}%, method=TM_CCOEFF_NORMED)")
        
        return is_detected
        
    except Exception as e:
        log_message(f"[WOODCUT] ⚠️ Lỗi detect_go_template: {type(e).__name__}: {e}")
        import traceback
        log_message(f"[WOODCUT] Traceback: {traceback.format_exc()}")
        return False

def detect_vango_template():
    """
    Phát hiện template vango.png (van gỗ đã cưa xong - không còn gỗ để xẻ)
    Region: (TEMPLATE_REGION_X1, TEMPLATE_REGION_Y1) to (TEMPLATE_REGION_X2, TEMPLATE_REGION_Y2)
    
    Logic: So sánh màu pixel template với screenshot, dùng tolerance 0.9 (90% match)
    """
    try:
        if not CV2_AVAILABLE or cv2 is None or np is None:
            log_message(f"[WOODCUT] ⚠️ cv2/numpy không khả dụng, bỏ qua vango template detection")
            return False
        
        # Load template file
        template_path = os.path.join(SCRIPT_DIR, "templates", "vango.png")
        log_message(f"[WOODCUT] 📁 Vango Template path: {template_path}")
        
        if not os.path.exists(template_path):
            log_message(f"[WOODCUT] ⚠️ Template vango.png không tìm thấy: {template_path}")
            return False
        
        log_message(f"[WOODCUT] ✅ Vango Template file tìm thấy")
        
        # Load template image
        template = cv2.imread(template_path)
        if template is None:
            log_message(f"[WOODCUT] ⚠️ Không thể load vango.png: {template_path}")
            return False
        
        log_message(f"[WOODCUT] ✅ Vango Template loaded: {template.shape}")
        
        # Screenshot với mss (nhanh hơn pyautogui)
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            screenshot = sct.grab(monitor)
            screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGBA2BGR)
        
        # Crop vùng tìm kiếm từ screenshot
        search_region = screenshot_cv[TEMPLATE_REGION_Y1:TEMPLATE_REGION_Y2+1, TEMPLATE_REGION_X1:TEMPLATE_REGION_X2+1]
        
        # Kiểm tra template có nhỏ hơn search region không
        if template.shape[0] > search_region.shape[0] or template.shape[1] > search_region.shape[1]:
            log_message(f"[WOODCUT] ⚠️ Template vango.png lớn hơn search region, không thể tìm kiếm")
            return False
        
        # Dùng cv2.matchTemplate để tìm template
        result = cv2.matchTemplate(search_region, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        # max_val là độ match cao nhất (0 to 1 scale)
        match_percentage = max_val
        
        # Threshold: nếu max_val >= 0.7 thì coi là tìm thấy
        MATCH_THRESHOLD = 0.7  # 70% match là đủ
        is_detected = match_percentage >= MATCH_THRESHOLD
        
        # 📝 LUÔN LOG kết quả
        log_message(f"[WOODCUT] 🎯 Vango Template Match: {match_percentage*100:.1f}% | Detect: {is_detected} | (threshold={MATCH_THRESHOLD*100}%, method=TM_CCOEFF_NORMED)")
        
        return is_detected
        
    except Exception as e:
        log_message(f"[WOODCUT] ⚠️ Lỗi detect_vango_template: {type(e).__name__}: {e}")
        import traceback
        log_message(f"[WOODCUT] Traceback: {traceback.format_exc()}")
        return False

# ====================================================================
# KIỂM TRA TÚI ĐỒ ĐẦY & KÍCH HOẠT ĐI BÁN GỖ NGAY LẬP TỨC
# ====================================================================
FULL_BAG_TEMPLATE = None
FULL_BAG_LOADED = False

def detect_inventory_full():
    """
    Phát hiện thông báo 'THẤT BẠI - Túi đồ của bạn đã đầy, không thể nhặt Gỗ x1'
    Vùng quét: Nửa bên phải màn hình 1280x720 (okokNotify của FiveM)
    (X: 720 -> 1280, Y: 10 -> 480)
    """
    global FULL_BAG_TEMPLATE, FULL_BAG_LOADED
    try:
        if not CV2_AVAILABLE or cv2 is None or np is None:
            return False
        
        # Load template một lần và cache
        if not FULL_BAG_LOADED:
            for tmpl_name in ["full_bag.png", "daytui_card.png", "full_bag_notify.png"]:
                tmpl_path = os.path.join(SCRIPT_DIR, "templates", tmpl_name)
                if not os.path.exists(tmpl_path) and getattr(sys, 'frozen', False):
                    alt_path = os.path.join(os.path.dirname(sys.executable), "templates", tmpl_name)
                    if os.path.exists(alt_path):
                        tmpl_path = alt_path
                if os.path.exists(tmpl_path):
                    FULL_BAG_TEMPLATE = cv2.imread(tmpl_path)
                    if FULL_BAG_TEMPLATE is not None:
                        break
            FULL_BAG_LOADED = True
            
        if FULL_BAG_TEMPLATE is None:
            return False

        # Vùng thông báo bên phải trên màn hình 1280x720
        with mss.mss() as sct:
            monitor = {"top": 10, "left": 720, "width": 560, "height": 470}
            sct_img = sct.grab(monitor)
            screen_bgr = cv2.cvtColor(np.array(sct_img), cv2.COLOR_BGRA2BGR)
            
        if screen_bgr.shape[0] < FULL_BAG_TEMPLATE.shape[0] or screen_bgr.shape[1] < FULL_BAG_TEMPLATE.shape[1]:
            return False

        # 1. Match Template
        res = cv2.matchTemplate(screen_bgr, FULL_BAG_TEMPLATE, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(res)
        
        # 2. Kiểm tra màu đỏ đặc trưng của badge 'THẤT BẠI' (okokNotify error)
        # BGR: R > 180, R - B > 40, R - G > 40
        b, g, r = cv2.split(screen_bgr.astype(int))
        red_pixels = int(np.sum((r > 180) & (r - b > 40) & (r - g > 40)))
        
        # Nếu match template >= 0.65 hoặc (match >= 0.50 và có badge màu đỏ >= 200 pixel)
        if max_val >= 0.65 or (max_val >= 0.50 and red_pixels >= 200):
            log_message(f"[INVENTORY] 🎒 Phát hiện túi đồ đã đầy! (Match: {max_val*100:.1f}%, Red: {red_pixels}px)")
            return True
            
        return False
    except Exception as e:
        return False

def trigger_sell_due_to_full_inventory():
    """Kích hoạt đi bán gỗ ngay lập tức khi đầy túi đồ"""
    global auto_sell_enabled, is_selling, sell_point_index, sell_click_count
    global is_chopping, chop_state, spam_key, keys_pressed, is_moving
    
    log_message("[INVENTORY] 🎒 TÚI ĐỒ ĐÃ ĐẦY! Dừng chặt cây và chuyển sang NPC bán gỗ ngay...")
    
    # Nhả tất cả các phím đang nhấn
    for k in [KEY_FORWARD, KEY_AUTORUN, 'e', 'f', 'y', 'w', 's', 'a', 'd', 'space']:
        try:
            keyboard.release(k)
        except Exception:
            pass
            
    is_chopping = False
    chop_state = "IDLE"
    spam_key = "None"
    keys_pressed = "None"
    is_moving = False
    
    # Bật quy trình bán gỗ ngay lập tức
    auto_sell_enabled = True
    select_random_route()
    is_selling = True
    sell_point_index = 0
    sell_click_count = 0
    set_moving(False, "Túi đồ đã đầy - Đi bán gỗ ngay lập tức")

# ====================================================================
# KIỂM TRA VÀ TỰ ĐỘNG TẮT BẢN ĐỒ (PAUSE MENU / MAP) KHI LỠ BẤM ESC
# ====================================================================
MAP_TAB_TEMPLATE = None
MAP_ESC_TEMPLATE = None
MAP_TEMPLATES_LOADED = False
last_map_close_time = 0.0

def detect_map_active():
    """
    Phát hiện nếu game đang bị mở Menu Bản Đồ (GTA V / FiveM Pause Menu / Map)
    Dựa trên nhận diện:
    1. Tab 'MAP' màu trắng nổi bật ở thanh menu trên cùng (y ~ 80..170, x ~ 170..380 trên 1280x720)
    2. Nút 'Back Esc' ở góc dưới bên phải (y ~ 640..720, x ~ 1060..1240 trên 1280x720)
    """
    global MAP_TAB_TEMPLATE, MAP_ESC_TEMPLATE, MAP_TEMPLATES_LOADED
    try:
        if not CV2_AVAILABLE or cv2 is None or np is None:
            return False
            
        if not MAP_TEMPLATES_LOADED:
            tab_path = os.path.join(SCRIPT_DIR, "templates", "map_tab_720p.png")
            if not os.path.exists(tab_path) and getattr(sys, 'frozen', False):
                alt = os.path.join(os.path.dirname(sys.executable), "templates", "map_tab_720p.png")
                if os.path.exists(alt):
                    tab_path = alt
            if os.path.exists(tab_path):
                MAP_TAB_TEMPLATE = cv2.imread(tab_path)
                
            esc_path = os.path.join(SCRIPT_DIR, "templates", "map_esc_720p.png")
            if not os.path.exists(esc_path) and getattr(sys, 'frozen', False):
                alt = os.path.join(os.path.dirname(sys.executable), "templates", "map_esc_720p.png")
                if os.path.exists(alt):
                    esc_path = alt
            if os.path.exists(esc_path):
                MAP_ESC_TEMPLATE = cv2.imread(esc_path)
                
            MAP_TEMPLATES_LOADED = True
            
        if MAP_TAB_TEMPLATE is None and MAP_ESC_TEMPLATE is None:
            return False
            
        with mss.mss() as sct:
            score_tab = 0.0
            if MAP_TAB_TEMPLATE is not None:
                mon_tab = {"top": 80, "left": 170, "width": 210, "height": 90}
                img_tab = sct.grab(mon_tab)
                bgr_tab = cv2.cvtColor(np.array(img_tab), cv2.COLOR_BGRA2BGR)
                if bgr_tab.shape[0] >= MAP_TAB_TEMPLATE.shape[0] and bgr_tab.shape[1] >= MAP_TAB_TEMPLATE.shape[1]:
                    res_tab = cv2.matchTemplate(bgr_tab, MAP_TAB_TEMPLATE, cv2.TM_CCOEFF_NORMED)
                    score_tab = float(cv2.minMaxLoc(res_tab)[1])
                    
            score_esc = 0.0
            if MAP_ESC_TEMPLATE is not None:
                mon_esc = {"top": 640, "left": 1060, "width": 180, "height": 80}
                img_esc = sct.grab(mon_esc)
                bgr_esc = cv2.cvtColor(np.array(img_esc), cv2.COLOR_BGRA2BGR)
                if bgr_esc.shape[0] >= MAP_ESC_TEMPLATE.shape[0] and bgr_esc.shape[1] >= MAP_ESC_TEMPLATE.shape[1]:
                    res_esc = cv2.matchTemplate(bgr_esc, MAP_ESC_TEMPLATE, cv2.TM_CCOEFF_NORMED)
                    score_esc = float(cv2.minMaxLoc(res_esc)[1])
                    
        # Nếu tab MAP hiển thị (score >= 0.70) hoặc nút Back Esc hiển thị (score >= 0.70)
        if score_tab >= 0.70 or score_esc >= 0.70:
            return True
            
        return False
    except Exception:
        return False

def check_and_close_map_if_open():
    """
    Kiểm tra nếu lỡ bị mở Menu Bản Đồ (Pause Menu / Map) thì tự động bấm ESC để đóng lại
    """
    global last_map_close_time
    current_time = time.time()
    
    # Debounce 0.6s để tránh spam phím ESC quá nhanh
    if current_time - last_map_close_time < 0.6:
        return False
        
    if detect_map_active():
        log_message("[MAP] 🗺️ Phát hiện Menu Bản Đồ (Map) đang mở! Tự động bấm ESC để đóng lại...")
        
        # Thả các phím di chuyển nếu đang giữ
        for k in [KEY_FORWARD, KEY_AUTORUN, 'e', 'w', 's', 'a', 'd']:
            try:
                keyboard.release(k)
            except Exception:
                pass
                
        time.sleep(0.05)
        # Bấm ESC dứt khoát
        try:
            keyboard.press('esc')
            time.sleep(0.12)
            keyboard.release('esc')
        except Exception:
            pass
            
        last_map_close_time = current_time
        time.sleep(0.3)
        log_message("[MAP] ✅ Đã bấm ESC đóng bản đồ, bot tiếp tục hoạt động!")
        return True
        
    return False

# ====================================================================
# TỰ ĐỘNG ĐÓNG BẢNG MÃ PIN (NẾU XUẤT HIỆN TRONG GAME)
# ====================================================================
PIN_DIALOG_TEMPLATE = None
PIN_TEMPLATES_LOADED = False
last_pin_close_time = 0.0

def detect_pin_dialog_active():
    """
    Phát hiện nếu game đang bị mở bảng tạo mã PIN ('Tạo mã PIN mới' / 'HỆ THỐNG MÃ PIN CÔNG DÂN')
    """
    global PIN_DIALOG_TEMPLATE, PIN_TEMPLATES_LOADED
    try:
        if not CV2_AVAILABLE or cv2 is None or np is None:
            return False
            
        if not PIN_TEMPLATES_LOADED:
            for tmpl_name in ["pin_dialog_title.png", "pin_code_title.png", "pin_code_system_text.png"]:
                p = os.path.join(SCRIPT_DIR, "templates", tmpl_name)
                if not os.path.exists(p) and getattr(sys, 'frozen', False):
                    alt = os.path.join(os.path.dirname(sys.executable), "templates", tmpl_name)
                    if os.path.exists(alt):
                        p = alt
                if os.path.exists(p):
                    PIN_DIALOG_TEMPLATE = cv2.imread(p)
                    if PIN_DIALOG_TEMPLATE is not None:
                        break
            PIN_TEMPLATES_LOADED = True
            
        if PIN_DIALOG_TEMPLATE is None:
            return False
            
        with mss.mss() as sct:
            mon = {"top": 20, "left": 350, "width": 600, "height": 220}
            img = sct.grab(mon)
            bgr = cv2.cvtColor(np.array(img), cv2.COLOR_BGRA2BGR)
            
        if bgr.shape[0] < PIN_DIALOG_TEMPLATE.shape[0] or bgr.shape[1] < PIN_DIALOG_TEMPLATE.shape[1]:
            return False
            
        res = cv2.matchTemplate(bgr, PIN_DIALOG_TEMPLATE, cv2.TM_CCOEFF_NORMED)
        score = float(cv2.minMaxLoc(res)[1])
        if score >= 0.70:
            return True
            
        return False
    except Exception:
        return False

def check_and_close_pin_dialog_if_open():
    """
    Kiểm tra nếu thấy bảng mã PIN thì tự động bấm ESC để đóng
    """
    global last_pin_close_time
    current_time = time.time()
    if current_time - last_pin_close_time < 1.0:
        return False
        
    if detect_pin_dialog_active():
        log_message("[PIN] 🔐 Phát hiện bảng Tạo mã PIN mới -> Tự động bấm ESC để đóng...")
        try:
            keyboard.press('esc')
            time.sleep(0.12)
            keyboard.release('esc')
        except Exception:
            pass
        last_pin_close_time = current_time
        time.sleep(0.4)
        log_message("[PIN] ✅ Đã đóng bảng mã PIN, game tiếp tục hoạt động!")
        return True
    return False

# ====================================================================
# TỰ ĐỘNG ĐĂNG NHẬP LẠI LAUNCHER GTA5VN KHI VĂNG GAME
# ====================================================================
def kill_launcher_and_game_processes():
    """Tắt sạch tiến trình launcher hoặc game bị treo để restart sạch"""
    try:
        for proc in psutil.process_iter(['name']):
            try:
                name = (proc.info.get('name') or '').lower()
                if any(x in name for x in ['gta5vn', 'roslauncher', 'fivem']):
                    proc.kill()
            except Exception:
                pass
    except Exception:
        pass

def launch_gta5vn():
    """Khởi động GTA5VN Launcher"""
    global last_auto_launch_time
    current_time = time.time()
    if current_time - last_auto_launch_time < 8.0:
        return False
    last_auto_launch_time = current_time

    log_message("[RELOGIN] 🚀 Đang khởi động GTA5VN Launcher...")
    
    paths = [
        os.path.expandvars(r"%LOCALAPPDATA%\GTA5VN\GTA5VN.exe"),
        r"C:\Users\ASUS\AppData\Local\GTA5VN\GTA5VN.exe",
        os.path.expandvars(r"%USERPROFILE%\Downloads\GTA5VN.exe"),
        r"C:\Users\ASUS\Downloads\GTA5VN.exe"
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                subprocess.Popen([p], cwd=os.path.dirname(p))
                log_message(f"[RELOGIN] ✅ Đã khởi chạy: {p}")
                return True
            except Exception as e:
                log_message(f"[RELOGIN] ⚠️ Không thể mở trực tiếp {p}: {e}")
                
    try:
        log_message("[RELOGIN] 🔍 Mở qua Windows Search: Win -> 'GTA5VN' -> Enter...")
        pyautogui.press('win')
        time.sleep(0.5)
        keyboard.write("GTA5VN")
        time.sleep(0.6)
        pyautogui.press('enter')
        return True
    except Exception as e:
        log_message(f"[RELOGIN] ⚠️ Lỗi mở Windows Search: {e}")
        return False

def is_launcher_running():
    """Kiểm tra có launcher GTA5VN đang chạy hay không"""
    try:
        for proc in psutil.process_iter(['name']):
            name = (proc.info.get('name') or '').lower()
            if 'gta5vn' in name and 'subprocess' not in name:
                return True
    except Exception:
        pass
    return False

def check_and_handle_launcher_screens():
    """
    Tự động xử lý các màn hình launcher:
    - Màn hình 0: Đang kết nối... bị kẹt quá 5s -> Bấm Hủy kết nối & mở lại
    - Màn hình 1 (Đăng nhập): Nhập tài khoản, mật khẩu -> click Tham gia
    - Màn hình 2 (Roleplay): Click THAM GIA trong thẻ Roleplay
    - Màn hình 3 (Thành phố): Click VINEWOOD -> click THAM GIA (nút xanh)
    """
    global last_launcher_action_time, auto_relogin_enabled, login_username, login_password
    global connecting_stuck_start_time
    if not auto_relogin_enabled:
        return False
        
    current_time = time.time()
    if current_time - last_launcher_action_time < 2.5:
        return False

    try:
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            screenshot = sct.grab(monitor)
            screen_bgr = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGRA2BGR)

        # -------------------------------------------------------------
        # 0. KIỂM TRA MÀN HÌNH ĐANG KẾT NỐI BỊ KẸT (0/100 quá 5s)
        # -------------------------------------------------------------
        tmpl_cancel = cv2.imread(get_resource_path("templates/launcher_cancel_connecting_btn.png"))
        tmpl_conn_title = cv2.imread(get_resource_path("templates/launcher_connecting_title.png"))
        
        is_connecting_screen = False
        cancel_btn_loc = None
        
        if tmpl_cancel is not None and screen_bgr.shape[0] >= tmpl_cancel.shape[0] and screen_bgr.shape[1] >= tmpl_cancel.shape[1]:
            res = cv2.matchTemplate(screen_bgr, tmpl_cancel, cv2.TM_CCOEFF_NORMED)
            val, loc = cv2.minMaxLoc(res)[1], cv2.minMaxLoc(res)[3]
            if val >= 0.70:
                is_connecting_screen = True
                cancel_btn_loc = (loc[0] + tmpl_cancel.shape[1] // 2, loc[1] + tmpl_cancel.shape[0] // 2)

        if not is_connecting_screen and tmpl_conn_title is not None and screen_bgr.shape[0] >= tmpl_conn_title.shape[0] and screen_bgr.shape[1] >= tmpl_conn_title.shape[1]:
            res = cv2.matchTemplate(screen_bgr, tmpl_conn_title, cv2.TM_CCOEFF_NORMED)
            val, loc = cv2.minMaxLoc(res)[1], cv2.minMaxLoc(res)[3]
            if val >= 0.70:
                is_connecting_screen = True
                cancel_btn_loc = (loc[0] + 100, loc[1] + 120)

        if is_connecting_screen:
            if connecting_stuck_start_time == 0.0:
                connecting_stuck_start_time = current_time
                log_message("[RELOGIN] ⏳ Phát hiện ĐANG KẾT NỐI... Đang theo dõi...")
            elif current_time - connecting_stuck_start_time >= 5.0:
                log_message("[RELOGIN] ⚠️ Bị kẹt ĐANG KẾT NỐI quá 5s -> Bấm Hủy kết nối & Khởi động lại...")
                if cancel_btn_loc:
                    pyautogui.click(cancel_btn_loc[0], cancel_btn_loc[1])
                    time.sleep(1.0)
                kill_launcher_and_game_processes()
                time.sleep(1.5)
                connecting_stuck_start_time = 0.0
                launch_gta5vn()
                last_launcher_action_time = time.time() + 5.0
                return True
        else:
            connecting_stuck_start_time = 0.0

        # -------------------------------------------------------------
        # 1. KIỂM TRA MÀN HÌNH 1 (ĐĂNG NHẬP LAUNCHER)
        # -------------------------------------------------------------
        tmpl_login = cv2.imread(get_resource_path("templates/launcher_logo_login.png"))
        if tmpl_login is not None and screen_bgr.shape[0] >= tmpl_login.shape[0] and screen_bgr.shape[1] >= tmpl_login.shape[1]:
            res = cv2.matchTemplate(screen_bgr, tmpl_login, cv2.TM_CCOEFF_NORMED)
            val, loc = cv2.minMaxLoc(res)[1], cv2.minMaxLoc(res)[3]
            if val >= 0.70:
                origin_x = loc[0] - 680
                origin_y = loc[1] - 60
                log_message(f"[RELOGIN] 🔑 Phát hiện Màn hình Đăng nhập Launcher tại ({origin_x}, {origin_y})")
                
                # Thả hết phím di chuyển tránh nhập linh tinh
                for k in ['w', 's', 'a', 'd', 'space', 'e', KEY_FORWARD, KEY_AUTORUN]:
                    try: keyboard.release(k)
                    except: pass
                time.sleep(0.1)

                # Nhập tên đăng nhập
                user_x = origin_x + 765
                user_y = origin_y + 222
                pyautogui.click(user_x, user_y)
                time.sleep(0.2)
                pyautogui.hotkey('ctrl', 'a')
                time.sleep(0.1)
                pyautogui.press('backspace')
                time.sleep(0.1)
                if login_username:
                    try:
                        import pyperclip
                        pyperclip.copy(login_username)
                        pyautogui.hotkey('ctrl', 'v')
                    except Exception:
                        keyboard.write(login_username)
                time.sleep(0.2)

                # Nhập mật khẩu
                pass_x = origin_x + 765
                pass_y = origin_y + 287
                pyautogui.click(pass_x, pass_y)
                time.sleep(0.2)
                pyautogui.hotkey('ctrl', 'a')
                time.sleep(0.1)
                pyautogui.press('backspace')
                time.sleep(0.1)
                if login_password:
                    try:
                        import pyperclip
                        pyperclip.copy(login_password)
                        pyautogui.hotkey('ctrl', 'v')
                    except Exception:
                        keyboard.write(login_password)
                time.sleep(0.25)

                # Bấm nút Tham gia
                btn_x = origin_x + 765
                btn_y = origin_y + 438
                log_message(f"[RELOGIN] 🖱 Click nút 'Tham gia' đăng nhập tại ({btn_x}, {btn_y})...")
                pyautogui.moveTo(btn_x, btn_y, duration=0.15)
                pyautogui.click(btn_x, btn_y)

                last_launcher_action_time = time.time()
                return True

        # -------------------------------------------------------------
        # 2. KIỂM TRA MÀN HÌNH 2 (CHỌN ROLEPLAY)
        # -------------------------------------------------------------
        tmpl_rp = cv2.imread(get_resource_path("templates/launcher_roleplay_header.png"))
        if tmpl_rp is not None and screen_bgr.shape[0] >= tmpl_rp.shape[0] and screen_bgr.shape[1] >= tmpl_rp.shape[1]:
            res = cv2.matchTemplate(screen_bgr, tmpl_rp, cv2.TM_CCOEFF_NORMED)
            val, loc = cv2.minMaxLoc(res)[1], cv2.minMaxLoc(res)[3]
            if val >= 0.70:
                origin_x = loc[0] - 260
                origin_y = loc[1] - 50
                log_message(f"[RELOGIN] 🎮 Phát hiện Màn hình Chọn Roleplay tại ({origin_x}, {origin_y})")

                rp_btn_x = origin_x + 385
                rp_btn_y = origin_y + 532
                log_message(f"[RELOGIN] 🖱 Click nút 'THAM GIA' Roleplay tại ({rp_btn_x}, {rp_btn_y})...")
                pyautogui.moveTo(rp_btn_x, rp_btn_y, duration=0.15)
                pyautogui.click(rp_btn_x, rp_btn_y)

                last_launcher_action_time = time.time()
                return True

        # -------------------------------------------------------------
        # 3. KIỂM TRA MÀN HÌNH 3 (THÀNH PHỐ VINEWOOD)
        # -------------------------------------------------------------
        tmpl_vw = cv2.imread(get_resource_path("templates/launcher_vinewood_card.png"))
        if tmpl_vw is not None and screen_bgr.shape[0] >= tmpl_vw.shape[0] and screen_bgr.shape[1] >= tmpl_vw.shape[1]:
            res = cv2.matchTemplate(screen_bgr, tmpl_vw, cv2.TM_CCOEFF_NORMED)
            val, loc = cv2.minMaxLoc(res)[1], cv2.minMaxLoc(res)[3]
            if val >= 0.65:
                origin_x = loc[0] - 290
                origin_y = loc[1] - 360
                log_message(f"[RELOGIN] 🏙️ Phát hiện Màn hình Thành phố tại ({origin_x}, {origin_y})")

                # Click chọn VINEWOOD
                vw_x = origin_x + 397
                vw_y = origin_y + 435
                log_message(f"[RELOGIN] 🖱 Click chọn 'VINEWOOD' tại ({vw_x}, {vw_y})...")
                pyautogui.moveTo(vw_x, vw_y, duration=0.15)
                pyautogui.click(vw_x, vw_y)
                time.sleep(0.8)

                # Click nút THAM GIA màu xanh phía trên
                join_x = origin_x + 145
                join_y = origin_y + 240
                log_message(f"[RELOGIN] 🚀 Click nút 'THAM GIA' vào game tại ({join_x}, {join_y})...")
                pyautogui.moveTo(join_x, join_y, duration=0.15)
                pyautogui.click(join_x, join_y)

                log_message("[RELOGIN] ✅ Đã gửi lệnh vào game VINEWOOD! Chờ GTA5VN khởi động...")
                last_launcher_action_time = time.time() + 10.0
                return True

        return False
    except Exception as e:
        log_message(f"[RELOGIN] ⚠️ Lỗi kiểm tra launcher: {e}")
        return False


def chop_tree_sequence(target_index):
    global g_tree_cooldowns, is_chopping
    
    def spam_chop_thread():
        global chop_state, spam_e_count, spam_key, is_chopping, is_moving, keys_pressed
        is_chopping = True
        chop_state = "RUNNING"
        spam_e_count = 0
        spam_key = "None"
        log_message("[CHOP] Bắt đầu trình tự chặt cây. Vừa aim vừa di chuyển khi nhấn E.")
        monitor = {"top": REGION_MIN_Y, "left": REGION_MIN_X,
                   "width": REGION_WIDTH, "height": REGION_HEIGHT}

        with mss.mss() as sct:
            max_e_attempts = 50
            img = None
            found_bar = False

            # Giữ phím W và . liên tục trong quá trình spam E
            keyboard.press(KEY_FORWARD)
            keyboard.press(KEY_AUTORUN)
            is_moving = True  # Cập nhật flag để GUI hiển thị đúng
            keys_pressed = f"{KEY_FORWARD.upper()} + {KEY_AUTORUN} + {'e'.upper()}"

            while spam_e_count < max_e_attempts:
                keyboard.press('e')
                time.sleep(0.1)
                keyboard.release('e')
                spam_e_count += 1
                
                # Kiểm tra túi đầy trong khi nhấn E
                if spam_e_count % 3 == 0:
                    check_and_close_map_if_open()
                    if detect_inventory_full():
                        log_message("[INVENTORY] 🎒 Phát hiện túi đồ đã đầy khi đang nhấn E! Dừng chặt cây và đi bán ngay...")
                        trigger_sell_due_to_full_inventory()
                        return

                sct_img = sct.grab(monitor)
                img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)

                if is_color_in_area(img, EXPECTED_COLOR, CHECK_X, CHECK_Y, EXPECTED_TOLERANCE):
                    log_message(f"[CHOP] Thanh lực đã xuất hiện sau {spam_e_count} lần nhấn E. Bắt đầu spam.")
                    found_bar = True
                    break

                if spam_e_count % 5 == 0:
                    log_message(f"[CHOP] Đã nhấn E {spam_e_count} lần. Vẫn chưa thấy thanh lực...")


            # Release phím di chuyển khi phát hiện thanh lực hoặc hết lượt
            keyboard.release(KEY_FORWARD)
            keyboard.release(KEY_AUTORUN)
            is_moving = False
            keys_pressed = "None"

            if not found_bar:
                chop_state = "IDLE"
                spam_key = "None"
                is_chopping = False
                keys_pressed = "None"
                log_message(f"[ERROR] Đã vượt quá {max_e_attempts} lần nhấn E mà không thấy thanh lực. Coi như cây bị lỗi/chặt xong. Đặt cooldown.")
                cooldown_until = time.time() + CHOP_COOLDOWN_SECONDS
                g_tree_cooldowns[target_index] = cooldown_until
                return

            # --- GIAI ĐOẠN 2: SPAM E/Y/F ---
            try:
                sct_img = sct.grab(monitor)
                img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)
                base_color = get_pixel(img, *POINT_BASE)
            except IndexError:
                chop_state = "IDLE"
                spam_key = "None"
                log_message("[SPAM] Lỗi: Không thể lấy Base Color. Dừng.")
                return

            match1 = is_color_in_area(img, base_color, *POINT_MATCH1, 10)
            match2 = is_color_in_area(img, base_color, *POINT_MATCH2, 10)

            if match1 and match2:
                key_to_press = "e"
                spam_key = "E"
                keys_pressed = "E"
                log_message("[SPAM] Template: E")
            elif match1:
                key_to_press = "f"
                spam_key = "F"
                keys_pressed = "F"
                log_message("[SPAM] Template: F")
            elif match2:
                key_to_press = "y"
                spam_key = "Y"
                keys_pressed = "Y"
                log_message("[SPAM] Template: Y")
            else:
                chop_state = "IDLE"
                spam_key = "None"
                is_chopping = False
                keys_pressed = "None"
                log_message("[SPAM] Lỗi: Không tìm thấy Template để spam (cả E, F, Y). Dừng.")
                return

            chop_count = 0
            chop_state = "SPAM_KEY"
            # Cập nhật spam_key ngay khi bắt đầu spam (đã được set ở trên)
            while True:
                # Nhấn phím spam
                keyboard.press(key_to_press)
                time.sleep(0.05)
                keyboard.release(key_to_press)
                chop_count += 1
                
                # Kiểm tra bản đồ và túi đồ định kỳ mỗi 4 lần spam phím
                if chop_count % 4 == 0:
                    check_and_close_map_if_open()
                    if detect_inventory_full():
                        log_message(f"[INVENTORY] 🎒 Phát hiện túi đầy khi đang chặt (lần {chop_count})! Dừng chặt và đi bán ngay...")
                        cooldown_until = time.time() + CHOP_COOLDOWN_SECONDS
                        g_tree_cooldowns[target_index] = cooldown_until
                        trigger_sell_due_to_full_inventory()
                        return

                # Chờ 1 giây và kiểm tra thanh lực màu xanh
                sct_img = sct.grab(monitor)
                img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)

                has_expected_color = is_color_in_area(img, EXPECTED_COLOR, CHECK_X, CHECK_Y, EXPECTED_TOLERANCE)
                current_match1 = is_color_in_area(img, base_color, *POINT_MATCH1, 10)
                current_match2 = is_color_in_area(img, base_color, *POINT_MATCH2, 10)

                if not has_expected_color:
                    log_message(f"[SPAM] Thanh lực biến mất. Hoàn tất chặt. Tổng lần spam: {chop_count}.")
                    chop_state = "IDLE"
                    spam_key = "None"
                    
                    # Kiểm tra túi đầy ngay khi thanh lực biến mất
                    if detect_inventory_full():
                        log_message("[INVENTORY] 🎒 Thanh lực biến mất và túi đồ đã đầy! Chuyển ngay sang bán gỗ...")
                        cooldown_until = time.time() + CHOP_COOLDOWN_SECONDS
                        g_tree_cooldowns[target_index] = cooldown_until
                        trigger_sell_due_to_full_inventory()
                        return

                    log_message("[SPAM] Đợi 0.5s trước khi tiếp tục di chuyển...")
                    time.sleep(0.5)  # Chờ 0.5s trước khi chạy tiếp

                    # Kiểm tra túi đầy sau khi nghỉ 0.5s
                    if detect_inventory_full():
                        log_message("[INVENTORY] 🎒 Túi đồ đã đầy! Không chạy tiếp, chuyển sang bán gỗ ngay...")
                        cooldown_until = time.time() + CHOP_COOLDOWN_SECONDS
                        g_tree_cooldowns[target_index] = cooldown_until
                        trigger_sell_due_to_full_inventory()
                        return

                    # Đè phím W + . để tiếp tục chạy
                    keyboard.press(KEY_FORWARD)
                    keyboard.press(KEY_AUTORUN)
                    is_moving = True
                    keys_pressed = f"{KEY_FORWARD.upper()} + {KEY_AUTORUN}"
                    log_message("[SPAM] Tiếp tục di chuyển đến cây tiếp theo...")
                    break

                if current_match1 != match1 or current_match2 != match2:
                    log_message("[SPAM] Pattern bị lỗi/thay đổi. Dừng spam.")
                    chop_state = "IDLE"
                    spam_key = "None"
                    
                    # Kiểm tra túi đầy nếu pattern bị thay đổi
                    if detect_inventory_full():
                        log_message("[INVENTORY] 🎒 Pattern đổi và túi đồ đã đầy! Chuyển ngay sang bán gỗ...")
                        cooldown_until = time.time() + CHOP_COOLDOWN_SECONDS
                        g_tree_cooldowns[target_index] = cooldown_until
                        trigger_sell_due_to_full_inventory()
                        return

                    log_message("[SPAM] Đợi 0.5s trước khi tiếp tục di chuyển...")
                    time.sleep(0.5)  # Chờ 0.5s trước khi chạy tiếp

                    if detect_inventory_full():
                        log_message("[INVENTORY] 🎒 Túi đồ đã đầy! Không chạy tiếp, chuyển sang bán gỗ ngay...")
                        cooldown_until = time.time() + CHOP_COOLDOWN_SECONDS
                        g_tree_cooldowns[target_index] = cooldown_until
                        trigger_sell_due_to_full_inventory()
                        return

                    # Đè phím W + . để tiếp tục chạy
                    keyboard.press(KEY_FORWARD)
                    keyboard.press(KEY_AUTORUN)
                    is_moving = True
                    keys_pressed = f"{KEY_FORWARD.upper()} + {KEY_AUTORUN}"
                    log_message("[SPAM] Tiếp tục di chuyển đến cây khác...")
                    break

        # 3. Đặt Cooldown
        cooldown_until = time.time() + CHOP_COOLDOWN_SECONDS
        g_tree_cooldowns[target_index] = cooldown_until
        is_chopping = False
        
        # Kiểm tra túi đồ đầy sau khi hoàn tất cây
        if detect_inventory_full():
            log_message("[INVENTORY] 🎒 Túi đồ đã đầy sau khi hoàn tất cây! Chuyển sang bán gỗ...")
            trigger_sell_due_to_full_inventory()
            return
        
        # 4. Cập nhật số cây đã chặt
        global total_trees_chopped, tree_chop_limit, should_stop_bot, is_bot_active
        total_trees_chopped += 1
        log_message(f"[COOLDOWN] Cây {target_index} đã xong và sẽ nghỉ trong {CHOP_COOLDOWN_SECONDS} giây.")
        log_message(f"[COUNT] 📊 Đã chặt: {total_trees_chopped}/{tree_chop_limit if tree_chop_limit > 0 else '∞'} cây")
        
        # 5. Kiểm tra có đạt limit không
        if tree_chop_limit > 0 and total_trees_chopped >= tree_chop_limit:
            log_message(f"[SUCCESS] ✅ Đã chặt đủ {tree_chop_limit} cây!")
            
            global auto_sell_enabled, is_selling, sell_point_index, sell_click_count
            if auto_sell_enabled:
                # 🎲 Random chọn route để bán gỗ (tránh pattern detection)
                select_random_route()
                
                # Bắt đầu trình tự bán gỗ (KHÔNG khóa bot, cho phép tạm dừng bất kỳ lúc nào)
                log_message("[SELL] 🛒 Bắt đầu trình tự bán gỗ...")
                log_message("[SELL] 💡 Bạn vẫn có thể tạm dừng bot bằng phím '=' hoặc nút TẠM DỪNG")
                is_selling = True
                sell_point_index = 0
                sell_click_count = 0
                # KHÔNG force is_bot_active = True để user có thể tạm dừng
                set_moving(False, "Chuẩn bị bán gỗ")
            else:
                # Tắt bot nếu không bán
                is_bot_active = False
                should_stop_bot = True
                set_moving(False, "Đã đạt limit cây")

    threading.Thread(target=spam_chop_thread, daemon=True).start()


# ====================================================================
# VI. MAIN BOT LOOP
# ====================================================================

def main_bot_loop(pid, base_address, current_offsets, world_offset):
    global g_tree_cooldowns, g_last_space_time, is_bot_active, read_error_count, last_rescan_time, is_bot_paused, SUBPROCESS_DIR
    
    # ⏸️ KIỂM TRA BOT CÓ ĐANG BẬT KHÔNG (Nếu tạm dừng thì chỉ chờ, dừng tất cả logic)
    if not is_bot_active or is_bot_paused:
        if root:
            root.after(READ_INTERVAL_MS, lambda pid=pid, base_addr=base_address: main_bot_loop(pid, base_addr, current_offsets, world_offset))
        return
    
    current_time = time.time()
    
    # 🗺️ KIỂM TRA NẾU LỠ BỊ MỞ BẢN ĐỒ (MAP / PAUSE MENU) THÌ TỰ ĐỘNG BẤM ESC ĐÓNG LẠI
    check_and_close_map_if_open()

    # 🔐 KIỂM TRA NẾU BỊ MỞ BẢNG TẠO MÃ PIN CÔNG DÂN THÌ TỰ ĐỘNG BẤM ESC ĐÓNG LẠI
    check_and_close_pin_dialog_if_open()
    
    # 0. Cập nhật Cooldowns
    cooldowns_to_remove = []
    for index in list(g_tree_cooldowns.keys()): 
        available_time = g_tree_cooldowns[index]
        if current_time >= available_time: 
            cooldowns_to_remove.append(index)

    for index in cooldowns_to_remove:
        del g_tree_cooldowns[index]
        log_message(f"[COOLDOWN] Cây số {index} đã sẵn sàng trở lại.")
    
    # KIỂM TRA XEM TIẾN TRÌNH GAME CÒN SỐNG HAY BỊ VĂNG (CRASH)
    game_process_alive = False
    if pid is not None:
        try:
            if psutil.pid_exists(pid):
                p = psutil.Process(pid)
                if p.is_running() and p.status() != psutil.STATUS_ZOMBIE:
                    game_process_alive = True
        except Exception:
            game_process_alive = False

    # NẾU GAME ĐÃ BỊ VĂNG HOẶC CHƯA CÓ PID
    if not game_process_alive or pid is None:
        pid = None
        set_moving(False, "Game đã dừng hoặc bị văng")
        for k in ['w', 's', 'a', 'd', 'space', 'e', KEY_FORWARD, KEY_AUTORUN]:
            try:
                keyboard.release(k)
            except Exception:
                pass
        stop_auto_jumping()

        # Kiểm tra tự động xử lý launcher (Đang kết nối kẹt, Đăng nhập, Roleplay, Vinewood)
        if auto_relogin_enabled:
            handled = check_and_handle_launcher_screens()
            if handled:
                if root:
                    root.after(2500, lambda pid=None, base_addr=0: main_bot_loop(pid, base_addr, current_offsets, world_offset))
                return

        # Nếu SUBPROCESS_DIR cũ/không hợp lệ, detect lại
        if SUBPROCESS_DIR is None:
            new_subprocess_dir = auto_detect_GTA5VN_path()
            if new_subprocess_dir:
                SUBPROCESS_DIR = new_subprocess_dir
                log_message(f"[AUTO-DETECT] ✅ Phát hiện lại đường dẫn: {SUBPROCESS_DIR}")
        
        # Quét lại tiến trình GTA5VN
        new_pid, process_path, module_name = find_running_GTA5VN_subprocess(SUBPROCESS_DIR)
        
        if new_pid is not None:
            log_message(f"[RESCAN] ✅ Tìm thấy tiến trình GTA5VN! PID: {new_pid}")
            new_base_address = get_base_address_of_module(new_pid, module_name)
            if new_base_address != 0:
                log_message(f"[RESCAN] ✅ Base Address: 0x{new_base_address:X}")
                pid = new_pid
                base_address = new_base_address
                read_error_count = 0
            else:
                log_message("[RESCAN] ❌ Không thể lấy Base Address. Thử lại sau...")
                set_moving(False, "Không thể lấy Base Address")
                if root:
                    root.after(2000, lambda pid=None, base_addr=0: main_bot_loop(pid, base_addr, current_offsets, world_offset))
                return
        else:
            log_message("[RESCAN] ⏳ Chưa tìm thấy GTA5VN. Sẽ quét lại mỗi 3 giây...")
            # Nếu launcher cũng chưa mở, tự mở launcher
            if auto_relogin_enabled and not is_launcher_running():
                launch_gta5vn()
            set_moving(False, "Chờ GTA5VN khởi động")
            if root:
                root.after(3000, lambda pid=None, base_addr=0: main_bot_loop(pid, base_addr, current_offsets, world_offset))
            return
    
    # --- BƯỚC 1: Đọc Dữ liệu ---
    ped_address = get_local_player_ped_address(pid, base_address, world_offset)
    player_data = read_player_data(pid, ped_address, current_offsets) if ped_address else None
    camera_data = read_camera_data(pid, base_address, current_offsets)

    target_info = None
    delta_yaw_deg = 0.0
    p_x, p_y, current_yaw_rad = 0, 0, 0
    
    # Tải và lọc dữ liệu từ một nguồn duy nhất
    locations, special_locations, random_start_locations = load_and_filter_locations()
    
    if player_data is None or player_data.get('X') is None or camera_data is None or camera_data.get('CamYawRad') is None:
        read_error_count += 1
        log_message(f"[ERROR] Không thể đọc dữ liệu Ped hoặc Camera (lỗi #{read_error_count}). Đang chờ...")
        set_moving(False, "Không đọc được dữ liệu game")
        for k in ['w', 's', 'a', 'd', 'space', 'e', KEY_FORWARD, KEY_AUTORUN]:
            try:
                keyboard.release(k)
            except Exception:
                pass
        stop_auto_jumping()
        
        # Nếu lỗi liên tục quá 10 lần: kiểm tra game có còn tồn tại không
        if read_error_count >= 10:
            if not psutil.pid_exists(pid):
                log_message("[GAME] ⚠️ Tiến trình game đã tắt hoặc bị văng đột ngột!")
                pid = None
                read_error_count = 0
                if root:
                    root.after(READ_INTERVAL_MS, lambda: main_bot_loop(None, 0, current_offsets, world_offset))
                return
        
        # Nếu lỗi quá nhiều lần, thực hiện quét lại tiến trình
        if read_error_count >= MAX_ERROR_BEFORE_RESCAN and (current_time - last_rescan_time) >= RESCAN_INTERVAL:
            log_message(f"[RESCAN] 🔄 Lỗi liên tục {read_error_count} lần! Quét lại tiến trình GTA5VN...")
            
            # Nếu SUBPROCESS_DIR không hợp lệ, detect lại
            if SUBPROCESS_DIR is None:
                new_subprocess_dir = auto_detect_GTA5VN_path()
                if new_subprocess_dir:
                    SUBPROCESS_DIR = new_subprocess_dir
                    log_message(f"[AUTO-DETECT] ✅ Phát hiện lại đường dẫn: {SUBPROCESS_DIR}")
            
            new_pid, process_path, module_name = find_running_GTA5VN_subprocess(SUBPROCESS_DIR)
            
            if new_pid is not None and new_pid != pid:
                log_message(f"[RESCAN] ✅ Tìm thấy tiến trình GTA5VN mới: PID={new_pid}")
                new_base_address = get_base_address_of_module(new_pid, module_name)
                if new_base_address != 0:
                    log_message(f"[RESCAN] ✅ Cập nhật Base Address: 0x{new_base_address:X}")
                    # Cập nhật qua root.after callback
                    root.after(READ_INTERVAL_MS, lambda: main_bot_loop(new_pid, new_base_address, current_offsets, world_offset))
                    return
                else:
                    log_message(f"[RESCAN] ❌ Không thể lấy Base Address của tiến trình mới")
            elif new_pid is None:
                log_message(f"[RESCAN] ❌ Không tìm thấy tiến trình GTA5VN. Đánh dấu văng game...")
                pid = None
            
            read_error_count = 0  # Reset đếm lỗi
            last_rescan_time = current_time
        
    else:
        read_error_count = 0  # Reset khi đọc thành công
        p_x, p_y = player_data['X'], player_data['Y']
        current_yaw_rad = camera_data['CamYawRad']
        
        # === KIỂM TRA VÀ XỬ LÝ TRÌNH TỰ BÁN GỖ ===
        global is_selling, is_returning, is_going_to_random_start, is_woodcutting, woodcut_state, enable_woodcutting, current_sawmill, current_special_locations
        if is_selling:
            handle_sell_sequence(p_x, p_y, current_yaw_rad, locations, current_special_locations)
        
        # === XỬ LÝ CƯA GỖ (nếu enable_woodcutting = True) ===
        if is_woodcutting and enable_woodcutting:
            handle_woodcutting_sequence(p_x, p_y, current_yaw_rad, locations, current_special_locations)
        
        # === XỬ LÝ ĐƯỜNG QUAY VỀ SAU KHI BÁN HOẶC CƯA ===
        if is_returning:
            handle_return_journey(p_x, p_y, current_yaw_rad, locations, current_special_locations, random_start_locations)
        
        # === XỬ LÝ ĐI ĐẾN RANDOM START POINT ===
        if is_going_to_random_start:
            handle_random_start_point(p_x, p_y, current_yaw_rad)
        
        # === CHỈ CHẶT CÂY NẾU KHÔNG ĐANG BÁN, CƯA, QUAY VỀ, HOẶC ĐI ĐẾN RANDOM START ===
        if not is_selling and not is_woodcutting and not is_returning and not is_going_to_random_start:
            # 🎒 KIỂM TRA TÚI ĐỒ ĐẦY TRƯỚC KHI TÌM CÂY MỚI (nếu không đang trong animation chặt)
            if not is_chopping and detect_inventory_full():
                log_message("[INVENTORY] 🎒 Túi đồ đã đầy! Không tìm cây tiếp mà chuyển ngay sang bán gỗ...")
                trigger_sell_due_to_full_inventory()
                if root:
                    root.after(READ_INTERVAL_MS, lambda pid=pid, base_addr=base_address: main_bot_loop(pid, base_addr, current_offsets, world_offset))
                return

            # --- BƯỚC 2: Tìm Cây Gần Nhất (CHỈ TỪ Normal Points) ---
            available_trees = []
            for index, loc in enumerate(locations): # Sử dụng locations (đã được lọc là normal)
                if index not in g_tree_cooldowns and isinstance(loc, dict) and loc.get('x') is not None and loc.get('y') is not None:
                    t_x, t_y = loc['x'], loc['y']
                    distance = math.hypot(t_x - p_x, t_y - p_y)
                    available_trees.append((distance, index, t_x, t_y))
            
            if available_trees and is_bot_active:
                available_trees.sort(key=lambda x: x[0])
                target_info = available_trees[0]
                distance, target_index, t_x, t_y = target_info
                
                # --- KIỂM TRA KẸT (chỉ khi KHÔNG đang chặt cây) ---
                if is_chopping:
                    # Đang spam E/Y/F, không chạy anti-stuck để tránh gián đoạn
                    is_handling_stuck = False
                else:
                    # Đang đi tới cây (phần chặt gỗ: thresholds dài hơn 2s, 12s, 16s, 20s)
                    is_handling_stuck = check_and_handle_stuck_chopping(p_x, p_y, t_x, t_y)
                
                # --- BƯỚC 3: Hành động (Aim -> Chạy -> Chặt) ---
                aimed_at_target, delta_yaw_deg = aim_at_target(current_yaw_rad, p_x, p_y, t_x, t_y)

                # Xác định trạng thái mong muốn
                should_move = False
                reason = ""
                
                if is_chopping:
                    # Đang chặt cây, không thay đổi gì
                    pass
                elif distance <= MOVE_DISTANCE_THRESHOLD and not is_chopping:
                    # Đã đến cây, bắt đầu chặt
                    log_message(f"[ACTION] Đã tới cây (d={distance:.2f}m). Kích hoạt trình tự chặt cây...")
                    chop_tree_sequence(target_index)
                    should_move = False
                    reason = "Đã đến cây, chuẩn bị chặt"
                else:
                    # Tiếp tục di chuyển gần cây (aim sẽ điều chỉnh hướng)
                    # Chỉ dừng nếu không có cây khả dụng hoặc bot tắt
                    should_move = True
                    if aimed_at_target:
                        reason = f"Đã aim đúng, di chuyển đến cây (còn {distance:.1f}m)"
                    else:
                        reason = f"Re-aim trong khi di chuyển (chênh {delta_yaw_deg:.1f}°, còn {distance:.1f}m)"
                
                # Chỉ thay đổi trạng thái movement nếu không đang chặt cây
                if not is_chopping:
                    set_moving(should_move, reason)
            else:
                 # Không có cây khả dụng, dừng di chuyển
                 if not is_chopping:
                     set_moving(False, "Không có cây khả dụng hoặc bot tắt")
    
    # --- CẬP NHẬT GUI ---
    if root:
        # draw_radar(p_x, p_y, current_yaw_rad, target_info, locations, special_locations, g_tree_cooldowns)
        update_gui_info(player_data, target_info, is_bot_active, delta_yaw_deg, is_moving, g_tree_cooldowns)
        
        # Schedule next loop với PID và base_address hiện tại (có thể đã được cập nhật)
        root.after(READ_INTERVAL_MS, lambda pid=pid, base_addr=base_address: main_bot_loop(pid, base_addr, current_offsets, world_offset)) 

# ====================================================================
# VII. KHỞI CHẠY CHÍNH
# ====================================================================

if __name__ == "__main__":
    
    print("=" * 70)
    print(f"BỘT TỰ ĐỘNG CHẶT CÂY (BUILD ID: {TARGET_BUILD_ID})")
    print(f"Nhấn phím '{KEY_TOGGLE}' để BẬT/TẮT Bot.")
    print("✅ Đã cập nhật: Giao diện luôn hiển thị trên cùng (Always-on-Top).")
    print("=" * 70)
    
    # ====================================================================
    # KIỂM TRA KEY TRƯỚC KHI CHẠY BOT - BỎ QUA
    # ====================================================================
    # print("\n[KEY] 🔐 Kiểm tra Key...")
    # current_key, saved_hwid = read_key_from_ini()
    # hwid = get_hwid()
    
    key_verified = True  # BỎ QUA KIỂM TRA KEY - Luôn cho phép chạy
    
    # # Nếu có key cũ, kiểm tra trước
    # if current_key and current_key.strip():
    #     print(f"[KEY] Tìm thấy key cũ. Kiểm tra...")
    #     status, expire_time_ms, is_lifetime = check_key(current_key, hwid)
    #     if status == "active":
    #         print(f"[KEY] ✅ Key hợp lệ!")

    #         GLOBAL_KEY_INFO["is_lifetime"] = is_lifetime
    #         GLOBAL_KEY_INFO["expire_time_ms"] = expire_time_ms
    #         GLOBAL_KEY_INFO["hwid_mismatch"] = False
    #         GLOBAL_KEY_INFO["initial_check_done"] = True
            
    #         # Tính toán thời gian hết hạn
    #         if is_lifetime:
    #             GLOBAL_KEY_INFO['expiry'] = "Vĩnh viễn"
    #         elif expire_time_ms:
    #             expiry_dt = dt.fromtimestamp(expire_time_ms / 1000.0)
    #             GLOBAL_KEY_INFO['expiry'] = expiry_dt.strftime("%Y-%m-%d %H:%M:%S")
            
    #         key_verified = True
    #     else:
    #         print(f"[KEY] ❌ Key không hợp lệ ({status}). Vui lòng nhập key mới.")
    #         current_key = None
    
    # # Nếu không có key hoặc key cũ không hợp lệ, yêu cầu nhập
    # if not key_verified:
    #     print("[KEY] 🔑 Vui lòng nhập key để kích hoạt Tool...")
    #     key_verified = activation_gui_and_wait(hwid)
    
    # if not key_verified:
    #     print("[KEY] ❌ Không có key hợp lệ. Tool sẽ thoát.")
    #     sys.exit(1)
    
    print("[KEY] ✅ Đã bỏ qua kiểm tra Key! Bắt đầu Tool...")
    print("=" * 70 + "\n")
    # ====================================================================
    # AUTO-DETECT SUBPROCESS DIRECTORY (KHÔNG DÙNG config.json)
    # ====================================================================
    print("[CONFIG] 🔍 Đang tự động phát hiện đường dẫn GTA5VN...")
    
    # Auto-detect lần đầu để có subprocess_dir
    subprocess_dir = auto_detect_GTA5VN_path()
    
    if subprocess_dir:
        print(f"[CONFIG] ✅ Tìm thấy subprocess directory: {subprocess_dir}")
    else:
        print("[CONFIG] ⏳ Chưa tìm thấy GTA5VN... Bước 1 sẽ tìm lại...")
        subprocess_dir = None  # Để bước 1 tự quét

    # ====================================================================
    # TÌM TIẾN TRÌNH GAME VỚI CỬA SỔ CHỜ (3 BƯỚC) - BẮT BUỘC
    # ====================================================================
    print("[GAME] 🎮 Đang khởi động tool với 3 bước quét...")
    print("[GAME] ⚠️ LÀM ĐỦ 3 BƯỚC MỚI ĐƯỢC VÀO TOOL!")
    
    pid, process_path, module_name, base_address_int = wait_for_game_process(subprocess_dir)
    
    # Kiểm tra BẮT BUỘC - Nếu thiếu bất kỳ thông tin nào = LỖI NGHIÊM TRỌNG
    if pid is None or base_address_int is None or base_address_int == 0: 
        print("[GAME] ❌ LỖI NGHIÊM TRỌNG: Không hoàn thành đủ 3 bước!")
        print("[GAME] ❌ Tool không thể hoạt động. Thoát...")
        sys.exit(1)
    
    # Chỉ in thông báo thành công khi ĐỦ 3 bước
    print(f"[GAME] ✅ Hoàn tất 3 bước quét!")
    print(f"[GAME]    - PID: {pid}")
    print(f"[GAME]    - Base Address: 0x{base_address_int:X}")
    
    build_name, current_offsets = get_game_build_offsets(TARGET_BUILD_ID)
    if build_name is None: 
        sys.exit(1)
    
    world_offset = current_offsets.get("world_ptr")
    
    # ====================================================================
    # LOAD SAWMILL LOCATIONS (NẾU CÓ) - Tự động load khi bán xong
    # ====================================================================
    print("[WOODCUT] 🏭 Tải sẵn các máy cưa từ location.json để cưa gỗ sau bán...")
    load_sawmill_locations()
    if sawmill_locations:
        print(f"[WOODCUT] ✅ Đã load {len(sawmill_locations)} máy cưa - Sẽ cưa gỗ sau bán")
    else:
        print("[WOODCUT] ⚠️ Không tìm thấy máy cưa trong location.json")
    
    # Khởi tạo biến thời gian
    g_last_space_time = time.time()
    last_change_time = time.time()
    
    # 0. Khởi động background thread detect realtime (mss)
    start_template_detection_thread()
    
    # 1. Khởi tạo GUI
    setup_gui()
    
    # 2. Bắt đầu vòng lặp Bot trong vòng lặp sự kiện của Tkinter
    root.after(READ_INTERVAL_MS, lambda: main_bot_loop(pid, base_address_int, current_offsets, world_offset))
    
    # 3. Khởi chạy GUI
    try:
        root.mainloop()
    except Exception as e:
        log_message(f"[FATAL ERROR] Lỗi trong vòng lặp chính của GUI: {e}.")
        print(f"[FATAL ERROR] Lỗi trong vòng lặp chính của GUI: {e}.")