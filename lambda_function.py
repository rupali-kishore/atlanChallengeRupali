from src.component.create_s3_obj_asset_with_lineage import create_s3_obj_asset_with_lineage
from src.constant.constant import SUFFIX

from src.util.logger_util import get_logger
from delete_util.delete_util import delete_all_asset

logger = get_logger()

# for testing locally
if __name__ == '__main__':
    # deleting previously created assets(if any)
    delete_all_asset(SUFFIX)

    # create all asset
    create_s3_obj_asset_with_lineage(SUFFIX)


def lambda_handler(event, context):
    """
    Method to trigger AWS lambda function which then invokes the controller/component

    :param event: Lambda event
    :param context: AWS context for Lamdbda execution
    :return: Status code and message
    """

    # begin with new assets creation
    try:
        # fetch suffix from payload
        suffix = event['suffix']
        logger.info(f"Suffix value from payload:{suffix}")
        if suffix is None or suffix == "":
            raise KeyError('Suffix value not provided')

        # deleting previously created assets (if any) using delete utility
        delete_all_asset(suffix)

        # create all asset
        create_s3_obj_asset_with_lineage(suffix)

        # Return a success response with HTTP status code 200
        return {
            'statusCode': 200,
            'body': 'Success'
        }
    except KeyError as e:
        logger.error(f'KeyError: {str(e)}')
        # Return an error response with HTTP status code 400
        return {
            'statusCode': 400,
            'body': 'Invalid request payload-suffix not provided'
        }

    except Exception as e:
        # Log the exception
        logger.error(f'Error: {str(e)}')
        # Return an error response with HTTP status code 500
        return {
            'statusCode': 500,
            'body': 'Internal Server Error'
        }
