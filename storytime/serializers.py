from rest_framework import serializers
from .models import User, ChildProfile, Story, QuizQuestion, Recording, QuizResult

class ChildProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildProfile
        fields = ['id', 'name', 'avatar', 'color']


class QuizQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestion
        fields = ['question', 'options', 'correct_answer_index']

class StorySerializer(serializers.ModelSerializer):
    # Define quiz as a nested serializer (writable)
    quiz = QuizQuestionSerializer(many=True, required=False)

    class Meta:
        model = Story
        fields = ['id', 'title', 'author', 'category', 'age_range', 'script', 'quiz', 'default_audio']
        read_only_fields = ['created_by']

    def create(self, validated_data):
        # 1. Extract quiz data if present
        quiz_data = validated_data.pop('quiz', [])
        
        # 2. Create the Story instance first
        story = Story.objects.create(**validated_data)
        
        # 3. Loop through the quiz data and create QuizQuestion objects linked to the new story
        for q_data in quiz_data:
            QuizQuestion.objects.create(story=story, **q_data)
            
        return story

class RecordingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recording
        fields = '__all__'
        read_only_fields = ['parent', 'created_at']

class UserSerializer(serializers.ModelSerializer):
    children = ChildProfileSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'children', 'is_parent', 'is_staff']
        

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        # Use create_user to handle password hashing automatically
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_parent=True  # Automatically mark public registrations as Parents
        )
        return user