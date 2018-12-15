from menu_functions import read_functions as rf


class User:

    def __init__(self, username):
        user_data = rf.get_employee_data(username)
        self.username = user_data["username"]
        self.access_level_id = user_data["access_level_id"]
        self.first_name = user_data["first_name"]
        self.last_name = user_data["last_name"]
        self.location_id = user_data["location_id"]
        self.department = user_data["department"]
        self.role = user_data["role"]
        self.locality = user_data["locality"]
        self.phone_no = user_data["phone_no"]
        self.email = user_data["email"]
        self.address_line1 = user_data["address_line1"]
        self.address_line2 = user_data["address_line2"]
        self.region = user_data["region"]
        self.postcode = user_data["postcode"]
        self.country = user_data["country"]
        self.salary_huf = user_data["salary_huf"]

    def __repr__(self):
        return f"Name: {self.last_name}, {self.first_name} \nLocation ID: {self.location_id} \n" \
            f"Department: {self.department} Role: {self.role}\n" \
            f"Address: {self.country} {self.postcode} {self.locality} {self.address_line1} {self.address_line2} \n" \
            f"Contacts: \nPhone: {self.phone_no}, e-mail: {self.email} "
