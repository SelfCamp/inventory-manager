from common import cnx


class Table:

    def __init__(self, sql_read_statement, params):
        self.headers, self.data = self._connection(sql_read_statement, params)
        self.table = tuple([self.headers]) + tuple(self.data)

    @staticmethod
    @cnx.connection_handler()
    def _connection(cursor, statement, params):
        cursor.execute(statement, params)
        data = cursor.fetchall()
        return tuple(i[0] for i in cursor.description), data

    def __repr__(self):
        column_lengths = [max([len(str(i[x])) for i in self.table]) for x in range(len(self.data[0]))]
        divider_text, header_text = "+", ""

        for i, header in enumerate(self.headers):
            padding_left = round((column_lengths[i] - len(header))/2 + 0.5) + 1
            padding_right = round((column_lengths[i] - len(header))/2 - 0.5) + 1
            header_text += "|" + " " * padding_left + str(header) + " " * padding_right
            divider_text += "-" * (padding_left + padding_right + len(header)) + "+"
        header_text += "|"
        full_text = divider_text + "\n" + header_text + "\n" + divider_text + "\n"

        for record in self.data:
            for i, field in enumerate(record):
                padding_left = 1
                padding_right = (column_lengths[i] - len(str(field))) + 1
                full_text += "|" + " " * padding_left + str(field) + " " * padding_right
            full_text += "|\n"
        full_text += divider_text
        return full_text

    def sort_by(self, column, asc=False):
        self.data = sorted(self.data, key=lambda x: x[column], reverse=asc)
