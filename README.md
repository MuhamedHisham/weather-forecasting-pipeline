Serverless Weather Forecasting Pipeline
Overview

This project implements a serverless, automated weather data processing system on AWS. It fetches raw weather data from an external API, processes it, aggregates it hourly, stores it in DynamoDB, and exposes it via a REST API. The system demonstrates event-driven architecture, serverless components, and automated EC2 aggregation.

Architecture Diagram

High-level Flow:
EventBridge → Weather Collector Lambda → S3 Raw Bucket → Weather Processor Lambda → S3 Processed Bucket → EC2 Aggregation Script → DynamoDB → API Gateway → Lambda API Handler → Users

AWS Services Used

Amazon S3 – Stores raw and processed CSV data

AWS Lambda – Collects weather data, processes CSVs, and serves API

Amazon EC2 – Runs hourly aggregation script

Amazon DynamoDB – Stores hourly aggregated weather data

Amazon API Gateway – Exposes /weather REST API endpoint

Amazon EventBridge – Triggers collector Lambda hourly

AWS IAM – Manages roles and permissions

Data Flow

EventBridge triggers the Weather Collector Lambda hourly.

Lambda fetches data from the external Weather API.

Raw CSV data is stored in S3 Raw Bucket.

Weather Processor Lambda is triggered by new files in S3 Raw Bucket, processes the CSV, and stores results in S3 Processed Bucket.

EC2 Aggregation Script reads processed CSVs, aggregates fully completed hours, and stores results in DynamoDB.

API Lambda Handler serves data from DynamoDB through the /weather endpoint exposed via API Gateway.
