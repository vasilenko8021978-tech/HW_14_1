import pytest
from src.product_category import Product, Category


@pytest.fixture(autouse=True)
def reset_counters():
    """Сбрасывает счётчики перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0


def test_product_initialization():
    product = Product("Телефон", "Описание", 10000.0, 5)
    assert product.name == "Телефон"
    assert product.description == "Описание"
    assert product.price == 10000.0
    assert product.quantity == 5


def test_category_initialization():
    product = Product("Телефон", "Описание", 10000.0, 5)
    category = Category("Электроника", "Вся электроника", [product])

    assert category.name == "Электроника"
    assert category.description == "Вся электроника"
    assert len(category.products) == 1
    assert category.products[0] == product


def test_category_counters_via_instance_and_class():
    p1 = Product("P1", "Desc1", 100.0, 1)
    p2 = Product("P2", "Desc2", 200.0, 1)

    cat1 = Category("Категория 1", "Первая", [p1])
    assert cat1.category_count == 1
    assert cat1.product_count == 1
    assert Category.category_count == 1
    assert Category.product_count == 1

    cat2 = Category("Категория 2", "Вторая", [p2])
    assert cat2.category_count == 2
    assert cat2.product_count == 2
    assert Category.category_count == 2
    assert Category.product_count == 2


def test_main_scenario_like_in_14_1_main():
    # Эмулируем логику из main.py
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3]
    )

    assert category1.name == "Смартфоны"
    assert len(category1.products) == 3
    assert category1.category_count == 1
    assert category1.product_count == 3

    product4 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)
    category2 = Category(
        "Телевизоры",
        "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
        [product4]
    )

    assert Category.category_count == 2
    assert Category.product_count == 4