from django.core.management.base import BaseCommand
import pandas as pd
from your_app.models import UserActivity  # Replace with the correct model

class Command(BaseCommand):
    help = 'Fetches user activity data for anomaly detection'

    def handle(self, *args, **options):
        # Query relevant database table
        data = pd.DataFrame(list(UserActivity.objects.all().values()))  # Adjust model and fields as needed
        
        # Example: Save data to CSV (optional)
        data.to_csv('user_activity_data.csv', index=False)
        
        # Or process directly (for anomaly detection)
        self.stdout.write(self.style.SUCCESS('Successfully fetched user activity data'))
