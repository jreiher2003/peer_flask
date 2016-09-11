from dateutil.parser import parse as parse_date 


# register = template.Library()

# @register.filter
def dateify(value):
    return parse_date(value)