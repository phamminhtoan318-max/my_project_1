# 🛒 Sales Data ETL Pipeline

Hệ thống xử lý, làm sạch và chuẩn hóa dữ liệu bán hàng tự động (**ETL - Extract, Transform, Load**) viết bằng **Python**, hỗ trợ container hóa toàn diện với **Docker**.

---

## 📌 Mục lục
- [Giới thiệu](#-giới-thiệu)
- [Cấu trúc dự án](#-cấu-trúc-dự-án)
- [Quy trình ETL](#-quy-trình-etl)
  - [1. Extract (Trích xuất)](#1-extract-trích-xuất)
  - [2. Transform & Validate (Làm sạch & Kiểm định)](#2-transform--validate-làm-sạch--kiểm-định)
  - [3. Load (Lưu trữ)](#3-load-lưu-trữ)
- [Hướng dẫn cài đặt & Chạy trực tiếp](#-hướng-dẫn-cài-đặt--chạy-trực-tiếp)
- [Chạy với Docker](#-chạy-với-docker)
- [Báo cáo Kiểm định Dữ liệu (Data Validation Report)](#-báo-cáo-kiểm-định-dữ-liệu)

---

## 📖 Giới thiệu

Trong thực tế, dữ liệu bán hàng thường gặp rất nhiều lỗi:
- Ký tự đặc biệt, định dạng ngày tháng không nhất quán (`YYYY-MM-DD`, `DD/MM/YYYY`, timestamp giây/mili-giây).
- Tỷ lệ giảm giá lẫn lộn giữa số thập phân (`0.12`) và phần trăm (`15%`).
- Giá tiền chứa ký tự tiền tệ (`$`, dấu phẩy nghìn `,`).
- Dữ liệu bị rỗng, `null`, `nan`, `N/A`, số lượng âm hoặc bằng 0.

Dự án này xây dựng một luồng pipeline tự động hóa hoàn toàn việc trích xuất, làm sạch, tính toán doanh thu thực tế và kiểm tra chất lượng dữ liệu trước khi lưu vào kho dữ liệu sạch.

---

## 📂 Cấu trúc dự án

```text
my_project_1/
│
├── data/
│   ├── raw/                  # Dữ liệu thô ban đầu (CSV)
│   └── processed/            # Dữ liệu sau khi làm sạch (CSV)
│
├── src/
│   ├── __init__.py
│   ├── extract.py            # Trích xuất dữ liệu từ nguồn file
│   ├── transform.py          # Logic làm sạch, chuẩn hóa & validation
│   └── load.py               # Lưu dữ liệu sạch ra đích đến
│
├── .dockerignore             # Cấu hình bỏ qua file thừa khi build Docker
├── Dockerfile                # File cấu hình container hóa ứng dụng
├── main.py                   # Điểm khởi chạy chính điều phối luồng ETL
├── requirements.txt          # Danh sách thư viện phụ thuộc
└── README.md                 # Tài liệu hướng dẫn dự án
```

---

## ⚙️ Quy trình ETL

### 1. Extract (Trích xuất)
- Đọc file CSV đầu vào từ thư mục `data/raw/` bằng encoding UTF-8.
- Chuyển đổi dữ liệu thành danh sách các dictionary chuẩn hóa.

### 2. Transform & Validate (Làm sạch & Kiểm định)
- **Mã đơn hàng (`order_id`)**: Chuẩn hóa chữ in hoa, loại bỏ ký tự lạ, giữ lại chữ và số.
- **Tên khách hàng (`customer_name`)**: Xóa số điện thoại thừa, bỏ ngoặc, chuẩn hóa khoảng trắng và viết hoa từng từ (`Title Case`).
- **Danh mục (`category`)**: Chuẩn hóa chữ, điền giá trị mặc định nếu rỗng.
- **Giá bán (`price`)**: Xóa ký hiệu tiền tệ (`$`, `,`), ép kiểu số thực (`float`), loại bỏ giá trị âm.
- **Số lượng (`quantity`)**: Ép kiểu số nguyên (`int`), lọc bỏ số lượng <= 0.
- **Tỷ lệ chiết khấu (`discount_rate`)**: Nhận diện thông minh cả dạng `%` (ví dụ `15%`) và dạng số thập phân (`0.1`, `0.2`), chuẩn hóa về khoảng `[0.0, 1.0]`.
- **Doanh thu thuần (`net_revenue`)**: Tính toán theo công thức:
  $$\text{net\_revenue} = \text{price} \times \text{quantity} \times (1 - \text{discount\_rate})$$
- **Ngày đặt hàng (`order_date`)**: Nhận diện đa định dạng (chuỗi ISO, DD/MM/YYYY, timestamp 10 chữ số hoặc 13 chữ số) đưa về định dạng chuẩn `YYYY-MM-DD`.
- **Bóc tách thời gian**: Tách riêng `day`, `month`, `quarter`, `year` phục vụ phân tích nghiệp vụ.
- **Trạng thái & Thành viên**: Chuẩn hóa `is_member` (`True`/`False`), thành phố (`city`) và trạng thái đơn hàng (`order_status`).
- **Kiểm định chất lượng (`data_validation`)**: Quét và báo cáo tất cả các dòng dữ liệu không đạt chuẩn.

### 3. Load (Lưu trữ)
- Xuất dữ liệu đã làm sạch vào `data/processed/clean_sales_dataset.csv`.
- Tự động tạo thư mục đích nếu chưa tồn tại.

---

## 💻 Hướng dẫn cài đặt & Chạy trực tiếp

### Yêu cầu
- **Python** 3.10 trở lên.

### Các bước thực hiện:

1. **Clone dự án hoặc mở thư mục dự án:**
   ```bash
   cd d:/code/my_project_1
   ```

2. **Tạo và kích hoạt môi trường ảo (Khuyến nghị):**
   ```bash
   # Tạo môi trường ảo
   python -m venv .venv

   # Kích hoạt trên Windows (Git Bash):
   source .venv/Scripts/activate

   # Hoặc kích hoạt trên PowerShell:
   .venv\Scripts\Activate.ps1
   ```

3. **Cài đặt thư viện phụ thuộc:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Chạy pipeline ETL:**
   ```bash
   python main.py
   ```

---

## 🐳 Chạy với Docker

Dự án đã được cấu hình sẵn **Dockerfile** (sử dụng base image `python:3.11-slim` nhẹ và tối ưu).

### 1. Build Docker Image
```bash
docker build -t etl-sales-pipeline .
```

### 2. Chạy Container
- **Chạy thông thường:**
  ```bash
  docker run --rm etl-sales-pipeline
  ```

- **Chạy và lưu file kết quả trực tiếp ra máy host (Mount Volume):**
  - *Trên Git Bash:*
    ```bash
    docker run --rm -v "${PWD}/data/processed:/app/data/processed" etl-sales-pipeline
    ```
  - *Trên PowerShell:*
    ```powershell
    docker run --rm -v ${PWD}/data/processed:/app/data/processed etl-sales-pipeline
    ```

---

## 📊 Báo cáo Kiểm định Dữ liệu

Khi chạy pipeline, hệ thống sẽ tự động in ra bảng báo cáo kiểm định chất lượng:

```text
=======================================================
         DATA VALIDATION REPORT
=======================================================
  Total rows       : 100
  Passed           : 77  (77.0%)
  Rows with issues : 23  (23.0%)
=======================================================
  ERROR SUMMARY:
-------------------------------------------------------
    net_revenue is invalid            10  ██████████
    invalid quantity                   7  ███████
    category is default                5  █████
    customer_name is default           4  ████
    price is missing                   3  ███
    order_status is unknown            2  ██
    order_date is missing              2  ██
=======================================================
```
File dữ liệu hoàn chỉnh sẽ được lưu tại: `data/processed/clean_sales_dataset.csv`.
