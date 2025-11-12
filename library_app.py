import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
# Import DatabaseManager từ file database_manager.py
from database_manager import DatabaseManager
import re # Để kiểm tra regex cho mật khẩu

class LibraryApp:
    def __init__(self, master):
        self.master = master
        master.title("Hệ Thống Quản Lý Thư Viện")
        master.geometry("1000x700")
        master.resizable(False, False)

        # Khởi tạo đối tượng DatabaseManager
        self.db = DatabaseManager()

        # Cấu hình phong cách chung cho ứng dụng
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#e0f2f7')
        self.style.configure('TLabel', background='#e0f2f7', font=('Segoe UI', 12))
        self.style.configure('TButton', font=('Segoe UI', 12, 'bold'), background='#007acc', foreground='white', relief='flat')
        self.style.map('TButton', background=[('active', '#005f99')])
        self.style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'), background='#cce7f5', foreground='#333333')
        self.style.configure('Treeview', font=('Segoe UI', 10), rowheight=25)
        self.style.map('Treeview', background=[('selected', '#a8d7ec')])

        self.current_user_id = None
        self.current_librarian_id = None

        self.create_login_screen()

    def clear_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def create_login_screen(self):
        self.clear_screen()
        
        login_frame = ttk.Frame(self.master, padding="50 50 50 50", style='TFrame')
        login_frame.pack(expand=True)

        ttk.Label(login_frame, text="HỆ THỐNG QUẢN LÝ THƯ VIỆN", font=("Segoe UI", 28, "bold"), foreground='#007acc').pack(pady=30)
        ttk.Label(login_frame, text="ĐĂNG NHẬP", font=("Segoe UI", 20, "bold")).pack(pady=20)

        ttk.Label(login_frame, text="Tên đăng nhập:", font=("Segoe UI", 14)).pack(pady=5)
        self.username_entry = ttk.Entry(login_frame, font=("Segoe UI", 14), width=30)
        self.username_entry.pack(pady=5)
        self.username_entry.focus_set()

        ttk.Label(login_frame, text="Mật khẩu:", font=("Segoe UI", 14)).pack(pady=5)
        self.password_entry = ttk.Entry(login_frame, show="*", font=("Segoe UI", 14), width=30)
        self.password_entry.pack(pady=5)

        ttk.Button(login_frame, text="Đăng nhập", command=self.login, style='TButton', width=20).pack(pady=25)
        ttk.Button(login_frame, text="Đăng ký tài khoản người dùng", command=self.register_user, style='TButton', width=25).pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Lỗi đăng nhập", "Vui lòng nhập tên đăng nhập và mật khẩu.")
            return

        # Kiểm tra quản lý thư viện (hardcoded)
        if username == "admin" and password == "admin":
            messagebox.showinfo("Đăng nhập thành công", "Chào mừng Admin!")
            self.show_admin_dashboard()
            return

        # Kiểm tra thủ thư thông qua DatabaseManager
        librarian_id = self.db.authenticate_librarian(username, password)
        if librarian_id:
            self.current_librarian_id = librarian_id
            messagebox.showinfo("Đăng nhập thành công", f"Chào mừng Thủ thư {username}!")
            self.show_librarian_dashboard()
            return

        # Kiểm tra người dùng thông qua DatabaseManager
        user_id = self.db.authenticate_user(username, password)
        if user_id:
            self.current_user_id = user_id
            messagebox.showinfo("Đăng nhập thành công", f"Chào mừng {username}!")
            self.show_user_dashboard()
            return

        messagebox.showerror("Lỗi đăng nhập", "Tên đăng nhập hoặc mật khẩu không đúng.")

    # Hàm kiểm tra mật khẩu mới
    def _validate_password(self, password):
        if not re.search(r'[a-zA-Z]{3,}', password):
            return False, "Mật khẩu phải chứa ít nhất 3 chữ cái."
        if not re.search(r'[0-9]{3,}', password):
            return False, "Mật khẩu phải chứa ít nhất 3 chữ số."
        if re.search(r'[^a-zA-Z0-9]', password):
            return False, "Mật khẩu không được chứa ký tự đặc biệt."
        return True, ""

    def register_user(self):
        top = tk.Toplevel(self.master)
        top.title("Đăng ký tài khoản người dùng")
        top.geometry("400x380") # Tăng chiều cao để hiển thị thông báo mật khẩu
        top.transient(self.master)
        top.grab_set()

        register_frame = ttk.Frame(top, padding="20", style='TFrame')
        register_frame.pack(expand=True, fill='both')

        ttk.Label(register_frame, text="ĐĂNG KÝ TÀI KHOẢN NGƯỜI DÙNG", font=("Segoe UI", 16, "bold")).pack(pady=20)

        ttk.Label(register_frame, text="Tên đăng nhập:", font=("Segoe UI", 12)).pack(pady=5)
        new_username_entry = ttk.Entry(register_frame, font=("Segoe UI", 12), width=30)
        new_username_entry.pack(pady=5)

        ttk.Label(register_frame, text="Mật khẩu:", font=("Segoe UI", 12)).pack(pady=5)
        new_password_entry = ttk.Entry(register_frame, show="*", font=("Segoe UI", 12), width=30)
        new_password_entry.pack(pady=5)
        
        ttk.Label(register_frame, text="Mật khẩu phải có ít nhất 3 chữ cái và 3 chữ số,\nkhông chứa ký tự đặc biệt.", font=("Segoe UI", 9), foreground='gray').pack(pady=2, padx=5)


        def save_new_user():
            username = new_username_entry.get().strip()
            password = new_password_entry.get().strip()

            if not username or not password:
                messagebox.showerror("Lỗi", "Tên đăng nhập và mật khẩu không được để trống.", parent=top)
                return
            
            # Kiểm tra mật khẩu theo quy tắc mới
            is_valid_password, msg = self._validate_password(password)
            if not is_valid_password:
                messagebox.showerror("Lỗi mật khẩu", msg, parent=top)
                return

            # Gọi hàm từ DatabaseManager để thêm người dùng
            new_user_id = self.db.add_user(username, password)
            if new_user_id:
                messagebox.showinfo("Thành công", f"Tài khoản người dùng đã được tạo. ID của bạn là: {new_user_id}", parent=top)
                top.destroy()
                self.master.grab_release()
            else:
                messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại.", parent=top)

        ttk.Button(register_frame, text="Đăng ký", command=save_new_user, style='TButton', width=15).pack(pady=20)
        top.protocol("WM_DELETE_WINDOW", lambda: (self.master.grab_release(), top.destroy()))

    # --- Giao diện Quản lý Thư viện (Admin) ---
    def show_admin_dashboard(self):
        self.clear_screen()
        
        main_frame = ttk.Frame(self.master, padding="20", style='TFrame')
        main_frame.pack(fill='both', expand=True)

        ttk.Label(main_frame, text="TRANG QUẢN LÝ THƯ VIỆN", font=("Segoe UI", 24, "bold"), foreground='#007acc').pack(pady=20)

        button_frame = ttk.Frame(main_frame, style='TFrame')
        button_frame.pack(pady=20)

        ttk.Button(button_frame, text="Quản lý Tài Khoản Thủ Thư", command=self.manage_librarian_accounts, style='TButton', width=35).grid(row=0, column=0, padx=15, pady=10)
        ttk.Button(button_frame, text="Quản lý Tài Khoản Người Dùng", command=self.manage_user_accounts, style='TButton', width=35).grid(row=0, column=1, padx=15, pady=10)
        ttk.Button(button_frame, text="Quản lý Sách (Thêm/Xóa)", command=self.manage_books_admin, style='TButton', width=35).grid(row=1, column=0, padx=15, pady=10)
        ttk.Button(button_frame, text="Quản lý Chủ Đề Sách", command=self.manage_book_topics, style='TButton', width=35).grid(row=1, column=1, padx=15, pady=10)
        ttk.Button(button_frame, text="Xem Số Lượng Tài Khoản", command=self.view_account_counts, style='TButton', width=35).grid(row=2, column=0, padx=15, pady=10)
        ttk.Button(button_frame, text="Xem Lịch Sử Mượn/Trả Sách", command=self.view_all_borrow_records, style='TButton', width=35).grid(row=2, column=1, padx=15, pady=10)

        ttk.Button(main_frame, text="Đăng Xuất", command=self.create_login_screen, style='TButton', width=20).pack(pady=40)

    # --- Quản lý Tài Khoản Thủ Thư ---
    def manage_librarian_accounts(self):
        top = tk.Toplevel(self.master)
        top.title("Quản lý tài khoản thủ thư")
        top.geometry("700x500")
        top.transient(self.master)
        top.grab_set()

        frame = ttk.Frame(top, padding="20", style='TFrame')
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="QUẢN LÝ TÀI KHOẢN THỦ THƯ", font=("Segoe UI", 18, "bold"), foreground='#007acc').pack(pady=15)

        button_frame = ttk.Frame(frame, style='TFrame')
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Tạo Tài Khoản Thủ Thư", command=lambda: self.create_librarian_account(top), style='TButton', width=25).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Xóa Tài Khoản Thủ Thư", command=lambda: self.delete_librarian_account(top), style='TButton', width=25).pack(side=tk.LEFT, padx=10)
        
        self.librarian_tree_frame = ttk.Frame(frame, style='TFrame')
        self.librarian_tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        self.display_librarians_in_treeview(self.librarian_tree_frame)
        
        top.protocol("WM_DELETE_WINDOW", lambda: (self.master.grab_release(), top.destroy()))

    def display_librarians_in_treeview(self, parent_frame):
        for widget in parent_frame.winfo_children():
            widget.destroy()

        tree = ttk.Treeview(parent_frame, columns=("ID", "Tên đăng nhập"), show="headings", style='Treeview')
        tree.heading("ID", text="ID Thủ thư", anchor=tk.W)
        tree.heading("Tên đăng nhập", text="Tên đăng nhập", anchor=tk.W)
        tree.column("ID", width=120, anchor=tk.CENTER)
        tree.column("Tên đăng nhập", width=250, anchor=tk.W)

        # Lấy dữ liệu từ DatabaseManager
        librarians_df = self.db.get_all_librarians()
        for index, row in librarians_df.iterrows():
            tree.insert("", "end", values=(row['ID Thủ thư'], row['Tên đăng nhập']))
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        tree.configure(yscrollcommand=scrollbar.set)

    def create_librarian_account(self, parent_window):
        top = tk.Toplevel(parent_window)
        top.title("Tạo tài khoản thủ thư")
        top.geometry("380x350") # Tăng chiều cao để hiển thị thông báo mật khẩu
        top.transient(parent_window)
        top.grab_set()

        frame = ttk.Frame(top, padding="20", style='TFrame')
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="TẠO TÀI KHOẢN THỦ THƯ", font=("Segoe UI", 14, "bold")).pack(pady=15)

        ttk.Label(frame, text="Tên đăng nhập:", font=("Segoe UI", 12)).pack(pady=5)
        username_entry = ttk.Entry(frame, font=("Segoe UI", 12), width=30)
        username_entry.pack(pady=5)

        ttk.Label(frame, text="Mật khẩu:", font=("Segoe UI", 12)).pack(pady=5)
        password_entry = ttk.Entry(frame, show="*", font=("Segoe UI", 12), width=30)
        password_entry.pack(pady=5)
        
        ttk.Label(frame, text="Mật khẩu phải có ít nhất 3 chữ cái và 3 chữ số,\nkhông chứa ký tự đặc biệt.", font=("Segoe UI", 9), foreground='gray').pack(pady=2, padx=5)

        def save_librarian():
            username = username_entry.get().strip()
            password = password_entry.get().strip()

            if not username or not password:
                messagebox.showerror("Lỗi", "Tên đăng nhập và mật khẩu không được để trống.", parent=top)
                return
            
            # Kiểm tra mật khẩu theo quy tắc mới
            is_valid_password, msg = self._validate_password(password)
            if not is_valid_password:
                messagebox.showerror("Lỗi mật khẩu", msg, parent=top)
                return
            
            # Gọi hàm từ DatabaseManager để thêm thủ thư
            new_librarian_id = self.db.add_librarian(username, password)
            if new_librarian_id:
                messagebox.showinfo("Thành công", f"Tài khoản thủ thư đã được tạo. ID: {new_librarian_id}", parent=top)
                top.destroy()
                self.display_librarians_in_treeview(self.librarian_tree_frame)
                parent_window.grab_release()
            else:
                messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại.", parent=top)

        ttk.Button(frame, text="Tạo", command=save_librarian, style='TButton', width=12).pack(pady=20)
        top.protocol("WM_DELETE_WINDOW", lambda: (parent_window.grab_release(), top.destroy()))

    def delete_librarian_account(self, parent_window):
        selected_item = self.librarian_tree_frame.winfo_children()[0].selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một thủ thư để xóa.", parent=parent_window)
            return
        
        librarian_id_to_delete = self.librarian_tree_frame.winfo_children()[0].item(selected_item, 'values')[0]

        if messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc chắn muốn xóa tài khoản thủ thư ID {librarian_id_to_delete} không?", parent=parent_window):
            # Gọi hàm từ DatabaseManager để xóa thủ thư
            if self.db.delete_librarian(librarian_id_to_delete):
                messagebox.showinfo("Thành công", "Tài khoản thủ thư đã được xóa.", parent=parent_window)
                self.display_librarians_in_treeview(self.librarian_tree_frame)
            else:
                messagebox.showerror("Lỗi", "ID Thủ thư không tồn tại.", parent=parent_window)
        parent_window.grab_release()


    # --- Quản lý Tài Khoản Người Dùng (Mới) ---
    def manage_user_accounts(self):
        top = tk.Toplevel(self.master)
        top.title("Quản lý tài khoản người dùng")
        top.geometry("700x500")
        top.transient(self.master)
        top.grab_set()

        frame = ttk.Frame(top, padding="20", style='TFrame')
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="QUẢN LÝ TÀI KHOẢN NGƯỜI DÙNG", font=("Segoe UI", 18, "bold"), foreground='#007acc').pack(pady=15)

        button_frame = ttk.Frame(frame, style='TFrame')
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Tạo Tài Khoản Người Dùng", command=lambda: self.create_user_account_admin(top), style='TButton', width=28).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Xóa Tài Khoản Người Dùng", command=lambda: self.delete_user_account_admin(top), style='TButton', width=28).pack(side=tk.LEFT, padx=10)
        
        self.user_tree_frame = ttk.Frame(frame, style='TFrame')
        self.user_tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        self.display_users_in_treeview(self.user_tree_frame)
        
        top.protocol("WM_DELETE_WINDOW", lambda: (self.master.grab_release(), top.destroy()))

    def display_users_in_treeview(self, parent_frame):
        for widget in parent_frame.winfo_children():
            widget.destroy()

        tree = ttk.Treeview(parent_frame, columns=("ID", "Tên đăng nhập"), show="headings", style='Treeview')
        tree.heading("ID", text="ID Người dùng", anchor=tk.W)
        tree.heading("Tên đăng nhập", text="Tên đăng nhập", anchor=tk.W)
        tree.column("ID", width=120, anchor=tk.CENTER)
        tree.column("Tên đăng nhập", width=250, anchor=tk.W)

        # Lấy dữ liệu từ DatabaseManager
        users_df = self.db.get_all_users()
        for index, row in users_df.iterrows():
            tree.insert("", "end", values=(row['ID Người dùng'], row['Tên đăng nhập']))
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        tree.configure(yscrollcommand=scrollbar.set)

    def create_user_account_admin(self, parent_window):
        top = tk.Toplevel(parent_window)
        top.title("Tạo tài khoản người dùng")
        top.geometry("380x350") # Tăng chiều cao để hiển thị thông báo mật khẩu
        top.transient(parent_window)
        top.grab_set()

        frame = ttk.Frame(top, padding="20", style='TFrame')
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="TẠO TÀI KHOẢN NGƯỜI DÙNG", font=("Segoe UI", 14, "bold")).pack(pady=15)

        ttk.Label(frame, text="Tên đăng nhập:", font=("Segoe UI", 12)).pack(pady=5)
        username_entry = ttk.Entry(frame, font=("Segoe UI", 12), width=30)
        username_entry.pack(pady=5)

        ttk.Label(frame, text="Mật khẩu:", font=("Segoe UI", 12)).pack(pady=5)
        password_entry = ttk.Entry(frame, show="*", font=("Segoe UI", 12), width=30)
        password_entry.pack(pady=5)

        ttk.Label(frame, text="Mật khẩu phải có ít nhất 3 chữ cái và 3 chữ số,\nkhông chứa ký tự đặc biệt.", font=("Segoe UI", 9), foreground='gray').pack(pady=2, padx=5)

        def save_user():
            username = username_entry.get().strip()
            password = password_entry.get().strip()

            if not username or not password:
                messagebox.showerror("Lỗi", "Tên đăng nhập và mật khẩu không được để trống.", parent=top)
                return
            
            # Kiểm tra mật khẩu theo quy tắc mới
            is_valid_password, msg = self._validate_password(password)
            if not is_valid_password:
                messagebox.showerror("Lỗi mật khẩu", msg, parent=top)
                return

            # Gọi hàm từ DatabaseManager để thêm người dùng
            new_user_id = self.db.add_user(username, password)
            if new_user_id:
                messagebox.showinfo("Thành công", f"Tài khoản người dùng đã được tạo. ID: {new_user_id}", parent=top)
                top.destroy()
                self.display_users_in_treeview(self.user_tree_frame)
                parent_window.grab_release()
            else:
                messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại.", parent=top)

        ttk.Button(frame, text="Tạo", command=save_user, style='TButton', width=12).pack(pady=20)
        top.protocol("WM_DELETE_WINDOW", lambda: (parent_window.grab_release(), top.destroy()))

    def delete_user_account_admin(self, parent_window):
        selected_item = self.user_tree_frame.winfo_children()[0].selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một người dùng để xóa.", parent=parent_window)
            return
        
        user_id_to_delete = self.user_tree_frame.winfo_children()[0].item(selected_item, 'values')[0]

        if messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc chắn muốn xóa tài khoản người dùng ID {user_id_to_delete} không?", parent=parent_window):
            # Gọi hàm từ DatabaseManager để xóa người dùng
            if self.db.delete_user(user_id_to_delete):
                messagebox.showinfo("Thành công", "Tài khoản người dùng đã được xóa.", parent=parent_window)
                self.display_users_in_treeview(self.user_tree_frame)
            else:
                messagebox.showerror("Lỗi", "ID Người dùng không tồn tại.", parent=parent_window)
        parent_window.grab_release()

    def view_account_counts(self):
        # Lấy dữ liệu từ DatabaseManager
        user_count = len(self.db.get_all_users())
        librarian_count = len(self.db.get_all_librarians())
        messagebox.showinfo("Số Lượng Tài Khoản", f"Tổng số tài khoản Người dùng: {user_count}\nTổng số tài khoản Thủ thư: {librarian_count}")

    def manage_books_admin(self):
        top = tk.Toplevel(self.master)
        top.title("Quản lý sách (Admin)")
        top.geometry("900x650")
        top.transient(self.master)
        top.grab_set()

        frame = ttk.Frame(top, padding="20", style='TFrame')
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="QUẢN LÝ SÁCH", font=("Segoe UI", 18, "bold"), foreground='#007acc').pack(pady=15)

        button_frame = ttk.Frame(frame, style='TFrame')
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Thêm Sách", command=lambda: self.add_book(top, "admin"), style='TButton', width=20).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Xóa Sách", command=lambda: self.delete_book(top, "admin"), style='TButton', width=20).pack(side=tk.LEFT, padx=10)
        
        self.admin_book_tree_frame = ttk.Frame(frame, style='TFrame')
        self.admin_book_tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        # Truyền for_admin=True để hiển thị cột 'Số lượng ban đầu'
        self.display_books_in_treeview(self.admin_book_tree_frame, for_admin=True)
        
        top.protocol("WM_DELETE_WINDOW", lambda: (self.master.grab_release(), top.destroy()))


    def add_book(self, parent_window, user_role, librarian_id=None):
        top = tk.Toplevel(parent_window)
        top.title("Thêm Sách")
        top.geometry("450x650")
        top.transient(parent_window)
        top.grab_set()

        frame = ttk.Frame(top, padding="20", style='TFrame')
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="THÊM SÁCH MỚI", font=("Segoe UI", 16, "bold")).pack(pady=15)

        ttk.Label(frame, text="Tên sách:", font=("Segoe UI", 12)).pack(pady=5)
        title_entry = ttk.Entry(frame, font=("Segoe UI", 12), width=40)
        title_entry.pack(pady=5)

        ttk.Label(frame, text="Năm xuất bản:", font=("Segoe UI", 12)).pack(pady=5)
        year_entry = ttk.Entry(frame, font=("Segoe UI", 12), width=40)
        year_entry.pack(pady=5)

        ttk.Label(frame, text="Tác giả:", font=("Segoe UI", 12)).pack(pady=5)
        author_entry = ttk.Entry(frame, font=("Segoe UI", 12), width=40)
        author_entry.pack(pady=5)

        ttk.Label(frame, text="Số lượng:", font=("Segoe UI", 12)).pack(pady=5)
        quantity_entry = ttk.Entry(frame, font=("Segoe UI", 12), width=40)
        quantity_entry.pack(pady=5)

        ttk.Label(frame, text="Chủ đề:", font=("Segoe UI", 12)).pack(pady=5)
        topic_entry = ttk.Entry(frame, font=("Segoe UI", 12), width=40)
        topic_entry.pack(pady=5)

        def save_book():
            title = title_entry.get().strip()
            year = year_entry.get().strip()
            author = author_entry.get().strip()
            quantity = quantity_entry.get().strip()
            topic = topic_entry.get().strip()

            if not all([title, year, author, quantity, topic]):
                messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin.", parent=top)
                return
            
            try:
                quantity = int(quantity)
                year = int(year)
                if quantity <= 0:
                    messagebox.showerror("Lỗi", "Số lượng phải là số nguyên dương.", parent=top)
                    return
            except ValueError:
                messagebox.showerror("Lỗi", "Năm xuất bản và Số lượng phải là số nguyên hợp lệ.", parent=top)
                return
            
            added_by_librarian_id = librarian_id if user_role == "librarian" else "admin"

            # Gọi hàm từ DatabaseManager để thêm sách
            if self.db.add_book(title, year, author, quantity, topic, added_by_librarian_id):
                messagebox.showinfo("Thành công", "Sách đã được thêm vào thư viện.", parent=top)
                top.destroy()
                if user_role == "admin":
                    # Cập nhật lại Treeview của admin, hiển thị cả cột "Số lượng ban đầu"
                    self.display_books_in_treeview(self.admin_book_tree_frame, for_admin=True)
                else:
                    self.display_books_in_treeview(self.librarian_book_tree_frame, for_admin=False, librarian_id=librarian_id)
                parent_window.grab_release()
            else:
                messagebox.showerror("Lỗi", "Không thể thêm sách. Vui lòng thử lại.", parent=top) # Nên chi tiết hơn nếu có lỗi từ DB

        ttk.Button(frame, text="Thêm Sách", command=save_book, style='TButton', width=15).pack(pady=20)
        top.protocol("WM_DELETE_WINDOW", lambda: (parent_window.grab_release(), top.destroy()))

    def delete_book(self, parent_window, user_role, librarian_id=None):
        tree = None
        if user_role == "admin":
            tree = self.admin_book_tree_frame.winfo_children()[0]
        else: # librarian
            tree = self.librarian_book_tree_frame.winfo_children()[0]
        
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một cuốn sách để xóa.", parent=parent_window)
            return

        book_id_to_delete = tree.item(selected_item, 'values')[0]

        if messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc chắn muốn xóa sách ID {book_id_to_delete} không?", parent=parent_window):
            # Gọi hàm từ DatabaseManager để xóa sách
            success, message = self.db.delete_book(book_id_to_delete, user_role, librarian_id)
            if success:
                messagebox.showinfo("Thành công", message, parent=parent_window)
                if user_role == "admin":
                    # Cập nhật lại Treeview của admin, hiển thị cả cột "Số lượng ban đầu"
                    self.display_books_in_treeview(self.admin_book_tree_frame, for_admin=True)
                else:
                    self.display_books_in_treeview(self.librarian_book_tree_frame, for_admin=False, librarian_id=librarian_id)
            else:
                messagebox.showerror("Lỗi", message, parent=parent_window)
        parent_window.grab_release()

    def display_books_in_treeview(self, parent_frame, for_admin=True, librarian_id=None):
        for widget in parent_frame.winfo_children():
            widget.destroy()
        
        # Thêm cột "Số lượng ban đầu" nếu là admin
        columns = ("ID", "Tên sách", "Năm XB", "Tác giả", "Số lượng", "Chủ đề")
        if for_admin:
            columns = ("ID", "Tên sách", "Năm XB", "Tác giả", "Số lượng", "Số lượng ban đầu", "Chủ đề")
            columns += ("Thủ thư thêm",)

        tree = ttk.Treeview(parent_frame, columns=columns, show="headings", style='Treeview')
        tree.heading("ID", text="ID Sách", anchor=tk.W)
        tree.heading("Tên sách", text="Tên sách", anchor=tk.W)
        tree.heading("Năm XB", text="Năm XB", anchor=tk.W)
        tree.heading("Tác giả", text="Tác giả", anchor=tk.W)
        tree.heading("Số lượng", text="Số lượng hiện tại", anchor=tk.W) # Đổi tên cho rõ nghĩa
        
        if for_admin: # Chỉ hiển thị cột này cho admin
            tree.heading("Số lượng ban đầu", text="Số lượng ban đầu", anchor=tk.W)

        tree.heading("Chủ đề", text="Chủ đề", anchor=tk.W)
        if for_admin:
            tree.heading("Thủ thư thêm", text="Thủ thư thêm", anchor=tk.W)
        
        tree.column("ID", width=70, anchor=tk.CENTER)
        tree.column("Tên sách", width=150, anchor=tk.W)
        tree.column("Năm XB", width=70, anchor=tk.CENTER)
        tree.column("Tác giả", width=100, anchor=tk.W)
        tree.column("Số lượng", width=80, anchor=tk.CENTER) # Cần đủ rộng cho 2 cột số lượng
        
        if for_admin:
            tree.column("Số lượng ban đầu", width=80, anchor=tk.CENTER) # Cần đủ rộng

        tree.column("Chủ đề", width=100, anchor=tk.W)
        if for_admin:
            tree.column("Thủ thư thêm", width=100, anchor=tk.CENTER)

        # Lấy dữ liệu từ DatabaseManager
        all_books_df = self.db.get_all_books()
        display_df = all_books_df
        if not for_admin and librarian_id:
            display_df = all_books_df[all_books_df['ID Thủ thư thêm'] == librarian_id]

        for index, row in display_df.iterrows():
            values = (row['ID Sách'], row['Tên sách'], row['Năm xuất bản'], row['Tác giả'], row['Số lượng'])
            if for_admin:
                values += (row['Số lượng ban đầu'],) # Thêm số lượng ban đầu vào đây
            values += (row['Chủ đề'],)
            if for_admin:
                values += (row['ID Thủ thư thêm'],)
            tree.insert("", "end", values=values)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        tree.configure(yscrollcommand=scrollbar.set)

    def manage_book_topics(self):
        top = tk.Toplevel(self.master)
        top.title("Quản lý Chủ đề Sách")
        top.geometry("450x450")
        top.transient(self.master)
        top.grab_set()

        frame = ttk.Frame(top, padding="20", style='TFrame')
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="QUẢN LÝ CHỦ ĐỀ SÁCH", font=("Segoe UI", 16, "bold"), foreground='#007acc').pack(pady=15)

        ttk.Label(frame, text="Chủ đề hiện có:", font=("Segoe UI", 12)).pack(pady=5)
        
        topic_listbox_frame = ttk.Frame(frame, style='TFrame')
        topic_listbox_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.topic_listbox = tk.Listbox(topic_listbox_frame, width=40, height=8, font=("Segoe UI", 12), selectmode=tk.SINGLE, bd=0, highlightthickness=0, relief='flat')
        self.topic_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        listbox_scrollbar = ttk.Scrollbar(topic_listbox_frame, orient="vertical", command=self.topic_listbox.yview)
        listbox_scrollbar.pack(side=tk.RIGHT, fill="y")
        self.topic_listbox.config(yscrollcommand=listbox_scrollbar.set)
        
        self.refresh_topic_listbox()

        ttk.Label(frame, text="Thêm chủ đề mới:", font=("Segoe UI", 12)).pack(pady=5)
        new_topic_entry = ttk.Entry(frame, font=("Segoe UI", 12), width=35)
        new_topic_entry.pack(pady=5)

        def add_new_topic():
            new_topic = new_topic_entry.get().strip()
            if new_topic:
                all_topics = self.db.get_book_topics()
                if new_topic.lower() not in [t.lower() for t in all_topics]:
                    # In this simple model, topics are implicitly created when a book with a new topic is added.
                    # We are simulating a "check" for existing topics here.
                    messagebox.showinfo("Thông báo", f"Chủ đề '{new_topic}' đã sẵn sàng để sử dụng khi thêm sách.", parent=top)
                    new_topic_entry.delete(0, tk.END)
                    self.refresh_topic_listbox() # Refresh to reflect the potential new topic if user enters it
                else:
                    messagebox.showwarning("Cảnh báo", "Chủ đề này đã tồn tại (hoặc tương tự).", parent=top)
            else:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập chủ đề.", parent=top)

        def delete_selected_topic():
            try:
                selected_index = self.topic_listbox.curselection()[0]
                topic_to_delete = self.topic_listbox.get(selected_index)
                
                # Kiểm tra xem có sách nào đang dùng chủ đề này không thông qua DatabaseManager
                all_books_df = self.db.get_all_books()
                if topic_to_delete in all_books_df['Chủ đề'].values:
                    messagebox.showerror("Lỗi", f"Không thể xóa chủ đề '{topic_to_delete}' vì có sách đang sử dụng nó.", parent=top)
                else:
                    if messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc chắn muốn xóa chủ đề '{topic_to_delete}' không?", parent=top):
                        # Since topics are not stored in a separate table, deleting it here
                        # only removes it from the listbox's current display and has no DB impact.
                        # This part would require a separate 'topics' table in DB to be fully functional.
                        self.topic_listbox.delete(selected_index)
                        messagebox.showinfo("Thành công", f"Chủ đề '{topic_to_delete}' đã được xóa (nếu không có sách nào sử dụng).", parent=top)
            except IndexError:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn một chủ đề để xóa.", parent=top)

        ttk.Button(frame, text="Thêm Chủ đề", command=add_new_topic, style='TButton', width=15).pack(pady=5)
        ttk.Button(frame, text="Xóa Chủ đề đã chọn", command=delete_selected_topic, style='TButton', width=20).pack(pady=5)
        top.protocol("WM_DELETE_WINDOW", lambda: (self.master.grab_release(), top.destroy()))

    def refresh_topic_listbox(self):
        self.topic_listbox.delete(0, tk.END)
        # Lấy chủ đề từ DatabaseManager
        all_topics = self.db.get_book_topics()
        for topic in all_topics:
            self.topic_listbox.insert(tk.END, topic)


    # --- Giao diện Thủ thư ---
    def show_librarian_dashboard(self):
        self.clear_screen()
        main_frame = ttk.Frame(self.master, padding="20", style='TFrame')
        main_frame.pack(fill='both', expand=True)

        user_name = self.db.get_librarian_username(self.current_librarian_id)
        ttk.Label(main_frame, text=f"TRANG THỦ THƯ (Chào mừng, {user_name})", font=("Segoe UI", 24, "bold"), foreground='#007acc').pack(pady=20)

        button_frame = ttk.Frame(main_frame, style='TFrame')
        button_frame.pack(pady=20)

        ttk.Button(button_frame, text="Thêm Sách", command=lambda: self.add_book(self.master, "librarian", self.current_librarian_id), style='TButton', width=30).grid(row=0, column=0, padx=15, pady=10)
        ttk.Button(button_frame, text="Xóa Sách Của Tôi", command=lambda: self.delete_book(self.master, "librarian", self.current_librarian_id), style='TButton', width=30).grid(row=0, column=1, padx=15, pady=10)
        ttk.Button(button_frame, text="Xem Sách Đã Thêm", command=lambda: self.view_my_books(self.current_librarian_id), style='TButton', width=30).grid(row=1, column=0, padx=15, pady=10)
        ttk.Button(button_frame, text="Xem Sách Đang Được Mượn", command=self.view_borrowed_books_librarian, style='TButton', width=30).grid(row=1, column=1, padx=15, pady=10)
        # New button for librarians to confirm returns
        ttk.Button(button_frame, text="Xác nhận trả sách", command=self.view_pending_return_requests_librarian, style='TButton', width=30).grid(row=2, column=0, padx=15, pady=10)


        ttk.Button(main_frame, text="Đăng Xuất", command=self.create_login_screen, style='TButton', width=20).pack(pady=40)
    
    def view_my_books(self, librarian_id):
        top = tk.Toplevel(self.master)
        top.title("Sách do tôi thêm")
        top.geometry("900x600")
        top.transient(self.master)
        top.grab_set()

        frame = ttk.Frame(top, padding="20", style='TFrame')
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text=f"SÁCH DO THỦ THƯ {librarian_id} THÊM", font=("Segoe UI", 18, "bold"), foreground='#007acc').pack(pady=15)

        self.librarian_book_tree_frame = ttk.Frame(frame, style='TFrame')
        self.librarian_book_tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        # Truyền for_admin=False vì thủ thư không cần thấy cột "Số lượng ban đầu" của người khác
        self.display_books_in_treeview(self.librarian_book_tree_frame, for_admin=False, librarian_id=librarian_id)

        # Lấy dữ liệu từ DatabaseManager
        all_books_df = self.db.get_all_books()
        if all_books_df[all_books_df['ID Thủ thư thêm'] == librarian_id].empty:
            ttk.Label(frame, text="Bạn chưa thêm sách nào.", font=("Segoe UI", 12)).pack(pady=20)
            
        top.protocol("WM_DELETE_WINDOW", lambda: (self.master.grab_release(), top.destroy()))


    def view_borrowed_books_librarian(self):
        top = tk.Toplevel(self.master)
        top.title("Sách đang được mượn từ thư viện của tôi")
        top.geometry("1000x650")
        top.transient(self.master)
        top.grab_set()

        frame = ttk.Frame(top, padding="20", style='TFrame')
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text=f"SÁCH ĐANG ĐƯỢC MƯỢN (THỦ THƯ ID: {self.current_librarian_id})", font=("Segoe UI", 18, "bold"), foreground='#007acc').pack(pady=15)

        # Lấy dữ liệu từ DatabaseManager
        all_borrowed_df = self.db.get_all_borrowed_books()
        # Filter for books borrowed where this librarian is the 'ID Thủ thư' and status is 'Đang mượn'
        borrowed_from_me = all_borrowed_df[
            (all_borrowed_df['ID Thủ thư'] == self.current_librarian_id) &
            (all_borrowed_df['Trạng thái'] == 'Đang mượn')
        ]


        if borrowed_from_me.empty:
            ttk.Label(frame, text="Chưa có sách nào của bạn được người dùng mượn.", font=("Segoe UI", 12)).pack(pady=20)
            top.protocol("WM_DELETE_WINDOW", lambda: (self.master.grab_release(), top.destroy()))
            return
        
        borrowed_tree_frame = ttk.Frame(frame, style='TFrame')
        borrowed_tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        tree = ttk.Treeview(borrowed_tree_frame, columns=("ID Mượn", "ID Sách", "Tên sách", "ID Người dùng", "Tên người dùng", "Ngày mượn", "Trạng thái"), show="headings", style='Treeview')
        tree.heading("ID Mượn", text="ID Mượn", anchor=tk.W)
        tree.heading("ID Sách", text="ID Sách", anchor=tk.W)
        tree.heading("Tên sách", text="Tên sách", anchor=tk.W)
        tree.heading("ID Người dùng", text="ID Người dùng", anchor=tk.W)
        tree.heading("Tên người dùng", text="Tên người dùng", anchor=tk.W)
        tree.heading("Ngày mượn", text="Ngày mượn", anchor=tk.W)
        tree.heading("Trạng thái", text="Trạng thái", anchor=tk.W)


        tree.column("ID Mượn", width=80, anchor=tk.CENTER)
        tree.column("ID Sách", width=80, anchor=tk.CENTER)
        tree.column("Tên sách", width=180, anchor=tk.W)
        tree.column("ID Người dùng", width=100, anchor=tk.CENTER)
        tree.column("Tên người dùng", width=120, anchor=tk.W)
        tree.column("Ngày mượn", width=150, anchor=tk.CENTER)
        tree.column("Trạng thái", width=120, anchor=tk.CENTER)
        
        for index, row in borrowed_from_me.iterrows():
            tree.insert("", "end", values=(row['ID Mượn'], row['ID Sách'], row['Tên sách'], row['ID Người dùng'], row['Tên người dùng'], row['Ngày mượn'], row['Trạng thái']))
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(borrowed_tree_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        tree.configure(yscrollcommand=scrollbar.set)
        top.protocol("WM_DELETE_WINDOW", lambda: (self.master.grab_release(), top.destroy()))

    def view_pending_return_requests_librarian(self):
        top = tk.Toplevel(self.master)
        top.title("Yêu cầu trả sách đang chờ xác nhận")
        top.geometry("1000x650")
        top.transient(self.master)
        top.grab_set()

        frame = ttk.Frame(top, padding="20", style='TFrame')
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text=f"YÊU CẦU TRẢ SÁCH ĐANG CHỜ XÁC NHẬN (THỦ THƯ ID: {self.current_librarian_id})", font=("Segoe UI", 18, "bold"), foreground='#007acc').pack(pady=15)

        self.pending_returns_tree_frame = ttk.Frame(frame, style='TFrame')
        self.pending_returns_tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        self.display_pending_return_requests(self.pending_returns_tree_frame)

        button_frame = ttk.Frame(frame, style='TFrame')
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Xác nhận đã trả", command=lambda: self.confirm_book_return_action(self.pending_returns_tree_frame, top), style='TButton', width=20).pack(pady=10)

        top.protocol("WM_DELETE_WINDOW", lambda: (self.master.grab_release(), top.destroy()))

    def display_pending_return_requests(self, parent_frame):
        for widget in parent_frame.winfo_children():
            widget.destroy()

        tree = ttk.Treeview(parent_frame, columns=("ID Mượn", "ID Sách", "Tên sách", "ID Người dùng", "Tên người dùng", "Ngày mượn", "Trạng thái"), show="headings", style='Treeview')
        tree.heading("ID Mượn", text="ID Mượn", anchor=tk.W)
        tree.heading("ID Sách", text="ID Sách", anchor=tk.W)
        tree.heading("Tên sách", text="Tên sách", anchor=tk.W)
        tree.heading("ID Người dùng", text="ID Người dùng", anchor=tk.W)
        tree.heading("Tên người dùng", text="Tên người dùng", anchor=tk.W)
        tree.heading("Ngày mượn", text="Ngày mượn", anchor=tk.W)
        tree.heading("Trạng thái", text="Trạng thái", anchor=tk.W)

        tree.column("ID Mượn", width=80, anchor=tk.CENTER)
        tree.column("ID Sách", width=80, anchor=tk.CENTER)
        tree.column("Tên sách", width=180, anchor=tk.W)
        tree.column("ID Người dùng", width=100, anchor=tk.CENTER)
        tree.column("Tên người dùng", width=120, anchor=tk.W)
        tree.column("Ngày mượn", width=150, anchor=tk.CENTER)
        tree.column("Trạng thái", width=120, anchor=tk.CENTER)
        
        pending_requests_df = self.db.get_pending_return_requests(self.current_librarian_id)

        if pending_requests_df.empty:
            ttk.Label(parent_frame, text="Không có yêu cầu trả sách nào đang chờ xử lý.", font=("Segoe UI", 12)).pack(pady=20)
            return

        for index, row in pending_requests_df.iterrows():
            tree.insert("", "end", values=(row['ID Mượn'], row['ID Sách'], row['Tên sách'], row['ID Người dùng'], row['Tên người dùng'], row['Ngày mượn'], row['Trạng thái']))
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        tree.configure(yscrollcommand=scrollbar.set)

    def confirm_book_return_action(self, parent_tree_frame, parent_window):
        tree = parent_tree_frame.winfo_children()[0]
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một yêu cầu để xác nhận.", parent=parent_window)
            return
        
        item_values = tree.item(selected_item, 'values')
        borrow_id = item_values[0]
        book_id = item_values[1]
        book_title = item_values[2]
        user_name = item_values[4]

        if messagebox.askyesno("Xác nhận trả sách", f"Bạn có chắc chắn muốn xác nhận sách '{book_title}' của '{user_name}' đã được trả không?", parent=parent_window):
            # Update book quantity (+1)
            self.db.update_book_quantity(book_id, 1)
            # Update borrow record status to 'Đã trả'
            self.db.update_borrow_status(borrow_id, 'Đã trả')
            messagebox.showinfo("Thành công", f"Đã xác nhận trả sách '{book_title}' thành công.", parent=parent_window)
            self.display_pending_return_requests(self.pending_returns_tree_frame) # Refresh the list
        parent_window.grab_release()

    # --- Giao diện Người dùng ---
    def show_user_dashboard(self):
        self.clear_screen()
        main_frame = ttk.Frame(self.master, padding="20", style='TFrame')
        main_frame.pack(fill='both', expand=True)

        user_name = self.db.get_user_username(self.current_user_id)
        ttk.Label(main_frame, text=f"TRANG CHỦ NGƯỜI DÙNG (Chào mừng, {user_name})", font=("Segoe UI", 24, "bold"), foreground='#007acc').pack(pady=20)

        # Thanh tìm kiếm và bộ lọc
        control_frame = ttk.Frame(main_frame, style='TFrame')
        control_frame.pack(pady=15, fill=tk.X)

        search_label = ttk.Label(control_frame, text="Tìm kiếm sách:", font=("Segoe UI", 12))
        search_label.pack(side=tk.LEFT, padx=(0, 5))
        self.search_entry = ttk.Entry(control_frame, font=("Segoe UI", 12), width=35)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(control_frame, text="Tìm kiếm", command=self.search_books, style='TButton', width=10).pack(side=tk.LEFT, padx=(0, 20))

        filter_label = ttk.Label(control_frame, text="Lọc theo chủ đề:", font=("Segoe UI", 12))
        filter_label.pack(side=tk.LEFT, padx=(0, 5))
        
        # Lấy danh sách chủ đề từ DatabaseManager
        all_topics = ['Tất cả'] + self.db.get_book_topics()
        self.topic_filter_var = tk.StringVar(self.master)
        self.topic_filter_var.set(all_topics[0])
        
        self.topic_filter_menu = ttk.OptionMenu(control_frame, self.topic_filter_var, all_topics[0], *all_topics, command=self.filter_books_by_topic)
        self.topic_filter_menu.config(width=20)
        self.topic_filter_menu.pack(side=tk.LEFT, padx=(0, 10))

        self.book_display_frame = ttk.Frame(main_frame, style='TFrame')
        self.book_display_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        self.display_all_books_for_user()

        # New button for users to view their borrowed books and return
        ttk.Button(main_frame, text="Xem sách đang mượn và Trả sách", command=self.view_user_borrowed_books, style='TButton', width=35).pack(pady=10)

        ttk.Button(main_frame, text="Đăng Xuất", command=self.create_login_screen, style='TButton', width=20).pack(pady=30)
    
    def display_all_books_for_user(self):
        for widget in self.book_display_frame.winfo_children():
            widget.destroy()

        self.user_book_tree = ttk.Treeview(self.book_display_frame, columns=("ID", "Tên sách", "Năm XB", "Tác giả", "Số lượng", "Chủ đề"), show="headings", style='Treeview')
        self.user_book_tree.heading("ID", text="ID Sách", anchor=tk.W)
        self.user_book_tree.heading("Tên sách", text="Tên sách", anchor=tk.W)
        self.user_book_tree.heading("Năm XB", text="Năm XB", anchor=tk.W)
        self.user_book_tree.heading("Tác giả", text="Tác giả", anchor=tk.W)
        self.user_book_tree.heading("Số lượng", text="Số lượng", anchor=tk.W)
        self.user_book_tree.heading("Chủ đề", text="Chủ đề", anchor=tk.W)
        
        self.user_book_tree.column("ID", width=70, anchor=tk.CENTER)
        self.user_book_tree.column("Tên sách", width=180, anchor=tk.W)
        self.user_book_tree.column("Năm XB", width=80, anchor=tk.CENTER)
        self.user_book_tree.column("Tác giả", width=120, anchor=tk.W)
        self.user_book_tree.column("Số lượng", width=80, anchor=tk.CENTER)
        self.user_book_tree.column("Chủ đề", width=120, anchor=tk.W)

        # Lấy dữ liệu từ DatabaseManager
        all_books_df = self.db.get_all_books()
        for index, row in all_books_df.iterrows():
            self.user_book_tree.insert("", "end", values=(row['ID Sách'], row['Tên sách'], row['Năm xuất bản'], row['Tác giả'], row['Số lượng'], row['Chủ đề']))
        
        self.user_book_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(self.book_display_frame, orient="vertical", command=self.user_book_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.user_book_tree.configure(yscrollcommand=scrollbar.set)

        self.user_book_tree.bind("<Double-1>", self.borrow_book_popup)

    def search_books(self):
        query = self.search_entry.get().lower().strip()
        all_books_df = self.db.get_all_books() # Lấy tất cả sách từ DB
        filtered_df = all_books_df[
            all_books_df['Tên sách'].str.lower().str.contains(query, na=False) |
            all_books_df['Tác giả'].str.lower().str.contains(query, na=False) |
            all_books_df['Chủ đề'].str.lower().str.contains(query, na=False)
        ]
        self.update_user_book_treeview(filtered_df)

    def filter_books_by_topic(self, selected_topic):
        all_books_df = self.db.get_all_books() # Lấy tất cả sách từ DB
        if selected_topic == "Tất cả":
            filtered_df = all_books_df
        else:
            filtered_df = all_books_df[all_books_df['Chủ đề'] == selected_topic]
        self.update_user_book_treeview(filtered_df)

    def update_user_book_treeview(self, df):
        for item in self.user_book_tree.get_children():
            self.user_book_tree.delete(item)
        
        for index, row in df.iterrows():
            self.user_book_tree.insert("", "end", values=(row['ID Sách'], row['Tên sách'], row['Năm xuất bản'], row['Tác giả'], row['Số lượng'], row['Chủ đề']))

    def borrow_book_popup(self, event):
        selected_item = self.user_book_tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một cuốn sách để mượn.")
            return

        item_values = self.user_book_tree.item(selected_item, 'values')
        book_id = item_values[0]
        book_title = item_values[1]
        available_quantity = int(item_values[4])

        if available_quantity <= 0:
            messagebox.showwarning("Không có sẵn", "Sách này hiện đã hết.")
            return

        response = messagebox.askyesno("Mượn Sách", f"Bạn có muốn mượn sách '{book_title}' không?")
        if response:
            self.process_borrow_book(book_id, book_title)
            
    def view_all_borrow_records(self):
        top = tk.Toplevel(self.master)
        top.title("Lịch sử mượn/trả sách")
        top.geometry("1000x600")
        top.transient(self.master)
        top.grab_set()

        frame = ttk.Frame(top, padding="20", style='TFrame')
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="LỊCH SỬ MƯỢN/TRẢ SÁCH", font=("Segoe UI", 18, "bold"), foreground='#007acc').pack(pady=15)

        tree_frame = ttk.Frame(frame, style='TFrame')
        tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        tree = ttk.Treeview(tree_frame, columns=("ID Mượn", "ID Sách", "Tên sách", "ID Người dùng", "Tên người dùng", "ID Thủ thư", "Ngày mượn", "Trạng thái"), show="headings", style='Treeview')
        headings = [
            ("ID Mượn", 80), ("ID Sách", 80), ("Tên sách", 180),
            ("ID Người dùng", 100), ("Tên người dùng", 120),
            ("ID Thủ thư", 100), ("Ngày mượn", 150), ("Trạng thái", 120)
        ]

        for col, width in headings:
            tree.heading(col, text=col, anchor=tk.W)
            tree.column(col, width=width, anchor=tk.CENTER if "ID" in col or "Ngày" in col else tk.W)

        borrowed_df = self.db.get_all_borrowed_books()
        if borrowed_df.empty:
            ttk.Label(frame, text="Không có đơn mượn sách nào.", font=("Segoe UI", 12)).pack(pady=20)
        else:
            for _, row in borrowed_df.iterrows():
                tree.insert("", "end", values=(
                    row['ID Mượn'], row['ID Sách'], row['Tên sách'],
                    row['ID Người dùng'], row['Tên người dùng'],
                    row['ID Thủ thư'], row['Ngày mượn'], row['Trạng thái']
                ))

            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
            scrollbar.pack(side=tk.RIGHT, fill="y")
            tree.configure(yscrollcommand=scrollbar.set)

        top.protocol("WM_DELETE_WINDOW", lambda: (self.master.grab_release(), top.destroy()))


    def process_borrow_book(self, book_id, book_title):
        user_id = self.current_user_id
        user_name = self.db.get_user_username(user_id) # Lấy tên người dùng từ DB

        book_details = self.db.get_book_details(book_id) # Lấy chi tiết sách từ DB
        if not book_details:
            messagebox.showerror("Lỗi", "Sách không tồn tại.")
            return

        current_quantity = book_details['Số lượng']
        if current_quantity <= 0:
            messagebox.showwarning("Không có sẵn", "Sách này hiện đã hết.")
            return
        
        librarian_id_of_book = book_details['ID Thủ thư thêm']

        # Cập nhật số lượng sách thông qua DatabaseManager
        self.db.update_book_quantity(book_id, -1)

        # Thêm vào danh sách sách mượn thông qua DatabaseManager
        self.db.record_borrow(book_id, book_title, user_id, user_name, librarian_id_of_book)

        messagebox.showinfo("Mượn thành công", f"Bạn đã mượn sách '{book_title}' thành công.\n(Thông báo đã được gửi đến thủ thư liên quan).")
        self.display_all_books_for_user() # Refresh the main book list

    def view_user_borrowed_books(self):
        top = tk.Toplevel(self.master)
        top.title("Sách bạn đang mượn")
        top.geometry("900x600")
        top.transient(self.master)
        top.grab_set()

        frame = ttk.Frame(top, padding="20", style='TFrame')
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text=f"SÁCH BẠN ĐANG MƯỢN (ID Người dùng: {self.current_user_id})", font=("Segoe UI", 18, "bold"), foreground='#007acc').pack(pady=15)

        self.user_borrowed_tree_frame = ttk.Frame(frame, style='TFrame')
        self.user_borrowed_tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        self.display_user_borrowed_books_in_treeview(self.user_borrowed_tree_frame)

        button_frame = ttk.Frame(frame, style='TFrame')
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Yêu cầu trả sách", command=lambda: self.request_return_book_action(self.user_borrowed_tree_frame, top), style='TButton', width=20).pack(pady=10)

        top.protocol("WM_DELETE_WINDOW", lambda: (self.master.grab_release(), top.destroy()))

    def display_user_borrowed_books_in_treeview(self, parent_frame):
        for widget in parent_frame.winfo_children():
            widget.destroy()

        tree = ttk.Treeview(parent_frame, columns=("ID Mượn", "ID Sách", "Tên sách", "Ngày mượn", "Trạng thái"), show="headings", style='Treeview')
        tree.heading("ID Mượn", text="ID Mượn", anchor=tk.W)
        tree.heading("ID Sách", text="ID Sách", anchor=tk.W)
        tree.heading("Tên sách", text="Tên sách", anchor=tk.W)
        tree.heading("Ngày mượn", text="Ngày mượn", anchor=tk.W)
        tree.heading("Trạng thái", text="Trạng thái", anchor=tk.W)

        tree.column("ID Mượn", width=100, anchor=tk.CENTER)
        tree.column("ID Sách", width=100, anchor=tk.CENTER)
        tree.column("Tên sách", width=250, anchor=tk.W)
        tree.column("Ngày mượn", width=150, anchor=tk.CENTER)
        tree.column("Trạng thái", width=150, anchor=tk.CENTER)
        
        borrowed_books_df = self.db.get_borrowed_books_by_user(self.current_user_id)

        if borrowed_books_df.empty:
            ttk.Label(parent_frame, text="Bạn chưa mượn cuốn sách nào hoặc đã trả tất cả.", font=("Segoe UI", 12)).pack(pady=20)
            return

        for index, row in borrowed_books_df.iterrows():
            tree.insert("", "end", values=(row['ID Mượn'], row['ID Sách'], row['Tên sách'], row['Ngày mượn'], row['Trạng thái']))
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        tree.configure(yscrollcommand=scrollbar.set)

    def request_return_book_action(self, parent_tree_frame, parent_window):
        tree = parent_tree_frame.winfo_children()[0]
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một cuốn sách để yêu cầu trả.", parent=parent_window)
            return
        
        item_values = tree.item(selected_item, 'values')
        borrow_id = item_values[0]
        book_title = item_values[2]
        current_status = item_values[4]

        if current_status == 'Đang chờ xác nhận trả' or current_status == 'Đã trả':
            messagebox.showinfo("Thông báo", "Yêu cầu trả sách này đã được gửi hoặc sách đã được trả.", parent=parent_window)
            return

        if messagebox.askyesno("Yêu cầu trả sách", f"Bạn có muốn yêu cầu trả sách '{book_title}' không? Yêu cầu này sẽ được gửi đến thủ thư.", parent=parent_window):
            if self.db.update_borrow_status(borrow_id, 'Đang chờ xác nhận trả'):
                messagebox.showinfo("Thành công", f"Yêu cầu trả sách '{book_title}' đã được gửi đến thủ thư.", parent=parent_window)
                self.display_user_borrowed_books_in_treeview(self.user_borrowed_tree_frame) # Refresh the list
            else:
                messagebox.showerror("Lỗi", "Không thể gửi yêu cầu trả sách. Vui lòng thử lại.", parent=parent_window)
        parent_window.grab_release()

        
# --- Chạy ứng dụng ---
if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
    
    