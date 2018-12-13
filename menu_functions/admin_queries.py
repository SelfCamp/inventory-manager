create_tables_multi = """
    CREATE TABLE inventory (
    inventory_id    INT NOT NULL AUTO_INCREMENT,
    product_id      INT NOT NULL,
    quantity        INT NOT NULL,                               -- product table has info on units
    location_id     CHAR(6) NOT NULL,
    rack_no         INT NOT NULL,
    shelf_no        INT NOT NULL,
    expiration_date DATE NOT NULL,
    po_id           INT NOT NULL,                               -- traces item back to order/supplier
    PRIMARY KEY (inventory_id)
    );
    
    
    CREATE TABLE locations (
    location_id     CHAR(6) NOT NULL,                           -- 3-letter city name + 3-letter sequence no. (e.g. 'BUD001')
    location_name   VARCHAR(20) NOT NULL,
    manager_id      INT NOT NULL,
    contact_id      INT NOT NULL,
    PRIMARY KEY (location_id)
    );
    
    
    CREATE TABLE products (                                     -- stuff we buy (e.g. ingredients, beverages)
    product_id      INT NOT NULL AUTO_INCREMENT,
    name            VARCHAR(50) NOT NULL,
    kind            VARCHAR(20) NOT NULL,
    unit            VARCHAR(10) NOT NULL,                       -- 'grams' / 'pieces'
    PRIMARY KEY (product_id)
    );
    
    
    CREATE TABLE products_to_suppliers (
    product_id      INT NOT NULL,
    supplier_id     INT NOT NULL,
    PRIMARY KEY (product_id)
    );
    
    
    CREATE TABLE menu_items (                                   -- dishes, beverages, etc.
    menu_item_id    INT NOT NULL AUTO_INCREMENT,
    name            VARCHAR(50) NOT NULL,
    description     VARCHAR(500) NOT NULL,                      -- to be displayed on the menu
    price_huf       DECIMAL(6,2) NOT NULL,
    portions        INT NOT NULL,                               -- how many portions to make by default (e.g. pizza is 1, but soup may be 30)
    PRIMARY KEY (menu_item_id)
    );
    
    
    CREATE TABLE proportions (                                  -- ingredients for 1 portion
    menu_item_id    INT NOT NULL,
    ingredient_id   INT NOT NULL,
    amount          INT NOT NULL                                -- gross amount (before prepping)
    );
    
    
    CREATE TABLE suppliers (
    supplier_id     INT NOT NULL AUTO_INCREMENT,
    name            VARCHAR(50) NOT NULL,
    contact_id      INT NOT NULL,
    PRIMARY KEY (supplier_id)
    );
    
    
    CREATE TABLE contacts (                                     -- structured as per https://stackoverflow.com/questions/929684/is-there-common-street-addresses-database-design-for-all-addresses-of-the-world
    contact_id      INT NOT NULL AUTO_INCREMENT,
    address_line1   VARCHAR(100) NOT NULL,                      -- street name & number, etc.
    address_line2   VARCHAR(100),
    locality        VARCHAR(50) NOT NULL,                       -- city/town/village
    region          VARCHAR(50),                                -- a.k.a. county
    postcode        VARCHAR(18),                                -- a.k.a. ZIP code
    country         VARCHAR(50) NOT NULL,                       -- `country_id` might be better for relation to tax info, language, etc.
    phone_no        VARCHAR(20) NOT NULL,                       -- 15 + padding
    email           VARCHAR(255) NOT NULL,
    PRIMARY KEY (contact_id)
    );
    
    
    CREATE TABLE users (
    user_id         INT NOT NULL AUTO_INCREMENT,                -- needed only to enable changing of usernames later
    access_level_id INT NOT NULL,
    employee_id     INT NOT NULL,
    username        VARCHAR(50) NOT NULL UNIQUE,
    password        CHAR(64) NOT NULL,
    PRIMARY KEY (user_id)
    );
    
    
    CREATE TABLE purchase_orders (
    po_id           INT NOT NULL AUTO_INCREMENT,
    supplier_id     INT,
    date_ordered    DATETIME,
    date_eta        DATETIME,
    date_arrived    DATETIME,
    signee_id       INT,                                        -- employee who received the shipment
    status          VARCHAR(20) NOT NULL,                       -- draft / ordered / confirmed / signed for / stocked
    PRIMARY KEY (po_id)
    );
    
    
    CREATE TABLE purchase_order_contents (
    po_id           INT NOT NULL,
    product_id      INT NOT NULL,
    amount          INT NOT NULL
    );
    
    
    CREATE TABLE mid_exchange_rate (
    currency_id     CHAR(3) NOT NULL,                           -- ISO 4217 code (e.g. 'EUR')
    date_updated    DATE NOT NULL,
    midrate_to_huf  DECIMAL(10,5),
    PRIMARY KEY (currency_id)
    );
    
    
    CREATE TABLE access_levels (                                -- TODO: define privileges
    access_level_id INT NOT NULL AUTO_INCREMENT,
    privilege1      BOOL NOT NULL DEFAULT 0,
    privilege2      BOOL NOT NULL DEFAULT 0,
    privilege3      BOOL NOT NULL DEFAULT 0,
    PRIMARY KEY (access_level_id)
    );
    
    
    CREATE TABLE employees (
    employee_id     INT NOT NULL AUTO_INCREMENT,
    first_name      VARCHAR(50) NOT NULL,
    last_name       VARCHAR(50) NOT NULL,
    contact_id      INT NOT NULL,
    location_id     CHAR(6) NOT NULL,
    status          VARCHAR(20) NOT NULL,
    department      VARCHAR(20) NOT NULL,
    role            VARCHAR(20) NOT NULL,
    salary_huf      DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (employee_id)
    );

    CREATE TABLE shelves_by_location (
    shelf_loc_id    INT NOT NULL AUTO_INCREMENT, 
    location_id     CHAR(6) NOT NULL,
    shelf_no        INT NOT NULL,
    PRIMARY KEY (shelf_loc_id)
    );
"""
    
