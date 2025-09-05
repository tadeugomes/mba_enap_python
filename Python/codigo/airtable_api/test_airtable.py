from pyairtable import Table
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Airtable credentials from environment variables
AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
BASE_ID = os.getenv('AIRTABLE_BASE_ID')
TABLE_NAME = os.getenv('AIRTABLE_TABLE_NAME')

def read_airtable_data():
    try:
        # Initialize Airtable table directly
        table = Table(AIRTABLE_API_KEY, BASE_ID, TABLE_NAME)
        
        # Get all records from the table
        records = table.all()
        
        # Print each record
        i=0
        for record in records:
            i = i + 1
            print(f"Record ID: {record['id']}")
            print(f"Fields: {record['fields']}")
            print("-------------------")
            if i == 10:
                break
            
        return records
    
    except Exception as e:
        print(f"Error reading from Airtable: {str(e)}")
        return None

if __name__ == "__main__":
    read_airtable_data()
