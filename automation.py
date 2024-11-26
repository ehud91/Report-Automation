import schedule
from exporter import DataExporter
from datetime import datetime, timedelta
from mailer import send_email

def main():
    today = datetime.now()
    sheet_name = "Booking_Data.xlsx"

    if today.weekday() == 0: # Check if it's Monday (0 means Monday)
        start_timestamp = (today - timedelta(days=7)
            ).replace(hour=0, minute=0, second=0, microsecond=0)
        
        end_timestamp = (today - timedelta(days=1)
            ).replace(hour=23, minutes=59, second=59, microsecond=0)
        
        sheet_name = "Weekly_Report.xlsx"
    elif today.day == 29:
        # It's the 1st day of the month, fetch data for the last month
        start_timestamp = (today.replace(day=1) - timedelta(days=1)
            ).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_timestamp = (today.replace(day=1) - timedelta(days=1)
            ).replace(hour=23, minute=59, second=59, microsecond=0)
        sheet_name = "Monthly_Report"