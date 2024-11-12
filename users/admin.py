from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser  # Importer le modèle CustomUser

# Personnalisation de l'interface d'administration pour le modèle CustomUser
class CustomUserAdmin(UserAdmin):
    # Champs à afficher dans la liste des utilisateurs
    list_display = ('phone_number', 'email', 'is_active', 'is_staff', 'is_superuser')
    
    # Champs sur lesquels il est possible de rechercher dans l'admin
    search_fields = ('phone_number', 'email')
    
    # Définir la disposition des champs dans le formulaire de modification et de création
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Informations personnelles', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )
    
    ordering = ('phone_number',)

# Enregistrement du modèle CustomUser avec son admin personnalisé
admin.site.register(CustomUser, CustomUserAdmin)
