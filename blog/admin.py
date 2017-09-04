from django.contrib import admin
from .models import User, Profile, Article

models = User, Profile, Article

for model in models:
    admin.site.register(model)
