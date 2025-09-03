import argparse
import sys
from features.ingest import LogParser
from features.prime import PrimeCalculator


def run_ingest(args: argparse.Namespace) -> None:
    log_parser = LogParser(args.path, args.worker, args.mode)
    results = log_parser.parse_logs()
    log_parser.display_results(results)


def run_prime(args: argparse.Namespace) -> None:
    prime_calc = PrimeCalculator(args.worker, args.mode)
    prime_calc.calculate_primes()


def main():
    parser = argparse.ArgumentParser(
        description="Mini Orchestrator - Log parsing and Prime calculations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py ingest --path ./data/log --worker 4 --mode threading
  python main.py prime --worker 2 --mode process
        """
    )

    subparsers = parser.add_subparsers(dest='command')

    # Ingest subcommand
    ingest_parser = subparsers.add_parser(
        'ingest',
        help='Log parsing feature'
    )
    ingest_parser.add_argument('--path', required=True, help='Path to log directory')
    ingest_parser.add_argument('--worker', type=int, default=2, help='Number of workers (default: 2)')
    ingest_parser.add_argument('--mode', choices=['threading', 'process'], default='threading',
                               help='Execution mode: threading or process (default: threading)')
    ingest_parser.set_defaults(func=run_ingest)

    # Prime subcommand
    prime_parser = subparsers.add_parser(
        'prime',
        help='Prime calculations feature'
    )
    prime_parser.add_argument('--worker', type=int, default=2, help='Number of workers (default: 2)')
    prime_parser.add_argument('--mode', choices=['threading', 'process'], default='threading',
                              help='Execution mode: threading or process (default: threading)')
    prime_parser.set_defaults(func=run_prime)

    args = parser.parse_args()

    if not hasattr(args, 'func'):
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
