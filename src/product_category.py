from typing import List, Optional


class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name.strip()
        self.description = description.strip()
        self.__price = price
        self.quantity = quantity

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
                    prod.__price = max(prod.__price, price)
                    return prod

        return cls(name, description, price, quantity)

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        if not isinstance(other, Product):
            raise TypeError("Нельзя складывать продукт с объектом другого типа")
        if type(self) is not type(other):  # ← строго одинаковые классы
            raise TypeError("Нельзя складывать товары разных типов")
        return self.price * self.quantity + other.price * other.quantity


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
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


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
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: List[Product]):
        self.name = name.strip()
        self.description = description.strip()
        self.__products: List[Product] = []
        for product in products:
            self.add_product(product)  # используем защищённый метод

        Category.category_count += 1
        # product_count обновляется в add_product

    def add_product(self, product: Product):
        if not isinstance(product, Product):
            raise TypeError(
                "Можно добавлять только экземпляры Product или его наследников"
            )
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        return "\n".join(str(product) for product in self.__products) + "\n"

    def __str__(self):
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def _get_products(self) -> List[Product]:
        return self.__products


class CategoryIterator:
    def __init__(self, category: Category):
        self._products = category._get_products()
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._products):
            raise StopIteration
        product = self._products[self._index]
        self._index += 1
        return product
