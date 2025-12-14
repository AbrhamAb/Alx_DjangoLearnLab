from typing import Optional

from django.contrib.contenttypes.models import ContentType

from .models import Notification


def create_notification(*, recipient, actor, verb: str, target: Optional[object] = None) -> Optional[Notification]:
    if recipient == actor:
        return None
    content_type = None
    object_id = None
    if target is not None:
        content_type = ContentType.objects.get_for_model(target)
        object_id = target.pk
    return Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb=verb,
        content_type=content_type,
        object_id=object_id,
    )
