read_global_inventory = """
    SELECT
        inventory.location_id,
        inventory.product_id,
        products.name,
        inventory.inventory_id,
        inventory.quantity,
        products.unit,
        inventory.rack_no,
        inventory.shelf_no,
        inventory.expiration_date,
        inventory.po_id
    FROM inventory JOIN products
    ON inventory.product_id = products.product_id
    ORDER BY products.name, location_id, expiration_date
"""

read_local_inventory = f"""
    SELECT *
    FROM ({read_global_inventory})
        AS read_global_inventory
    WHERE location_id = %(location_id)s
"""

read_global_inventory_for_product_id = f"""
    SELECT *
    FROM ({read_global_inventory})
        AS read_global_inventory
    WHERE product_id = %(product_id)s
"""

read_local_inventory_for_product_id = f"""
    SELECT *
    FROM ({read_global_inventory_for_product_id})
        AS read_global_inventory_for_product_id
    WHERE location_id = %(location_id)s
"""

read_global_stock_level_for_product_id = f"""
    SELECT name, SUM(quantity) AS total_stock, unit
    FROM ({read_global_inventory_for_product_id})
        AS read_global_inventory_for_product_id
"""

read_local_stock_level_for_product_id = f"""
    SELECT name, SUM(quantity) AS total_stock, unit
    FROM ({read_local_inventory_for_product_id})
        AS read_local_inventory_for_product_id
"""

read_global_inventory_for_inventory_id = f"""
    SELECT *
    FROM ({read_global_inventory})
        AS read_global_inventory
    WHERE inventory_id = %(inventory_id)s
"""

# TODO ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓

read_local_inventory_for_menu_item = """
    SELECT
        menu_items.name AS 'menu_item_name',
        products.name AS 'product_name',
        proportions.amount AS 'needed_per_portion',
        inventory.quantity AS 'available',
        products.unit,
        inventory.rack_no,
        inventory.shelf_no,
        expiration_date
    FROM menu_items
        JOIN proportions ON menu_items.menu_item_id = proportions.menu_item_id
		JOIN products ON proportions.ingredient_id = products.product_id
		JOIN inventory ON products.product_id = inventory.product_id
    WHERE location_id = %(location_id)s AND menu_items.menu_item_id = %(menu_item_id)s
    ORDER BY products.name, expiration_date
"""

read_local_max_portions_by_ingredient_for_menu_item = f"""
    SELECT
        menu_item_name,
        product_name,
        CONCAT(SUM(available), ' ', unit) AS amount,
        FLOOR(SUM(available/needed_per_portion)) AS portions
    FROM ({read_local_inventory_for_menu_item})
        AS read_local_inventory_for_menu_item
    GROUP BY product_name, unit
"""

read_local_max_portions_for_menu_item = f"""
    SELECT
        menu_item_name,
        MIN(portions) AS can_make
    FROM ({read_local_max_portions_by_ingredient_for_menu_item})
        AS read_local_max_portions_by_ingredient_for_menu_item
    GROUP BY menu_item_name
"""

# TODO ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑

read_available_suppliers = """
    SELECT suppliers.supplier_id, suppliers.name, products.name AS "supplies", contacts.email, contacts.phone_no 
    FROM suppliers JOIN products_to_suppliers ON suppliers.supplier_id = products_to_suppliers.product_id 
    JOIN products ON products.product_id = products_to_suppliers.product_id 
    JOIN contacts ON contacts.contact_id = suppliers.contact_id
"""

read_po_status_for_po_id = """
    SELECT
        suppliers.name AS supplier,
        date_ordered,
        date_eta,
        date_arrived,
        CONCAT(first_name, ' ', last_name) AS signee,
        purchase_orders.status AS po_status
    FROM purchase_orders
        LEFT JOIN suppliers ON purchase_orders.supplier_id = suppliers.supplier_id
        LEFT JOIN employees ON purchase_orders.signee_id = employees.employee_id
    WHERE po_id = %(po_id)s
"""

read_user_info = """
    SELECT username, access_levels.access_level_id AS access_level_id, first_name, last_name, location_id, department,
    role, locality, phone_no, email, address_line1, address_line2, region, postcode, country, salary_huf
    FROM users
    JOIN access_levels ON users.access_level_id = access_levels.access_level_id
    JOIN employees ON users.employee_id = employees.employee_id
    JOIN contacts ON contacts.contact_id = employees.employee_id
    WHERE username = %(username)s
"""
