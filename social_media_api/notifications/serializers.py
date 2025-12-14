from rest_framework import serializers

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.ReadOnlyField(source='actor.username')
    recipient = serializers.ReadOnlyField(source='recipient.username')
    target_type = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = (
            'id',
            'recipient',
            'actor',
            'verb',
            'target_type',
            'object_id',
            'is_read',
            'timestamp',
            'created_at',
        )
        read_only_fields = fields

    def get_target_type(self, obj):
        return obj.content_type.model if obj.content_type else None
