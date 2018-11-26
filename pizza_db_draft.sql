/*
- TODO: decide - have duplicate prefixes like `item_*` and `quantity_*` or leave off?
- TODO: agree on *temporary* simplifications of reality (in order to speed up partial delivery)
  - we always buy the same item from the same place (no multiple suppliers for the same item)
  - we don't care about items that were semi-prepared (e.g. 100 pizza doughs were made but not baked yet)
  - no database maintenance (data integrity doesn't matter, we always reset to default values for testing)
*/


CREATE DATABASE pizza_db;


USE pizza_db;


CREATE TABLE inventory (
inventory_id    INT NOT NULL AUTO_INCREMENT,
name            VARCHAR(255) NOT NULL,
quantity        INT NOT NULL,
unit            ,  -- TODO: grams / pieces
location_id     CHAR(6) NOT NULL,
rack_no         INT NOT NULL,
shelf_no        INT NOT NULL,
PRIMARY KEY (inventory_id),
FOREIGN KEY (location_id) REFERENCES locations(location_id)
);


CREATE TABLE locations (
location_id     CHAR(6) NOT NULL,                           -- 3-letter city name + 3-letter sequence no. (e.g. 'BUD001')
manager_id      INT NOT NULL,
contact_id      INT NOT NULL,
PRIMARY KEY (location_id),
FOREIGN KEY (manager_id) REFERENCES employees(employee_id),
FOREIGN KEY (contact_id) REFERENCES contacts(contact_id)
);


CREATE TABLE products (  -- TODO: clarify - what is this? how is it different from menu_items?
product_id      INT NOT NULL AUTO_INCREMENT,
product_name    ,  -- TODO
supplier_id     ,  -- TODO
PRIMARY KEY (product_id)
);


CREATE TABLE menu_items (                                   -- dishes, beverages, etc.
menu_item_id    INT NOT NULL AUTO_INCREMENT,
name            VARCHAR(255),
price           DECIMAL(6,2),                               -- e.g. `1195.00`, meaning 1 195 HUF
portions        INT NOT NULL,                               -- how many portions to make by default (e.g. pizza is 1, but soup may be 30)
proportions_id  -- TODO: map to proportions.DISH
PRIMARY KEY (dish_id)
);


CREATE TABLE proportions.DISH (                             -- ingredients for 1 portion
ingredient_id   INT NOT NULL,
amount          INT NOT NULL,                               -- gross amount (before prepping)
unit            ,  -- TODO: grams / pieces
PRIMARY KEY (ingredient_id),
FOREIGN KEY (ingredient_id) REFERENCES inventory(inventory_id)
);


CREATE TABLE suppliers (
supplier_id     INT NOT NULL AUTO_INCREMENT,
contact_id      INT NOT NULL,
product_id      ,  -- TODO: decide - wouldn't this be duplicate information?
                   --                requires a whole table for each supplier,
                   --                when we already have this info the other way around in `products`
PRIMARY KEY (supplier_id),
FOREIGN KEY (contact_id) REFERENCES contacts(contact_id)
);


CREATE TABLE contacts (                                     -- structured as per https://stackoverflow.com/questions/929684/is-there-common-street-addresses-database-design-for-all-addresses-of-the-world
contact_id      INT NOT NULL AUTO_INCREMENT,
address_line1   VARCHAR(100) NOT NULL,                      -- street name & number, etc.
address_line2   VARCHAR(100),
address_line3   VARCHAR(100),
address_line4   VARCHAR(100),
locality        VARCHAR(100) NOT NULL,                      -- city/town/village
region          VARCHAR(100),                               -- a.k.a. county
postcode        VARCHAR(18),                                -- a.k.a. ZIP code
country         VARCHAR(100) NOT NULL,                      -- `country_id` might be better for relation to tax info, language, etc.
phone_no        VARCHAR(20) NOT NULL,                       -- 15 + padding -- TODO: use masking
email           VARCHAR(255) NOT NULL,
PRIMARY KEY (contact_id)
);


CREATE TABLE users (
user_id         INT NOT NULL AUTO_INCREMENT,                -- needed only to enable changing of usernames later
access_level_id INT NOT NULL,
employee_id     INT NOT NULL,
username        VARCHAR(255) NOT NULL,
password        VARCHAR(255) NOT NULL,
PRIMARY KEY (user_id),
FOREIGN KEY (access_level_id) REFERENCES access_levels(access_level_id),
FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);


CREATE TABLE purchase_orders (
po_id           INT NOT NULL AUTO_INCREMENT,
supplier_id     INT NOT NULL,
date_ordered    DATETIME,
date_arrived    DATETIME,
status          ,  -- TODO: drafted / ordered / confirmed
contents        ,  -- TODO: map to purchase_order_contents.PO
PRIMARY KEY (po_id),
FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
);


CREATE TABLE purchase_order_contents.PO (
content_id      ,  -- TODO
po_id           ,  -- TODO
product_id      ,  -- TODO
amount          ,  -- TODO
PRIMARY KEY (),    -- TODO
FOREIGN KEY () REFERENCES ()  -- TODO
);


CREATE TABLE mid_exchange_rate (
currency_id     CHAR(3) NOT NULL,                           -- ISO 4217 code (e.g. 'EUR')
date_updated    DATETIME NOT NULL,
rate_to_huf     DECIMAL(10,5),
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
contact_id      INT NOT NULL,
location_id     INT NOT NULL,
status          ,  -- TODO
department      ,  -- TODO
role            ,  -- TODO
salary          ,  -- TODO
PRIMARY KEY (employee_id),
FOREIGN KEY (contact_id) REFERENCES contacts(contact_id),
FOREIGN KEY (location_id) REFERENCES locations(location_id)
);
