import pytest
from product_category import Product, Category


@pytest.fixture
def sample_product():
    return Product("Смартфон", "Мощный смартфон", 50000.0, 10)


@pytest.fixture
def sample_category(sample_product):
    return Category("Электроника", "Техника для дома и офиса", [sample_product])


def test_product_initialization(sample_product):
    assert sample_product.name == "Смартфон"
    assert sample_product.description == "Мощный смартфон"
    assert sample_product.price == 50000.0
    assert sample_product.quantity == 10


def test_category_initialization(sample_category):
    assert sample_category.name == "Электроника"
    assert sample_category.description == "Техника для дома и офиса"
    assert len(sample_category.products) == 1
    assert sample_category.products[0].name == "Смартфон"


def test_category_counters():
    # Обнулим счётчики перед тестом (для изоляции)
    Category.total_categories = 0
    Category.total_products = 0

    p1 = Product("Телевизор", "4K TV", 80000.0, 5)
    p2 = Product("Ноутбук", "Игровой ноутбук", 120000.0, 3)

    Category("Бытовая техника", "Для дома", [p1])
    Category("Компьютеры", "Гаджеты", [p2])

    assert Category.total_categories == 2
    assert Category.total_products == 2  # 1 товар в cat1 + 1 товар в cat2
