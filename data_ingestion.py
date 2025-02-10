import time
import json
import requests
import boto3
from botocore.exceptions import ClientError

# Configuration Variables
KINESIS_STREAM_NAME = 'LATransitStream'
REGION_NAME = 'us-west-2'  # Adjust based on your AWS region
TRANSIT_API_URL = 'https://api.metro.net/LACMTA/route_overview'
POLL_INTERVAL = 30  # seconds

# Initialize the Kinesis client
kinesis_client = boto3.client('kinesis', region_name=REGION_NAME)

def fetch_transit_data():
    """
    Poll the LA Metro transit API for real-time data.
    Returns the data as a JSON object.
    """
    try:
        response = requests.get(TRANSIT_API_URL)
        response.raise_for_status()
        # Assuming the API returns JSON data. If it's in Protobuf, add a parsing step here.
        data = response.json()
        return data
    except requests.RequestException as e:
        print(f"Error fetching transit data: {e}")
        return None

def push_to_kinesis(record):
    """
    Push a single record to the AWS Kinesis stream.
    """
    try:
        # Convert the record (Python dict) to a JSON string
        data_str = json.dumps(record)
        # response = kinesis_client.put_record(
        #     StreamName=KINESIS_STREAM_NAME,
        #     Data=data_str,
        #     PartitionKey="LA_Transit"  # Using a constant partition key for simplicity; consider a dynamic key for load balancing
        # )
        # print(f"Record sent to Kinesis. Sequence Number: {response.get('SequenceNumber')}")

        print(data_str)
    except ClientError as e:
        print(f"Error sending record to Kinesis: {e}")

def main():
    while True:
        # Step 1: Fetch data from the transit API
        transit_data = fetch_transit_data()
        if transit_data:
            # Optionally, process or filter data here if needed.
            # Step 2: Push each relevant record to Kinesis. If the API returns a batch, iterate over the records.
            # Here, we assume the data has a key 'entity' that holds a list of vehicle positions.
            for record in transit_data:
                push_to_kinesis(record)
        else:
            print("No data received in this iteration.")
        
        # Wait for the next polling cycle
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
