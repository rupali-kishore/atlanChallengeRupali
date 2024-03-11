import os

# S3 bucket details
S3_BUCKET_NAME = "atlan-tech-challenge"
S3_REGION = "us-east-2"

# Connection details
POSTGRES_DB_CONN_QNAME = "default/postgres/1709558357"
POSTGRES_DB_NAME = "FOOD_BEVERAGE"
POSTGRES_DB_SCHEMA_NAME = "SALES_ORDERS"

SNOWFLAKE_DB_CONN_QNAME = "default/snowflake/1709558216"
SNOWFLAKE_DB_NAME = "FOOD_BEVERAGE"
SNOWFLAKE_DB_SCHEMA_NAME = "SALES_ORDERS"

# Atlan constants - Lambda or Local
BASE_URL = os.environ.get('BASE_URL') if 'BASE_URL' in os.environ else "https://tech-challenge.atlan.com/"
API_KEY = os.environ.get('API_KEY') if 'API_KEY' in os.environ else "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJsYmM5QTJfTjFOM0FqbElpWU9wTGNLTUw1RVRaV1I2Q2w5MFhqajBwQWlzIn0.eyJleHAiOjIxMTk2MzIwOTEsImlhdCI6MTcwOTY2NDA5MSwianRpIjoiNGIyNGZmNWEtMmE1Mi00MTI5LWJlOTQtMjFjMWQ5ZDViZTQxIiwiaXNzIjoiaHR0cHM6Ly90ZWNoLWNoYWxsZW5nZS5hdGxhbi5jb20vYXV0aC9yZWFsbXMvZGVmYXVsdCIsImF1ZCI6WyJyZWFsbS1tYW5hZ2VtZW50IiwiYWNjb3VudCJdLCJzdWIiOiJhNDQwZTQ2OS0xZmVhLTRjY2EtYWYzZC01OWE1ZTAwMGQ2YmEiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJhcGlrZXktZDRhNDhhODYtODA2NC00MDMwLTk2YmQtMTczYzU5MzkyYzZkIiwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIiRndWVzdCIsIm9mZmxpbmVfYWNjZXNzIiwiZGVmYXVsdC1yb2xlcy1kZWZhdWx0IiwiJGFwaS10b2tlbi1kZWZhdWx0LWFjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsicmVhbG0tbWFuYWdlbWVudCI6eyJyb2xlcyI6WyJ2aWV3LXJlYWxtIiwidmlldy1pZGVudGl0eS1wcm92aWRlcnMiLCJtYW5hZ2UtaWRlbnRpdHktcHJvdmlkZXJzIiwiaW1wZXJzb25hdGlvbiIsInJlYWxtLWFkbWluIiwiY3JlYXRlLWNsaWVudCIsIm1hbmFnZS11c2VycyIsInF1ZXJ5LXJlYWxtcyIsInZpZXctYXV0aG9yaXphdGlvbiIsInF1ZXJ5LWNsaWVudHMiLCJxdWVyeS11c2VycyIsIm1hbmFnZS1ldmVudHMiLCJtYW5hZ2UtcmVhbG0iLCJ2aWV3LWV2ZW50cyIsInZpZXctdXNlcnMiLCJ2aWV3LWNsaWVudHMiLCJtYW5hZ2UtYXV0aG9yaXphdGlvbiIsIm1hbmFnZS1jbGllbnRzIiwicXVlcnktZ3JvdXBzIl19LCJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6ImVtYWlsIHByb2ZpbGUgb2ZmbGluZV9hY2Nlc3MiLCJjcmVhdGVkQXQiOiIxNzA5NjY0MDYwNjE2IiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJjbGllbnRJZCI6ImFwaWtleS1kNGE0OGE4Ni04MDY0LTQwMzAtOTZiZC0xNzNjNTkzOTJjNmQiLCJjbGllbnRIb3N0IjoiMTAuMTkwLjMzLjIyMyIsImdyb3VwcyI6W10sInJlYWxtIjoiZGVmYXVsdCIsInByZWZlcnJlZF91c2VybmFtZSI6InNlcnZpY2UtYWNjb3VudC1hcGlrZXktZDRhNDhhODYtODA2NC00MDMwLTk2YmQtMTczYzU5MzkyYzZkIiwidXNlcklkIjoiYTQ0MGU0NjktMWZlYS00Y2NhLWFmM2QtNTlhNWUwMDBkNmJhIiwiY2xpZW50QWRkcmVzcyI6IjEwLjE5MC4zMy4yMjMiLCJ1c2VybmFtZSI6InNlcnZpY2UtYWNjb3VudC1hcGlrZXktZDRhNDhhODYtODA2NC00MDMwLTk2YmQtMTczYzU5MzkyYzZkIn0.WFSbcFhvTM45waOff90FdiQ9SiNXMO_C0Nx1MAd7xeI25s_JyMhgYFjW-ar-97BR5cdjaIJq0-aY3QC68Boe82vNCcPPDbQH3UNms2V_LrJchw5Ddlp0h60PrcXD0SfETJDdy619TrnB02Bkoo8PRURTVk0wJVuqFhUgKuO4MX4nb-v8S_48Im1fTOjW-OYNRalaciVx2v-B8R76EbANtL-Umfv5O0lePsHiN0OHenSSzuZnhJspG-ViVqLd8MSM7vQhIblC-2wpnj588oiXYo7VSJNUoJR5H9D44UwoB48M-oOqor3rI1pD8HZqoSLjMjx1u9-p3-hvxgMiEfnNPw"

# Suffix
SUFFIX = "rupali-atlan-dev"

ATLAN_S3_OBJ_LIST = ['CATEGORIES.csv', 'CUSTOMERS.csv', 'EMPLOYEES.csv', 'ORDERDETAILS.csv',
                     'ORDERS.csv', 'PRODUCTS.csv', 'SHIPPERS.csv', 'SUPPLIERS.csv']