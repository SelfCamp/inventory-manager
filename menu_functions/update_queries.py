update_quantity_for_inventory_id = """
    UPDATE inventory SET quantity = %(new_quantity)s
    WHERE inventory_id = %(inventory_id)s
"""
