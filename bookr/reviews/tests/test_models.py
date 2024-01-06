from django.test import TestCase, Client, RequestFactory
from reviews.models import Publisher, Contributor, Book

def TestContributorModel(TestCase):
    def setUp(self):
        self.c = Contributor(
            first_names='Test',
            last_names='Contributor',
            email='test@contributor.com'
        )

    def test_create_contributor(self):
        self.assertIsInstance(self.c, Contributor)

    def test_str_representation(self):
        self.assertIsEqual(str(self.c), 'Test')


    def TestBookModel(TestCase):
        def setUp(self):
            self.publisher = Publisher(
                name='Packt',
                website='www.packt.com',
                email='contact@packt.com'
            )
            self.contributor = Contributor(
                first_names='Test',
                last_names='Contributor',
                email='test@contributor.com'
            )

        def test_create_book(self):
            book = Book(
                title='Test Book',
                publication_date='2000-01-01',
                isbn='000000000',
                publisher=self.publisher,
                contributors=[self.contributor]
            )
            self.assertIsInstance(book, Book)