import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InventoryManagement95.settings')

# Create the Celery app
app = Celery('InventoryManagement95')

# Configure Celery using Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load tasks from all registered Django app configs
app.autodiscover_tasks()

# Configure periodic tasks
app.conf.beat_schedule = {
    'check-stock-levels': {
        'task': 'inventory.tasks.check_stock_levels',
        'schedule': crontab(hour='*/4'),  # Run every 4 hours
    },
}

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
