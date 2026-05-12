# tests/test_load_data.py

import json
import os
import tempfile

import pytest

from src.load_data import load_data_from_json
from src.product_category import Category, Product


def test_load_data_from_json_success():
    """Тест успешной загрузки данных из корректного JSON-файла."""
    # Создаём временный JSON-файл
    data = [
        {
            "name": "Смартфоны",
            "description": "Телефоны",
            "products": [
                {
                    "name": "Samsung Galaxy S23",
                    "description": "Флагман",
                    "price": 80000.0,
                    "quantity": 10,
                }
            ],
        }
    ]

    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=".json", encoding="utf-8"
    ) as tmp:
        json.dump(data, tmp, ensure_ascii=False)
        tmp_path = tmp.name

    try:
        categories = load_data_from_json(tmp_path)

        assert len(categories) == 1
        cat = categories[0]
        assert isinstance(cat, Category)
        assert cat.name == "Смартфоны"
        assert len(cat.products) == 1

        prod = cat.products[0]
        assert isinstance(prod, Product)
        assert prod.name == "Samsung Galaxy S23"
        assert prod.price == 80000.0
        assert prod.quantity == 10

    finally:
        os.unlink(tmp_path)


def test_load_data_from_json_empty_file():
    """Тест загрузки из пустого списка (корректный JSON, но без категорий)."""
    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=".json", encoding="utf-8"
    ) as tmp:
        json.dump([], tmp)
        tmp_path = tmp.name

    try:
        categories = load_data_from_json(tmp_path)
        assert categories == []
    finally:
        os.unlink(tmp_path)


def test_load_data_from_json_multiple_categories_and_products():
    """Тест загрузки нескольких категорий и товаров."""
    data = [
        {
            "name": "Категория 1",
            "description": "Описание 1",
            "products": [
                {"name": "Товар A", "description": "A", "price": 100.0, "quantity": 1},
                {"name": "Товар B", "description": "B", "price": 200.0, "quantity": 2},
            ],
        },
        {
            "name": "Категория 2",
            "description": "Описание 2",
            "products": [
                {"name": "Товар C", "description": "C", "price": 300.0, "quantity": 3},
            ],
        },
    ]

    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=".json", encoding="utf-8"
    ) as tmp:
        json.dump(data, tmp, ensure_ascii=False)
        tmp_path = tmp.name

    try:
        categories = load_data_from_json(tmp_path)
        assert len(categories) == 2
        assert len(categories[0].products) == 2
        assert len(categories[1].products) == 1
        assert categories[1].products[0].name == "Товар C"
    finally:
        os.unlink(tmp_path)


def test_load_data_from_json_file_not_found():
    """Тест обработки отсутствующего файла."""
    with pytest.raises(FileNotFoundError):
        load_data_from_json("non_existent_file_12345.json")


def test_load_data_from_json_invalid_json():
    """Тест обработки некорректного JSON."""
    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=".json", encoding="utf-8"
    ) as tmp:
        tmp.write("{ invalid json }")
        tmp_path = tmp.name

    try:
        with pytest.raises(json.JSONDecodeError):
            load_data_from_json(tmp_path)
    finally:
        os.unlink(tmp_path)


def test_load_data_from_json_missing_fields():
    """Тест обработки JSON с отсутствующими обязательными полями."""
    data = [
        {
            "name": "Без товаров",
            # отсутствует "description" и "products"
        }
    ]

    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=".json", encoding="utf-8"
    ) as tmp:
        json.dump(data, tmp)
        tmp_path = tmp.name

    try:
        with pytest.raises(KeyError):
            load_data_from_json(tmp_path)
    finally:
        os.unlink(tmp_path)
