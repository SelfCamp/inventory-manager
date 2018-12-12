class User:

    def __init__(self, username, access_level, first_name, last_name, location_id, department, role, locality, phone,
                 email, address_line1, address_line2, region, postcode, country, salary):
        self.username = username
        self.access = access_level
        self.first_name = first_name
        self.last_name = last_name
        self.location = location_id
        self.department = department
        self.role = role
        self.locality = locality
        self.phone = phone
        self.email = email
        self.address_line1 = address_line1
        self.address_line2 = address_line2
        self.region = region
        self.postcode = postcode
        self.country = country
        self.salary = salary

    def __repr__(self):
        return f"Name: {self.last_name}, {self.first_name} \nLocation ID: {self.location} \n" \
            f"Department: {self.department} Role: {self.role}\n" \
            f"Address: {self.country} {self.postcode} {self.locality} {self.address_line1} {self.address_line2} \n" \
            f"Contacts: \nPhone: {self.phone}, e-mail: {self.email} "