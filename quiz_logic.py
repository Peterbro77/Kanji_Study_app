import pandas as pd
import random

def load_kanji_data(csv_path):
    return pd.read_csv(csv_path)

def get_quiz_data(df, start, end):
    return df.iloc[start-1:end].sample(frac=1).reset_index(drop=True)
