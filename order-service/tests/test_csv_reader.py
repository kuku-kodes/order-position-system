from app.csv_reader import read_csv_rows


def test_csv_is_read_incrementally(tmp_path):

    csv_file = tmp_path / "orders.csv"

    csv_file.write_text(
        "event_id,symbol,transaction_type,quantity\n"
        "evt-001,RELIANCE,BUY,90\n"
        "evt-002,TCS,SELL,75\n"
    )

    rows = read_csv_rows(str(csv_file))

    first_row = next(rows)

    assert first_row["event_id"] == "evt-001"
    assert first_row["symbol"] == "RELIANCE"

    second_row = next(rows)

    assert second_row["event_id"] == "evt-002"