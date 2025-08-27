from decimal import Decimal
import boto3
import csv
from io import StringIO
from datetime import datetime

# ----- AWS Configuration -----
REGION = 'us-east-1'
S3_BUCKET = 'weather-data-processed-142857'
DYNAMO_TABLE_NAME = 'weather_summary'

# ----- AWS Clients -----
s3 = boto3.client('s3', region_name=REGION)
dynamodb = boto3.resource('dynamodb', region_name=REGION)
table = dynamodb.Table(DYNAMO_TABLE_NAME)

# ----- Helper function to generate ID -----
def generate_id(date_str, hour_str):
    return int(date_str.replace("_","") + hour_str)  # e.g., 2025082709

# ----- Aggregate function -----
def process_hourly_aggregates():
    try:
        resp = s3.list_objects_v2(Bucket=S3_BUCKET)
    except Exception as e:
        print(f"Error listing S3 objects: {e}")
        return

    for obj in resp.get('Contents', []):
        key = obj['Key']
        try:
            data = s3.get_object(Bucket=S3_BUCKET, Key=key)['Body'].read().decode('utf-8')
            reader = csv.DictReader(StringIO(data))
            rows = list(reader)
            if not rows:
                continue
        except Exception as e:
            print(f"Error reading {key}: {e}")
            continue

        # Group rows by hour
        hourly_data = {}
        for row in rows:
            date = row['date']  # e.g., "2025-08-27"
            time_str = row['time']  # e.g., "05:11"
            hour = time_str.split(":")[0]  # e.g., "05"

            datehour = f"{date.replace('-','_')}_{hour}"  # e.g., "2025_08_27_05"

            # Skip the last incomplete hour
            # Determine if this hour is the latest hour in the file
            last_row_time = rows[-1]['time']
            last_row_hour = last_row_time.split(":")[0]
            if hour == last_row_hour:
                continue

            if datehour not in hourly_data:
                hourly_data[datehour] = {
                    'temps': [],
                    'humidity': [],
                    'country': row['country']
                }

            hourly_data[datehour]['temps'].append(float(row['temp_c']))
            hourly_data[datehour]['humidity'].append(float(row['humidity']))

        # Write aggregates to DynamoDB
        for datehour, values in hourly_data.items():
            temps = values['temps']
            humidity = values['humidity']
            avg_temp = round(sum(temps)/len(temps), 2)
            min_temp = min(temps)
            max_temp = max(temps)
            avg_humidity = round(sum(humidity)/len(humidity), 2)

            # Generate numeric ID
            id_num = generate_id(datehour.split("_")[0]+"_"+datehour.split("_")[1]+"_"+date>

            try:
                table.put_item(Item={
                        'datehour': datehour,
                        'ID': id_num,
                        'country': values['country'],
                        'avg_temp': Decimal(str(avg_temp)),
                        'min_temp': Decimal(str(min_temp)),
                        'max_temp': Decimal(str(max_temp)),
                        'avg_humidity': Decimal(str(avg_humidity))
                                })

                print(f"Processed {datehour} -> DynamoDB")
            except Exception as e:
                print(f"Error writing {datehour} to DynamoDB: {e}")

# ----- Main -----
if __name__ == "__main__":
    process_hourly_aggregates()


