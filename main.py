import argparse
import sys
from core.command_registry import registry
from features.ingest import LogParser
from features.prime import PrimeCalculator

@registry.add_argument_decorator('ingest', '--path', type=str, required=True, help='Path to log file')
@registry.add_argument_decorator('ingest', '--worker', type=int, default=2, help='Number of workers (default: 2)')
@registry.add_argument_decorator('ingest', '--mode', choices=['threading', 'process'], default='threading',
                     help='Execution mode: threading or process (default: threading)')
def run_ingest(args: argparse.Namespace) -> None:

    log_parser = LogParser(args.path, args.worker, args.mode)
    results = log_parser.parse_logs()
    log_parser.display_results(results)

@registry.register_decorator('prime', 'Prime calculations feature')
def run_prime(args: argparse.Namespace) -> None:
    prime_calc = PrimeCalculator(args.worker, args.mode)
    prime_calc.calculate_primes()

def main():
    registry.register('ingest', run_ingest, 'Log parsing feature')

    registry.add_argument('prime', '--worker', type=int, default=2, help='Number of workers (default: 2)')
    registry.add_argument('prime', '--mode', choices=['threading', 'process'], default='threading',
                     help='Execution mode: threading or process (default: threading)')

    parser = argparse.ArgumentParser(
        description="Mini Orchestrator - Log parsing and Prime calculations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest='command', required=True)

    for cmd_name, cmd_info in registry.commands.items():
        cmd_parser = subparsers.add_parser(cmd_name, help=cmd_info['help'])
        for arg_args, arg_kwargs in cmd_info['args']:
            cmd_parser.add_argument(*arg_args, **arg_kwargs)
        cmd_parser.set_defaults(func=cmd_info['func'])

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
