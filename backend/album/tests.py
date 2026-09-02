from django.test import TestCase
from django.contrib.auth.models import User
from album.models import Especie, FigurinhaCapturada


class EspecieModelTest(TestCase):
    def setUp(self):
        self.especie = Especie.objects.create(
            nome_popular="Onça-Pintada",
            nome_cientifico="Panthera onca",
            dieta="Carnívoro",
            habitat="Pantanal",
            raridade="lendario",
            pontos_xp=500,
        )

    def test_criacao_especie(self):
        self.assertEqual(self.especie.nome_popular, "Onça-Pintada")
        self.assertEqual(self.especie.pontos_xp, 500)


class APIAlbumTest(TestCase):
    def setUp(self):
        Especie.objects.create(
            nome_popular="Capivara",
            nome_cientifico="Hydrochoerus hydrochaeris",
            dieta="Herbívoro",
            habitat="Rios e Lagos",
            raridade="comum",
            pontos_xp=50,
        )

    def test_endpoint_listar_especies(self):
        response = self.client.get("/api/especies")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["nome_popular"], "Capivara")
