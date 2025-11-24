from django.contrib import admin
from .models import User, ChildProfile, Story, QuizQuestion, Recording, QuizResult

admin.site.register(User)
admin.site.register(ChildProfile)
admin.site.register(Story)
admin.site.register(QuizQuestion)
admin.site.register(Recording)
admin.site.register(QuizResult)
