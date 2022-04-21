def check_null(value):
    value if value is not None or value != '' else ""
    return value


def extract_values(edu: str, constant_values: dict, count, all_edu, header, head_idx):
    c = 0

    is_exist = edu.find(':')
    if is_exist:
        c += 1
        constant_values[f"{head_idx}{c}"] = edu[is_exist + 1:]

    print(c)