from time import sleep


def break_up_query(multi_query):
    """Return list of individual SQL statements in `multi_query`

    Args
        - `multi_query`: string containing one or more SQL statements separated by semicolons
    """
    multi_query = multi_query.strip('; \n\t')  # prevent final `split(';')` from creating empty strings
    return multi_query.split(';')


def quit_application(current_user=None):
    if not current_user:
        print(f'\nGoodbye!')
    else:
        print(f'\nGoodbye, {current_user.first_name}!')
    sleep(1)
    quit()
