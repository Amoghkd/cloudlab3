from products import dao


class Product:
    def __init__(self, id: int, name: str, description: str, cost: float, qty: int = 0):
        self.id = id
        self.name = name
        self.description = description
        self.cost = cost
        self.qty = qty

    @staticmethod
    def load(data: dict):
        """
        Load a product instance from a dictionary.
        """
        return Product(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            cost=data['cost'],
            qty=data.get('qty', 0)  # Default to 0 if not present
        )


def list_products() -> list[Product]:
    """
    Retrieve all products from the database.
    """
    # Optimize by processing in bulk and avoiding redundant object creation
    products_data = dao.list_products()
    return [Product.load(product) for product in products_data]


def get_product(product_id: int) -> Product:
    """
    Retrieve a single product by its ID, with optimized error handling.
    """
    product_data = dao.get_product(product_id)
    if not product_data:
        raise ValueError(f"Product with ID {product_id} not found.")
    return Product.load(product_data)


def get_products_by_ids(product_ids: set[int]) -> list[Product]:
    """
    Retrieve multiple products by their IDs in bulk, avoiding redundant queries.
    """
    if not product_ids:
        return []
    products_data = dao.get_products_by_ids(product_ids)  # Bulk fetch
    return [Product.load(product) for product in products_data]


def add_product(product: dict):
    """
    Add a new product to the database with validation.
    """
    if 'id' not in product or 'name' not in product:
        raise ValueError("Product must include 'id' and 'name'.")
    dao.add_product(product)


def update_qty(product_id: int, qty: int):
    """
    Update the quantity of a product, validating input to avoid negative values.
    """
    if qty < 0:
        raise ValueError("Quantity cannot be negative.")
    dao.update_qty(product_id, qty)
