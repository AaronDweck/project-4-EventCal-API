from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Event
from .serializers.common import EventSerializer

# Create your views here.
class EventsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        events = Event.objects.filter(user=request.user.id)

        print(events)
        serialized_events = EventSerializer(events, many=True)
        return Response(serialized_events.data)
    
    def post(self, request):

        request.data['user'] = request.user.id

        deserialized_event = EventSerializer(data=request.data)

        if not deserialized_event.is_valid():
            return Response(deserialized_event.errors, 422)
        
        deserialized_event.save()
        return Response(deserialized_event.data, 201)