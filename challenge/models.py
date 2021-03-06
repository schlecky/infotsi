from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.


class Epreuve(models.Model):
    titre = models.CharField(max_length=50, default="")
    enonce = models.TextField(default="")
    test = models.TextField(default="")
    points = models.IntegerField(default=0)
    difficulte = models.IntegerField(default=0)

    def __str__(self):
        return "*"*self.difficulte+self.titre

    class Meta:
        order_with_respect_to = 'difficulte'


class Etudiant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    estClasse = models.BooleanField(default=True)
    estDoublePrenom = models.BooleanField(default=False)
    CPGE1 = 0
    CPGE2 = 1
    ANCIENS = 2
    PROFS = 3
    AUTRE = 4
    choixGroupes = (
            (CPGE1, "CPGE 1"),
            (CPGE2, "CPGE 2"),
            (ANCIENS, "Anciens"),
            (PROFS, "Profs"),
            (AUTRE, "Autre"),
            )
    groupe = models.IntegerField(choices = choixGroupes, default=CPGE1)

    def nomGroupe(self):
        return self.choixGroupes[self.groupe][1]

    def __str__(self):
        return self.user.last_name+" "+self.user.first_name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Etudiant.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.etudiant.save()


class Code(models.Model):
    epreuve = models.ForeignKey(Epreuve, on_delete=models.CASCADE)
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    code = models.TextField(default="")
    score = models.IntegerField(default=0)

    def __str__(self):
        return str(self.epreuve)+"-"+self.etudiant.user.username

class Notification(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    message = models.TextField(default="")
    def __str__(self):
        return str(self.date)+"-"+self.message

