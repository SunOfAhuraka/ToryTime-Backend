from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User Model
class User(AbstractUser):
    is_parent = models.BooleanField(default=True)

class ChildProfile(models.Model):
    parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='children')
    name = models.CharField(max_length=100)
    avatar = models.CharField(max_length=10, default='👶')
    color = models.CharField(max_length=20, default='#FF6B9D')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} (Child of {self.parent.username})"

class Story(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100, default="Admin")
    category = models.CharField(max_length=50)
    age_range = models.CharField(max_length=20)
    script = models.TextField()
    duration = models.CharField(max_length=20, default="5 min") 
    default_audio = models.FileField(upload_to='audio/', null=True, blank=True)
    cover_image = models.ImageField(upload_to='covers/', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} by {self.author}"

class QuizQuestion(models.Model):
    story = models.ForeignKey(Story, related_name='quiz', on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    # This stores ["Option A", "Option B", "Option C", "Option D"]
    options = models.JSONField() 
    correct_answer_index = models.IntegerField()
    
    def __str__(self):
        return f"Question for {self.story.title}: {self.question}"

class Recording(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    parent = models.ForeignKey(User, on_delete=models.CASCADE)
    for_child = models.ForeignKey(ChildProfile, on_delete=models.SET_NULL, null=True, blank=True)
    audio_file = models.FileField(upload_to='audio/recordings/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Recording of {self.story.title} by {self.parent.username}"


class QuizResult(models.Model):
    child = models.ForeignKey(ChildProfile, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    date_taken = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"QuizResult: {self.child.name} - {self.story.title} ({self.score}/{self.total_questions})"