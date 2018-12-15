read_stock_level_for_product_id = """
    SELECT inv.location_id, inv.quantity, inv.expiration_date, inv.rack_no, inv.shelf_no,
           prod.name, prod.unit
    FROM inventory inv JOIN products prod
    ON inv.product_id = prod.product_id
    WHERE prod.product_id = %(product_id)s
    ORDER BY inv.location_id, inv.expiration_date
"""

read_available_suppliers = """
    SELECT suppliers.supplier_id, suppliers.name, products.name AS "supplies", contacts.email, contacts.phone_no 
    FROM suppliers JOIN products_to_suppliers ON suppliers.supplier_id = products_to_suppliers.product_id 
    JOIN products ON products.product_id = products_to_suppliers.product_id 
    JOIN contacts ON contacts.contact_id = suppliers.contact_id
"""

read_inventory = """
    SELECT inv.location_id, inv.quantity, inv.expiration_date, inv.rack_no, inv.shelf_no,
           prod.name, prod.unit
    FROM inventory inv JOIN products prod
    ON inv.product_id = prod.product_id
    ORDER BY prod.name, inv.location_id, inv.expiration_date
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

read_stock_level_for_inventory_id = """
    SELECT inv.location_id, inv.quantity, inv.expiration_date, inv.rack_no, inv.shelf_no,
           prod.name, prod.unit
    FROM inventory inv JOIN products prod
    ON inv.product_id = prod.product_id
    WHERE inv.inventory_id = %(inventory_id)s
"""

read_user_info = """
    SELECT username, access_levels.access_level_id AS access_level_id, first_name, last_name, location_id, department, role, locality,
           phone_no, email, address_line1, address_line2, region, postcode, country, salary_huf
    FROM users
    JOIN access_levels ON users.access_level_id = access_levels.access_level_id
    JOIN employees ON users.employee_id = employees.employee_id
    JOIN contacts ON contacts.contact_id = employees.employee_id
    WHERE username = %(username)s
"""

read_inventory_on_location = """
    SELECT products.name, quantity, shelf_no, rack_no, expiration_date FROM inventory
    JOIN products ON inventory.product_id = products.product_id
    WHERE location_id = %(location_id)s
    ORDER BY name
"""

read_inventory_for_menu_item_on_location = """
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

read_max_portions_by_ingredient_for_menu_item_on_location = f"""
    SELECT
        menu_item_name,
        product_name,
        CONCAT(SUM(available), ' ', unit) AS amount,
        FLOOR(SUM(available/needed_per_portion)) AS portions
    FROM ({read_inventory_for_menu_item_on_location})
        AS read_inventory_for_menu_item_on_location
    GROUP BY product_name, unit
"""

read_max_portions_for_menu_item_on_location = f"""
    SELECT
        menu_item_name,
        MIN(portions) AS can_make
    FROM ({read_max_portions_by_ingredient_for_menu_item_on_location})
        AS read_max_portions_by_ingredient_for_menu_item_on_location
    GROUP BY menu_item_name
"""
