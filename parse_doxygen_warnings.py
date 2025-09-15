#!/usr/bin/env python3
import argparse, csv, os, re, sys

# Match: file:line: kind: message
PATTERN = re.compile(r'^(?P<file>.+?):(?P<line>\d+):\s*(?P<kind>\w+):\s*(?P<text>.+)$')

def main():
    ap = argparse.ArgumentParser(description="Parse Doxygen warnings into CSV")
    ap.add_argument("--input", "-i", required=True, help="Path to Doxygen warnings log file")
    ap.add_argument("--output", "-o", required=True, help="Path to output CSV file")
    args = ap.parse_args()

    if not os.path.exists(args.input):
        print(f"Input file not found: {args.input}", file=sys.stderr)
        return 2

    rows, ignored = [], 0
    with open(args.input, encoding="utf-8", errors="replace") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            m = PATTERN.match(line)
            if not m:
                ignored += 1
                continue
            gd = m.groupdict()
            rows.append({
                "Line": gd.get("line", ""),
                "File": gd.get("file", ""),
                "Message": gd.get("text", ""),
            })

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["Line", "File", "Message"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Parsed {len(rows)} warnings. Ignored {ignored} non-standard lines.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
