import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from src.model import train_pre

def main():
    train_pre()

if __name__ == '__main__':
    main()