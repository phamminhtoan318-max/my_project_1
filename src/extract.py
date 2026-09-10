import csv 

def extract_data(raw_data):
    try:
        with open(raw_data, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            data = list(reader)
            return data
    except FileNotFoundError: 
        return None 
    except UnicodeDecodeError:
        return None 
    except csv.Error:
        return None 
    except Exception as e:
        return None 