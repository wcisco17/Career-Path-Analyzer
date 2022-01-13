def check_null(value):
    value if value is not None or value != '' else ""
    return value


def extract_values(experiences, constant_values, i, values, header, headIdx):
    h = experiences[i][experiences[i].index(header) + 1]
    constant_values[f"{headIdx}-{values}"] = h
