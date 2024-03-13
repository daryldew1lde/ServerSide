from django.db import models
from django.contrib.auth.hashers import make_password
from datetime import date, datetime, timedelta

class Employe(models.Model):
    matricule = models.CharField(max_length=6, primary_key=True)
    nom = models.TextField(blank=True, null=True)
    prenom = models.TextField(blank=True, null=True)
    fonction = models.TextField(blank=True, null=True)
    date_created = models.DateField(default=date.today)
   

    def save(self, *args, **kwargs):
        if not self.matricule:
            last_employe = Employe.objects.order_by('-matricule').first()
            if last_employe:
                last_matricule = int(last_employe.matricule[3:])  # Extract the numeric part
                new_matricule = f"EMP{last_matricule + 1:03d}"
            else:
                new_matricule = "EMP001"
            self.matricule = new_matricule
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.matricule})"


class Stagiaire(models.Model):
    matricule = models.CharField(max_length=6, primary_key=True)
    nom = models.TextField(blank=True, null=True)
    prenom = models.TextField(blank=True, null=True)
    département_svc = models.TextField(blank=True, null=True)
    date_created = models.DateField(default=date.today)

    def save(self, *args, **kwargs):
        if not self.matricule:
            last_stagiaire = Stagiaire.objects.order_by('-matricule').first()
            if last_stagiaire:
                last_matricule = int(last_stagiaire.matricule[3:])  # Extract the numeric part
                new_matricule = f"STA{last_matricule + 1:03d}"
            else:
                new_matricule = "STA001"
            self.matricule = new_matricule
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.matricule})"

class Profil(models.Model):
    id = models.TextField(primary_key=True)
    description = models.TextField(blank=True, null=True)
    password = models.TextField()
    date_created = models.DateField(default=date.today)

    def save(self, *args, **kwargs):
        # Hash the password before saving
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.id



class ArriveeRetourEmploye(models.Model):
    date = models.DateField()
    heure_arrive = models.TimeField(blank=True, null=True)
    heure_retour = models.TimeField(blank=True, null=True)
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='arrivee_retour_employe')

    class Meta:
        unique_together = ('date', 'employe')
        ordering = ['-date', '-heure_arrive']
 

    def time_spent(self):
        if self.heure_retour:
            heure_arrive_dt = datetime.combine(datetime.today(), self.heure_arrive)
            heure_retour_dt = datetime.combine(datetime.today(), self.heure_retour)
            time_diff = heure_retour_dt - heure_arrive_dt

            # Check if the time difference is more than 2 hours
            if time_diff > timedelta(hours=2):
                adjusted_time_diff = time_diff - timedelta(hours=2)
            else:
                adjusted_time_diff = time_diff

            hours = adjusted_time_diff.seconds // 3600
            minutes = (adjusted_time_diff.seconds // 60) % 60
            time_spent_formatted = f"{hours:02d}:{minutes:02d}"
            return time_spent_formatted
        else:
            return 'Non disponible'
            
        
    

    def __str__(self):
        return f"ArriveeRetourEmploye: {self.date} - {self.employe}"

class DetailsAccess(models.Model):
    date = models.DateField()
    heure = models.TimeField(blank=True, null=True)
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='details_access')

    class Meta:
        ordering = ['-date', 'heure']
    
    

class ArriveeRetourStagiaire(models.Model):
    date = models.DateField()
    heure_arrive = models.TimeField(blank=True, null=True)
    heure_retour = models.TimeField(blank=True, null=True)
    stagiaire = models.ForeignKey(Stagiaire, on_delete=models.CASCADE, related_name='arrivee_retour_stagiaire')

    class Meta:
        unique_together = ('date', 'stagiaire')

    def __str__(self):
        return f"ArriveeRetourStagiaire: {self.date} - {self.stagiaire}"