from django import template
from bbapp.models import Notification

register = template.Library()


def unseen_notifications(user):
    a = Notification.objects.filter(user=user,seen=False).count() + Notification.objects.filter(user=user,seen=True,bet__bet_status='Proposed').count()
    return a
    #replace the messages_set with the appropriate related_name, and also the filter field. (I am assuming it to be "read")

register.simple_tag(unseen_notifications)

def get_notifications(user):
    return Notification.objects.filter(user=user,seen=False)
    #replace the messages_set with the appropriate related_name, and also the filter field. (I am assuming it to be "read")

register.simple_tag(get_notifications)