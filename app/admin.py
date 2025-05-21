from django.contrib import admin
from .models import (
    PersonalAcademic,
    Student,
    Searcher,
    Thesis,
    Memory,
    Commentaire,
    Author,
)

# Register your models here.
admin.site.register(Student)
admin.site.register(Searcher)
admin.site.register(Thesis)
admin.site.register(Memory)
admin.site.register(Commentaire)
admin.site.register(Author)
