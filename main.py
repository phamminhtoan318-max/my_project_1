from src.extract import extract_data
from src.transform import transform_data
from src.load import load_data

def main():
    print('-------------------Start ELT pipeline-------------------')

    raw_data = extract_data(r'D:\code\my_project_1\data\raw\raw_sales_dataset_100 (1).csv')
    if not raw_data: 
        print("Falied to extract data")
    clean_data = transform_data(raw_data)
    


if __name__ == '__main__':
    main()