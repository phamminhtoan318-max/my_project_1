import csv
import os

def load_data(data, output_path):

    if not data:
        print("[WARNING] Không có dữ liệu để lưu (data is empty).")
        return False

    try:
        dir_name = os.path.dirname(output_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

        fieldnames = list(data[0].keys())

        with open(output_path, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

        print(f"[SUCCESS] Đã lưu thành công {len(data)} dòng vào: {output_path}")
        return True

    except Exception as e:
        print(f"[ERROR] Lỗi khi lưu dữ liệu vào {output_path}: {e}")
        return False
