
import tkinter as tk
from tkinter import ttk, messagebox
from db import connect_db

def tao_frame_tonkho(root, show_home):
    frame_tk = tk.Frame(root)
    frame_tk.pack(fill="both", expand=True)

    # ====== HÀM HIỂN THỊ TỒN KHO ======
    def hien_tonkho():
        # Xóa dữ liệu cũ trên cây
        for row in tree_tk.get_children():
            tree_tk.delete(row)
        
        try:
            conn = connect_db()
            cursor = conn.cursor()

            # Lấy hãng xe được chọn từ combobox
            hang_xe_chon = combo_hangxe_filter.get()

            # Câu truy vấn SQL để tính toán tồn kho
            # 1. Lấy tất cả xe từ bảng XeMay
            # 2. Dùng LEFT JOIN để liên kết với tổng số xe đã bán từ bảng HoaDon
            # 3. Dùng IFNULL để xử lý xe chưa bán (trả về 0 thay vì NULL)
            # 4. Nhóm theo từng xe
            query = """
                SELECT 
                    x.MaXe, 
                    x.TenXe, 
                    x.HangXe, 
                    x.SoLuong AS SoLuongGoc, 
                    IFNULL(SUM(h.SoLuong), 0) AS TongDaBan
                FROM XeMay x
                LEFT JOIN HoaDon h ON x.MaXe = h.MaXe
            """
            
            params = []
            # Nếu người dùng đã chọn một hãng xe (và không phải "Tất cả")
            if hang_xe_chon and hang_xe_chon != "Tất cả":
                query += " WHERE x.HangXe = %s"
                params.append(hang_xe_chon)

            query += " GROUP BY x.MaXe, x.TenXe, x.HangXe, x.SoLuong"
            
            cursor.execute(query, tuple(params))
            
            rows = cursor.fetchall()
            conn.close()

            # Hiển thị dữ liệu lên Treeview
            for row in rows:
                ma_xe = row[0]
                ten_xe = row[1]
                hang_xe = row[2]
                so_luong_goc = int(row[3])
                da_ban = int(row[4])
                
                # Tính tồn kho thực tế
                ton_kho = so_luong_goc - da_ban
                
                # Thêm vào bảng
                tree_tk.insert("", tk.END, values=(ma_xe, ten_xe, hang_xe, so_luong_goc, da_ban, ton_kho))
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu tồn kho:\n{str(e)}")

    # ====== HÀM TẢI CÁC HÃNG XE VÀO COMBOBOX ======
    def load_hangxe_combobox():
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT HangXe FROM XeMay ORDER BY HangXe")
            hang_xe_list = [row[0] for row in cursor.fetchall()]
            
            # Thêm "Tất cả" vào đầu danh sách
            combo_hangxe_filter["values"] = ["Tất cả"] + hang_xe_list
            combo_hangxe_filter.set("Tất cả") # Đặt giá trị mặc định
            
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách hãng xe:\n{str(e)}")

    # ====== GIAO DIỆN ======

    # --- Frame cho bộ lọc ---
    filter_frame = tk.Frame(frame_tk)
    filter_frame.pack(pady=15)
    
    tk.Label(filter_frame, text="Lọc theo hãng xe:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
    
    combo_hangxe_filter = ttk.Combobox(filter_frame, width=30, font=("Arial", 12))
    combo_hangxe_filter.grid(row=0, column=1, padx=5, pady=5)
    # Gán sự kiện: khi chọn hãng khác, tự động gọi hàm hien_tonkho
    combo_hangxe_filter.bind("<<ComboboxSelected>>", lambda event: hien_tonkho())

    # --- Frame cho các nút ---
    # --- Frame cho các nút ---
    btn_frame = tk.Frame(frame_tk)
    btn_frame.pack(pady=5)
    
    # --- Cài đặt kiểu nút ---
    btn_font = ("Arial", 10, "bold")
    btn_width = 10
    btn_pady = 5
    
    tk.Button(btn_frame, text="Quay lại", command=lambda:[frame_tk.pack_forget(), show_home()],
              bg="#f39c12", fg="white", font=btn_font, width=btn_width, pady=btn_pady, relief="flat"
              ).grid(row=0, column=0, padx=10)
    # --- Bảng Treeview hiển thị tồn kho ---
    tree_frame = tk.Frame(frame_tk)
    tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

    cols = ("Mã xe", "Tên xe", "Hãng xe", "Số lượng gốc", "Đã bán", "Tồn kho")
    tree_tk = ttk.Treeview(tree_frame, columns=cols, show="headings", height=20)
    
    for col in cols:
        tree_tk.heading(col, text=col)
        tree_tk.column(col, width=150, anchor='center')

    # Đặt độ rộng cột cho phù hợp
    tree_tk.column("Tên xe", width=250)
    tree_tk.column("Tồn kho", width=100)
    
    tree_tk.pack(fill="both", expand=True)
    
    # --- Tải dữ liệu lần đầu ---
    load_hangxe_combobox()
    hien_tonkho()

    return frame_tk