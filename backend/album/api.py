from ninja import NinjaAPI, Schema
from typing import List
from .models import Especie

api = NinjaAPI(title="Stickers Album API", version="1.0.0")


class EspecieSchema(Schema):
    id: int
    nome_popular: str
    nome_cientifico: str
    dieta: str
    habitat: str
    raridade: str
    pontos_xp: int


@api.get("/especies", response=List[EspecieSchema])
def listar_especies(request):
    return list(Especie.objects.all())
