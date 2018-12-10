read_stock_level_for_product_id = f"""
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

read_stock_level_for_inventory_id = """
    SELECT inv.location_id, inv.quantity, inv.expiration_date, inv.rack_no, inv.shelf_no,
           prod.name, prod.unit
    FROM inventory inv JOIN products prod
    ON inv.product_id = prod.product_id
    WHERE inv.inventory_id = %(inventory_id)s
"""
