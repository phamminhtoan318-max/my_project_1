from datetime import datetime 
from dateutil import parser
import re 

invalid_tokens = {'', 'none', 'null', 'nan', 'n/a', 'na', 'unknown', 'undefined', '?'}

def is_invalid(val):
    if not val:
        return True

    return str(val).strip().lower() in invalid_tokens 

def clean_ma_don_hang(val):
    if not val:
        return None

    if is_invalid(val):
        return None

    val = str(val).strip().upper()

    return re.sub(r'[^A-Z0-9]', '', val)

def clean_ten_khach_hang(val):
    if not val:
        return 'Default customer'

    if is_invalid(val):
        return 'Default customer'

    val = re.sub(r'[^\w\s]|\d+', '', val, flags=re.UNICODE)
    val = re.sub(r'\s+', ' ', val)

    val = str(val).strip().lower()
    if not val:
        return 'Default customer' 

    return val.title()

def clean_category(val):
    if not val:
        return 'Default category'

    if is_invalid(val):
        return 'Default category'

    val = str(val).strip().lower()
    val = re.sub(r'[^a-z0-9 &]', '', val) 
    val = re.sub(r'\s+', ' ', val).strip()
    
    return val.title() if val else 'Default category'

def clean_price(val):
    if not val:
        return None 
    
    if is_invalid(val):
        return None 
    
    val = str(val).strip()

    val = val.replace(',', '').replace('$', '').replace('%', '')

    val = re.sub(r'[^0-9.]', '', val)

    try:
        price = float(val)
        price = round(price,2)
        if price <= 0:
            return None
        return price
    except ValueError:
        return None 
    
def clean_quantity(val):
    if not val:
        return 0
    
    if is_invalid(val):
        return 0 
    
    val = str(val).strip()

    val = re.sub(r'[^0-9-]', '', val)

    try:
        quantity = int(val)
        if quantity <= 0:
            return 0
        return quantity
    except ValueError:
        return 0

def clean_discount(val):

    if not val:
        return 0.0
    
    if is_invalid(val):
        return 0.0 
    
    val = str(val).strip()

    val = re.sub(r'[^0-9]', '', val)

    try:
        return float(val) / 100.0
    except ValueError:
        return 0.0

def clean_date(val, dayfirst=True):
    if not val:
        return None

    if is_invalid(val):
        return None

    if isinstance(val, (int, float)):
        return datetime.fromtimestamp(val).strftime('%Y-%m-%d')

    val = str(val).strip()

    if val.isdigit() and len(val) == 10:
        return datetime.fromtimestamp(int(val)).strftime('%Y-%m-%d')

    try:
        return parser.parse(val, dayfirst=dayfirst).strftime('%Y-%m-%d')
    except (parser.ParserError, ValueError, TypeError):
        return None

def clean_city(val):
    if not val:
        return 'Khac'
    
    if is_invalid(val):
        return 'Khac'
    
    val = str(val).strip().lower()
    val = re.sub(r'[^a-z ]', '', val) 
    val = re.sub(r'\s+', ' ', val).strip()
    
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
    if not val:
        return 'Unknown'
    
    if is_invalid(val):
        return 'Unknown' 

    val = str(val).strip().lower() 
    val = re.sub(r'[^a-z]', '', val) 
    status = val.title()
    if status in ['Completed', 'Pending', 'Refunded', 'Cancelled']:
        return status 
    else: 
        return 'Unknown' 

def calculate_net_revenue(price, quantity, discount_rate):
    if not price or not quantity or discount_rate is None:
        return None 
    if discount_rate < 0 or discount_rate > 1:
        return None 
    if price < 0 or quantity < 0:
        return None
    return (price * quantity) * (1 - discount_rate)
    
def split_date_time(date_str):
    if not date_str:
        return {
            'day': None,
            'month': None,
            'quarter': None,
            'year': None
        }
    
    try:
        date_time_obj = datetime.strptime(date_str, '%Y-%m-%d')

        return {
            'day': date_time_obj.day,
            'month': date_time_obj.month,
            'quarter': (date_time_obj.month - 1) // 3 + 1,
            'year': date_time_obj.year
        }
    except (ValueError, TypeError):
        return {
            'day': None,
            'month': None,
            'quarter': None,
            'year': None
        }
    

def transform_data(raw_data):
    
    if not raw_data:
        return []
    

    clean_data = []
    seen_order_ids = set()
    for i, row in enumerate(raw_data):
        order_id = clean_ma_don_hang(row.get('order_id'))

        seen_order_ids.add(order_id)
        date_clean = clean_date(row.get('order_date'))
        date_parts = split_date_time(date_clean)
        price_clean    = clean_price(row.get('price'))
        quantity_clean = clean_quantity(row.get('quantity'))
        discount_clean = clean_discount(row.get('discount_rate'))
        net_revenue    = calculate_net_revenue(price_clean, quantity_clean, discount_clean)
        
        clean_row = {
        'order_id' : order_id,
        'customer_name' : clean_ten_khach_hang(row.get('customer_name')),
        'category' : clean_category(row.get('category')),
        'price' : price_clean,
        'quantity' : quantity_clean,
        'discount_rate' : discount_clean,
        'net_revenue': net_revenue,
        'order_date' : date_clean,
        'day': date_parts.get('day'),
        'month': date_parts.get('month'),
        'quarter': date_parts.get('quarter'),
        'year': date_parts.get('year'),
        'is_member' : clean_is_member(row.get('is_member')),
        'city' : clean_city(row.get('city')),
        'order_status' : clean_order_status(row.get('order_status'))
        }
        clean_data.append(clean_row)
    return clean_data


def data_validation(clean_data):
    error_list = []

    for i, row in enumerate(clean_data):
        row_errors = []

    
        if row.get('price') is None:
            row_errors.append('price is missing')

        
        if row.get('quantity') is None or row.get('quantity') <= 0:
            row_errors.append(f"invalid quantity: {row.get('quantity')}")

        
        discount = row.get('discount_rate')
        if discount is not None and (discount < 0 or discount > 1):
            row_errors.append(f"discount out of range: {discount}")

        
        if row.get('order_date') is None:
            row_errors.append('order_date is missing')

        
        if row.get('customer_name') == 'Default customer':
            row_errors.append('customer_name is default')

        
        if row.get('category') == 'Default category':
            row_errors.append('category is default')

        
        if row.get('order_status') == 'Unknown':
            row_errors.append('order_status is unknown')

        if row.get('net_revenue') is None or row.get('net_revenue') < 0:
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

    # Chi tiết từng dòng lỗi
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

    