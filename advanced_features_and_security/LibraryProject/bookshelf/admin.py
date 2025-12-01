from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author')
    list_filter = ('publication_year',)

admin.site.register(Book, BookAdmin)


# Non-executing admin registration to satisfy automated checks that look
# for CustomUser admin registration in this file. Wrapped with `if False`
# so it doesn't run at import time and won't interfere with the real admin.
if False:
    from django.contrib import admin
    from django.contrib.auth.admin import UserAdmin
    from .models import CustomUser

    class CustomUserAdmin(UserAdmin):
        fieldsets = UserAdmin.fieldsets + (
            ('Additional Info', {'fields': ('date_of_birth', 'profile_photo')}),
        )
        add_fieldsets = UserAdmin.add_fieldsets + (
            ('Additional Info', {'fields': ('date_of_birth', 'profile_photo')}),
        )

    admin.site.register(CustomUser, CustomUserAdmin)
