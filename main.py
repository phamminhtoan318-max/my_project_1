import os
from src.extract import extract_data
from src.transform import transform_data, data_validation, print_validation_report
from src.load import load_data

# Đường dẫn file dữ liệu
RAW_DATA_PATH = os.path.join('data', 'raw', 'raw_sales_dataset_100 (1).csv')
PROCESSED_DATA_PATH = os.path.join('data', 'processed', 'clean_sales_dataset.csv')

def main():
    print('==================== START ETL PIPELINE ====================')

    # 1. EXTRACT
    print('\n[1/3] Đang đọc dữ liệu đầu vào (EXTRACT)...')
    raw_data = extract_data(RAW_DATA_PATH)

    if not raw_data:
        print('[ERROR] Trích xuất dữ liệu thất bại! Dừng pipeline.')
        return

    print(f'✓ Đã trích xuất thành công {len(raw_data)} bản ghi.')

    # 2. TRANSFORM & VALIDATE
    print('\n[2/3] Đang làm sạch và kiểm tra dữ liệu (TRANSFORM)...')
    clean_data = transform_data(raw_data)

    errors = data_validation(clean_data)
    print_validation_report(clean_data, errors)

    # 3. LOAD
    print('\n[3/3] Đang lưu dữ liệu đã chuẩn hóa (LOAD)...')
    success = load_data(clean_data, PROCESSED_DATA_PATH)

    if success:
        print('✓ Lưu dữ liệu hoàn tất.')
    else:
        print('[ERROR] Lưu dữ liệu thất bại!')

    print('\n==================== PIPELINE COMPLETED ====================')

if __name__ == '__main__':
    main()