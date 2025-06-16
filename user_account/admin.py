from django.contrib import admin
from .models import User, RatingandReview

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    list_filter = ('join_date',)

admin.site.register(User, UserAdmin)
admin.site.register(RatingandReview)
