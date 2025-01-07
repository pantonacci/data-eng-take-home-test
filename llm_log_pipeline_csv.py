import pandas as pd
import json

if __name__ == "__main__":
  with open('data/llm-logs.json') as f:
    data = json.load(f)

  print('Finished reading llm-logs from storage.')

  # Read json data as pandas dataframe and rename the columns
  df = pd.json_normalize(data['data'])
  df.columns = df.columns.str.replace(r"\.", "_", regex=True)

  # Convert the data to desired data format
  df.created = pd.to_datetime(df.created).astype('datetime64[s]')
  df.metrics_end = pd.to_datetime((df.metrics_end * (10**9))).astype('datetime64[s]')
  df.metrics_start = pd.to_datetime((df.metrics_start * (10**9))).astype('datetime64[s]')

  print('Begin writing llm-logs to csv.')
  df.to_csv('data/llm-logs.csv')

  print(f'Loaded {df.shape[0]} rows to data/llm-logs.csv.')