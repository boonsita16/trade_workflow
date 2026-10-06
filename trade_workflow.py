from pathlib import Path

import pandas as pd


DATA_DIR = Path(__file__).resolve().parent / "notebooks"


def trades(df):
    # Adapted from https://stackoverflow.com/a/73664277 (CC BY-SA 4.0).
    df["SignedQty"] = pd.Series(df["Qty"] * -1, index=df.index).mask(
        df["Action"] == "Buy", df["Qty"]
    )
    return df


def positions(df):
    return (
        trades(df)
        .groupby(["Commodity", "Delivery", "Book"])["SignedQty"]
        .sum()
        .reset_index()
        .rename(columns={"SignedQty": "Net Position"})
    )


def exposure(df):
    position = positions(df)
    result = position.pivot_table(
        index=["Commodity", "Delivery"],
        columns="Book",
        values="Net Position",
        fill_value=0,
    ).reset_index()
    result["Delta"] = result["Physical"] + result["Hedge"]
    result["Coverage %"] = abs(result["Hedge"]) / abs(result["Physical"]) * 100
    result = result.rename_axis(None, axis=1).reset_index(drop=True)

    print(f"Total unhedged exposure {result['Delta'].sum()} MWh")
    return result


def trades_market(df, df_market):
    return trades(df).merge(df_market, on=["Commodity", "Delivery"], how="left")


def MtM_PnL(df, df_market):
    result = trades_market(df, df_market)
    result["MtM_PnL(£)"] = (
        result["Market Price(£/MWh)"] - result["Price(£/MWh)"]
    ) * result["SignedQty"]
    print(
        result.groupby("Book")["MtM_PnL(£)"].sum().reset_index().rename_axis(None, axis=1)
    )
    print(f"Total P&L : {result['MtM_PnL(£)'].sum()} £")
    return result


def main():
    df = pd.read_csv(DATA_DIR / "trade_data_example.csv")
    df_market = pd.read_csv(DATA_DIR / "market_price_example.csv")

    exposure(df).to_csv(DATA_DIR / "exposure_example.csv")
    MtM_PnL(df, df_market).to_csv(DATA_DIR / "PnL_report_example.csv")


if __name__ == "__main__":
    main()