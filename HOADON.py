
import tkinter as tk
from tkinter import ttk, messagebox
from db import connect_db

def tao_frame_hoadon(root, show_home):
    frame_hd = tk.Frame(root)

    # ====== HIỂN THỊ DANH SÁCH HÓA ĐƠN ======
    def hien_hoadon():
        for row in tree_hd.get_children():
            tree_hd.delete(row)
        try:
            conn = connect_db()
            cursor = conn.cursor()
            query = """
                SELECT h.MaHD, k.HoTen, x.TenXe, h.NgayLap, h.SoLuong, h.TongTien
                FROM HoaDon h
                JOIN KhachHang k ON h.MaKH = k.MaKH
                JOIN XeMay x ON h.MaXe = x.MaXe
            """
            cursor.execute(query)
            for row in cursor.fetchall():
                tree_hd.insert("", tk.END, values=row)
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    # ====== LẤY DANH SÁCH KHÁCH HÀNG + XE ======
    def load_combo_data():
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT MaKH, HoTen FROM KhachHang")
            khach = cursor.fetchall()
            combo_kh["values"] = [f"{k[0]} - {k[1]}" for k in khach]

            cursor.execute("SELECT MaXe, TenXe, GiaXe FROM XeMay")
            xe = cursor.fetchall()
            combo_xe["values"] = [f"{x[0]} - {x[1]}" for x in xe]

            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    # ====== TỰ ĐỘNG TÍNH TỔNG TIỀN ======
    def tinh_tong_tien(*args):
        try:
            xe_info = combo_xe.get()
            soluong = int(entry_soluong.get())
            if "-" in xe_info:
                ma_xe = xe_info.split(" - ")[0]
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("SELECT GiaXe FROM XeMay WHERE MaXe=%s", (ma_xe,))
                gia = cursor.fetchone()[0]
                tong = float(gia) * soluong
                entry_tongtien.delete(0, tk.END)
                entry_tongtien.insert(0, tong)
                conn.close()
        except:
            entry_tongtien.delete(0, tk.END)

    # ====== THÊM HÓA ĐƠN ======
    def them_hoadon():
        try:
            kh_info = combo_kh.get()
            xe_info = combo_xe.get()
            ngaylap = entry_ngaylap.get()
            soluong = entry_soluong.get()
            tongtien = entry_tongtien.get()

            if not (kh_info and xe_info and ngaylap and soluong and tongtien):
                messagebox.showwarning("Thiếu dữ liệu", "Nhập đầy đủ thông tin hóa đơn.")
                return

            ma_kh = kh_info.split(" - ")[0]
            ma_xe = xe_info.split(" - ")[0]

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO HoaDon (MaKH, MaXe, NgayLap, SoLuong, TongTien)
                VALUES (%s, %s, %s, %s, %s)
            """, (ma_kh, ma_xe, ngaylap, soluong, tongtien))
            conn.commit()
            conn.close()
            messagebox.showinfo("Thành công", "Đã thêm hóa đơn.")
            hien_hoadon()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    # ====== SỬA HÓA ĐƠN ======
    def sua_hoadon():
        selected = tree_hd.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Chọn hóa đơn để sửa.")
            return
        ma_hd = tree_hd.item(selected[0])['values'][0]

        kh_info = combo_kh.get()
        xe_info = combo_xe.get()
        ngaylap = entry_ngaylap.get()
        soluong = entry_soluong.get()
        tongtien = entry_tongtien.get()

        if not (kh_info and xe_info and ngaylap and soluong and tongtien):
            messagebox.showwarning("Thiếu dữ liệu", "Nhập đầy đủ thông tin.")
            return

        try:
            ma_kh = kh_info.split(" - ")[0]
            ma_xe = xe_info.split(" - ")[0]
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE HoaDon 
                SET MaKH=%s, MaXe=%s, NgayLap=%s, SoLuong=%s, TongTien=%s
                WHERE MaHD=%s
            """, (ma_kh, ma_xe, ngaylap, soluong, tongtien, ma_hd))
            conn.commit()
            conn.close()
            messagebox.showinfo("Thành công", "Đã cập nhật hóa đơn.")
            hien_hoadon()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    # ====== XÓA HÓA ĐƠN ======
    def xoa_hoadon():
        selected = tree_hd.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Chọn hóa đơn để xóa.")
            return
        ma_hd = tree_hd.item(selected[0])['values'][0]
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM HoaDon WHERE MaHD=%s", (ma_hd,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Thành công", "Đã xóa hóa đơn.")
            hien_hoadon()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    # ====== CHỌN HÓA ĐƠN TRONG BẢNG ======
    def chon_hoadon(event):
        selected = tree_hd.selection()
        if selected:
            values = tree_hd.item(selected[0])['values']
            # Giá trị: MaHD, HoTen, TenXe, NgayLap, SoLuong, TongTien
            entry_ngaylap.delete(0, tk.END)
            entry_ngaylap.insert(0, values[3])
            entry_soluong.delete(0, tk.END)
            entry_soluong.insert(0, values[4])
            entry_tongtien.delete(0, tk.END)
            entry_tongtien.insert(0, values[5])

    # ====== GIAO DIỆN ======
    # --- Khung form nhập liệu ---
    form_frame = tk.Frame(frame_hd)
    form_frame.pack(pady=20) # <-- Dùng pack để canh giữa

    tk.Label(form_frame, text="Khách hàng:").grid(row=0, column=0, padx=5, pady=5)
    combo_kh = ttk.Combobox(form_frame, width=30)
    combo_kh.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Xe máy:").grid(row=0, column=2)
    combo_xe = ttk.Combobox(form_frame, width=30)
    combo_xe.grid(row=0, column=3, padx=5)
    combo_xe.bind("<<ComboboxSelected>>", tinh_tong_tien)

    tk.Label(form_frame, text="Ngày lập (YYYY-MM-DD):").grid(row=1, column=0)
    entry_ngaylap = tk.Entry(form_frame) # Bạn có thể thay = DateEntry(form_frame)
    entry_ngaylap.grid(row=1, column=1)

    tk.Label(form_frame, text="Số lượng:").grid(row=1, column=2)
    entry_soluong = tk.Entry(form_frame)
    entry_soluong.grid(row=1, column=3)
    entry_soluong.bind("<KeyRelease>", tinh_tong_tien)

    tk.Label(form_frame, text="Tổng tiền:").grid(row=2, column=0)
    entry_tongtien = tk.Entry(form_frame)
    entry_tongtien.grid(row=2, column=1)

    # --- Khung nút chức năng ---
    btn_frame = tk.Frame(frame_hd)
    btn_frame.pack(pady=10) # <-- Dùng pack để canh giữa
    
    # --- Cài đặt kiểu nút ---
    btn_font = ("Arial", 10, "bold")
    btn_width = 10
    btn_pady = 5
    
    tk.Button(btn_frame, text="Thêm", command=them_hoadon,
              bg="#27ae60", fg="white", font=btn_font, width=btn_width, pady=btn_pady, relief="flat"
              ).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Sửa", command=sua_hoadon,
              bg="#3498db", fg="white", font=btn_font, width=btn_width, pady=btn_pady, relief="flat"
              ).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="Xóa", command=xoa_hoadon,
              bg="#e74c3c", fg="white", font=btn_font, width=btn_width, pady=btn_pady, relief="flat"
              ).grid(row=0, column=2, padx=5)
    tk.Button(btn_frame, text="Quay lại", command=lambda:[frame_hd.pack_forget(), show_home()],
              bg="#f39c12", fg="white", font=btn_font, width=btn_width, pady=btn_pady, relief="flat"
              ).grid(row=0, column=3, padx=5)

    # ====== BẢNG HIỂN THỊ ======
    # --- Khung cho Treeview ---
    tree_frame = tk.Frame(frame_hd)
    tree_frame.pack(fill="both", expand=True, padx=20, pady=10) # <-- Dùng pack
    
    cols = ("Mã HD", "Khách hàng", "Xe", "Ngày lập", "Số lượng", "Tổng tiền")
    tree_hd = ttk.Treeview(tree_frame, columns=cols, show="headings", height=15)
    for col in cols:
        tree_hd.heading(col, text=col)
        tree_hd.column(col, width=130)
        
    tree_hd.pack(fill="both", expand=True) # <-- Dùng pack
    tree_hd.bind("<<TreeviewSelect>>", chon_hoadon)

    load_combo_data()
    hien_hoadon()
    return frame_hd