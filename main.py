import tkinter as tk
from tkinter import messagebox
from db import connect_db  
import XEMAY
import KHACHHANG
import HOADON
import TONKHO


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # --- CÀI ĐẶT CỬA SỔ CHÍNH ---
        self.title("Hệ Thống Quản Lý Cửa Hàng Xe Máy")
        self.geometry("1200x750")
        self.attributes('-fullscreen', True)

        # --- CÀI ĐẶT MÀU SẮC ---
        self.toolbar_bg = "#2c3e50"  # màu thanh công cụ
        self.button_bg = "#3498db"
        self.fg_color = "white"
        self.main_bg = "#ecf0f1"

        # --- TẠO GIAO DIỆN ---
        self._create_toolbar()  # thanh công cụ ngang
        self._create_main_frame()  # khung nội dung

        # --- KIỂM TRA KẾT NỐI DATABASE ---
        if self._check_db_connection():
            self.show_trangchu_view()
        else:
            self.after(100, self.destroy)

    # ====== KIỂM TRA DATABASE ======
    def _check_db_connection(self):
        try:
            conn = connect_db()
            conn.close()
            return True
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Không thể kết nối đến CSDL.\n{e}")
            return False

# ====== THANH CÔNG CỤ NGANG (ĐÃ SỬA LỖI BỐ CỤC LẦN 3) ======
    def _create_toolbar(self):
        self.toolbar_frame = tk.Frame(self, bg=self.toolbar_bg, height=60)
        self.toolbar_frame.pack(side="top", fill="x")

        # Tiêu đề bên trái
        title_label = tk.Label(
            self.toolbar_frame,
            text="🏍️ HỆ THỐNG QUẢN LÝ CỬA HÀNG XE MÁY",
            font=("Arial", 15, "bold"),  # <--- GIẢM: Cỡ chữ 16 -> 15
            bg=self.toolbar_bg,
            fg=self.fg_color
        )
        title_label.pack(side="left", padx=10) # <--- GIẢM: Đệm 15 -> 10

        # --- NÚT THOÁT BÊN PHẢI ---
        logout_btn = tk.Button(
            self.toolbar_frame,
            text="🚪 Thoát",
            bg="#e74c3c",
            fg=self.fg_color,
            font=("Arial", 12, "bold"),
            relief="flat",
            width=7,  # <--- GIẢM: Rộng 8 -> 7
            pady=8,
            command=self.on_logout
        )
        logout_btn.pack(side="right", padx=10) # <--- GIẢM: Đệm 15 -> 10

        # --- DANH SÁCH CÁC NÚT CHỨC NĂNG ---
        buttons_info = [
            ("🏠 Trang chủ", self.show_trangchu_view),
            ("🛵 Xe Máy", self.show_xemay_view),
            ("👤 Khách Hàng", self.show_khachhang_view),
            ("🧾 Hóa Đơn", self.show_hoadon_view),
            ("📦 Tồn Kho", self.show_tonkho_view), 
        ]

        # --- TẠO NÚT ---
        for text, command in buttons_info:
            btn = tk.Button(
                self.toolbar_frame,
                text=text,
                bg=self.button_bg,
                fg=self.fg_color,
                font=("Arial", 12, "bold"),
                relief="flat",
                width=12, # <--- GIẢM: Rộng 13 -> 12
                pady=8,
                command=command
            )
            btn.pack(side="left", padx=5)
            
    # ====== KHUNG NỘI DUNG CHÍNH ======
    def _create_main_frame(self):
        self.main_frame = tk.Frame(self, bg=self.main_bg)
        self.main_frame.pack(side="top", fill="both", expand=True)

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # ====== TRANG CHỦ ======
    def show_trangchu_view(self):
        self.clear_main_frame()
        tk.Label(
            self.main_frame,
            text="HỆ THỐNG QUẢN LÝ CỬA HÀNG XE MÁY",
            font=("Arial", 30, "bold"),
            bg=self.main_bg,
            fg="#2c3e50"
        ).pack(pady=100)
        tk.Label(
            self.main_frame,
            text="Chào mừng bạn đến với hệ thống quản lý!",
            font=("Arial", 20),
            bg=self.main_bg,
            fg="#555"
        ).pack()

    # ====== CÁC TRANG CHỨC NĂNG ======
    def show_xemay_view(self):
        self.clear_main_frame()
        frame = XEMAY.tao_frame_xe(self.main_frame, self.show_trangchu_view)
        frame.pack(fill="both", expand=True)

    def show_khachhang_view(self):
        self.clear_main_frame()
        frame = KHACHHANG.tao_frame_khachhang(self.main_frame, self.show_trangchu_view)
        frame.pack(fill="both", expand=True)

    def show_hoadon_view(self):
        self.clear_main_frame()
        frame = HOADON.tao_frame_hoadon(self.main_frame, self.show_trangchu_view)
        frame.pack(fill="both", expand=True)
        
    def show_tonkho_view(self):
        self.clear_main_frame()
        frame = TONKHO.tao_frame_tonkho(self.main_frame, self.show_trangchu_view)
        frame.pack(fill="both", expand=True)
    # ====== NÚT THOÁT ======
    def on_logout(self):
        if messagebox.askyesno("Thoát", "Bạn có chắc muốn thoát chương trình?"):
            self.destroy()


# ====== CHẠY ỨNG DỤNG ======
if __name__ == "__main__":
    app = App()
    app.mainloop()
