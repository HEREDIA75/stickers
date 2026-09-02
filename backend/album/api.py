import random
from typing import List
from django.db import transaction
from ninja import NinjaAPI, Schema
from .models import Especie, FigurinhaCapturada

api = NinjaAPI(title="Stickers Album API", version="1.0.0")


# --- Schemas ---
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


# --- Funções Auxiliares ---
def _popular_banco_se_vazio():
    """Popula o banco com espécies iniciais caso ainda não existam registros."""
    if not Especie.objects.exists():
        Especie.objects.bulk_create(
            [
                Especie(
                    nome_popular="Onça-Pintada",
                    nome_cientifico="Panthera onca",
                    dieta="Carnívoro",
                    habitat="Pantanal",
                    raridade="Lendário",
                    pontos_xp=500,
                ),
                Especie(
                    nome_popular="Mico-Leão-Dourado",
                    nome_cientifico="Leontopithecus rosalia",
                    dieta="Omnívoro",
                    habitat="Mata Atlântica",
                    raridade="Raro",
                    pontos_xp=250,
                ),
                Especie(
                    nome_popular="Capivara",
                    nome_cientifico="Hydrochoerus hydrochaeris",
                    dieta="Herbívoro",
                    habitat="Rios e Lagos",
                    raridade="Comum",
                    pontos_xp=50,
                ),
                Especie(
                    nome_popular="Arara-Juba",
                    nome_cientifico="Guaruba guarouba",
                    dieta="Frugívoro",
                    habitat="Florestas Tropicais",
                    raridade="Comum",
                    pontos_xp=100,
                ),
            ]
        )


# --- Endpoints ---
@api.get("/especies", response=List[EspecieSchema])
def listar_especies(request):
    _popular_banco_se_vazio()
    return Especie.objects.all()


@api.post("/capturar", response=CapturaResponse)
@transaction.atomic
def capturar_animal(request, payload: CapturaInput):
    _popular_banco_se_vazio()

    # Sorteia uma espécie cadastrada no banco
    especie_ids = Especie.objects.values_list("id", flat=True)
    especie_sorteada = Especie.objects.get(id=random.choice(list(especie_ids)))

    # Lógica de duplicidade de captura
    ja_possui = FigurinhaCapturada.objects.filter(especie=especie_sorteada).exists()

    # Se for repetida, concede apenas 10% do XP
    ganho_xp = (
        int(especie_sorteada.pontos_xp * 0.1)
        if ja_possui
        else especie_sorteada.pontos_xp
    )

    # Persiste o registro de captura no banco
    FigurinhaCapturada.objects.create(
        especie=especie_sorteada, foto_base64=payload.foto_base64
    )

    return {
        "sucesso": True,
        "especie": especie_sorteada,
        "ganho_xp": ganho_xp,
        "ja_possui": ja_possui,
    }
