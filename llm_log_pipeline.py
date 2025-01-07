import pandas as pd
from google.colab import auth
import json
import google.cloud.bigquery as bq

PROJECT_ID = 'sandbox-447022'
DATASET_ID = 'durable'
TABLE_NAME = f'{PROJECT_ID}.{DATASET_ID}.llm_logs'

# I ran this on Google Colab where I manually authenticated myself but if this
# were a cloud function or ran elsewhere I would change this authentication method
auth.authenticate_user()

if __name__ == "__main__":
  # I ran this on Google Colab with the json file in the directory but ideally it would
  # be read from a cloud storage like Google Storage, so I've commented out this section which:
  # Instantiates a Google Cloud Storage client and specify required bucket and file
  # and downloads the contents of the blob as a string and then parse it using json.loads() method

  # from google.cloud import storage
  # storage_client = storage.Client()
  # bucket = storage_client.get_bucket('bucket_name')
  # blob = bucket.blob('llm_logs.json')
  # data = json.loads(blob.download_as_string(client=None))

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

  # Start BigQuery client to write dataframe to
  client = bq.Client(project=PROJECT_ID)

  # Set schema of BigQuery table and other configs for job
  job_config = bq.LoadJobConfig(
      schema=[
          bq.SchemaField('created',                     'TIMESTAMP'),
          bq.SchemaField('model',                       'STRING'),
          bq.SchemaField('stream',                      'BOOL'),
          bq.SchemaField('max_tokens',                  'INTEGER'),
          bq.SchemaField('temperature',                 'FLOAT'),
          bq.SchemaField('type',                        'STRING' ),
          bq.SchemaField('metrics_end',                 'TIMESTAMP'),
          bq.SchemaField('metrics_start',               'TIMESTAMP'),
          bq.SchemaField('metrics_tokens',              'FLOAT'),
          bq.SchemaField('metrics_prompt_tokens',       'FLOAT'),
          bq.SchemaField('metrics_completion_tokens',   'FLOAT'),
          bq.SchemaField('metrics_time_to_first_token', 'FLOAT')
      ],
      # Currently setting the write disposition with WRITE_TRUNCATE write
      # disposition which replaces the table with the loaded data.
      # If I were to continuously run this pipeline with new data I would use WRITE_APPEND
      write_disposition="WRITE_TRUNCATE",
  )

  table = bq.Table(TABLE_NAME)

  print('Begin writing llm-logs to BigQuery.')
  load_job = client.load_table_from_dataframe(df, table, job_config=job_config)

  print(f'Loaded {df.shape[0]} rows to {TABLE_NAME}.')