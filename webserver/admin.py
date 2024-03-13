from django.contrib import admin
from .models import *


class DetailsAccessAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'employe' , 'heure')

class EmployeAdmin(admin.ModelAdmin):
    list_display = ('matricule', 'nom', 'prenom', 'fonction', 'date_created')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not obj:  # Prepopulate the field only for new records
            last_employe = Employe.objects.order_by('-matricule').first()
            if last_employe:
                last_matricule = int(last_employe.matricule[3:])  # Extract the numeric part
                new_matricule = f"EMP{last_matricule + 1:03d}"
            else:
                new_matricule = "EMP001"
            form.base_fields['matricule'].initial = new_matricule
        return form


class StagiaireAdmin(admin.ModelAdmin):
    list_display = ('matricule', 'nom', 'prenom', 'département_svc', 'date_created')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not obj:  # Prepopulate the field only for new records
            last_stagiaire = Stagiaire.objects.order_by('-matricule').first()
            if last_stagiaire:
                last_matricule = int(last_stagiaire.matricule[3:])  # Extract the numeric part
                new_matricule = f"STA{last_matricule + 1:03d}"
            else:
                new_matricule = "STA001"
            form.base_fields['matricule'].initial = new_matricule
        return form

class ArriveeRetourEmployeAdmin(admin.ModelAdmin):
    list_display = ('id', 'employe', 'date', 'heure_arrive', 'heure_retour')  # Add all the columns you want to display



class ProfilAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'password', 'date_created')  # Add all the columns you want to display
    
    

admin.site.register(Employe, EmployeAdmin)
admin.site.register(ArriveeRetourEmploye, ArriveeRetourEmployeAdmin)
admin.site.register(Profil, ProfilAdmin)
admin.site.register(DetailsAccess, DetailsAccessAdmin)

