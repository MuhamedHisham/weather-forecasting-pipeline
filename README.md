# -*- coding: utf-8 -*-

readme_content = """
# **Serverless Weather Forecasting Pipeline**

## **Overview**
This project implements a **serverless, automated weather data processing system** on AWS. It fetches raw weather data from an external API, processes it, aggregates it hourly, stores it in DynamoDB, and exposes it via a REST API. The system demonstrates **event-driven architecture, serverless components, and automated EC2 aggregation**.

## **Architecture Diagram**
<img width="2880" height="2360" alt="Hourly Weather Aggregation   API" src="https://github.com/user-attachments/assets/7de6b54a-338d-4021-b627-d32fc53fba56" />

**High-level Flow:**  
**EventBridge → Weather Collector Lambda → S3 Raw Bucket → Weather Processor Lambda → S3 Processed Bucket → EC2 Aggregation Script → DynamoDB → API Gateway → Lambda API Handler → Users**

## **AWS Services Used**
- **Amazon S3** – Stores raw and processed CSV data  
- **AWS Lambda** – Collects weather data, processes CSVs, and serves API  
- **Amazon EC2** – Runs hourly aggregation script  
- **Amazon DynamoDB** – Stores hourly aggregated weather data  
- **Amazon API Gateway** – Exposes `/weather` REST API endpoint  
- **Amazon EventBridge** – Triggers collector Lambda hourly  
- **AWS IAM** – Manages roles and permissions  

## **Data Flow**
1. **EventBridge** triggers the **Weather Collector Lambda** hourly.  
2. **Lambda** fetches data from the **external Weather API**.  
3. **Raw CSV data** is stored in **S3 Raw Bucket**.  
4. **Weather Processor Lambda** is triggered by new files in **S3 Raw Bucket**, processes the CSV, and stores results in **S3 Processed Bucket**.  
5. **EC2 Aggregation Script** reads processed CSVs, aggregates fully completed hours, and stores results in **DynamoDB**.  
6. **API Lambda Handler** serves data from DynamoDB through the `/weather` endpoint exposed via **API Gateway**.  

## **Setup Instructions**
1. **Clone the repository:**  
```bash
git clone https://github.com/yourusername/weather-forecasting-pipeline.git
cd weather-forecasting-pipeline
```
2. **Install Python dependencies:**  
```bash
pip install -r requirements.txt
```
3. **Deploy AWS resources:**  
- Create **S3 buckets** for raw and processed data.
- Create **DynamoDB table** with **datehour** as **partition key** and **ID** as **sort key**.
- Deploy **Lambda functions** for collector, processor, and API handler.
- Launch **EC2 instance** for aggregation script, configure cron to run hourly.
- Set up **EventBridge rule** to trigger collector Lambda every hour.
- Configure **IAM roles** with proper permissions for Lambda, EC2, S3, and DynamoDB.

**Usage Example**
To fetch hourly aggregated weather data:
```bash
curl https://l1d7b8v0s6.execute-api.us-east-1.amazonaws.com/prod/weather?datehour=2025_08_27_05
```
**Sample response:**
```json
[
  {
    'max_temp': Decimal('27.3'),
    'avg_humidity': Decimal('59.44'),
    'min_temp': Decimal('26.1'),
    'avg_temp': Decimal('26.72'),
    'datehour': '2025_08_27_05',
    'ID': Decimal('2025082705'),
    'country': 'egypt'
  }
]
```
















