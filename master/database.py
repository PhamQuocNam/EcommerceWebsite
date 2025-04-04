import sqlite3

# Kết nối đến cơ sở dữ liệu
conn = sqlite3.connect('ecommerce.db')
cursor = conn.cursor()

# Kích hoạt hỗ trợ khóa ngoại
cursor.execute('PRAGMA foreign_keys = ON;')

# Tạo bảng User
cursor.execute('''
CREATE TABLE IF NOT EXISTS User (
    USER_ID INTEGER PRIMARY KEY,
    User_Name VARCHAR(50) NOT NULL,
    Password VARCHAR(50) NOT NULL,
    First_Name VARCHAR(50),
    Last_Name VARCHAR(50),
    Birthday DATETIME
)
''')

# Tạo bảng Staff
cursor.execute('''
CREATE TABLE IF NOT EXISTS Staff (
    STAFF_ID INTEGER PRIMARY KEY,
    USER_ID INTEGER,
    Datetime DATETIME,
    First_Name VARCHAR(50),
    Last_Name VARCHAR(50),
    Card VARCHAR(50),
    Started_Datetime DATETIME,
    Birthday DATETIME,
    Position VARCHAR(50),
    FOREIGN KEY (USER_ID) REFERENCES User(USER_ID)
)
''')

# Tạo bảng Wishlist
cursor.execute('''
CREATE TABLE IF NOT EXISTS Wishlist (
    ID INTEGER PRIMARY KEY,
    ID_User INTEGER,
    Card INTEGER,
    FOREIGN KEY (ID_User) REFERENCES User(USER_ID)
)
''')

# Tạo bảng Review
cursor.execute('''
CREATE TABLE IF NOT EXISTS Review (
    RV_ID INTEGER PRIMARY KEY,
    Product_ID INTEGER,
    ID_User INTEGER,
    Card INTEGER,
    Rating INTEGER,
    Comment TEXT,
    FOREIGN KEY (ID_User) REFERENCES User(USER_ID),
    FOREIGN KEY (Product_ID) REFERENCES Product(PRODUCT_ID)
)
''')

# Tạo bảng Discount
cursor.execute('''
CREATE TABLE IF NOT EXISTS Discount (
    DISCOUNT_ID INTEGER PRIMARY KEY,
    Name VARCHAR(50),
    Desc VARCHAR(255),
    Discount_Percent REAL,
    Active INTEGER
)
''')

# Tạo bảng Product_Category
cursor.execute('''
CREATE TABLE IF NOT EXISTS Product_Category (
    CATEGORY_ID INTEGER PRIMARY KEY,
    Name VARCHAR(50),
    Desc VARCHAR(255),
    Image VARCHAR(255),
    Discount_ID INTEGER,
    FOREIGN KEY (Discount_ID) REFERENCES Discount(DISCOUNT_ID)
)
''')

# Tạo bảng Product
cursor.execute('''
CREATE TABLE IF NOT EXISTS Product (
    PRODUCT_ID INTEGER PRIMARY KEY,
    Name VARCHAR(100),
    Desc VARCHAR(255),
    Price REAL,
    Image TEXT,
    Category_ID INTEGER,
    Discount_ID INTEGER,
    INVENTORY_ID INTEGER,
    FOREIGN KEY (Category_ID) REFERENCES Product_Category(CATEGORY_ID),
    FOREIGN KEY (Discount_ID) REFERENCES Discount(DISCOUNT_ID),
    FOREIGN KEY (INVENTORY_ID) REFERENCES Product_Inventory(INVENTORY_ID)
)
''')

# Tạo bảng Address
cursor.execute('''
CREATE TABLE IF NOT EXISTS Address (
    ADDRESS_ID INTEGER PRIMARY KEY,
    User_ID INTEGER,
    Address1 VARCHAR(100),
    Address2 VARCHAR(100),
    City VARCHAR(50),
    Country VARCHAR(50),
    Phone VARCHAR(20),
    FOREIGN KEY (User_ID) REFERENCES User(USER_ID)
)
''')

# Tạo bảng Payment
cursor.execute('''
CREATE TABLE IF NOT EXISTS Payment (
    PAYMENT_ID INTEGER PRIMARY KEY,
    Desc TEXT,
    Date DATETIME,
    Method TEXT,
    Money REAL
)
''')

# Tạo bảng Order_Detail
cursor.execute('''
CREATE TABLE IF NOT EXISTS Order_Detail (
    ORDETAIL_ID INTEGER PRIMARY KEY,
    CLIENT_ID INTEGER,
    PAYMENT_ID INTEGER,
    Total_Money REAL,
    Date DATETIME,
    Payment_Status INTEGER,
    Delivery_Status INTEGER,
    FOREIGN KEY (CLIENT_ID) REFERENCES User(USER_ID),
    FOREIGN KEY (PAYMENT_ID) REFERENCES Payment(PAYMENT_ID)
)
''')

# Tạo bảng Order_Item
cursor.execute('''
CREATE TABLE IF NOT EXISTS Order_Item (
    Product_ID INTEGER,
    Order_Detail_ID INTEGER,
    Quantity INTEGER,
    Note TEXT,
    PRIMARY KEY (Product_ID, Order_Detail_ID),
    FOREIGN KEY (Product_ID) REFERENCES Product(PRODUCT_ID),
    FOREIGN KEY (Order_Detail_ID) REFERENCES Order_Detail(ORDETAIL_ID)
)
''')

# Tạo bảng Salary
cursor.execute('''
CREATE TABLE IF NOT EXISTS Salary (
    STAFF_ID INTEGER PRIMARY KEY,
    Staff_Varchar TEXT,
    Date DATETIME,
    Salary REAL,
    Bonus REAL,
    FOREIGN KEY (STAFF_ID) REFERENCES Staff(STAFF_ID)
)
''')

# Tạo bảng Product_Inventory
cursor.execute('''
CREATE TABLE IF NOT EXISTS Product_Inventory (
    INVENTORY_ID INTEGER PRIMARY KEY,
    Quantity INTEGER,
    Created_at DATETIME,
    Modified_at DATETIME
)
''')

# Lưu các thay đổi và đóng kết nối
conn.commit()
conn.close()

print("Cơ sở dữ liệu đã được tạo thành công!")