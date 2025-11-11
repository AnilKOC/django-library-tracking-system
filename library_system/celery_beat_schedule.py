from celery.schedules import crontab, schedule

CELERY_BEAT_SCHEDULE = {
    "send-overdue-loan-notification": {
        "task": "library.tasks.send_overdue_loan_notification",
        "schedule": crontab(),
    },
    "send-notification-to-overdued-loans": {
        "task": "send_notification_to_overdued_loans",
        "schedule": crontab(hour="8"),
    },
}
