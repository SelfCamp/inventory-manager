"""Meaningless queries for testing database access and basic main() functionality"""

import random


def get_random_employees(n):
    generate_name = lambda x, y: (''.join(random.choice('abcdefghijklmnopqrstuvwxyz')
                                          for char in range(random.randint(x, y))).capitalize())
    generated = []
    contact_ids = list(range(1, n+1))
    random.shuffle(contact_ids)
    for i in range(n):
        first_name = generate_name(3, 9)
        last_name = generate_name(5, 15)
        contact_id = contact_ids.pop()
        location_id = random.choice(('BUD001', 'BUD002', 'DEB001', 'MIS001'))
        status = random.choice(('employed', 'terminated'))
        department = random.choice(('sales', 'marketing', 'kitchen', 'waitstaff'))
        role = random.choice(('junior', 'senior', 'manager'))
        salary_huf = f'{random.randint(160000, 900000)}.00'
        generated.append(f"""('{first_name}', '{last_name}', {contact_id}, '{location_id}', '{status}', '{department}', '{role}', {salary_huf})""")
    return ",\n       ".join(generated)


drop = """DROP TABLE test_employees;"""


create = """\
CREATE TABLE test_employees (
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
);"""


populate = f"""\
INSERT INTO test_employees (first_name, last_name, contact_id, location_id, status, department, role, salary_huf)
VALUES {get_random_employees(1000)};"""

select_by_salary = """\
SELECT * FROM test_employees WHERE salary_huf > 850000;
"""