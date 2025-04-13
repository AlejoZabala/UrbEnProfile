def process_ueu(df):

    # Use the last row as the new header
    df.columns = df.iloc[-1]

    # Drop the last row (since it's now the header)
    df = df.iloc[:-1]

    # Reset the index
    df.reset_index(drop=True, inplace=True)

    return df


