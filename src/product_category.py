from typing import List, Optional


class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @property
    def price(self) -> float:
        """Геттер для цены."""
        return self.__price

    @price.setter
    def price(self, value: float):
        """Сеттер с проверкой на положительность."""
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return
        # Для автоматических тестов input закомментирован
        # if value < self.__price:
        #     confirm = input(f"Подтвердите понижение цены с {self.__price} до {value} (y/n): ")
        #     if confirm.lower() != 'y':
        #         print("Действие отменено")
        #         return
        self.__price = value

    @classmethod
    def new_product(
        cls, product_data: dict, products_list: Optional[List["Product"]] = None
    ) -> "Product":
        """Создаёт продукт из словаря, объединяет дубли."""
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


class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: List[Product]):
        self.name = name
        self.description = description
        self.__products = products

        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product: Product):
        """Добавляет продукт в категорию."""
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Возвращает строку со всеми товарами."""
        result = ""
        for product in self.__products:
            result += f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.\n"
        return result
