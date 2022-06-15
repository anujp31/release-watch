# release-watch
A simple script to retrieve the latest version/tag for interesting repos.

## How to use
Create a `~/.config/release-watch.toml` with your github creds and the repositories you want to watch

    ```toml
    github_user = "anujp31"
    github_token = "XXXXXXXXXXXXXXXXXX"
    sub_urls = [
        "apache/airflow",
        "apache/spark",
        "databricks/dbt-databricks",
        "dbt/dbt-core",
    ]
    ```

Run via poetry

    ```bash
    poetry install
    poetry run releases
    ```
