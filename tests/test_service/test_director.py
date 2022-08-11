from unittest.mock import MagicMock

import pytest

from dao.director import DirectorDAO
from dao.model.director import Director
from service.director import DirectorService
from setup_db import db


@pytest.fixture()
def director_dao():
    director_dao = DirectorDAO(db.session)

    d1 = Director(id=1, name="Spirit Jack")
    d2 = Director(id=2, name='Josh Cornell')
    d3 = Director(id=3, name='Blab Blab')

    director_dao.get_one = MagicMock(return_value=d1)
    director_dao.get_all = MagicMock(return_value=[d1, d2, d3])
    director_dao.update = MagicMock()
    director_dao.create = MagicMock()
    director_dao.delete = MagicMock(return_value=Director(id=3))
    return director_dao

class TestDirectorService:
    @pytest.fixture(autouse=True)
    def director_service(self, director_dao):
        self.director_service = DirectorService(director_dao)

    def test_get_one(self):
        director = self.director_service.get_one(1)
        assert director is not None
        assert director.id is not None

    def test_get_all(self):
        directors = self.director_service.get_all()
        assert len(directors) > 0

    def test_create(self):
        director_data = {
            "name": "Ivan",
        }
        director = self.director_service.create(director_data)
        assert director.id is not None

    def test_delete(self):
        self.director_service.delete(1)

    def test_update(self):
        director_data = {
            "id": 3,
            "name": "Ivan",
        }
        self.director_service.update(director_data)

    def test_partially_update(self):
        director_data = {
            "id": 3,
            "name": "OLOLOLloLOLO",
        }
        self.director_service.partially_update(director_data)

