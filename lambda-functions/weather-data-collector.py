import os
import json
import boto3
import csv
import io
from datetime import datetime
import urllib.request
import urllib.parse

s3 = boto3.client('s3')
BUCKET_NAME = "weather-data-raw-142857"   # <-- your bucket name

def lambda_handler(event, context):
    api_key = os.environ.get("WEATHER_API_KEY")
    if not api_key:
        raise Exception("WEATHER_API_KEY environment variable not set")
    city = os.environ.get("WEATHER_CITY", "Cairo")

    params = urllib.parse.urlencode({"key": api_key, "q": city})
    url = f"http://api.weatherapi.com/v1/current.json?{params}"

    # Fetch data
    with urllib.request.urlopen(url, timeout=15) as resp:
        data = json.loads(resp.read().decode())

    # Build record
    record = {
        "city": data["location"]["name"],
        "country": data["location"]["country"],
        "temp_c": data["current"]["temp_c"],
        "humidity": data["current"]["humidity"],
        "condition": data["current"]["condition"]["text"],
        "timestamp": datetime.utcnow().isoformat()
    }

    # Daily file name: weather_DD_MM_YYYY.csv
    filename = f"raw_weather_{datetime.utcnow().strftime('%d_%m_%Y')}.csv"

    # Try to fetch existing file from S3
    try:
        existing_obj = s3.get_object(Bucket=BUCKET_NAME, Key=filename)
        existing_data = existing_obj['Body'].read().decode('utf-8')

        # Load existing CSV into buffer
        csv_buffer = io.StringIO(existing_data)
        reader = csv.DictReader(csv_buffer)
        rows = list(reader)

    except s3.exceptions.NoSuchKey:
        rows = []  # No file yet, start fresh

    # Append new record
    rows.append(record)

    # Write all rows back to CSV
    csv_buffer = io.StringIO()
    writer = csv.DictWriter(csv_buffer, fieldnames=record.keys())
    writer.writeheader()
    writer.writerows(rows)

    # Upload updated file to S3 (overwrite)
    s3.put_object(Bucket=BUCKET_NAME, Key=filename, Body=csv_buffer.getvalue())

    return {"statusCode": 200, "body": json.dumps(f"Appended record to {filename}")}

