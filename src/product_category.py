# src/product_category.py

from abc import ABC, abstractmethod
from typing import List, Optional


class BaseProduct(ABC):
    """Абстрактный базовый класс для всех продуктов."""

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __add__(self, other) -> float:
        pass


class CreationLoggerMixin:
    """Миксин: логирует создание объекта через repr при инициализации."""

    def __init__(self, *args, **kwargs):
        # Не вызываем super() — только логируем
        print(repr(self))


class Product(BaseProduct, CreationLoggerMixin):
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name.strip()
        self.description = description.strip()
        self.__price = price
        self.quantity = quantity
        # Вызываем миксин после инициализации полей
        CreationLoggerMixin.__init__(self)

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, value: float):
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return
        self.__price = value

    @classmethod
    def new_product(
        cls, product_data: dict, products_list: Optional[List["Product"]] = None
    ) -> "Product":
        name = product_data["name"]
        description = product_data["description"]
        price = product_data["price"]
        quantity = product_data["quantity"]

        if products_list:
            for prod in products_list:
                if prod.name == name:
                    prod.quantity += quantity
                    if price > prod.price:
                        prod.price = price
                    return prod

        return cls(name, description, price, quantity)

    def __str__(self) -> str:
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: "Product") -> float:
        if not isinstance(other, Product):
            raise TypeError("Нельзя складывать продукт с объектом другого типа")
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать товары разных типов")
        return self.price * self.quantity + other.price * other.quantity

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"'{self.name}', '{self.description}', {self.price}, {self.quantity}"
            f")"
        )


class Smartphone(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: str,
        model: str,
        memory: int,
        color: str,
    ):
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color
        super().__init__(name, description, price, quantity)


class LawnGrass(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ):
        self.country = country
        self.germination_period = germination_period
        self.color = color
        super().__init__(name, description, price, quantity)


class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: List[Product]):
        self.name = name.strip()
        self.description = description.strip()
        self.__products: List[Product] = []
        for product in products:
            self.add_product(product)
        Category.category_count += 1

    def add_product(self, product: Product):
        if not isinstance(product, Product):
            raise TypeError(
                "Можно добавлять только экземпляры Product или его наследников"
            )
        self.__products.append(product)
        Category.product_count += 1

    def middle_price(self) -> float:
        """Возвращает средний ценник всех товаров в категории.

        Если категория пуста (деление на ноль), возвращает 0.
        """
        try:
            total = sum(product.price for product in self.__products)
            return total / len(self.__products)
        except ZeroDivisionError:
            return 0.0

    @property
    def products(self) -> List[Product]:
        """Возвращаем список, чтобы len(category.products) работало корректно."""
        return self.__products

    def __str__(self) -> str:
        total = sum(p.quantity for p in self.__products)
        return f"{self.name}, количество продуктов: {total} шт."
