from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
from .models import Story, ChildProfile, Recording, QuizResult
from .serializers import StorySerializer, ChildProfileSerializer, RecordingSerializer, RegisterSerializer

from django.contrib.auth import get_user_model
User = get_user_model()

from django.db.models import Q
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from .models import Story, ChildProfile
from .serializers import StorySerializer

class StoryViewSet(viewsets.ModelViewSet):
    serializer_class = StorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        # If user is a parent
        if user.is_parent:
            # Show: Global stories + their custom stories
            return Story.objects.filter(
                Q(created_by__isnull=True) | Q(created_by=user)
            )
        
        # If user is a child
        else:
            
            try:
                child_profile = user.child_profile  
                parent = child_profile.parent
                
                return Story.objects.filter(
                    Q(created_by__isnull=True) | Q(created_by=parent)
                )
            except:
                # Fallback: Only global stories if no parent found
                return Story.objects.filter(created_by__isnull=True)

    def perform_create(self, serializer):
        if self.request.user.is_staff:
            serializer.save()  
        else:
            serializer.save(created_by=self.request.user)

class ChildViewSet(viewsets.ModelViewSet):
    serializer_class = ChildProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only show children belonging to the logged-in parent
        return ChildProfile.objects.filter(parent=self.request.user)

    def perform_create(self, serializer):
        serializer.save(parent=self.request.user)

class RecordingViewSet(viewsets.ModelViewSet):
    serializer_class = RecordingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Recording.objects.filter(parent=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(parent=self.request.user)
    
    @action(detail=False, methods=['get'])
    def check_audio(self, request):
        """
        Custom endpoint for the Frontend 'Smart Audio Logic'.
        Call: /api/recordings/check_audio/?story_id=1&child_id=5
        """
        story_id = request.query_params.get('story_id')
        child_id = request.query_params.get('child_id')
        
        # Check if specific recording exists for this child
        recording = Recording.objects.filter(
            parent=request.user, 
            story_id=story_id, 
            for_child_id=child_id
        ).first()
        
        if recording:
            return Response({'audio_url': recording.audio_file.url})
        
        # Fallback: Check if there is a general recording for this story by this parent
        recording = Recording.objects.filter(
            parent=request.user, 
            story_id=story_id, 
            for_child__isnull=True
        ).first()

        if recording:
            return Response({'audio_url': recording.audio_file.url})
            
        return Response({'audio_url': None}) # Frontend will play default



class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]



