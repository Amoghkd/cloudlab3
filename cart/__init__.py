import json
from cart import dao
from products import Product, get_product


class Cart:
    def __init__(self, id: int, username: str, contents: list[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data):
        return Cart(data['id'], data['username'], data['contents'], data['cost'])


def get_cart(username: str) -> list[Product]:
    """
    Retrieve the user's cart with product details.
    """
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []

    # Use a list comprehension for efficiency
    items = [
        item
        for cart_detail in cart_details
        for item in json.loads(cart_detail['contents'])  # Replace `eval` with `json.loads` for safety and speed
    ]

    # Reduce repeated database calls with bulk fetching
    product_ids = set(items)
    products_map = {product.id: product for product in get_product_bulk(product_ids)}

    return [products_map[item] for item in items if item in products_map]


def get_product_bulk(product_ids: set[int]) -> list[Product]:
    """
    Fetch product details in bulk to reduce database calls.
    """
    return products.get_products_by_ids(product_ids)


def add_to_cart(username: str, product_id: int):
    """
    Add a product to the user's cart.
    """
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int):
    """
    Remove a product from the user's cart.
    """
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str):
    """
    Delete the user's cart.
    """
    dao.delete_cart(username)
