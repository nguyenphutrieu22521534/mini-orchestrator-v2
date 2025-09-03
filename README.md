# Mini Orchestrator v2

A lightweight Python application that demonstrates concurrent processing capabilities for two main features: log parsing and prime number calculations. This project showcases different approaches to parallel processing using threading and multiprocessing.

## Features

### 🔍 Log Parser (`ingest`)

- **Concurrent log file processing** using ThreadPoolExecutor
- **HTTP log analysis** with support for various log formats
- **Comprehensive statistics** including:
  - Request counts by HTTP method (GET, POST, PUT, DELETE)
  - Status code distribution (2xx, 3xx, 4xx, 5xx)
  - Latency analysis (min, max, average)
  - User agent frequency analysis
- **Multi-file support** - processes entire directories of `.log` files
- **Configurable worker threads** for optimal performance

### 🔢 Prime Calculator (`prime`)

- **Parallel prime number discovery** using multiprocessing
- **Efficient prime checking algorithm** with mathematical optimizations
- **Workload distribution** across multiple processes
- **Performance benchmarking** with execution time tracking
- **Comprehensive results** including prime statistics and ranges

## Project Structure

```
mini-orchestrator-v2/
├── main.py                 # Main entry point with CLI interface
├── features/
│   ├── __init__.py
│   ├── ingest.py          # Log parsing functionality
│   └── prime.py           # Prime calculation functionality
├── data/
│   └── log/               # Sample log files for testing
│       ├── sample1.log
│       ├── sample2.log
│       ├── sample3.log
│       └── sample4.log
└── README.md
```

### Log Parser Implementation

- Uses `ThreadPoolExecutor` for concurrent file processing
- Thread-safe statistics collection with locks
- Regular expression-based log line parsing
- Efficient memory usage with streaming file reading

### Prime Calculator Implementation

- Multiprocessing with `Pool` for parallel computation
- Mathematical optimizations (square root limit, even number skipping)
- Workload distribution across process boundaries
- Results aggregation and statistical analysis

## License

This project is open source and available under the MIT License.
