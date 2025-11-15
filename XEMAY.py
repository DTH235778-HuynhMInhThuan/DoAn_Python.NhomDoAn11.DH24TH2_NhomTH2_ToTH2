import tkinter as tk
from tkinter import ttk, messagebox
from db import connect_db
from XEGOIY import xe_goi_y

def tao_frame_xe(root, show_home):
    frame_xe = tk.Frame(root)
    frame_xe.pack(fill="both", expand=True)  # full màn hình

    # =====================================================================
    # ====== TẤT CẢ CÁC HÀM (ĐÃ DI CHUYỂN LÊN ĐẦU ĐỂ SỬA LỖI) ======
    # =====================================================================

    def cap_nhat_xe_goi_y(event):
        hang = combo_hangxe.get()
        combo_tenxe["values"] = list(xe_goi_y.get(hang, {}).keys())
        combo_tenxe.set("")
        entry_giaxe.delete(0, tk.END)

    def dien_gia(event):
        hang = combo_hangxe.get()
        ten = combo_tenxe.get()
        if hang in xe_goi_y and ten in xe_goi_y[hang]:
            entry_giaxe.delete(0, tk.END)
            entry_giaxe.insert(0, xe_goi_y[hang][ten])

    def hien_xe():
        for row in tree_xe.get_children():
            tree_xe.delete(row)
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT MaXe,TenXe,HangXe,MauXe,GiaXe,SoLuong FROM XeMay")
            for row in cursor.fetchall():
                tree_xe.insert("", tk.END, values=row)
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def them_xe():
        tenxe = combo_tenxe.get()
        hangxe = combo_hangxe.get()
        mauxe = entry_mauxe.get()
        giaxe = entry_giaxe.get()
        soluong = entry_soluong.get()
        if not tenxe or not hangxe or not giaxe or not soluong:
            messagebox.showwarning("Thiếu dữ liệu","Nhập đầy đủ thông tin xe.")
            return
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO XeMay (TenXe,HangXe,MauXe,GiaXe,SoLuong) VALUES (%s,%s,%s,%s,%s)",
                        (tenxe, hangxe, mauxe, giaxe, soluong))
            conn.commit()
            messagebox.showinfo("Thành công", f"Đã thêm xe {tenxe}.")
            hien_xe()
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def sua_xe():
        selected = tree_xe.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn","Chọn xe để sửa.")
            return
        ma_xe = tree_xe.item(selected[0])['values'][0]
        tenxe = combo_tenxe.get()
        hangxe = combo_hangxe.get()
        mauxe = entry_mauxe.get()
        giaxe = entry_giaxe.get()
        soluong = entry_soluong.get()
        if not tenxe or not hangxe or not giaxe or not soluong or not mauxe:
            messagebox.showwarning("Thiếu dữ liệu","Nhập đầy đủ thông tin xe.")
            return
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""UPDATE XeMay 
                              SET TenXe=%s,HangXe=%s,MauXe=%s,GiaXe=%s,SoLuong=%s 
                              WHERE MaXe=%s""",
                           (tenxe, hangxe, mauxe, giaxe, soluong, ma_xe))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã cập nhật xe.")
            hien_xe()
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def xoa_xe():
        selected = tree_xe.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn","Chọn xe để xóa.")
            return
        ma_xe = tree_xe.item(selected[0])['values'][0]
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM XeMay WHERE MaXe=%s",(ma_xe,))
            conn.commit()
            messagebox.showinfo("Thành công","Đã xóa xe.")
            hien_xe()
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def chon_xe(event):
        selected = tree_xe.selection()
        if selected:
            values = tree_xe.item(selected[0])['values']
            combo_tenxe.set(values[1])
            combo_hangxe.set(values[2])
            entry_mauxe.delete(0, tk.END)
            entry_mauxe.insert(0, values[3])
            entry_giaxe.delete(0, tk.END)
            entry_giaxe.insert(0, values[4])
            entry_soluong.delete(0, tk.END)
            entry_soluong.insert(0, values[5])

    # =====================================================================
    # ====== GIAO DIỆN (Bắt đầu từ đây) ======
    # =====================================================================

    # ====== FORM NHẬP DỮ LIỆU ======
    form_frame = tk.Frame(frame_xe)
    form_frame.pack(pady=20)

    tk.Label(form_frame, text="Hãng xe:").grid(row=0, column=0, padx=5, pady=5)
    combo_hangxe = ttk.Combobox(form_frame, values=list(xe_goi_y.keys()))
    combo_hangxe.grid(row=0, column=1, padx=5)
    combo_hangxe.bind("<<ComboboxSelected>>", cap_nhat_xe_goi_y)

    tk.Label(form_frame, text="Tên xe:").grid(row=0, column=2, padx=5)
    combo_tenxe = ttk.Combobox(form_frame, values=[])
    combo_tenxe.grid(row=0, column=3, padx=5)
    combo_tenxe.bind("<<ComboboxSelected>>", dien_gia)

    tk.Label(form_frame, text="Màu xe:").grid(row=1, column=0, padx=5)
    entry_mauxe = tk.Entry(form_frame)
    entry_mauxe.grid(row=1, column=1, padx=5)

    tk.Label(form_frame, text="Giá xe:").grid(row=1, column=2, padx=5)
    entry_giaxe = tk.Entry(form_frame)
    entry_giaxe.grid(row=1, column=3, padx=5)

    tk.Label(form_frame, text="Số lượng:").grid(row=2, column=0, padx=5)
    entry_soluong = tk.Entry(form_frame)
    entry_soluong.grid(row=2, column=1, padx=5)

    # ====== NÚT HÀNH ĐỘNG (ĐÃ SỬA MÀU) ======
    btn_frame = tk.Frame(frame_xe)
    btn_frame.pack(pady=10)
    
    # --- Cài đặt kiểu nút ---
    btn_font = ("Arial", 10, "bold")
    btn_width = 10
    btn_pady = 5

    # Các command=... này giờ sẽ hoạt động vì hàm đã được định nghĩa ở trên
    tk.Button(btn_frame, text="Thêm", command=them_xe, 
              bg="#27ae60", fg="white", font=btn_font, width=btn_width, pady=btn_pady, relief="flat"
              ).grid(row=0,column=0,padx=5)
    tk.Button(btn_frame, text="Sửa", command=sua_xe,
              bg="#3498db", fg="white", font=btn_font, width=btn_width, pady=btn_pady, relief="flat"
              ).grid(row=0,column=1,padx=5)
    tk.Button(btn_frame, text="Xóa", command=xoa_xe,
              bg="#e74c3c", fg="white", font=btn_font, width=btn_width, pady=btn_pady, relief="flat"
              ).grid(row=0,column=2,padx=5)
    tk.Button(btn_frame, text="Quay lại", command=lambda:[frame_xe.pack_forget(), show_home()],
              bg="#f39c12", fg="white", font=btn_font, width=btn_width, pady=btn_pady, relief="flat"
              ).grid(row=0,column=3,padx=5)

    # ====== TREEVIEW (KHÔI PHỤC LẠI BẢNG) ======
    tree_frame = tk.Frame(frame_xe)
    tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

    cols = ("Mã xe","Tên xe","Hãng xe","Màu xe","Giá xe","Số lượng")
    tree_xe = ttk.Treeview(tree_frame, columns=cols, show="headings")
    for col in cols:
        tree_xe.heading(col, text=col)
        tree_xe.column(col, width=150, anchor='center')  # căn giữa cột
    tree_xe.pack(fill="both", expand=True)
    
    # .bind() này cũng sẽ hoạt động vì hàm chon_xe đã được định nghĩa
    tree_xe.bind("<<TreeviewSelect>>", chon_xe) 

    # ====== TẢI DỮ LIỆU LẦN ĐẦU ======
    hien_xe()
    
    return frame_xe