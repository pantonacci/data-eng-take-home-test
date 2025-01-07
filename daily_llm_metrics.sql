create or replace table `sandbox-447022.durable.daily_llm_metrics` as (

  SELECT
    extract(date from created) as date,
    count(*) as total_daily_api_calls,
    countif(stream) as total_streamed_api_calls,
    countif(not stream) as total_non_streamed_api_calls,
    countif(type = 'text') as total_text_api_calls,
    countif(type = 'json_schema') as total_json_api_calls,
    avg(metrics_time_to_first_token) as avg_metrics_time_to_first_token,
    avg(case when type = 'text' then metrics_time_to_first_token else NULL end) as avg_text_prompt_time_to_first_token,
    avg(case when type = 'json_schema' then metrics_time_to_first_token else NULL end) as avg_json_prompt_time_to_first_token,
    avg(temperature) as avg_temperature,
    avg(max_tokens) as avg_max_tokens,
    sum(metrics_tokens) as total_metrics_tokens,
    sum(metrics_prompt_tokens) as total_metrics_prompt_tokens,
    sum(metrics_completion_tokens) as total_metrics_completion_tokens,
    sum(metrics_tokens) + sum(metrics_prompt_tokens) + sum(metrics_completion_tokens) as daily_total_tokens
  FROM `sandbox-447022.durable.llm_logs`
  group by 1
  order by 1

);
