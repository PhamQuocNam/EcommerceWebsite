<p align="center">
  <a href="https://www.uit.edu.vn/" title="Trường Đại học Công nghệ Thông tin">
    <img src="./assets/img1.png" alt="UIT - University of Information Technology">
  </a>
</p>

<h1 align="center"><b>NHẬP MÔN CÔNG NGHỆ PHẦN MỀM</b></h1>

---

## 👥 Nhóm thực hiện

| STT | MSSV     | Họ và tên         | Chức vụ     | GitHub                                                | Email                        |
|-----|----------|-------------------|-------------|--------------------------------------------------------|------------------------------|
| 1   | 23520984 | Phạm Quốc Nam     | Nhóm trưởng | [PhamQuocNam](https://github.com/PhamQuocNam)          | 23520984@gm.uit.edu.vn       |
| 2   | 23520958 | Trần Quang Minh   | Thành viên  | [MingNhayMua](https://github.com/MingNhayMua)          | 23520958@gm.uit.edu.vn       |
| 3   | 23520701 | Nguyễn Vũ Khang   | Thành viên  | [nguyenvukhanguit](https://github.com/nguyenvukhanguit)| 23520701@gm.uit.edu.vn       |

---

## 📘 Thông tin môn học

- **Tên môn học**: Nhập môn Công nghệ Phần mềm  
- **Mã môn học**: SE104  
- **Mã lớp**: SE104.P28  
- **Năm học**: Học kỳ 2 (2024–2025)  
- **Giảng viên**: Thầy Đỗ Văn Tiến

---

## 📝 Đồ án cuối kỳ

- **Đề tài**: Website quản lý bán hàng hóa thông minh

---

## 🏗️ Kiến trúc hệ thống

![architecture](https://github.com/user-attachments/assets/e09fae12-3945-4710-9f74-123b96ac8cb5)

---

## 🧩 Chức năng & Giao diện

### 1. Giao diện chính
![main_interface](https://github.com/user-attachments/assets/4184a053-e8b3-4f7f-87d8-83b4f9fd0383)

### 2. Đăng nhập
![login](https://github.com/user-attachments/assets/e318a12f-5cb1-4a01-a9d7-6025af0c3fae)

### 3. Đăng ký
![signup](https://github.com/user-attachments/assets/06148bea-b8d5-49f5-b51a-55f8db45f75b)

---

### 4. Trang chính sau đăng nhập

- **Khách hàng**  
  ![index_customer](https://github.com/user-attachments/assets/5045bfd3-410e-4630-920b-215a2bdd4818)

- **Nhân viên**  
  ![index_staff](https://github.com/user-attachments/assets/774e62b9-372d-4fbf-82e1-b1ea6b0dbed6)

- **Chủ doanh nghiệp**  
  ![index_seller](https://github.com/user-attachments/assets/a6237089-6263-4641-8892-447922b56d5c)

---

### 5. Quản lý đơn hàng

- **Thêm sản phẩm vào giỏ hàng**  
  ![cart](https://github.com/user-attachments/assets/a4b525af-4d70-422d-a0e2-4878b6b02b10)

- **Kiểm tra đơn hàng**  
  ![order](https://github.com/user-attachments/assets/7cf72c80-1093-480f-a976-327b9f7e1fcd)

---

### 6. Thông tin khách hàng

- **Thông tin cá nhân**  
  ![customer_info](https://github.com/user-attachments/assets/c46d45c0-11bd-402d-a3a3-86f2ce0cebd6)

- **Địa chỉ đặt hàng**  
  ![address](https://github.com/user-attachments/assets/4c5c5774-ff15-49d4-8200-46bc8cedf366)

- **Lịch sử đơn hàng**  
  ![order_history](https://github.com/user-attachments/assets/8c2363d6-c4d2-4944-85f9-e2965e1580a6)

- **Quản lý đơn hàng đã đặt**  
  ![order_tracking](https://github.com/user-attachments/assets/8045e294-4840-4063-8400-d1671a275f2a)

- **Hủy đơn hàng**  
  ![cancellation](https://github.com/user-attachments/assets/bfbcedb3-6f31-4041-b52e-abd8f265c053)

---

### 7. Quản lý dành cho nhân viên

- **Quản lý đơn hàng**  
  ![order_management](https://github.com/user-attachments/assets/91fcb22b-621f-4805-aae2-0a41a098ac76)

- **Quản lý hàng tồn kho**  
  ![inventory_management](https://github.com/user-attachments/assets/7645fd5d-8ae2-418f-a3a4-c5da5ac5e78f)

---

### 8. Quản lý dành cho chủ doanh nghiệp

- **Doanh thu**  
  ![revenue_management](https://github.com/user-attachments/assets/fbc7fe66-65c7-4f70-92a1-52f55010a446)

- **Nhân sự**  
  ![staff_management](https://github.com/user-attachments/assets/74821245-5540-43db-afc9-81d466ad62ea)

---

### 9. Wishlist  
![wishlist](https://github.com/user-attachments/assets/88046751-f328-4ab7-be8b-b834cd06a96f)

---

### 10. Chatbot  
![chatbot](https://github.com/user-attachments/assets/cdde5c34-925e-4c6a-b78c-e35d1543c70b)

---

## 🎯 Recommendation System

### 📊 Cơ chế tính điểm xếp hạng sản phẩm

Hệ thống đề xuất sử dụng công thức **Weighted Rating** để đánh giá độ phổ biến và chất lượng sản phẩm dựa trên số lượt đánh giá và điểm trung bình.

#### 📌 Công thức:

\[
WR = \left( \frac{v}{v + m} \right) \cdot R + \left( \frac{m}{v + m} \right) \cdot C
\]

Trong đó:

- **R**: Điểm đánh giá trung bình của sản phẩm  
- **v**: Số lượng lượt đánh giá của sản phẩm  
- **m**: Số lượng đánh giá tối thiểu để sản phẩm đủ điều kiện (ví dụ: phân vị thứ 80%)  
- **C**: Điểm đánh giá trung bình của toàn bộ sản phẩm

---
