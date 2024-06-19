def wrap_row(title: str, length: int) -> str:
    """Перенос строк по заданной длине."""
    split_title = title.split()
    new_title = ''
    current_len = 0

    for word in split_title:

        if current_len + len(word) <= length:
            new_title += word + ' '
            current_len += len(word) + 1
        else:
            new_title += '\n' + word + ' '
            current_len = len(word) + 1

    return new_title.strip()
