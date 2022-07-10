import argparse


def parse_test_args():
    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument('--arg_one', help='H1')
    parser.add_argument('--arg_two', help='H2')
    parser.add_argument('--arg_three', action='store_true')

    return parser.parse_args()


def main(args):
    print(args.arg_one)
    print(args.arg_two)
    if args.arg_three:
        print('arg_three')


if __name__ == '__main__':
    main(parse_test_args())
