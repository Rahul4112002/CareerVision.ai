from django.contrib import admin
from .models import Roadmap, Question, Choice

class RoadmapAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'image_tag')

    # Optional: To show the image in the form as well
    readonly_fields = ('image_tag',)

admin.site.register(Roadmap, RoadmapAdmin)

admin.site.register(Question)
admin.site.register(Choice)
