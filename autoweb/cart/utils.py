def get_pk_from_path(path):
    path_of_next = path.split('/')

    if path_of_next[-2] == '?next=':
        product_pk = int(path_of_next[-3])
    else:
        product_pk = int(path_of_next[-2])

    return product_pk
