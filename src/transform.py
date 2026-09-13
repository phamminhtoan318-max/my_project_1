from datetime import datetime 
from dateutil import parser
import re 

invalid_tokens = {'', 'none', 'null', 'nan', 'n/a', 'na', 'unknown', 'undefined', '?'}

def is_invalid(val):
    if val is None:
        return True

    if isinstance(val, str):
        return val.strip().lower() in invalid_tokens

    return False 


def clean_string(val):
    if is_invalid(val):
        return None

    val = str(val)
    # Gom nhiều khoảng trắng, tab hoặc 
    # xuống dòng liên tiếp lại thành 1 dấu cách duy nhất.
    # Vd '  hello    world' -> 'hello world'
    val = re.sub(r'\s+', ' ', val) 
    
    return val.strip()


def clean_ma_don_hang(val):
    if not val:
        return None

    if is_invalid(val):
        return None

    val = str(val).strip().upper()

    # Giữ nguyên chữ A-Z và số 0-9, loại bỏ ký tự đặc biệt
    # Vd 'ORDER123' -> 'ORDER123'
    # Vd 'ORDER123##$$%' -> 'ORDER123'
    # Vd 'ORD_ER123_$' -> 'ORDER123'
    return re.sub(r'[^A-Z0-9]', '', val)

def clean_ten_khach_hang(raw_name, capitalize = True):
    if not raw_name:
        return 'Default customer'

    if is_invalid(raw_name): 
        return 'Default customer'

    text = str(raw_name)

    # Xóa số điện thoại
    text = re.sub(r'[\(\[\{]?\b\d{6,15}\b[\)\]\}]?', '', text)

    # Xóa các ký tự ngoặc 
    text = re.sub(r'[\(\)\[\]\{\}]', '', text) 

    # Chuẩn hóa khoảng trắng
    text = " ".join(text.split())  

    if not text:
        return 'Default customer'

    if capitalize:
        text = text.title()

    return text

def clean_category(val):
    if not val:
        return 'Default category'

    if is_invalid(val):
        return 'Default category'

    val = clean_string(val)
    
    return val.title() if val else 'Default category'

def clean_price(val):
    if not val:
        return None 
    
    if is_invalid(val):
        return None 
    
    val = str(val).strip()

    val = val.replace(',', '').replace('$', '')

    val = re.sub(r'[^0-9.]', '', val)

    try:
        price = float(val)
    except ValueError:
        return None

    if price <= 0:
        return None
    
    return round(price,2)
    
def clean_quantity(val):
    if not val:
        return 0
    
    if is_invalid(val):
        return 0 
    
    val = str(val).strip()

    val = re.sub(r'[^0-9-]', '', val)

    try:
        quantity = int(val)
    except ValueError:
        return 0
    
    if quantity <= 0:
        return 0
    
    return quantity

def clean_discount(val):

    if not val or is_invalid(val):
        return 0.0
    
    val = str(val).strip()

    try:
        if '%' in val:
            val = val.replace('%', '').strip()
            return round(float(val) / 100.0, 4)
        
        d = float(val)
        if d > 1.0:
            d = d / 100.0
        return round(d, 4)
    except ValueError:
        return 0.0

def clean_date(raw_date, dayfirst=True):
    if not raw_date:
        return None

    if is_invalid(raw_date):
        return None

    try:
        # 1. Đã là object datetime thì chỉ cần format
        if isinstance(raw_date, datetime):
            return raw_date.strftime('%Y-%m-%d')

        # 2. Xử lý trường hợp số (timestamp hoặc số 8 chữ số YYYYMMDD)
        if isinstance(raw_date, (int, float)):
            val = float(raw_date)
            # Nếu là timestamp mili-giây (13 chữ số) 
            if val > 1e11:
                val /= 1000
            # Nếu là timestamp giây bình thường (10 chữ số)
            if 1e8 <= val <= 3e9:
                return datetime.fromtimestamp(val).strftime('%Y-%m-%d')
            # Nếu là số dạng 20240510 (8 chữ số), để trôi xuống dưới xử lý như text

        date_string = str(raw_date).strip()

        # 3. Xử lý chuỗi số liền 8 ký tự (YYYYMMDD hoặc DDMMYYYY)
        if date_string.isdigit():
            # Timestamp 10 số (giây)
            if len(date_string) == 10:
                return datetime.fromtimestamp(int(date_string)).strftime('%Y-%m-%d')

            # Timestamp 13 số (mili-giây)
            if len(date_string) == 13:
                return datetime.fromtimestamp(int(date_string) / 1000).strftime('%Y-%m-%d')

            # Chuỗi 8 số dạng YYYYMMDD hoặc DDMMYYYY
            if len(date_string) == 8:
                fmt = "%d%m%Y" if dayfirst else "%Y%m%d"
                try:
                    return datetime.strptime(date_string, fmt).strftime('%Y-%m-%d')
                except ValueError:
                    return datetime.strptime(date_string, "%Y%m%d").strftime('%Y-%m-%d')

        # 4. Các định dạng chuỗi ngày thông thường (có fuzzy=True để lọc chữ thừa)
        dt = parser.parse(date_string, dayfirst=dayfirst, fuzzy=True)
        return dt.strftime('%Y-%m-%d')

    except (parser.ParserError, ValueError, TypeError, OSError, OverflowError): 
        return None

def clean_city(val):
    if not val:
        return 'Khac'
    
    if is_invalid(val):
        return 'Khac'
    
    val = clean_string(val) 
    
    return val.title() if val else 'Khac' 

