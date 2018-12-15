from decimal import Decimal


STARTER_DATA_FILES = {
    "inventory": r"starter_data/inventory_table.csv",
    "locations": r"starter_data/locations_table.csv",
    "products": r"starter_data/products_table.csv",
    "products_to_suppliers": r"starter_data/products_to_suppliers_table.csv",
    "menu_items": r"starter_data/menu_items_table.csv",
    "proportions": r"starter_data/proportions_table.csv",
    "suppliers": r"starter_data/suppliers_table.csv",
    "contacts": r"starter_data/contacts_table.csv",
    "users": r"starter_data/users_table.csv",
    "purchase_orders": r"starter_data/purchase_orders_table.csv",
    "purchase_order_contents": r"starter_data/purchase_order_contents_table.csv",
    "access_levels": r"starter_data/access_levels_table.csv",
    "employees": r"starter_data/employees_table.csv",
    "shelves_by_location": r"starter_data/shelves_by_location.csv"
}


CURRENCIES = [
    "AUD", "DKK", "JPY", "CAD", "NOK", "CHF", "SEK", "USD", "CZK",
    "PLN", "EUR", "HRK", "RON", "TRY", "BGN", "RSD", "GBP"
]


SUPERUSERS = {

    'super': {
        'username': 'super',
        'password_hash': '88020e6deccb21e4110b911e07489e2fb948e4c68bb8be2c21be87bb5e505a2c',
        'access_level_id': 0,
        'first_name': 'Super',
        'last_name': 'User',
        'location_id': 'BUD001',
        'department': 'IT',
        'role': 'God',
        'locality': 'Budapest',
        'phone_no': '(123) 456-7890',
        'email': 'superuser@inv-mgr.com',
        'address_line1': '1 Python street',
        'address_line2': '99th floor',
        'region': '',
        'postcode': '0000',
        'country': 'HU',
        'salary_huf': Decimal(9999999)
    }

}
