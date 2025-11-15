# File: KHACHHANG.py (Đã sửa lỗi canh lề)
import tkinter as tk
from tkinter import ttk, messagebox
from db import connect_db

def tao_frame_khachhang(root, show_home):
    frame_kh = tk.Frame(root)

    # ====== HIỂN THỊ DANH SÁCH KHÁCH HÀNG ======
    def hien_khachhang():
        for row in tree_kh.get_children():
            tree_kh.delete(row)
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT MaKH, HoTen, SDT, DiaChi FROM KhachHang")
            for row in cursor.fetchall():
                tree_kh.insert("", tk.END, values=row)
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    # ====== THÊM KHÁCH HÀNG ======
    def them_khachhang():
        hoten = entry_hoten.get()
        sdt = entry_sdt.get()
        diachi = entry_diachi.get()
        if not hoten or not sdt or not diachi:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin.")
            return
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO KhachHang (HoTen, SDT, DiaChi) VALUES (%s, %s, %s)",
                (hoten, sdt, diachi)
            )
            conn.commit()
            messagebox.showinfo("Thành công", f"Đã thêm khách hàng: {hoten}")
            hien_khachhang()
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    # ====== SỬA KHÁCH HÀNG ======
    def sua_khachhang():
        selected = tree_kh.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Chọn khách hàng để sửa.")
            return
        makh = tree_kh.item(selected[0])['values'][0]
        hoten = entry_hoten.get()
        sdt = entry_sdt.get()
        diachi = entry_diachi.get()
        if not hoten or not sdt or not diachi:
            messagebox.showwarning("Thiếu dữ liệu", "Nhập đầy đủ thông tin.")
            return
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE KhachHang 
                SET HoTen=%s, SDT=%s, DiaChi=%s 
                WHERE MaKH=%s
            """, (hoten, sdt, diachi, makh))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã cập nhật thông tin khách hàng.")
            hien_khachhang()
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    # ====== XÓA KHÁCH HÀNG ======
    def xoa_khachhang():
        selected = tree_kh.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Chọn khách hàng để xóa.")
            return
        makh = tree_kh.item(selected[0])['values'][0]
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM KhachHang WHERE MaKH=%s", (makh,))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã xóa khách hàng.")
            hien_khachhang()
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    # ====== CHỌN KHÁCH HÀNG TỪ BẢNG ======
    def chon_khachhang(event):
        selected = tree_kh.selection()
        if selected:
            values = tree_kh.item(selected[0])['values']
            entry_hoten.delete(0, tk.END)
            entry_hoten.insert(0, values[1])
            entry_sdt.delete(0, tk.END)
            entry_sdt.insert(0, values[2])
            entry_diachi.delete(0, tk.END)
            entry_diachi.insert(0, values[3])

    # ====== GIAO DIỆN (ĐÃ SỬA DÙNG PACK) ======
    
    # --- Khung form nhập liệu ---
    form_frame = tk.Frame(frame_kh)
    form_frame.pack(pady=20) # <-- Dùng pack để canh giữa

    tk.Label(form_frame, text="Họ tên:").grid(row=0, column=0, padx=5, pady=5)
    entry_hoten = tk.Entry(form_frame)
    entry_hoten.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="SĐT:").grid(row=0, column=2, padx=5)
    entry_sdt = tk.Entry(form_frame)
    entry_sdt.grid(row=0, column=3, padx=5)

    tk.Label(form_frame, text="Địa chỉ:").grid(row=1, column=0, padx=5)
    entry_diachi = tk.Entry(form_frame, width=40)
    entry_diachi.grid(row=1, column=1, columnspan=3, padx=5, pady=5)

   # ====== NÚT CHỨC NĂNG ======
    btn_frame = tk.Frame(frame_kh)
    btn_frame.pack(pady=10) # <-- Dùng pack để canh giữa
    
    # --- Cài đặt kiểu nút ---
    btn_font = ("Arial", 10, "bold")
    btn_width = 10
    btn_pady = 5
    
    tk.Button(btn_frame, text="Thêm", command=them_khachhang,
              bg="#27ae60", fg="white", font=btn_font, width=btn_width, pady=btn_pady, relief="flat"
              ).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Sửa", command=sua_khachhang,
              bg="#3498db", fg="white", font=btn_font, width=btn_width, pady=btn_pady, relief="flat"
              ).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="Xóa", command=xoa_khachhang,
              bg="#e74c3c", fg="white", font=btn_font, width=btn_width, pady=btn_pady, relief="flat"
              ).grid(row=0, column=2, padx=5)
    tk.Button(btn_frame, text="Quay lại", command=lambda:[frame_kh.pack_forget(), show_home()],
              bg="#f39c12", fg="white", font=btn_font, width=btn_width, pady=btn_pady, relief="flat"
              ).grid(row=0, column=3, padx=5)
    # ====== BẢNG HIỂN THỊ ======
    # --- Khung cho Treeview ---
    tree_frame = tk.Frame(frame_kh)
    tree_frame.pack(fill="both", expand=True, padx=20, pady=10) # <-- Dùng pack
    
    cols = ("Mã KH", "Họ tên", "SĐT", "Địa chỉ")
    tree_kh = ttk.Treeview(tree_frame, columns=cols, show="headings", height=15)
    for col in cols:
        tree_kh.heading(col, text=col)
        tree_kh.column(col, width=150)
        
    tree_kh.pack(fill="both", expand=True) # <-- Dùng pack
    tree_kh.bind("<<TreeviewSelect>>", chon_khachhang)

    hien_khachhang()
    return frame_kh