def clean_is_member(val):
    if not val:
        return False
    
    if is_invalid(val):
        return False 
    
    val = str(val).strip().lower() 

    truthy = {'true', '1', '1.0', 'yes', 'y', 't'}
    falsy = {'false', '0', '0.0', 'no', 'n', 'f'}

    if val in truthy:
        return True
    elif val in falsy:
        return False 
    else:
        return False 

def clean_order_status(val):
    if not val or is_invalid(val):
        return 'Unknown' 

    val = clean_string(val)  
    return val.title() if val else 'Unknown' 

def calculate_net_revenue(price, quantity, discount_rate):
    if price is None:
        return None

    if quantity is None:
        return None

    if discount_rate is None:
        return None

    if price < 0:
        return None

    if quantity <= 0:
        return None

    if not 0 <= discount_rate <= 1:
        return None

    return round(
        price * quantity * (1 - discount_rate),
        2
    )
    
def split_date_time(date_value):
    default_res = {'day': None, 'month': None, 'quarter': None, 'year': None}
    
    if not date_value:
        return default_res
    
    try:
        if isinstance(date_value, datetime):
            date_time_obj = date_value
        else:
            date_time_obj = datetime.strptime(str(date_value).strip(), '%Y-%m-%d')

        return {
            'day': date_time_obj.day,
            'month': date_time_obj.month,
            'quarter': (date_time_obj.month - 1) // 3 + 1,
            'year': date_time_obj.year
        }
    except (ValueError, TypeError):
        return default_res
    

def transform_data(raw_data):
    
    if not raw_data:
        return []
    

    clean_data = []

    for row in raw_data:
        order_id = clean_ma_don_hang(
            row.get('order_id')
        )
        date_clean = clean_date(
            row.get('order_date')
        )
        date_parts = split_date_time(
            date_clean
        )
        price_clean    = clean_price(
            row.get('price')
        )
        quantity_clean = clean_quantity(
            row.get('quantity')
        )
        discount_clean = clean_discount(
            row.get('discount_rate')
        )
        net_revenue    = calculate_net_revenue(
            price_clean,
            quantity_clean,
            discount_clean
            )
        
        clean_row = {
        'order_id' : order_id,
        'customer_name' : clean_ten_khach_hang(
            row.get('customer_name')
        ),
        'category' : clean_category(
            row.get('category')
        ),
        'price' : price_clean,
        'quantity' : quantity_clean,
        'discount_rate' : discount_clean,
        'net_revenue': net_revenue,
        'order_date' : date_clean,
        'day': date_parts.get('day'),
        'month': date_parts.get('month'),
        'quarter': date_parts.get('quarter'),
        'year': date_parts.get('year'),
        'is_member' : clean_is_member(
            row.get('is_member')
        ),
        'city' : clean_city(
            row.get('city')
        ),
        'order_status' : clean_order_status(
            row.get('order_status')
        )
        }
        clean_data.append(clean_row)
    return clean_data


def data_validation(clean_data):
    error_list = []

    for i, row in enumerate(clean_data):
        row_errors = []

        if not row.get('order_id'):
            row_errors.append('order_id is missing')

        if row.get('price') is None:
            row_errors.append('price is missing')

        quantity = row.get('quantity')

        if quantity is None or quantity <= 0:
            row_errors.append(
                f'invalid quantity: {quantity}'
            )

        discount = row.get('discount_rate')

        if discount is None or not 0 <= discount <= 1:
            row_errors.append(
                f'invalid discount: {discount}'
            )

        if row.get('order_date') is None:
            row_errors.append('order_date is missing')

        if row.get('customer_name') == 'Default customer':
            row_errors.append('customer_name is default')

        if row.get('category') == 'Default category':
            row_errors.append('category is default')

        if row.get('order_status') == 'Unknown':
            row_errors.append('order_status is unknown')

        net_revenue = row.get('net_revenue')

        if net_revenue is None or net_revenue < 0:
            row_errors.append('net_revenue is invalid')

        if row_errors:
            error_list.append({
                'row_index': i,
                'order_id': row.get('order_id'),
                'errors': row_errors
            })

    return error_list

def print_validation_report(clean_data, error_list):

    error_counts = {}
    for entry in error_list:
        for err in entry['errors']:
            key = err.split(':')[0].strip()
            error_counts[key] = error_counts.get(key, 0) + 1

    total     = len(clean_data)
    total_err = len(error_list)
    total_ok  = total - total_err
    rate      = (total_ok / total * 100) if total else 0

    sep  = '=' * 55
    sep2 = '-' * 55

    print(sep)
    print('         DATA VALIDATION REPORT')
    print(sep)
    print(f'  Total rows       : {total}')
    print(f'  Passed           : {total_ok}  ({rate:.1f}%)')
    print(f'  Rows with issues : {total_err}  ({100 - rate:.1f}%)')
    print(sep)

    # Tóm tắt lỗi
    if error_counts:
        print('  ERROR SUMMARY:')
        print(sep2)
        for err_type, count in sorted(error_counts.items(), key=lambda x: -x[1]):
            bar = '█' * count
            print(f'    {err_type:<32} {count:>3}  {bar}')
        print(sep)

    if error_list:
        print('  DETAIL:')
        print(sep2)
        for entry in error_list:
            print(f"  [{entry['order_id']}] row {entry['row_index']}")
            for err in entry['errors']:
                print(f"      ✗ {err}")
        print(sep)
    else:
        print('  ✓ No issues found!')
        print(sep)

    