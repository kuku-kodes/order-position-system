import csv
from collections.abc import Iterator


def read_csv_rows(file_path: str) -> Iterator[dict]:
    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            yield row