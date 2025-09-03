import argparse
import sys
from features.ingest import LogParser
from features.prime import PrimeCalculator


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

    parser.add_argument('feature', choices=['ingest', 'prime'],
                        help='Feature to run: ingest (log parsing) or prime (prime calculations)')
    parser.add_argument('--path', help='Path to log directory (for ingest feature)')
    parser.add_argument('--worker', type=int, default=2,
                        help='Number of workers (default: 2)')
    parser.add_argument('--mode', choices=['threading', 'process'], default='threading',
                        help='Execution mode: threading or process (default: threading)')

    args = parser.parse_args()

    if args.feature == 'ingest':
        if not args.path:
            print("Error: --path is required for ingest feature")
            sys.exit(1)

        log_parser = LogParser(args.path, args.worker, args.mode)
        results = log_parser.parse_logs()
        log_parser.display_results(results)

    elif args.feature == 'prime':
        prime_calc = PrimeCalculator(args.worker, args.mode)
        prime_calc.calculate_primes()

if __name__ == "__main__":
    main()
