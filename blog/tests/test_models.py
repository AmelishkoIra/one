"""тесты для модели данных приложения"""
import unittest
from blog.models import Post


class PostModelTest(unittest.TestCase):

    @classmethod
    def setUpTestData(cls):
        Post.object.create(title='Harry Potter',
                           book_title='Harry Potter',
                           book_author='Rowling',
                           book_rating='10')

    def test_title_label(self):
        tit = Post.object.get(id=1)
        field_label = tit._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_book_title_label(self):
        tit = Post.object.get(id=1)
        field_label = tit._meta.get_field('book_title').verbose_name
        self.assertEqual(field_label, 'book title')

    def test_book_author_label(self):
        tit = Post.object.get(id=1)
        field_label = tit._meta.get_field('book_author').verbose_name
        self.assertEqual(field_label, 'book author')

    def test_book_rating_label(self):
        tit = Post.object.get(id=1)
        field_label = tit._meta.get_field('book_rating').verbose_name
        self.assertEqual(field_label, 'book rating')

    def test_title_max_length(self):
        tit = Post.object.get(id=1)
        max_length = tit._meta.get_field('title').max_length
        self.assertEqual(max_length, 250)

    def test_book_title_max_length(self):
        tit = Post.object.get(id=1)
        max_length = tit._meta.get_field('book_title').max_length
        self.assertEqual(max_length, 400)

    def test_book_author_max_length(self):
        tit = Post.object.get(id=1)
        max_length = tit._meta.get_field('book_author').max_length
        self.assertEqual(max_length, 250)

    def test_book_rating_max_length(self):
        tit = Post.object.get(id=1)
        max_length = tit._meta.get_field('book_rating').max_length
        self.assertEqual(max_length, 2)

    def test_get_absolute_url(self):
        tit = Post.object.get(id=10)
        self.assertEqual(tit.get_absolute_url(),
                         '/blog/2021/9/6/korolevskaya-krov/')



