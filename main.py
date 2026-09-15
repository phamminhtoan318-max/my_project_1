import os
import sys
import logging
from src.extract import extract_data
from src.transform import transform_data, data_validation, print_validation_report
from src.load import load_data

# Đảm bảo thư mục logs tồn tại
os.makedirs(os.path.join('data', 'logs'), exist_ok=True)

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,  # Chỉ hiển thị mức INFO trở lên
    format='%(asctime)s [%(levelname)s] [%(name)s]: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(os.path.join('data', 'logs', 'etl_process.log'), encoding='utf-8'),
        logging.StreamHandler(sys.stdout)  # Hiển thị đồng bộ ra console
    ]
)

logger = logging.getLogger(__name__)

# Đường dẫn file dữ liệu
RAW_DATA_PATH = os.path.join('data', 'raw', 'raw_sales_dataset_100 (1).csv')
PROCESSED_DATA_PATH = os.path.join('data', 'processed', 'clean_sales_dataset.csv')

def main():
    logger.info('==================== START ETL PIPELINE ====================')

    # 1. EXTRACT
    logger.info('[1/3] Đang đọc dữ liệu đầu vào (EXTRACT)...')
    raw_data = extract_data(RAW_DATA_PATH)

    if not raw_data:
        logger.error('Trích xuất dữ liệu thất bại! Dừng pipeline.')
        return

    logger.info(f'✓ Đã trích xuất thành công {len(raw_data)} bản ghi.')

    # 2. TRANSFORM & VALIDATE
    logger.info('[2/3] Đang làm sạch và kiểm tra dữ liệu (TRANSFORM)...')
    clean_data = transform_data(raw_data)

    errors = data_validation(clean_data)
    print_validation_report(clean_data, errors)

    # 3. LOAD
    logger.info('[3/3] Đang lưu dữ liệu đã chuẩn hóa (LOAD)...')
    success = load_data(clean_data, PROCESSED_DATA_PATH)

    if success:
        logger.info('✓ Lưu dữ liệu hoàn tất.')
    else:
        logger.error('Lưu dữ liệu thất bại!')

    logger.info('==================== PIPELINE COMPLETED ====================')

if __name__ == '__main__':
    main()
