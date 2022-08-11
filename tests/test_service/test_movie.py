from unittest.mock import MagicMock

import pytest

from dao.movie import MovieDAO
from dao.model.movie import Movie
from service.movie import MovieService
from setup_db import db


@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(db.session)

    m1 = Movie(id=1, title="test_1", description='test_1', trailer='test_1', year=2001, rating=4.8, genre_id=4,
               director_id=7)
    m2 = Movie(id=2, title="test_2", description='test_2', trailer='test_2', year=2002, rating=4.8, genre_id=4,
               director_id=7)
    m3 = Movie(id=3, title="test_3", description='test_3', trailer='test_3', year=2003, rating=4.8, genre_id=4,
               director_id=7)

    movie_dao.get_one = MagicMock(return_value=m1)
    movie_dao.get_all = MagicMock(return_value=[m1, m2, m3])
    movie_dao.update = MagicMock()
    movie_dao.create = MagicMock()
    movie_dao.delete = MagicMock(return_value=Movie(id=3))
    return movie_dao


class TestGenreService:
    @pytest.fixture(autouse=True)
    def movie_dao(self, movie_dao):
        self.movie_dao = MovieService(movie_dao)

    def test_get_one(self):
        movie = self.movie_dao.get_one(1)
        assert movie is not None
        assert movie.id is not None

    def test_get_all(self):
        movies = self.movie_dao.get_all()
        assert len(movies) > 0

    def test_create(self):
        movie_data = {
            "title": 'TESTTEST',
            "description": 'TESTTEST',
            "trailer": 'TESTTEST',
            "year": 3002,
            "rating": 3.1,
            'genre_id': 5,
            "director_id": 8,

        }
        movie = self.movie_dao.create(movie_data)
        assert movie.id is not None

    def test_delete(self):
        self.movie_dao.delete(1)

    def test_update(self):
        movie_data = {
            "id": 3,
            "title": 'TESTTEST',
            "description": 'TESTTEST',
            "trailer": 'TESTTEST',
            "year": 3002,
            "rating": 2.1,
            'genre_id': 5,
            "director_id": 8,
        }
        self.movie_dao.update(movie_data)

    def test_partially_update(self):
        movie_data = {
            "id": 3,
            "trailer": 'TESTTEST',
            "year": 3002,
            "rating": 2.1,
        }
        self.movie_dao.partially_update(movie_data)
