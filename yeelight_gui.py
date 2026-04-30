#!/usr/bin/env python3
"""
Yeelight Desk Lamp Controller - GUI Version
Giao dien dieu khien den Yeelight qua WiFi
"""

import tkinter as tk
from tkinter import ttk, messagebox
from yeelight import Bulb, discover_bulbs
import threading

class YeelightGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Yeelight Controller")
        self.root.geometry("650x1150")
        self.root.resizable(True, True)
        self.root.configure(bg="#e8e8e8")
        
        self.bulb = None
        self.ip_var = tk.StringVar()
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=("Helvetica", 18, "bold"))
        style.configure('Subtitle.TLabel', font=("Helvetica", 10))
        style.configure('Card.TLabelframe', background="#e8e8e8", 
                       borderwidth=1, relief="solid")
        style.configure('Card.TLabelframe.Label', font=("Helvetica", 11, "bold"),
                       foreground="#2c3e50", background="#e8e8e8")
        style.configure('Light.TFrame', background="#e8e8e8")
        style.configure('Light.TLabel', background="#e8e8e8")
        
        # Create canvas with scrollbar
        self.canvas = tk.Canvas(self.root, bg="#e8e8e8", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, style='Light.TFrame')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.setup_ui()
    
    def setup_ui(self):
        main = self.scrollable_frame
        
        # Header
        header_frame = ttk.Frame(main, padding="20", style='Light.TFrame')
        header_frame.pack(fill=tk.X)
        
        title_label = ttk.Label(header_frame, text="💡 ĐIỀU KHIỂN ĐÈN YEELIGHT", 
                               font=("Helvetica", 18, "bold"))
        title_label.pack(pady=(0, 5))
        
        subtitle_label = ttk.Label(header_frame, text="Điều khiển đèn qua WiFi - Nhập IP để kết nối")
        subtitle_label.pack(pady=(0, 10))
        
        # Connection card
        conn_card = ttk.LabelFrame(main, text="KẾT NỐI ĐÈN", padding="15", style='Card.TLabelframe')
        conn_card.pack(fill=tk.X, padx=20, pady=(0, 12))
        
        ttk.Label(conn_card, text="IP đèn:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.ip_entry = ttk.Entry(conn_card, textvariable=self.ip_var, width=30, font=("Helvetica", 10))
        self.ip_entry.grid(row=0, column=1, sticky=tk.W, padx=(10, 10), pady=5)
        
        btn_frame = ttk.Frame(conn_card)
        btn_frame.grid(row=0, column=2, pady=5)
        
        ttk.Button(btn_frame, text="🔍 Quét mạng", command=self.discover, width=12).pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_frame, text="🔌 Kết nối", command=self.connect, width=12).pack(side=tk.LEFT, padx=3)
        
        # Status
        status_frame = ttk.Frame(main, style='Light.TFrame')
        status_frame.pack(pady=(0, 12))
        self.status_label = ttk.Label(status_frame, text="● Chưa kết nối", foreground="gray")
        self.status_label.pack()
        
        # Power card
        power_card = ttk.LabelFrame(main, text="ĐIỀU KHIỂN NGUỒN", padding="15", style='Card.TLabelframe')
        power_card.pack(fill=tk.X, padx=20, pady=(0, 12))
        
        power_btn_frame = ttk.Frame(power_card, style='Light.TFrame')
        power_btn_frame.pack(pady=5)
        
        self.create_btn(power_btn_frame, "⚡ BẬT ĐÈN", self.turn_on, "#2ecc71", 11).pack(side=tk.LEFT, padx=8)
        self.create_btn(power_btn_frame, "🔌 TẮT ĐÈN", self.turn_off, "#e74c3c", 11).pack(side=tk.LEFT, padx=8)
        self.create_btn(power_btn_frame, "🔄 ĐẢO TRẠNG THÁI", self.toggle, "#f39c12", 11).pack(side=tk.LEFT, padx=8)
        
        # Brightness card
        bright_card = ttk.LabelFrame(main, text="ĐIỀU CHỈNH ĐỘ SÁNG", padding="15", style='Card.TLabelframe')
        bright_card.pack(fill=tk.X, padx=20, pady=(0, 12))
        
        self.brightness_var = tk.StringVar(value="50%")
        self.brightness_scale = ttk.Scale(bright_card, from_=0, to=100, orient="horizontal", length=550)
        self.brightness_scale.set(50)
        self.brightness_scale.pack(pady=(5, 5), fill=tk.X)
        self.brightness_scale.configure(command=lambda v: self.brightness_var.set(f"{int(float(v))}%"))
        
        ttk.Label(bright_card, textvariable=self.brightness_var, font=("Helvetica", 10, "bold")).pack(pady=(0, 10))
        
        self.create_btn(bright_card, "✅ ÁP DỤNG ĐỘ SÁNG", self.set_brightness, "#8e44ad", 10).pack(pady=(0, 5))
        
        # Color temp card
        temp_card = ttk.LabelFrame(main, text="ĐIỀU CHỈNH NHIỆT ĐỘ MÀU", padding="15", style='Card.TLabelframe')
        temp_card.pack(fill=tk.X, padx=20, pady=(0, 12))
        
        self.temp_var = tk.StringVar(value="4000K")
        self.temp_scale = ttk.Scale(temp_card, from_=1700, to=6500, orient="horizontal", length=550)
        self.temp_scale.set(4000)
        self.temp_scale.pack(pady=(5, 5), fill=tk.X)
        self.temp_scale.configure(command=lambda v: self.temp_var.set(f"{int(float(v))}K"))
        
        ttk.Label(temp_card, textvariable=self.temp_var, font=("Helvetica", 10, "bold")).pack(pady=(0, 10))
        
        self.create_btn(temp_card, "✅ ÁP DỤNG NHIỆT ĐỘ", self.set_color_temp, "#16a085", 10).pack(pady=(0, 5))
        
        # Presets card
        preset_card = ttk.LabelFrame(main, text="CHẾ ĐỘ NHANH", padding="15", style='Card.TLabelframe')
        preset_card.pack(fill=tk.X, padx=20, pady=(0, 12))
        
        presets = [
            ("📖 Học tập (5000K, 100%)", 5000, 100, "#3498db"),
            ("📚 Đọc sách (4000K, 70%)", 4000, 70, "#9b59b6"),
            ("🌙 Thư giãn (2700K, 50%)", 2700, 50, "#e67e22"),
            ("🎯 Tập trung (6000K, 90%)", 6000, 90, "#1abc9c"),
        ]
        
        for name, temp, bright, color in presets:
            btn = tk.Button(preset_card, text=name,
                          command=lambda t=temp, b=bright, n=name: self.set_preset(t, b, n),
                          bg=color, fg="black", font=("Helvetica", 10, "bold"),
                          relief="flat", bd=0, cursor="hand2",
                          height=2)
            btn.pack(pady=4, fill=tk.X)
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.lighten_color(b['bg'])))
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.configure(bg=c))
        
        # Status card
        status_card = ttk.LabelFrame(main, text="TRẠNG THÁI ĐÈN", padding="15", style='Card.TLabelframe')
        status_card.pack(fill=tk.X, padx=20, pady=(0, 12))
        
        self.info_text = tk.Text(status_card, height=5, bg="#ffffff", fg="#2c3e50",
                                font=("Consolas", 10), relief="solid", bd=1)
        self.info_text.pack(fill=tk.X, pady=(0, 10))
        self.info_text.insert(1.0, "Chưa có thông tin...")
        self.info_text.config(state="disabled")
        
        self.create_btn(status_card, "🔄 CẬP NHẬT TRẠNG THÁI", self.show_status, "#2c3e50", 10).pack(fill=tk.X)
        
        # Add bottom padding
        ttk.Frame(main, height=20, style='Light.TFrame').pack()
    
    def create_btn(self, parent, text, cmd, color, size):
        btn = tk.Button(parent, text=text, command=cmd,
                       bg=color, fg="black", font=("Helvetica", size, "bold"),
                       relief="flat", bd=0, cursor="hand2",
                       height=1)
        btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.lighten_color(b['bg'])))
        btn.bind("<Leave>", lambda e, b=btn, c=color: b.configure(bg=c))
        return btn
    
    def lighten_color(self, hex_color):
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        lightened = tuple(min(255, int(c + (255 - c) * 0.2)) for c in rgb)
        return f'#{lightened[0]:02x}{lightened[1]:02x}{lightened[2]:02x}'
    
    def discover(self):
        def scan():
            try:
                self.status_label.config(text="● Đang quét mạng LAN...", foreground="#f39c12")
                bulbs = discover_bulbs()
                if bulbs:
                    ip = bulbs[0]['ip']
                    self.ip_var.set(ip)
                    self.status_label.config(text=f"● Tìm thấy đèn: {ip}", foreground="#2ecc71")
                else:
                    self.status_label.config(text="● Không tìm thấy đèn nào", foreground="#e74c3c")
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))
        
        threading.Thread(target=scan, daemon=True).start()
    
    def connect(self):
        ip = self.ip_var.get().strip()
        if not ip:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập IP của đèn!")
            return
        
        try:
            self.bulb = Bulb(ip, auto_on=True, effect="smooth", duration=300)
            props = self.bulb.get_properties()
            self.status_label.config(text=f"● Đã kết nối: {ip}", foreground="#2ecc71")
            self.show_status()
        except Exception as e:
            messagebox.showerror("Lỗi kết nối", str(e))
            self.status_label.config(text="● Lỗi kết nối", foreground="#e74c3c")
    
    def turn_on(self):
        if not self.bulb:
            messagebox.showwarning("Cảnh báo", "Chưa kết nối đèn!")
            return
        try:
            self.bulb.turn_on()
            self.show_status()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def turn_off(self):
        if not self.bulb:
            messagebox.showwarning("Cảnh báo", "Chưa kết nối đèn!")
            return
        try:
            self.bulb.turn_off()
            self.show_status()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def toggle(self):
        if not self.bulb:
            messagebox.showwarning("Cảnh báo", "Chưa kết nối đèn!")
            return
        try:
            self.bulb.toggle()
            self.show_status()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def set_brightness(self):
        if not self.bulb:
            messagebox.showwarning("Cảnh báo", "Chưa kết nối đèn!")
            return
        try:
            brightness = int(self.brightness_scale.get())
            self.bulb.set_brightness(brightness)
            self.show_status()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def set_color_temp(self):
        if not self.bulb:
            messagebox.showwarning("Cảnh báo", "Chưa kết nối đèn!")
            return
        try:
            temp = int(self.temp_scale.get())
            self.bulb.set_color_temp(temp)
            self.show_status()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def set_preset(self, temp, bright, name):
        if not self.bulb:
            messagebox.showwarning("Cảnh báo", "Chưa kết nối đèn!")
            return
        try:
            self.bulb.set_color_temp(temp)
            self.bulb.set_brightness(bright)
            self.temp_scale.set(temp)
            self.brightness_scale.set(bright)
            self.show_status()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def show_status(self):
        if not self.bulb:
            return
        try:
            props = self.bulb.get_properties()
            info = f"Power: {props['power']}\n"
            info += f"Độ sáng: {props['bright']}%\n"
            info += f"Nhiệt độ: {props['ct']}K\n"
            info += f"Chế độ: {props['color_mode']}"
            
            self.info_text.config(state="normal")
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(1.0, info)
            self.info_text.config(state="disabled")
        except Exception as e:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = YeelightGUI(root)
    root.mainloop()
