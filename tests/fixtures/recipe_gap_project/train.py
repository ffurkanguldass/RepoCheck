import argparse


def build_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument('--data-root', default='./data')
	parser.add_argument('--dry-run', action='store_true')
	return parser


def main():
	build_parser().parse_args()
	return 0


if __name__ == '__main__':
	raise SystemExit(main())
