import click

from dataskope.core.snowflake import load_credentials, get_snowflake_schema, get_snowflake_queries
from dataskope.core.detect_unused import detect_unused_columns as detect_unused_columns_core


@click.group(name="dataskope")
def cli():
    pass


@cli.command('detect', help="""
Detect unused columns in SQL queries. 
Requires two files: a query file and an information schema file. 
Run `show-queries` to see the SQL queries to run against your 
Snowflake instance to generate the two files.""")
@click.option('--queries_file', help='The SQL query file to analyze.')
@click.option('--info_schema_file',
              help='The file containing the information schema for the database.')
@click.option('--credentials_from_env',
              help='Load snowflake credentials from the environment.',
              is_flag=True)
def detect_unused_columns(queries_file: str, info_schema_file: str, credentials_from_env: bool):
    if credentials_from_env:
        schema = get_snowflake_schema()
        queries = get_snowflake_queries()


    detect_unused_columns_core(queries_file, info_schema_file)


@cli.command("show-queries")
def show_snowflake_queries():
    print("Run the below against your snowflake instance to generate a dataset you can"
          "export to CSV for analysis")
    print("""
-- query_file

SELECT *
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE QUERY_TEXT ILIKE 'select%'
ORDER BY START_TIME DESC
LIMIT 10000; -- or start_time > $SOME_DATE to get columns unused in the last N days


-- info_schema_file

use database MY_DATABASE; -- change me

SELECT
TABLE_CATALOG,
TABLE_SCHEMA,
TABLE_NAME,
COLUMN_NAME
FROM information_schema.columns
WHERE TABLE_SCHEMA != 'INFORMATION_SCHEMA';
        
        """
    )

if __name__ == "__main__":
    cli()