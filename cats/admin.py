from django.contrib import admin
from .models import Cat


class CatAdmin(admin.ModelAdmin):
    # Перечисляем поля, которые должны отображаться в админке
    list_display = ('pk', 'name', 'color', 'birth_year') 
    # Добавляем интерфейс для поиска по имени
    search_fields = ('name',) 
    # Добавляем возможность фильтрации по имени
    list_filter = ('name',)

# Register your models here.
admin.site.register(Cat, CatAdmin)
