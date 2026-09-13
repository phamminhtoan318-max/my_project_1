# 1. Base image Python chính thức (bản slim nhẹ và tối ưu dung lượng)
FROM python:3.11-slim

# 2. Ngăn Python tạo file .pyc và cho phép in log ra console ngay lập tức
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Đặt thư mục làm việc bên trong container
WORKDIR /app

# 4. Copy và cài đặt thư viện trước để tận dụng Docker cache layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy toàn bộ mã nguồn của project vào container
COPY . .

# 6. Lệnh chạy mặc định khi container được khởi chạy
CMD ["python", "main.py"]
