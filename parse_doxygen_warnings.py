import csv, re, argparse

def parse_warnings(input_file, output_file):
    pattern = re.compile(r'^(?P<file>.+?):(?P<line>\d+):\s*(?P<kind>\w+):\s*(?P<text>.+)$')
    rows = []
    with open(input_file) as f:
        for line in f:
            m = pattern.match(line.strip())
            if m:
                rows.append(m.groupdict())
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["file","line","kind","text"])
        writer.writeheader()
        writer.writerows(rows)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    parse_warnings(args.input, args.output)
