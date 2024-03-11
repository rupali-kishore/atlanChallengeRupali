# Atlan Data Challenge Code README

## Solution Design
I have created a code base which take ```suffix``` as input (for lambda), basis the suffix it create required assets which are mentioned in the challenge

### Below is the package structure
```
src
├── accessor
|   ├── atlan_accessorpy
|   └── s3_accessorpy
├── component
|   └── create_s3_obj_asset_with_lineagepy
├── constant
|   └── constantpy
└── util
    └── logger_utilpy
```
### Accessor
Accessor package contains accessor class/methods to interact with external API (Atlan and S3)

### Component
Component/controller package contains method with entire business logic of the solution
#### Component Steps:
#### 0. Delete previous asset with the suffix (if any present)
#### 1. Create S3 connection asset
#### 2. Create S3 bucket asset
#### 3. Fetch S3 object list from Atlan s3. 
#### 4. Iterate on List of object
#### 4.1 Create S3 object asset
#### 4.2 Upstream lineage
#### 4.3 Downstream lineage


### I have also created delete utility - delete_util/delete_util.py

## Executing the solution script
### Solution is also deployed on AWS Lambda
#### For running it follow step mentioned in below file - resource/command_to_invoke_lambda_from_local.md

### For running locally
#### Execute the main method in lambda_function.py
#### Please ensure that you have required pyatlan and boto3 lib installed