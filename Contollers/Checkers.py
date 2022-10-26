from Views.Main import ViewsInterface


def is_valid_option_key(option_key: str, list_len: int) -> bool:
    """
    Check if the option_key can convert to int and if it is in range of list_len
    :param option_key: str
    :param list_len: int
    :return: bool
    """
    if option_key.isnumeric():
        if int(option_key)-1 in range(list_len):
            return True
        else:
            return False
    else:
        return False


def check_menu(view: ViewsInterface, items: list, title: str = None, header: str = None, footer: str = None,
               submit: str = None, invalid_title: str = None, invalid_header: str = None,
               invalid_footer: str = None, invalid_submit: str = None) -> int:
    """
    Display the menu in loop while the option is not valid
    :param view: ViewsInterface
    :param items: list
    :param title: str
    :param header: str
    :param footer: str
    :param submit: str
    :param invalid_title: str
    :param invalid_header: str
    :param invalid_footer: str
    :param invalid_submit: str
    :return: int
    """
    option_key = view.menu(
        title=title,
        items=items,
        header=header,
        footer=footer,
        submit=submit
    )
    while not is_valid_option_key(option_key, len(items)):
        option_key = view.menu(
            title=invalid_title,
            items=items,
            header=invalid_header,
            footer=invalid_footer,
            submit=invalid_submit
        )
    return int(option_key)-1
