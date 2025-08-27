import boto3
import csv
import os
from datetime import datetime
import io

s3 = boto3.client("s3")

RAW_BUCKET = "weather-data-raw-142857"
PROCESSED_BUCKET = "weather-data-processed-142857"

def lambda_handler(event, context):
    # Get uploaded file info
    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    object_key = event["Records"][0]["s3"]["object"]["key"]

    # Download raw CSV to /tmp
    download_path = f"/tmp/{os.path.basename(object_key)}"
    s3.download_file(bucket_name, object_key, download_path)

    # Read CSV and take only the last line
    last_row = None
    with open(download_path, "r") as infile:
        reader = list(csv.DictReader(infile))
        if reader:
            last_row = reader[-1]

    if not last_row:
        return {"statusCode": 400, "body": "Raw CSV is empty."}

    # Transform the row
    ts = datetime.fromisoformat(last_row["timestamp"])
    processed_row = {
        "country": last_row["country"].lower(),
        "city": last_row["city"].lower(),
        "temp_c": last_row["temp_c"],
        "humidity": last_row["humidity"],
        "condition": last_row["condition"].lower(),
        "date": ts.date().isoformat(),
        "time": ts.time().strftime("%H:%M")
    }

    # Determine processed file name
    raw_filename = os.path.basename(object_key)  # e.g. raw_weather_27_08_2025.csv
    date_part = raw_filename.replace("raw_weather_", "")  # 27_08_2025.csv
    processed_filename = f"processed_weather_{date_part}"  # processed_weather_27_08_2025.csv

    # Check if processed file exists
    try:
        existing_obj = s3.get_object(Bucket=PROCESSED_BUCKET, Key=processed_filename)
        existing_data = existing_obj['Body'].read().decode('utf-8')
        csv_buffer = io.StringIO(existing_data)
        writer = csv.DictWriter(csv_buffer, fieldnames=processed_row.keys())
        csv_buffer.seek(0, io.SEEK_END)  # ✅ Move cursor to end before appending
        writer.writerow(processed_row)
        upload_data = csv_buffer.getvalue()
    except s3.exceptions.NoSuchKey:
        # File doesn't exist → create new with header
        csv_buffer = io.StringIO()
        writer = csv.DictWriter(csv_buffer, fieldnames=processed_row.keys())
        writer.writeheader()
        writer.writerow(processed_row)
        upload_data = csv_buffer.getvalue()

    # Upload to processed bucket
    s3.put_object(Bucket=PROCESSED_BUCKET, Key=processed_filename, Body=upload_data)

    return {
        "statusCode": 200,
        "body": f"Processed last row from {object_key} and saved to {processed_filename}"
    }
