# Embarca Challenge – AWS Step Functions Pipeline

This project was developed as a solution to Embarca's technical challenge, using **AWS Step Functions**, **Lambda Functions**, and **S3** to orchestrate the processing of a JSON input file.

## 🎯 Objective

Implement a serverless orchestration flow with AWS Step Functions, where:

- A JSON file stored in an S3 bucket is read;
- The data is processed and transformed using Lambda functions;
- The execution flow is managed and monitored through Step Functions.

## 🧰 Technologies and Services Used

- **AWS S3** – Input file storage
- **AWS Lambda** – Serverless data processing functions
- **AWS Step Functions** – Orchestration and control flow
- **AWS IAM** – Security and access control
- **AWS CLI / SDK** – Programmatic interaction with AWS services

## 📁 Project Structure

```
embarca-challenge/
├── lambdas/
│   ├── read_s3_data/
│   ├── process_data/
│   └── write_output/
├── state_machine/
│   └── step_function_definition.json
├── input/
│   └── inp_2023-09-20T14-29-57-ec.json  # Input file from S3
├── README.md
└── template.yaml  # Optional SAM or CloudFormation template
```

## 📂 Input File Details

The input file is stored in the following S3 bucket:

```
Bucket: embarca-challenge
File: input/inp_2023-09-20T14-29-57-ec.json
```

You can download it via the AWS CLI:

```bash
aws s3 cp s3://embarca-challenge/input/inp_2023-09-20T14-29-57-ec.json .
```

## 🚀 How to Run Locally (with AWS CLI or SAM)

### 1. Configure Credentials

Add to `~/.aws/credentials`:

```
[embarca-challenge]
aws_access_key_id = ABC
aws_secret_access_key = +123
```

And in `~/.aws/config`:

```
[profile embarca-challenge]
region = us-east-1
output = json
```

### 2. Test S3 Access

```bash
aws s3 ls s3://embarca-challenge --profile embarca-challenge
```

### 3. Deploy (optional, using AWS SAM)

```bash
sam build
sam deploy --guided
```

## 📎 Challenge Resources

- Challenge instructions repo:  
  https://github.com/ArcaSolucoes/data-embarca-challange-public

- Credentials file (⚠️ **Do not commit this**):  
  https://storage.3.basecamp.com/4828415/blobs/c90a143c-7a80-11ee-8a62-b2d1a80aa527/download/embarca-challenge_credentials.csv

## 🔐 Security Notice

> ⚠️ The credentials provided are **temporary and limited**.  
> **Never expose access keys in public repositories.**  
> Ensure this repository remains private, or remove all credential-related data before publishing.

## 📜 License

This project is intended solely for use as part of the Embarca technical challenge.  
Do not distribute or reuse without prior authorization.
