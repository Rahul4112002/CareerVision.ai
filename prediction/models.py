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



# New models for Skill Gap Analyzer feature
class Skill(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)  # e.g., "Technical", "Soft skill", etc.
    
    def __str__(self):
        return self.name

class JobRoleSkill(models.Model):
    job_role = models.CharField(max_length=100)  # e.g., "SE/SDE", "Analyst"
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    importance = models.IntegerField(default=5)  # Scale 1-10
    
    def __str__(self):
        return f"{self.job_role} - {self.skill.name}"

class LearningResource(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField()
    resource_type = models.CharField(max_length=50)  # e.g., "Course", "Video", "Book"
    is_free = models.BooleanField(default=True)
    provider = models.CharField(max_length=100, null=True, blank=True)  # e.g., "Coursera", "YouTube", "Udemy"
    
    def __str__(self):
        return self.title

class UserSkillGapAnalysis(models.Model):
    # No direct user relation since we're not using Django auth system in this project
    session_id = models.CharField(max_length=100)  # Store session ID to associate with a session
    job_role = models.CharField(max_length=100)
    current_skills = models.TextField()  # Store as JSON
    required_skills = models.TextField()  # Store as JSON
    skill_gaps = models.TextField()  # Store as JSON
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Analysis for {self.job_role} - {self.created_at}"