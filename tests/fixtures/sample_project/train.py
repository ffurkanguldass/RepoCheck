import argparse
from pathlib import Path


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--data-root", default="/mnt/private/data")
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main():
    args = build_parser().parse_args()
    Path("outputs").mkdir(exist_ok=True)
    print(f"batch_size={args.batch_size}; data_root={args.data_root}; seed={args.seed}")
    if args.dry_run:
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
