import pandas as pd
import os
import random
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        self.users_file = 'users.xlsx'
        self.librarians_file = 'librarians.xlsx'
        self.books_file = 'books.xlsx'
        self.borrowed_books_file = 'borrowed_books.xlsx'

        self.user_cols = ['ID Người dùng', 'Tên đăng nhập', 'Mật khẩu']
        self.librarian_cols = ['ID Thủ thư', 'Tên đăng nhập', 'Mật khẩu']

        self.book_cols = ['ID Sách', 'Tên sách', 'Năm xuất bản', 'Tác giả', 'Số lượng', 'Số lượng ban đầu', 'Chủ đề', 'ID Thủ thư thêm']
        self.borrowed_cols = ['ID Mượn', 'ID Sách', 'Tên sách', 'ID Người dùng', 'Tên người dùng', 'ID Thủ thư', 'Ngày mượn', 'Trạng thái']

        self.users_df = self._load_data(self.users_file, self.user_cols)
        self.librarians_df = self._load_data(self.librarians_file, self.librarian_cols)
        self.books_df = self._load_data(self.books_file, self.book_cols)
        self.borrowed_books_df = self._load_data(self.borrowed_books_file, self.borrowed_cols)

    def _load_data(self, filename, columns):
        if not os.path.exists(filename):
            df = pd.DataFrame(columns=columns)
            df.to_excel(filename, index=False)
            return df
        df = pd.read_excel(filename)
        for col in columns:
            if col not in df.columns:
                df[col] = pd.NA
        return df[columns]

    def _save_data(self, df, filename):
        """Lưu DataFrame vào file Excel."""
        df.to_excel(filename, index=False)
        print(f"Dữ liệu đã được lưu vào {filename}") 

    def _generate_unique_id(self, prefix, existing_ids):
        """Tạo ID duy nhất dựa trên tiền tố và danh sách ID hiện có."""
        while True:
            if prefix == "user":
                new_id_int = random.randint(1, 99999)
                new_id = f"{new_id_int:05d}"
                # Ensure new_id is not '00000' as it might be interpreted as non-existent
                if new_id_int == 0: 
                    continue
            elif prefix == "librarian":
                new_id_int = random.randint(90001, 99999)
                new_id = f"{new_id_int}"
            else: # For books, borrow records
                new_id_int = random.randint(100000, 999999)
                new_id = f"{new_id_int}"
            
            if new_id not in existing_ids:
                return new_id

    def get_all_users(self):
        return self.users_df

    def add_user(self, username, password):
        if username in self.users_df['Tên đăng nhập'].values:
            return None
        
        existing_user_ids = self.users_df['ID Người dùng'].astype(str).tolist()
        new_user_id = self._generate_unique_id("user", existing_user_ids)

        new_user = pd.DataFrame([{'ID Người dùng': new_user_id, 'Tên đăng nhập': username, 'Mật khẩu': password}])
        self.users_df = pd.concat([self.users_df, new_user], ignore_index=True)
        self._save_data(self.users_df, self.users_file)
        return new_user_id

    def delete_user(self, user_id):
        if user_id not in self.users_df['ID Người dùng'].values:
            return False # ID không tồn tại
        self.users_df = self.users_df[self.users_df['ID Người dùng'] != user_id]
        self._save_data(self.users_df, self.users_file)
        return True

    def authenticate_user(self, username, password):
        user_row = self.users_df[(self.users_df['Tên đăng nhập'] == username) & (self.users_df['Mật khẩu'] == password)]
        if not user_row.empty:
            return user_row.iloc[0]['ID Người dùng']
        return None
    
    def get_user_username(self, user_id):
        user_row = self.users_df[self.users_df['ID Người dùng'] == user_id]
        if not user_row.empty:
            return user_row.iloc[0]['Tên đăng nhập']
        return "Unknown"

    def get_all_librarians(self):
        return self.librarians_df

    def add_librarian(self, username, password):
        if username in self.librarians_df['Tên đăng nhập'].values:
            return None
        
        existing_librarian_ids = self.librarians_df['ID Thủ thư'].astype(str).tolist()
        new_librarian_id = self._generate_unique_id("librarian", existing_librarian_ids)

        new_librarian = pd.DataFrame([{'ID Thủ thư': new_librarian_id, 'Tên đăng nhập': username, 'Mật khẩu': password}])
        self.librarians_df = pd.concat([self.librarians_df, new_librarian], ignore_index=True)
        self._save_data(self.librarians_df, self.librarians_file)
        return new_librarian_id

    def delete_librarian(self, librarian_id):
        if librarian_id not in self.librarians_df['ID Thủ thư'].values:
            return False # ID không tồn tại
        self.librarians_df = self.librarians_df[self.librarians_df['ID Thủ thư'] != librarian_id]
        self._save_data(self.librarians_df, self.librarians_file)
        return True

    def authenticate_librarian(self, username, password):
        librarian_row = self.librarians_df[(self.librarians_df['Tên đăng nhập'] == username) & (self.librarians_df['Mật khẩu'] == password)]
        if not librarian_row.empty:
            return librarian_row.iloc[0]['ID Thủ thư']
        return None
    
    def get_librarian_username(self, librarian_id):
        librarian_row = self.librarians_df[self.librarians_df['ID Thủ thư'] == librarian_id]
        if not librarian_row.empty:
            return librarian_row.iloc[0]['Tên đăng nhập']
        return "Unknown"

    def get_all_books(self):
        return self.books_df

    def add_book(self, title, year, author, quantity, topic, added_by_librarian_id):
        existing_book_ids = self.books_df['ID Sách'].astype(str).tolist()
        new_book_id = self._generate_unique_id("book", existing_book_ids)

        new_book = pd.DataFrame([{
            'ID Sách': new_book_id, 
            'Tên sách': title, 
            'Năm xuất bản': year, 
            'Tác giả': author, 
            'Số lượng': quantity, 
            'Số lượng ban đầu': quantity,
            'Chủ đề': topic,
            'ID Thủ thư thêm': added_by_librarian_id
        }])
        self.books_df = pd.concat([self.books_df, new_book], ignore_index=True)
        self._save_data(self.books_df, self.books_file)
        return True

    def delete_book(self, book_id, user_role, current_librarian_id=None):
        book_to_delete = self.books_df[self.books_df['ID Sách'] == book_id]
        if book_to_delete.empty:
            return False, "Sách không tồn tại."
        
        if user_role == "librarian" and book_to_delete.iloc[0]['ID Thủ thư thêm'] != current_librarian_id:
            return False, "Bạn chỉ có thể xóa sách do mình thêm vào."
        
        self.books_df = self.books_df[self.books_df['ID Sách'] != book_id]
        self._save_data(self.books_df, self.books_file)
        return True, "Sách đã được xóa."

    def update_book_quantity(self, book_id, change):
        book_index = self.books_df[self.books_df['ID Sách'] == book_id].index
        if not book_index.empty:
            current_quantity = self.books_df.loc[book_index[0], 'Số lượng']
            self.books_df.loc[book_index[0], 'Số lượng'] = current_quantity + change
            self._save_data(self.books_df, self.books_file)
            return True
        return False

    def get_book_details(self, book_id):
        book_row = self.books_df[self.books_df['ID Sách'] == book_id]
        if not book_row.empty:
            return book_row.iloc[0].to_dict()
        return None

    def get_book_topics(self):
        return sorted(self.books_df['Chủ đề'].dropna().unique().tolist())

    def get_all_borrowed_books(self):
        return self.borrowed_books_df

    def record_borrow(self, book_id, book_title, user_id, user_name, librarian_id):
        existing_borrow_ids = self.borrowed_books_df['ID Mượn'].astype(str).tolist()
        new_borrow_id = self._generate_unique_id("borrow", existing_borrow_ids)
        
        borrow_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        new_borrow_record = pd.DataFrame([{
            'ID Mượn': new_borrow_id,
            'ID Sách': book_id,
            'Tên sách': book_title,
            'ID Người dùng': user_id,
            'Tên người dùng': user_name,
            'ID Thủ thư': librarian_id,
            'Ngày mượn': borrow_date,
            'Trạng thái': 'Đang mượn' 
        }])
        self.borrowed_books_df = pd.concat([self.borrowed_books_df, new_borrow_record], ignore_index=True)
        self._save_data(self.borrowed_books_df, self.borrowed_books_file)
        return True
    
    def get_borrowed_books_by_user(self, user_id):
        """Lấy danh sách sách mà một người dùng cụ thể đang mượn."""
        return self.borrowed_books_df[
            (self.borrowed_books_df['ID Người dùng'] == user_id) & 
            (self.borrowed_books_df['Trạng thái'].isin(['Đang mượn', 'Đang chờ xác nhận trả']))
        ]

    def update_borrow_status(self, borrow_id, new_status):
        """Cập nhật trạng thái của một bản ghi mượn sách."""
        borrow_index = self.borrowed_books_df[self.borrowed_books_df['ID Mượn'] == borrow_id].index
        if not borrow_index.empty:
            self.borrowed_books_df.loc[borrow_index[0], 'Trạng thái'] = new_status
            self._save_data(self.borrowed_books_df, self.borrowed_books_file)
            return True
        return False
    
    def get_pending_return_requests(self, librarian_id):
        """Lấy các yêu cầu trả sách đang chờ xử lý cho một thủ thư cụ thể."""
        return self.borrowed_books_df[
            (self.borrowed_books_df['ID Thủ thư'] == librarian_id) & 
            (self.borrowed_books_df['Trạng thái'] == 'Đang chờ xác nhận trả')
        ]

db_manager = DatabaseManager()

if __name__ == '__main__':
    dm = DatabaseManager()
    print("Users:")
    print(dm.get_all_users())
    print("\nLibrarians:")
    print(dm.get_all_librarians())
    print("\nBooks:")
    print(dm.get_all_books())
    print("\nBorrowed Books:")
    print(dm.get_all_borrowed_books())
    print("\nBook Topics:")
    print(dm.get_book_topics())