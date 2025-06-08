import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    # Filter messages by conversation participant user ids and date range
    # Assuming your Message model has 'created_at' DateTimeField and 'conversation' ForeignKey

    # Filter by start date (created_at >=)
    start_date = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    # Filter by end date (created_at <=)
    end_date = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    # Filter by conversation participants: custom method filter
    participants = django_filters.CharFilter(method='filter_by_participants')

    class Meta:
        model = Message
        fields = ['start_date', 'end_date', 'participants']

    def filter_by_participants(self, queryset, name, value):
        # 'value' is comma-separated user IDs, e.g. "1,2"
        user_ids = value.split(',')
        # Filter messages where conversation participants include any of the user_ids
        return queryset.filter(conversation__participants__id__in=user_ids).distinct()
