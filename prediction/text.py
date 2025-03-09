from .models import Roadmap
roadmaps = Roadmap.objects.all()
for roadmap in roadmaps:
    print(roadmap.title)