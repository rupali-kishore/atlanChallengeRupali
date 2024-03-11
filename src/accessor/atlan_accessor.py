from pyatlan.cache.role_cache import RoleCache
from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import Table, Connection, S3Bucket, S3Object, Process, Column, ColumnProcess
from pyatlan.model.enums import AtlanConnectorType

from src.constant.constant import BASE_URL, API_KEY
from src.util.logger_util import get_logger

logger = get_logger()


def get_atlan_client():
    """
    Initialize Atlan client and create connection

    :return:
    """
    try:
        return AtlanClient(
            base_url=BASE_URL,
            api_key=API_KEY
        )
    except Exception as e:
        logger.error(f'Error initializing AtlanClient: {str(e)}')
        raise Exception("Unable to create AtlanClient")


class AtlanAssetAccessor:
    """
    This is the accessor class responsible for fetching/creating required asset in Atlan platform
    """

    def __init__(self):
        """
        Initialise class instance
        """
        self.client = get_atlan_client()

    def fetch_all_column_list_from_table(self, table_qname):
        """
        Method to fetch all columns of a table in DB
        :param table_qname: Table's qualified name
        :return: List of columns
        """
        try:
            table = self.client.asset.get_by_qualified_name(
                asset_type=Table,
                qualified_name=table_qname
            )
            cols = []
            for item in table.columns:
                cols.append(item.display_text)
            return cols
        except Exception as e:
            logger.error(f'Error fetching column list from table: {str(e)}')
            raise Exception("Unable to fetch column list")

    def create_s3_conn_asset(self, asset_name, suffix):
        """
        Method to create S3 Connection asset
        :param asset_name: name of the connection asset
        :param suffix: suffix to be added after asset-name
        :return: qualified name of created connect asset
        """
        try:
            admin_role_guid = RoleCache.get_id_for_name("$admin")
            connection = Connection.create(
                name=f"{asset_name}-{suffix}",
                connector_type=AtlanConnectorType.S3,
                admin_roles=[admin_role_guid],
                admin_users=["rupalikishore93"]
            )
            response = self.client.asset.save(connection)
            return response.assets_created(asset_type=Connection)[0].qualified_name
        except Exception as e:
            logger.error(f"Error creating S3 connection asset: {e}")
            raise Exception("Unable to create S3 connection asset")

    def create_s3_bucket_asset(self, asset_name, suffix, s3_conn_qname):
        """
        Method to create S3 Bucket asset
        :param asset_name: name of the bucket asset
        :param suffix: suffix to be added after asset-name
        :param s3_conn_qname: qualified name of corresponding S3 connection asset
        :return: qualified name of created bucket asset
        """
        try:
            s3bucket = S3Bucket.create(
                name=f"{asset_name}-{suffix}",
                connection_qualified_name=s3_conn_qname,
                aws_arn=f"arn:aws:s3:::{asset_name}-{suffix}"
            )
            response = self.client.asset.save(s3bucket)
            bucket_qualified_name = response.assets_created(asset_type=S3Bucket)[0].qualified_name
            return bucket_qualified_name
        except Exception as e:
            logger.error(f"Error creating S3 bucket asset: {e}")
            raise Exception("Unable to create S3 bucket asset")

    def create_s3_obj(self, s3_obj, bucket_qualified_name, connection_qualified_name, suffix):
        """
        Method to create S3 Object asset
        :param s3_obj: name of the object asset
        :param bucket_qualified_name: qualified name of corresponding S3 bucket asset
        :param connection_qualified_name: qualified name of corresponding S3 connection asset
        :param suffix: suffix to be added after asset-name
        :return: qualified name of created object asset
        """
        try:
            s3object = S3Object.create(
                name=s3_obj,
                connection_qualified_name=connection_qualified_name,
                aws_arn=f"arn:aws:s3:::atlan-tech-challenge-{suffix}/{s3_obj}",
                s3_bucket_qualified_name=bucket_qualified_name
            )
            response = self.client.asset.save(s3object)
            object_qualified_name = response.assets_created(asset_type=S3Object)[0].qualified_name
            return object_qualified_name
        except Exception as e:
            logger.error(f"Error creating S3 object asset: {e}")
            raise Exception("Unable to create S3 object asset")

    def create_s3_to_db_obj_table_lineage(self, db_conn_qname, object_qname, table_name, db_name, schema_name,
                                          is_upstream):
        """
        Method to create upstream and downstream table lineage between S3 and DBs
        :param db_conn_qname: qualified name of DB connection asset
        :param object_qname: qualified name of S3 object asset
        :param table_name: name of table within schema
        :param db_name: name of DB
        :param schema_name: name of schema within DB
        :param is_upstream: Flag to decide whether lineage is upstream or downstream w.r.t S3
        :return: qualified name of table lineage created
        """
        try:
            if is_upstream:
                inputs = [
                    Table.ref_by_qualified_name(qualified_name=f"{db_conn_qname}/{db_name}/{schema_name}/{table_name}")]
                outputs = [S3Object.ref_by_qualified_name(qualified_name=object_qname)]
                p_name = f"{table_name} {db_conn_qname} -> S3"
            else:
                inputs = [S3Object.ref_by_qualified_name(qualified_name=object_qname)]
                outputs = [
                    Table.ref_by_qualified_name(qualified_name=f"{db_conn_qname}/{db_name}/{schema_name}/{table_name}")]
                p_name = f"{table_name} S3 -> {db_conn_qname}"
            process = Process.create(
                name=p_name,
                connection_qualified_name=db_conn_qname,
                process_id=p_name,
                inputs=inputs,
                outputs=outputs
            )
            self.client.asset.save(process)
            return f"{db_conn_qname}/{p_name}"
        except Exception as e:
            logger.error(f"Error creating table lineage between {object_qname} and {table_name}: {e}")
            raise Exception("Unable to create table lineage")

    def create_s3_to_db_obj_column_lineage(self, pqname, db_conn_qname, s3_obj_qname, db_name, schema_name, table_nm,
                                           is_upstream):
        """
        Method to create upstream and downstream column lineage between S3 and DBs
        :param pqname: qualified name of corresponding process(table lineage)
        :param db_conn_qname: qualified name of DB connection asset
        :param s3_obj_qname: qualified name of S3 object asset
        :param db_name: name of DB
        :param schema_name: name of schema within DB
        :param table_nm: name of table within schema
        :param is_upstream: Flag to decide whether lineage is upstream or downstream w.r.t S3
        :return: qualified name of column lineage created
        """
        try:
            db_column_process_inputs = []
            for item in self.fetch_all_column_list_from_table(f"{db_conn_qname}/{db_name}/{schema_name}/{table_nm}"):
                db_column_process_inputs.append(
                    Column.ref_by_qualified_name(f"{db_conn_qname}/{db_name}/{schema_name}/{table_nm}/{item}"))

            if is_upstream:
                inputs = db_column_process_inputs
                outputs = [S3Object.ref_by_qualified_name(qualified_name=s3_obj_qname)]
                pname = f"Column {table_nm} {db_conn_qname} -> S3"
            else:
                outputs = db_column_process_inputs
                inputs = [S3Object.ref_by_qualified_name(qualified_name=s3_obj_qname)]
                pname = f"Column {table_nm} S3 -> {db_conn_qname}"
            column_process = ColumnProcess.create(
                name=pname,
                connection_qualified_name=db_conn_qname,
                process_id=pname,
                inputs=inputs,
                outputs=outputs,
                parent=Process.ref_by_qualified_name(pqname),
            )
            self.client.asset.save(column_process)
            return f"{db_conn_qname}/{pname}"
        except Exception as e:
            logger.error(f"Error creating column lineage between {s3_obj_qname} and {table_nm}: {e}")
            raise Exception("Unable to create column lineage")
