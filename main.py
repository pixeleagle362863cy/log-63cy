"""Simple log parsing helper.

Provides functions to parse lines of a log file
formatted as "[timestamp] [level] message".
"""

import re, sys, argparse

_LOG_RE = re.compile(r'\[(.*?)\]\s+\[(.*?)\]\s+(.*)')

def parse_line(line):
    """Parse a single log line.

    Returns dict {'timestamp': str, 'level': str, 'message': str}
    or None if the line does not match the expected format.
    """
    m = _LOG_RE.match(line.rstrip())
    if not m:
        return None
    return {'timestamp': m.group(1), 'level': m.group(2), 'message': m.group(3)}

def parse_log(fileobj, level=None):
    """Yield parsed log entries from fileobj.

    If level is given, only yield entries with that level.
    """
    for line in fileobj:
        entry = parse_line(line)
        if entry and (level is None or entry['level'].lower() == level.lower()):
            yield entry

def main():
    parser = argparse.ArgumentParser(description="Parse log file and filter by level.")
    parser.add_argument('logfile', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                        help="Path to log file (default: stdin)")
    parser.add_argument('-l', '--level', help="Filter by log level (case-insensitive)")
    args = parser.parse_args()

    for entry in parse_log(args.logfile, args.level):
        print(f"{entry['timestamp']} [{entry['level']}] {entry['message']}")

if __name__ == "__main__":
    main()