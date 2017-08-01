from script_gui import sample
import sys

def main():
    if "--sample" in sys.argv:
        sample.main()


if __name__ == '__main__':
    main()
