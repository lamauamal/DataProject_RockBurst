import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import dataget, train_pre

def main():
    try:
        dataget.main()
        
        train_pre.main()
        
    except Exception as e:
        print(f"出错: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()