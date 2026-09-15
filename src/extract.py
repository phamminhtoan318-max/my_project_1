import csv
import logging

logger = logging.getLogger(__name__)

def extract_data(raw_data):
    logger.info(f"Bắt đầu đọc dữ liệu từ: {raw_data}")
    try:
        with open(raw_data, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            data = list(reader)
            logger.info(f"Đọc dữ liệu thành công: {len(data)} bản ghi từ {raw_data}")
            return data
    except FileNotFoundError: 
        logger.error(f"Không tìm thấy file nguồn: {raw_data}")
        return None 
    except UnicodeDecodeError as e:
        logger.error(f"Lỗi bảng mã font (encoding) khi đọc {raw_data}: {e}")
        return None 
    except csv.Error as e:
        logger.error(f"Lỗi định dạng CSV khi đọc {raw_data}: {e}")
        return None 
    except Exception as e:
        logger.error(f"Lỗi không xác định khi trích xuất dữ liệu từ {raw_data}: {e}")
        return None 