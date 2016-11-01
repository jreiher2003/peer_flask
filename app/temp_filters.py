from dateutil.parser import parse as parse_date
from datetime import datetime 
from slugify import slugify
from app import app

@app.template_filter()
def dateify(value):
    return parse_date(value)

@app.template_filter()
def datetimefilter(value):
    """convert a date string to datetime to format."""
    tt = datetime.strptime(value, '%m/%d/%Y %H:%M:%f %p')
    return tt.strftime('%b %d - %H:%M EST')

@app.template_filter()
def datetimefilter_f(value):
    """convert a datetime object to a formated string """
    return value.strftime("%m-%d-%Y %I:%M %p")

@app.template_filter() 
def game_time(value):
    return '{dt:%I:%M %p}'.format(dt=value)

@app.template_filter() 
def game_day(value):
    return '{dt:%A}'.format(dt=value)

@app.template_filter()
def day_first(value):
    return '{dt.day}-{dt:%b}-{dt.year}'.format(dt=value)

@app.template_filter()
def game_date(value):
    return  '{dt:%b} {dt.day}, {dt.year}'.format(dt=value)

@app.template_filter()
def urlify(value):
  return slugify(value)

# @app.template_filter()
# def format_date_reg(value):
#     return "{dt:%Y-%m-%d}".format(dt=value)

# @app.template_filter() 
# def format_time(value):
#     return '{dt:%I:%M %p}'.format(dt=value)

# @app.template_filter()
# def last_modified_date(value):
#     return '{dt:%A} {dt:%B} {dt.day}, {dt.year}'.format(dt=value)

# @app.template_filter() 
# def last_modified_time(value):
#     return '{dt:%I:%M %p}'.format(dt=value)

