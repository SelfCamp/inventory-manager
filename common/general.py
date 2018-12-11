def break_up_query(multi_query):
    """Return list of individual SQL statements in `multi_query`"""
    return multi_query.strip('; \n\t').split(';')
