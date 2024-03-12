from pyatlan.model.assets import Connection, S3Bucket, S3Object
from pyatlan.model.fluent_search import FluentSearch
from src.accessor.atlan_accessor import get_atlan_client

from src.constant.constant import SUFFIX
from src.util.logger_util import get_logger

# create global constants
client = get_atlan_client()
S3_OBJS = ['CATEGORIES.csv', 'CUSTOMERS.csv', 'EMPLOYEES.csv', 'ORDERDETAILS.csv',
           'ORDERS.csv', 'PRODUCTS.csv', 'SHIPPERS.csv', 'SUPPLIERS.csv']
logger = get_logger()


def delete_asset(guid, asset_type):
    response = client.asset.purge_by_guid(guid)  #
    if deleted := response.assets_deleted(asset_type=asset_type):  #
        term = deleted[0]


def delete_asset_with_str(asset_type, search_str, suffix):
    logger.info(f"# Starting deleting {asset_type} with name {search_str} and suffix {suffix}")
    # prepare request basis type and label name
    request = (
        FluentSearch()  #
        .where(FluentSearch.asset_type(asset_type))
        .where(FluentSearch.active_assets())
        .where(asset_type.NAME.eq(search_str))  #
    ).to_request()  #

    # Look for asset with my suffix and delete
    for result in client.asset.search(request):  #
        try:
            logger.info(f'## Attempting to deleting asset {result.name} with guid {result.qualified_name}')
            if asset_type != Connection:
                # we are looking for suffix for in qname for asset other than connection so that
                # I don't delete asset of other users
                if result.qualified_name.__contains__(suffix):
                    delete_asset(result.guid, asset_type)
                    logger.info(f'## Deleted asset {result.name}')
            else:
                # In connection qname suffix is no there so deleting basis label name
                delete_asset(result.guid, asset_type)
                logger.info(f'## Deleted asset {result.name}')
        except Exception as e:
            logger.info(f'## Unable to delete asset {result.name} with guid {result.qualified_name} \n with error {e}')


def delete_all_asset(suffix):
    # Delete s3 objects
    for item in S3_OBJS:
        delete_asset_with_str(S3Object, item, suffix)
    # Delete S3 bucket
    delete_asset_with_str(S3Bucket, f"atlan-tech-challenge-{suffix}", suffix)
    # Delete S3 connection
    delete_asset_with_str(Connection, f"aws-s3-connection-{suffix}",suffix)


# for running locally
if __name__ == '__main__':
    delete_all_asset(SUFFIX)
