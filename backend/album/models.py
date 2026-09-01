from django.db import models
from django.contrib.auth.models import User


class Especie(models.Model):
    RARIDADE_CHOICES = [
        ("comum", "Comum"),
        ("raro", "Raro"),
        ("lendario", "Lendário"),
    ]

    nome_popular = models.CharField(max_length=100)
    nome_cientifico = models.CharField(max_length=100, unique=True)
    dieta = models.CharField(max_length=100)
    habitat = models.CharField(max_length=150)
    raridade = models.CharField(
        max_length=10, choices=RARIDADE_CHOICES, default="comum"
    )
    pontos_xp = models.IntegerField(default=50)

    def __str__(self):
        return f"{self.nome_popular} ({self.nome_cientifico})"


class FigurinhaCapturada(models.Model):
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="figurinhas"
    )
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE)
    foto_base64 = models.TextField()
    data_captura = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("usuario", "especie")
