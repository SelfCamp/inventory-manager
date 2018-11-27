# inventory-manager
SelfCamp's first project, aimed at database practice with MySQL &amp; Python


- STANDARDS
  - design choices
    - no duplicate prefixes (only ids are prefixed with nature of record/table)
    - single-table data duplication ('switch') in favor of multi-table spawning
      (e.g. with `products_to_suppliers`, `proportions`, `purchase_order_contents`)
  - *temporarily* simplify reality to speed up delivery / enable working early prototype
    - we only sell pizza, nothing else
    - we always buy the same item from the same place (no multiple suppliers for the same item)
    - we don't care about items that were semi-prepared (e.g. 100 pizza doughs were made but not baked yet)
    - no database maintenance (data integrity doesn't matter, we always reset to default values for testing)
    - we assume a perfect FIFO system (same type of item from multiple sources / orders are all stored together)
    - we assume unlimited shelf size (1000 cases of tomato sauce fit on one shelf)

- BACKLOG
  - TODO: use external variables (?) (for VAT, etc.) so `constants` can be changed by admin users
  - TODO: use validation to prevent erroneous input (e.g. in inventory.unit or purchase_orders.status)
  - TODO: start versioning
  - TODO: add masking to sensitive data
  - TODO: unify this w/ Asana
    - decide what type of tasks to put in Asana, and what in the repo

- IDEAS/SUGGESTIONS
  - Add location name to location table
  - Add new table (location-shelf-rack) which would add relationship between locations, shelves, racks
  - Create check constraint to validate location-shelf-rack combinations