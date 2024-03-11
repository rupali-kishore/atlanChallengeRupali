# Below are the steps to run solution lambda
## Step 1- Use below credential to authenticate (use aws configure)
### Access key ID
AKIAYGCSFMVTZ53HJXPN
### Secret access key
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
### region
us-east-1

## Step 2 Execution lamda using below command. Required asset will be create with suffix provide in payload
aws lambda invoke \
--function-name challengeLambda \
--payload '{"suffix": "rupali-atlan-dev"}' \
--cli-binary-format raw-in-base64-out \
lambda_output.log