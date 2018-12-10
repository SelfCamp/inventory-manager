update_stock_level_for_inventory_id = """
    UPDATE inventory SET quantity = %(new_level)s
    WHERE inventory_id = %(inventory_id)s
"""
