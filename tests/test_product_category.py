import io
from unittest.mock import patch

import pytest

from src.product_category import (BaseProduct, Category, LawnGrass, Product,
                                  Smartphone)


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


# --- Исправленные и дополненные тесты для повышения покрытия до 100% ---


def test_product_negative_price(capsys):
    """Проверка установки отрицательной цены."""
    p = Product("Тест", "Описание", 100.0, 5)
    p.price = -50.0
    assert p.price == 100.0  # Цена не должна измениться
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out


def test_product_zero_price(capsys):
    """Проверка установки нулевой цены."""
    p = Product("Тест", "Описание", 100.0, 5)
    p.price = 0.0
    assert p.price == 100.0  # Цена не должна измениться
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out


def test_product_zero_quantity():
    """Проверка работы с нулевым количеством."""
    p = Product("Тест", "Описание", 100.0, 0)
    assert p.quantity == 0
    assert p.price == 100.0


def test_addition_different_types_raises_error():
    """Проверка сложения разных типов (Product + Smartphone)."""
    p = Product("Базовый", "Описание", 100.0, 2)
    s = Smartphone("Смартфон", "Описание", 1000.0, 1, "95.5", "S23", 256, "Серый")

    with pytest.raises(TypeError, match="Нельзя складывать товары разных типов"):
        _ = p + s


def test_addition_invalid_operand_raises_error():
    """Проверка сложения с некорректным операндом."""
    p = Product("Тест", "Описание", 100.0, 5)

    with pytest.raises(
        TypeError, match="Нельзя складывать продукт с объектом другого типа"
    ):
        _ = p + "Не продукт"


def test_add_product_invalid_type():
    """Проверка добавления не-продукта в категорию."""
    cat = Category("Тест", "Описание", [])
    with pytest.raises(
        TypeError, match="Можно добавлять только экземпляры Product или его наследников"
    ):
        cat.add_product("Это не продукт")


def test_category_empty_initialization():
    """Проверка создания категории с пустым списком продуктов."""
    cat = Category("Пустая", "Без товаров", [])
    assert cat.name == "Пустая"
    assert len(cat.products) == 0
    assert cat.product_count == 0


def test_new_product_with_empty_list():
    """Проверка new_product с пустым списком продуктов."""
    data = {"name": "Новый", "description": "Тест", "price": 200.0, "quantity": 3}
    p = Product.new_product(data, [])
    assert p.name == "Новый"
    assert p.quantity == 3


def test_new_product_with_none_list():
    """Проверка new_product с products_list=None."""
    data = {"name": "Новый2", "description": "Тест2", "price": 300.0, "quantity": 4}
    p = Product.new_product(data, None)
    assert p.name == "Новый2"
    assert p.quantity == 4


def test_lawn_grass_instantiation():
    """Проверка создания экземпляра LawnGrass."""
    g = LawnGrass(
        "Трава",
        "Для газона",
        50.0,
        100,
        country="Россия",
        germination_period="7 дней",
        color="Зелёный",
    )
    assert g.country == "Россия"
    assert g.germination_period == "7 дней"


def test_baseproduct_cannot_be_instantiated():
    """Проверка, что BaseProduct нельзя создать напрямую."""
    with pytest.raises(TypeError):
        BaseProduct()


def test_addition_with_invalid_operand_type():
    """Проверка сложения с некорректным типом (без вызова ошибки)."""
    p = Product("A", "D", 100.0, 1)

    # Проверяем, что сложение с объектом, не имеющим __add__, вызывает ошибку
    class InvalidOperand:
        pass

    with pytest.raises(TypeError):
        p + InvalidOperand()


def test_add_product_with_invalid_type_in_list():
    """Проверка добавления некорректного типа в список продуктов."""
    cat = Category("Тест", "Описание", [])
    products = [Product("P", "D", 100.0, 1), "Не продукт"]

    with pytest.raises(TypeError):
        for p in products:
            cat.add_product(p)


def test_product_repr():
    """Проверка строкового представления объекта через repr."""
    p = Product("Тест", "Описание", 100.0, 5)
    expected = "Product('Тест', 'Описание', 100.0, 5)"
    assert repr(p) == expected


def test_new_product_with_duplicates():
    """Проверка объединения дубликатов через new_product."""
    products = []
    p1 = Product.new_product(
        {"name": "Телефон", "description": "Описание", "price": 10000.0, "quantity": 5},
        products,
    )
    products.append(p1)

    p2 = Product.new_product(
        {"name": "Телефон", "description": "Описание", "price": 12000.0, "quantity": 3},
        products,
    )

    assert p2.quantity == 8  # 5 + 3
    assert p2.price == 12000.0  # Максимальная цена


def test_middle_price_with_products():
    p1 = Product("P1", "D1", 100.0, 1)
    p2 = Product("P2", "D2", 200.0, 1)
    cat = Category("Кат", "Описание", [p1, p2])
    assert cat.middle_price() == 150.0


def test_middle_price_empty_category():
    cat = Category("Пустая", "Описание", [])
    assert cat.middle_price() == 0.0
