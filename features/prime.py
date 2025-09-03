import multiprocessing as mp
from multiprocessing import Pool
import time
import math

class PrimeCalculator:
    def __init__(self, num_workers, mode):
        self.num_workers = num_workers
        self.mode = mode

        # Set multiprocessing start method
        if mode == 'process':
            mp.set_start_method('spawn', force=True)

    def is_prime(self, n):
        """Check if a number is prime"""
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False

        # Check odd numbers up to square root
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        return True

    def find_primes_in_range(self, start, end):
        """Find all primes in a given range"""
        primes = []
        for num in range(start, end + 1):
            if self.is_prime(num):
                primes.append(num)
        return primes

    def calculate_primes(self):
        """Calculate prime numbers using multiprocessing"""
        print(f"Prime Calculator using {self.num_workers} workers with {self.mode}")

        # Calculate primes up to 100,000 for demonstration
        max_number = 100000
        chunk_size = max_number // self.num_workers

        # Create ranges for each worker
        ranges = []
        for i in range(self.num_workers):
            start = i * chunk_size + 1
            end = (i + 1) * chunk_size if i < self.num_workers - 1 else max_number
            ranges.append((start, end))

        print(f"Dividing work into {len(ranges)} chunks:")
        for i, (start, end) in enumerate(ranges):
            print(f"  Worker {i + 1}: {start} to {end}")

        start_time = time.time()

        with Pool(processes=self.num_workers) as pool:
            results = pool.starmap(self.find_primes_in_range, ranges)

        end_time = time.time()

        # Combine results
        all_primes = []
        for result in results:
            all_primes.extend(result)

        # Sort and display results
        all_primes.sort()

        print(f"\nCalculation completed in {end_time - start_time:.2f} seconds")
        print(f"Found {len(all_primes)} prime numbers up to {max_number}")

        # Display first and last few primes
        if all_primes:
            print(f"\nFirst 10 primes: {all_primes[:10]}")
            print(f"Last 10 primes: {all_primes[-10:]}")

            # Show some statistics
            print(f"\nPrime Statistics:")
            print(f"  Smallest prime: {min(all_primes)}")
            print(f"  Largest prime: {max(all_primes)}")
            print(f"  Average of first 100: {sum(all_primes[:100]) / 100:.2f}")

        return all_primes
