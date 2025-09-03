import os
import re
import threading
from collections import defaultdict, Counter
from concurrent.futures import ThreadPoolExecutor
import time


class LogParser:
    def __init__(self, log_path, num_workers, mode):
        self.log_path = log_path
        self.num_workers = num_workers
        self.mode = mode
        self.lock = threading.Lock()

        # Statistics containers
        self.total_requests = 0
        self.by_method = Counter()
        self.by_status_class = Counter()
        self.latency_ms = []
        self.user_agents = Counter()

    def parse_log_line(self, line):
        """Parse a single log line and extract information"""
        # Pattern: [METHOD] /path, status=CODE, time=TIMEms user-agent=AGENT
        pattern = r'\[(\w+)\]\s+([^,]+),\s+status=(\d+),\s+time=([\d.]+)ms\s+user-agent=(.+)'
        match = re.match(pattern, line.strip())

        if match:
            method, path, status, time_ms, user_agent = match.groups()

            with self.lock:
                self.total_requests += 1
                self.by_method[method] += 1

                # Status class (2xx, 3xx, 4xx, 5xx)
                status_class = f"{status[0]}xx"
                self.by_status_class[status_class] += 1

                self.latency_ms.append(float(time_ms))
                self.user_agents[user_agent] += 1

            return True
        return False

    def parse_file(self, file_path):
        """Parse a single log file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                self.parse_log_line(line)

    def parse_logs(self):
        """Parse all log files in the directory using threading"""
        if not os.path.exists(self.log_path):
            raise FileNotFoundError(f"Log path not found: {self.log_path}")

        if os.path.isfile(self.log_path):
            # Single file
            files_to_parse = [self.log_path]
        else:
            # Directory - find all .log files
            files_to_parse = []
            for file in os.listdir(self.log_path):
                if file.endswith('.log'):
                    files_to_parse.append(os.path.join(self.log_path, file))

        if not files_to_parse:
            print(f"No .log files found in {self.log_path}")
            return None

        print(f"Found {len(files_to_parse)} log files to parse")
        print(f"Using {self.num_workers} workers with {self.mode}")

        start_time = time.time()

        # Use ThreadPoolExecutor for concurrent parsing
        with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            executor.map(self.parse_file, files_to_parse)

        end_time = time.time()
        print(f"Parsing completed in {end_time - start_time:.2f} seconds")

        return self.get_results()

    def get_results(self):
        """Get parsed results"""
        return {
            'total_requests': self.total_requests,
            'by_method': dict(self.by_method),
            'by_status_class': dict(self.by_status_class),
            'latency_ms': {
                'count': len(self.latency_ms),
                'avg': sum(self.latency_ms) / len(self.latency_ms) if self.latency_ms else 0,
                'min': min(self.latency_ms) if self.latency_ms else 0,
                'max': max(self.latency_ms) if self.latency_ms else 0
            },
            'user_agents': dict(self.user_agents)
        }

    def display_results(self, results):
        """Display parsed results in a formatted way"""
        if not results:
            print("No results to display")
            return

        print("\n" + "=" * 50)
        print("LOG PARSING RESULTS")
        print("=" * 50)

        print(f"\nTotal Requests: {results['total_requests']}")

        print(f"\nBy Method:")
        for method, count in results['by_method'].items():
            print(f"  {method}: {count}")

        print(f"\nBy Status Class:")
        for status, count in results['by_status_class'].items():
            print(f"  {status}: {count}")

        latency = results['latency_ms']
        print(f"\nLatency (ms):")
        print(f"  Count: {latency['count']}")
        print(f"  Average: {latency['avg']:.2f}")
        print(f"  Min: {latency['min']:.2f}")
        print(f"  Max: {latency['max']:.2f}")

        print(f"\nTop User Agents:")
        sorted_agents = sorted(results['user_agents'].items(),
                               key=lambda x: x[1], reverse=True)[:5]
        for agent, count in sorted_agents:
            print(f"  {agent}: {count}")
