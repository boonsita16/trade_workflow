A Python implementation of the exposure and P&L reports.

## What it calculates

- Aggregates signed trade quantities into net positions by commodity, delivery
	period, and book, keeping Physical and Hedge positions separate.
- Calculates delta exposure as the combined Physical and Hedge position. The
	residual delta shows the position that would need to be offset to bring the
	exposure flat (or to the desired naturalized position).
- Calculates financial hedge coverage as the absolute Hedge position divided
	by the absolute Physical position, expressed as a percentage.
- Joins each trade to its current market price and calculates mark-to-market
	P&L. The report includes trade-level results, totals by book (Physical and
	Hedge), and overall total P&L.

The position aggregation and delta exposure approach is informed by [Position
Aggregation & Delta Exposure | Energy Trading](https://a115.co.uk/position-aggregation-delta-exposure/).

Run the workflow from the project root with:

```powershell
python trade_workflow.py
```

The script reads its example trade and market data from `notebooks/` and writes
the exposure and P&L reports to that folder. The original notebook and all
example CSV files are also kept in `notebooks/`.
