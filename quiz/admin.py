from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Attempt)
admin.site.register(Answer)
admin.site.register(SelectedOptions)
