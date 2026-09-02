import random
from ninja import NinjaAPI, Schema
from typing import List
from django.shortcuts import get_object_or_404
from .models import Especie, FigurinhaCapturada

api = NinjaAPI(title="Stickers Album API", version="1.0.0")


class EspecieSchema(Schema):
    id: int
    nome_popular: str
    nome_cientifico: str
    dieta: str
    habitat: str
    raridade: str
    pontos_xp: int


class CapturaInput(Schema):
    foto_base64: str


class CapturaResponse(Schema):
    sucesso: bool
    especie: EspecieSchema
    ganho_xp: int
    ja_possui: bool


@api.get("/especies", response=List[EspecieSchema])
def listar_especies(request):
    return list(Especie.objects.all())


@api.post("/capturar", response=CapturaResponse)
def capturar_animal(request, payload: CapturaInput):
    especies = Especie.objects.all()
    if not especies.exists():
        # Popula o banco caso esteja vazio para testes
        Especie.objects.create(
            nome_popular="Onça-Pintada",
            nome_cientifico="Panthera onca",
            dieta="Carnívoro",
            habitat="Pantanal",
            raridade="lendario",
            pontos_xp=500,
        )
        Especie.objects.create(
            nome_popular="Mico-Leão-Dourado",
            nome_cientifico="Leontopithecus rosalia",
            dieta="Omnívoro",
            habitat="Mata Atlântica",
            raridade="raro",
            pontos_xp=250,
        )
        Especie.objects.create(
            nome_popular="Capivara",
            nome_cientifico="Hydrochoerus hydrochaeris",
            dieta="Herbívoro",
            habitat="Rios e Lagos",
            raridade="comum",
            pontos_xp=50,
        )
        Especie.objects.create(
            nome_popular="Arara-Juta",
            nome_cientifico="Ara macao",
            dieta="Frugívoro",
            habitat="Florestas Tropicais",
            raridade="comum",
            pontos_xp=100,
        )
        especies = Especie.objects.all()

    # Simulação da IA selecionando uma espécie aleatória do banco
    especie_sorteada = random.choice(list(especies))

    # Verifica duplicidade no banco ou ajusta XP
    ganho_xp = especie_sorteada.pontos_xp

    return {
        "sucesso": True,
        "especie": especie_sorteada,
        "ganho_xp": ganho_xp,
        "ja_possui": False,
    }
