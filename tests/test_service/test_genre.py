from unittest.mock import MagicMock

import pytest

from dao.genre import GenreDAO
from dao.model.genre import Genre
from service.genre import GenreService
from setup_db import db


@pytest.fixture()
def genre_dao():
    genre_dao = GenreDAO(db.session)

    g1 = Genre(id=1, name="Dramedy")
    g2 = Genre(id=2, name='Killing soft')
    g3 = Genre(id=3, name='LOL KEK')

    genre_dao.get_one = MagicMock(return_value=g1)
    genre_dao.get_all = MagicMock(return_value=[g1, g2, g3])
    genre_dao.update = MagicMock()
    genre_dao.create = MagicMock()
    genre_dao.delete = MagicMock(return_value=Genre(id=3))
    return genre_dao


class TestGenreService:
    @pytest.fixture(autouse=True)
    def genre_dao(self, genre_dao):
        self.genre_dao = GenreService(genre_dao)

    def test_get_one(self):
        genre = self.genre_dao.get_one(1)
        assert genre is not None
        assert genre.id is not None

    def test_get_all(self):
        genres = self.genre_dao.get_all()
        assert len(genres) > 0

    def test_create(self):
        genre_data = {
            "name": "Comedy",
        }
        genre = self.genre_dao.create(genre_data)
        assert genre.id is not None

    def test_delete(self):
        self.genre_dao.delete(1)

    def test_update(self):
        genre_data = {
            "id": 3,
            "name": "Comedy",
        }
        self.genre_dao.update(genre_data)

    def test_partially_update(self):
        genre_data = {
            "id": 3,
            "name": "Giga",
        }
        self.genre_dao.partially_update(genre_data)