update_table_relations_multi = """
    ALTER TABLE inventory
    ADD FOREIGN KEY (product_id) REFERENCES products(product_id);
    ALTER TABLE inventory
    ADD FOREIGN KEY (location_id) REFERENCES locations(location_id);
    ALTER TABLE inventory
    ADD FOREIGN KEY (po_id) REFERENCES purchase_orders(po_id);
    
    ALTER TABLE locations
    ADD FOREIGN KEY (manager_id) REFERENCES employees(employee_id);
    ALTER TABLE locations
    ADD FOREIGN KEY (contact_id) REFERENCES contacts(contact_id);
    
    
    ALTER TABLE products_to_suppliers
    ADD FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id);
    
    
    ALTER TABLE proportions
    ADD FOREIGN KEY (menu_item_id) REFERENCES menu_items(menu_item_id);
    ALTER TABLE proportions
    ADD FOREIGN KEY (ingredient_id) REFERENCES products(product_id);
    
    
    ALTER TABLE suppliers
    ADD FOREIGN KEY (contact_id) REFERENCES contacts(contact_id);
    
    
    ALTER TABLE users
    ADD FOREIGN KEY (access_level_id) REFERENCES access_levels(access_level_id);
    ALTER TABLE users
    ADD FOREIGN KEY (employee_id) REFERENCES employees(employee_id);
    
    
    ALTER TABLE purchase_orders
    ADD FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id);
    ALTER TABLE purchase_orders
    ADD FOREIGN KEY (signee_id) REFERENCES employees(employee_id);
    
    
    ALTER TABLE purchase_order_contents
    ADD FOREIGN KEY (po_id) REFERENCES purchase_orders(po_id);
    ALTER TABLE purchase_order_contents
    ADD FOREIGN KEY (product_id) REFERENCES products(product_id);
    
    
    ALTER TABLE employees
    ADD FOREIGN KEY (contact_id) REFERENCES contacts(contact_id);
    ALTER TABLE employees
    ADD FOREIGN KEY (location_id) REFERENCES locations(location_id);

    ALTER TABLE shelves_by_location
    ADD FOREIGN KEY (location_id) REFERENCES  locations(location_id);
"""
