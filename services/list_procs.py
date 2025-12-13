def FormListToDict(form_data: list) -> dict:
    rtn_dict = {}
    for form_field in form_data:
        rtn_dict[form_field['name']] = form_field['value']
    return rtn_dict
