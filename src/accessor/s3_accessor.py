import boto3
from botocore.exceptions import ClientError
from src.util.logger_util import get_logger

# Get the logger
logger = get_logger()


class S3Accessor:
    """
    This is the accessor class responsible for fetching required info from S3 bucket given in the challenge
    """

    def __init__(self, region):
        self.s3_client = boto3.client("s3", region_name=region)

    def get_s3_obj_list(self, bucket_name):
        """
        Method to get list of all the objects present in S3 bucket
        :param bucket_name: name of S3 bucket
        :return: list of S3 objects
        """
        try:
            logger.info("Fetching S3 object")
            s3_obj_list = []
            # List objects in S3 bucket
            response = self.s3_client.list_objects_v2(Bucket=bucket_name)
            for obj in response.get("Contents", []):
                s3_object_name = obj["Key"]
                s3_obj_list.append(s3_object_name)
            logger.info(f"Object list: {s3_obj_list}")
            return s3_obj_list
        except ClientError as e:
            # Handle S3 client errors
            logger.error(f"Error while fetching objects from S3: {str(e)}")
            raise Exception("Unable to fetch objects from S3")
        except Exception as e:
            # Handle other unexpected errors
            logger.error(f"Unexpected error occurred: {str(e)}")
            raise
