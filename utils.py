def make_abbreviation(string):
    ret_value = ""
    try:
        array = string.split("_")
        for element in array:
            if len(element) > 3:
                element = element[0:3]
            element = list(element)
            element[0] = element[0].upper()
            ret_value += "".join(element)
    except Exception as e:
        print(e)
    return ret_value


def merge_conditions(array):
    inserted = {
        "UA":True,
        "Bootstrapper":True
    }
    checkes = []
    for condition in array:
        if not isinstance(condition,str):
            continue
        condition = condition.split(".")
        parent_check = ""
        for sub in condition:
            if len(parent_check):
                parent_check+="."
            parent_check +=sub
            if parent_check not in inserted:
                inserted[parent_check] = True
                checkes.append(parent_check)
    return " && "+(" && ".join(checkes))


