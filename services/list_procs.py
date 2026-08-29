def FormListToDict(form_data: list) -> dict:
    rtn_dict = {}
    for form_field in form_data:
        if 'value' in form_field:
            rtn_dict[form_field['name']] = form_field['value']
        else:
            rtn_dict[form_field['name']] = None
    return rtn_dict
