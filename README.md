# inventory-manager
SelfCamp's first project, aimed at database practice with MySQL &amp; Python


#### Design choices
- No duplicate prefixes (only ids are prefixed with nature of record/table)
- Single-table data duplication in favor of multi-table spawning (e.g. with `products_to_suppliers`, `proportions`, `purchase_order_contents`)
- *Temporarily* simplify reality to enable early delivery
  - we only sell pizza, nothing else
  - we always buy the same item from the same place (no multiple suppliers for the same item)
  - we don't care about items that were semi-prepared (e.g. 100 pizza doughs were made but not baked yet)
  - no database maintenance (data integrity doesn't matter, we always reset to default values for testing)
  - we assume a perfect FIFO system (same type of item from multiple sources / orders are all stored together)
  - we assume unlimited shelf size (1000 cases of tomato sauce fit on one shelf)


#### Setup
- **Set environment variables for database access**
  - local_host
  - local_database
  - local_user
  - local_password
  - remote_host
  - remote_database
  - remote_user
  - remote_password
- **Install dependencies**
  - mysql-connector-python-rf==2.2.2
