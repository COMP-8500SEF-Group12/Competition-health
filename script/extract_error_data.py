import json
import os

# File paths
source_file = "20250208181531_camp_data_step_1_without_answer.jsonl"
results_file = "results_debug.jsonl"
failed_source_file = "failed_records_source.jsonl"

# Step 1: Extract failed IDs from results_debug.jsonl
failed_ids = set()

try:
    with open(results_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                record = json.loads(line.strip())
                # Check if this is a failed prediction
                if record.get("reason") and "处理失败" in record.get("diseases", ""):
                    failed_ids.add(record["id"])
            except json.JSONDecodeError:
                print(f"Warning: Could not parse line in results file: {line[:50]}...")
                continue

    print(f"Found {len(failed_ids)} failed prediction IDs")

except FileNotFoundError:
    print(f"Error: Could not find results file {results_file}")
    exit(1)

# Step 2: Extract the original records for failed IDs from source file
if not failed_ids:
    print("No failed predictions found. Exiting.")
    exit(0)

try:
    with open(source_file, 'r', encoding='utf-8') as source, \
            open(failed_source_file, 'w', encoding='utf-8') as output:

        count = 0
        for line in source:
            try:
                record = json.loads(line.strip())
                if record["id"] in failed_ids:
                    output.write(line)
                    count += 1
            except json.JSONDecodeError:
                print(f"Warning: Could not parse line in source file: {line[:50]}...")
                continue

        print(f"Extracted {count} records to {failed_source_file}")

except FileNotFoundError:
    print(f"Error: Could not find source file {source_file}")
    exit(1)

print("Process completed successfully!")