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
