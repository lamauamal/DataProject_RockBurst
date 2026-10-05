""" 处理流程：
pdf -> MinerU API -> MinerU_json -> table_json -> ZHIPU API -> ZHIPU_json -> csv -> input.csv """
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from src.processor import MUjson, get_table_from_json, extract, clean

def main():
    MUjson() # pdf -> MinerU_json
    get_table_from_json() # MinerU_json -> table_json
    extract() # table_json -> ZHIPU_json
    cols = ['σθ', 'σc', 'σt', 'SCF', 'B1', 'B2', 'Wet', 'MR']
    clean(cols) # ZHIPU_json -> csv -> input.csv

if __name__ == '__main__':
    main()
