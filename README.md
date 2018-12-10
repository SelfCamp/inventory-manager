# inventory-manager
Welcome to SelfCamp's very first project!

#### Goals
1. Practice database handling with MySQL & Python
1. Practice teamwork & git workflow
1. Fulfill success criteria
    1. Presentable functionality / possible real-world usefulness
    1. Acceptable security features (user privileges, password handling, etc.)
    1. Acceptable data integrity (validation, backups, etc.)
    1. Good test coverage
    1. 
1. Stretch goals
    1. Commercial viability
    1. 

#### Standards
- Keep it modular to enable easy UI swap from console to web
- Adhere to design & code style choices outlined below
- Make unit tests for everything (some actual TDD would be awesome)
- Workflow
  - Keep an approximate version history in Asana as completed todos for each sprint, and extract here occasionally

#### Design choices
- Single-table data duplication in favor of multi-table spawning (e.g. with `products_to_suppliers`, `proportions`, `purchase_order_contents`)
- *Temporarily* simplify reality to enable early delivery
  - we only sell pizza, nothing else
  - we always buy the same item from the same place (no multiple suppliers for the same item)
  - we don't care about items that were semi-prepared (e.g. 100 pizza doughs were made but not baked yet)
  - no database maintenance (data integrity doesn't matter, we always reset to default values for testing)
  - we assume a perfect FIFO system (same type of item from multiple sources / orders are all stored together)
  - we assume unlimited shelf size (1000 cases of tomato sauce fit on one shelf)

#### Code style
- PEP 8 and Clean Code principles are followed when possible
- F-strings are preferred over `.format()` and plain concatenation
- Multi-line statements in brackets are formatted in [Stroustrup style](https://en.wikipedia.org/wiki/Indentation_style#Variant:_Stroustrup)
- Quotes (single/double) are a personal preference
- Function names start with a verb describing what the function does (most likely `'get_'` or `'set_'`)
- SQL
    - No duplicate prefixes in database column names (only ids are prefixed with name of table)
    - Queries are stored as strings
    - Queries longer than 1 line are extracted to and imported from `queries` module
    - Multi-query statements are postfixed `'_multi'`
    - Query names are prefixed `'create_'`/`'read_'`/`'update_'`/`'delete_'` based on which CRUD category they belong to

#### SQL queries
- We don't use `multi=True` in `cursor.execute()` because it's nasty and even the Oracle docs say to avoid it
- We split `'*_multi'` queries on the semicolon instead, execute them separately and commit explicitly
- We use parameterized queries instead of concatenation wherever possible

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

#### Version history

##### inventory-manager 0.2a
*In development*
- ...
- ...
- ...

##### inventory-manager 0.1a
*December 5, 2018*
- Placeholder data uploaded to SQL
- SQL - Python connection established
- Program is runnable from terminal
- Automatic reset/restore database option added
- Foreign currency mid-rate check and update available
- User functions added:
    - Complete inventory check
    - Stock level check for certain item
    - Stock level update
  
