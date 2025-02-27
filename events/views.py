from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from .models import Event
from .serializers.common import EventSerializer

# Create your views here.
class EventsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        events = Event.objects.filter(user=request.user.id)

        serialized_events = EventSerializer(events, many=True)
        return Response(serialized_events.data)
    
    def post(self, request):

        request.data['user'] = request.user.id

        deserialized_event = EventSerializer(data=request.data)

        if not deserialized_event.is_valid():
            return Response(deserialized_event.errors, 422)
        
        deserialized_event.save()
        return Response(deserialized_event.data, 201)
    
class EventsDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, event_id):
        try:
            event = Event.objects.get(id=event_id)

        except Event.DoesNotExist as error:
            print(error)
            raise NotFound('Event not found')
        
        print (event.user)
        print (self.request.user)
        if event.user != self.request.user:
            raise PermissionDenied('You are unauthorized to make these changes')
            
        return event

    def patch(self, request, event_id):

        event = self.get_object(event_id)

        serialized_event = EventSerializer(event, data=request.data, partial=True)

        if not serialized_event.is_valid():
            return Response(serialized_event.errors, 422)
        
        serialized_event.save()

        return Response(serialized_event.data)