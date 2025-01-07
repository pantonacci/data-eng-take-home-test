# Data Engineering Take-Home Test

## Overview

Build a simple analytics pipeline to process LLM application logs and produce a chart or dashboard. The dataset contains 1,000 API call records with metrics like timestamps, token counts, and latency.


## Requirements

- Working code that processes the data:
  I have included two python files to process the data. `llm_log_pipeline.py` was the version I used on Google Colab to transform the json data and upload it to a BigQuery table,
  but sharing this is a bit harder, so I've also included an executable `llm_log_pipeline_csv.py` that will output the results as a csv file if you would like to upload it to a
  BigQuery or database of your own.
- A database to store the transformed data:
  The data is currently stored in a sandbox BigQuery that I created. I've also created a summary table for the visualization in the runnable `daily_llm_metrics.sql` file
  (runnable in BigQuery, some functions might not work in all SQL languages).
- At least one chart/visualization:
  Included in the `daily_llm_metrics.pdf` is a dashboard I created which is from Looker Studio. I have made it viewable and is interactable at the url:
  https://lookerstudio.google.com/reporting/2c1175ce-5a27-4ec1-906f-1f18d7c622fe

## Solution

I spent time on Google Colab doing some exploratory data analysis on the data and ended up extracting only the data portion of the json file.

### Data ingestion
I'm not sure where the log data resides, my solution assumes that it is in a cloud storage bucket like Google Storage where I would read the json and extract the data using the 
python function. I have also included a requirements.txt for the functions needed. If this log data comes in on regular intervals and isn't too big, I would use this python method
and ingest the data using a Google Cloud Function (or Google Run) on a timeframe that is reasonable. The file `llm_log_pipeline.py` would work in a cloud function by changing the authorization requirements, which is best done with roles in GCP.

  If live dashboarding is necessary then I would look into a streamable way to ingest the data into BigQuery (or a database instead of data warehouse if need be).
The log data would then be stored in a table with minimal transformations done so others can see raw versions of the data.

### ETL
For the ETL I have put the data in BigQuery and added the `daily_llm_metrics.sql` file. This would take the raw log data and aggregate it on a daily basis. I would use Google BigQuery and have this script run daily with scheduled queries. Depending on how in depth this solution would be it would be best to transition into Airflow or dbt to have better
scheduling and modeling.

### Data visualization
I have included the pdf which is download and viewable, but the current solution is also viewable (by link only) at https://lookerstudio.google.com/reporting/2c1175ce-5a27-4ec1-906f-1f18d7c622fe

I used Looker Studio as it is free, but this portion is easily replaceable with a data visualization tool of choice that hooks up to BigQuery.

I have included some daily metrics that seemed interesting. I think the average latency increasing the day after large calls seems interesting.

I think there would be more room to do analyses like hourly analysis of API calls (which times are more used) and looking at the different API versions.

### Final remarks
Please let me know if you have any questions about my solution. I included everything in the repo main directory, but if I would use multiple repos for this project since it has a lot of different GCP technologies.
