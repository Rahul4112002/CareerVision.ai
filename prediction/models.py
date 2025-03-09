from django.db import models
from django.utils.html import format_html
class Roadmap(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='roadmaps/')
    pdf = models.FileField(upload_to='roadmaps/')
    average_salary = models.IntegerField(null=True, blank=True)  # New field
    verified_by = models.CharField(max_length=255, null=True, blank=True)  # New field
    
    
    created_at = models.DateTimeField(auto_now_add=True)
    def image_tag(self):
        return format_html('<img src="/media/{}" style="width:40px;height:40px; "/>'.format(self.image))
    def __str__(self):
        return self.title
    
class Question(models.Model):
    question_text = models.CharField(max_length=255)
    
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text
