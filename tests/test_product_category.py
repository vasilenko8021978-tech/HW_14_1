import io
from unittest.mock import patch

import pytest

from src.product_category import BaseProduct, Category, LawnGrass, Product, Smartphone


@pytest.fixture(autouse=True)
def reset_counters():
    """Сбрасывает глобальные счётчики перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0


# === Тесты из задания 14.1 ===


def test_product_initialization():
    p = Product("Телефон", "Описание", 10000.0, 5)
    assert p.name == "Телефон"
    assert p.description == "Описание"
    assert p.price == 10000.0
    assert p.quantity == 5


def test_category_initialization():
    p = Product("Телефон", "Описание", 10000.0, 5)
    cat = Category("Электроника", "Вся электроника", [p])
    assert cat.name == "Электроника"
    assert cat.description == "Вся электроника"
    # products — строка, поэтому считаем строки
    assert len(cat.products) == 1


def test_category_counters():
    p1 = Product("P1", "D1", 100.0, 1)
    p2 = Product("P2", "D2", 200.0, 1)

    Category("Кат1", "Первая", [p1])
    Category("Кат2", "Вторая", [p2])

    assert Category.category_count == 2
    assert Category.product_count == 2


# === Новая функциональность: задание 15.1 ===


def test_product_str():
    p = Product(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5
    )
    expected = "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт."
    assert str(p) == expected


def test_category_str():
    p1 = Product("P1", "D1", 100.0, 3)
    p2 = Product("P2", "D2", 200.0, 7)
    cat = Category("Смартфоны", "Описание", [p1, p2])
    expected = "Смартфоны, количество продуктов: 10 шт."
    assert str(cat) == expected


def test_category_products_property():
    p = Product("Телефон", "Описание", 10000.0, 5)
    cat = Category("Электроника", "Техника", [p])
    assert any("Телефон, 10000.0 руб. Остаток: 5 шт." in str(p) for p in cat.products)


def test_product_add():
    p1 = Product("A", "D", 100.0, 10)
    p2 = Product("B", "D", 200.0, 2)
    total = p1 + p2
    assert total == 1400.0  # 100*10 + 200*2


def test_product_add_type_error():
    p = Product("A", "D", 100.0, 1)
    with pytest.raises(TypeError):
        p + "not a product"

    with pytest.raises(TypeError):
        p + 42


# === Интеграционный тест: логика из 15.1_main.py ===


def test_main_scenario_15_1():
    product1 = Product(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5
    )
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    # Проверка __str__
    assert str(product1) == "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт."

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации...",
        [product1, product2, product3],
    )

    # Проверка __str__ категории
    assert "Смартфоны, количество продуктов: 27 шт." == str(category1)

    # Проверка сложения
    assert product1 + product2 == 180000.0 * 5 + 210000.0 * 8
    assert product1 + product3 == 180000.0 * 5 + 31000.0 * 14


def test_smartphone_inheritance():
    phone = Smartphone(
        "iPhone",
        "Описание",
        100000.0,
        5,
        efficiency="A15",
        model="13",
        memory=256,
        color="Серый",
    )
    assert phone.name == "iPhone"
    assert phone.model == "13"
    assert phone.memory == 256


def test_lawn_grass_inheritance():
    grass = LawnGrass(
        "Трава",
        "Для газона",
        100.0,
        50,
        country="Канада",
        germination_period="5 дней",
        color="Тёмно-зелёный",
    )
    assert grass.country == "Канада"
    assert grass.color == "Тёмно-зелёный"


def test_add_product_type_check():
    cat = Category("Тест", "Описание", [])
    with pytest.raises(TypeError):
        cat.add_product("не продукт")


def test_add_product_allows_subclasses():
    cat = Category("Тест", "Описание", [])
    phone = Smartphone("P", "D", 100.0, 1, "E", "M", 128, "C")
    cat.add_product(phone)
    assert len(cat.products) == 1


def test_addition_same_type():
    p1 = Product("A", "D", 100.0, 2)
    p2 = Product("B", "D", 200.0, 3)
    assert p1 + p2 == 800.0


def test_addition_different_types():
    p = Product("A", "D", 100.0, 1)
    s = Smartphone("S", "D", 200.0, 1, "E", "M", 128, "C")
    with pytest.raises(TypeError):
        p + s


def test_product_is_not_abstract():
    """Проверяем, что Product можно инстанцировать (реализует абстрактные методы)."""
    p = Product("Тест", "Описание", 100.0, 5)
    assert isinstance(p, BaseProduct)
    assert str(p) == "Тест, 100.0 руб. Остаток: 5 шт."
    assert (p + p) == 1000.0


def test_creation_logger_mixin():
    """Проверяем, что при создании объекта печатается repr."""
    with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
        p = Product("Тест", "Описание", 100.0, 5)
        assert p.name == "Тест"
        output = mock_stdout.getvalue()
        expected = "Product('Тест', 'Описание', 100.0, 5)\n"
        assert output == expected


def test_smartphone_instantiation():
    phone = Smartphone(
        "iPhone",
        "Desc",
        1000.0,
        2,
        efficiency="A15",
        model="13",
        memory=256,
        color="Black",
    )
    assert phone.model == "13"
    assert "iPhone" in str(phone)
