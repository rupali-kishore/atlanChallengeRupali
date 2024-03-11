import time

from src.accessor.atlan_accessor import AtlanAssetAccessor
from src.accessor.s3_accessor import S3Accessor
from src.constant.constant import S3_BUCKET_NAME, S3_REGION, POSTGRES_DB_CONN_QNAME, POSTGRES_DB_NAME, \
    POSTGRES_DB_SCHEMA_NAME, ATLAN_S3_OBJ_LIST, SUFFIX
from src.constant.constant import SNOWFLAKE_DB_CONN_QNAME, SNOWFLAKE_DB_NAME, SNOWFLAKE_DB_SCHEMA_NAME

from src.util.logger_util import get_logger

# Get logger for the current module
logger = get_logger()

# create required accessor objects
atlan_accessor = AtlanAssetAccessor()
s3_accessor = S3Accessor(S3_REGION)


def create_s3_obj_asset_with_lineage(suffix):
    """
    This is the controller method with entire business logic
    :param suffix: suffix to be added after asset-name
    :return: None
    """
    # create s3 connection
    s3_conn_qname = atlan_accessor.create_s3_conn_asset("aws-s3-connection", SUFFIX)

    # Adding wait time after connection as mentioned in doc -
    # https://developer.atlan.com/patterns/create/aws/?h=s3#connection
    time.sleep(10)

    # create s3 bucket
    s3_bucket_qname = atlan_accessor.create_s3_bucket_asset("atlan-tech-challenge", suffix, s3_conn_qname)
    # fetch s3 objects
    s3_obj_list = s3_accessor.get_s3_obj_list(S3_BUCKET_NAME)
    # iterate over s3 items
    for s3_item in s3_obj_list:
        # fetch table_nm from s3 object csv
        table_nm = str(s3_item).replace(".csv", "")
        # create s3 object
        s3_obj_qname = atlan_accessor.create_s3_obj(s3_item, s3_bucket_qname, s3_conn_qname, suffix)
        # create obj and table lineage
        # upstream
        upstream_process = atlan_accessor.create_s3_to_db_obj_table_lineage(POSTGRES_DB_CONN_QNAME,
                                                                            s3_obj_qname,
                                                                            table_nm,
                                                                            POSTGRES_DB_NAME,
                                                                            POSTGRES_DB_SCHEMA_NAME,
                                                                            True
                                                                            )
        # downstream
        downstream_process = atlan_accessor.create_s3_to_db_obj_table_lineage(SNOWFLAKE_DB_CONN_QNAME,
                                                                              s3_obj_qname,
                                                                              table_nm,
                                                                              SNOWFLAKE_DB_NAME,
                                                                              SNOWFLAKE_DB_SCHEMA_NAME,
                                                                              False
                                                                              )

        # upstream column lineage
        atlan_accessor.create_s3_to_db_obj_column_lineage(upstream_process,
                                                          POSTGRES_DB_CONN_QNAME,
                                                          s3_obj_qname,
                                                          POSTGRES_DB_NAME,
                                                          POSTGRES_DB_SCHEMA_NAME,
                                                          table_nm,
                                                          True
                                                          )

        # downstream column lineage
        atlan_accessor.create_s3_to_db_obj_column_lineage(downstream_process,
                                                          SNOWFLAKE_DB_CONN_QNAME,
                                                          s3_obj_qname,
                                                          SNOWFLAKE_DB_NAME,
                                                          SNOWFLAKE_DB_SCHEMA_NAME,
                                                          table_nm,
                                                          False
                                                          )
