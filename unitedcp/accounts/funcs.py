from django.core.cache import cache
from unitedcp.models import PanelLogs


def get_latest_actions(user_id, amount):
    if not user_id:
        return False

    latest_logins = PanelLogs.objects.values().filter(code=1, user=user_id).order_by('-date').all()[:amount]
    latest_actions = PanelLogs.objects.values().filter(user=user_id).exclude(code=1).order_by('-date').all()[:amount]

    return {
        'LatestLogins': latest_logins,
        'LatestActions': latest_actions
    }
