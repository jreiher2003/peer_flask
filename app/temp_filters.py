from dateutil.parser import parse as parse_date
from datetime import datetime 
from slugify import slugify
from app import app

@app.template_filter()
def dateify(value):
    return parse_date(value)

@app.template_filter()
def datetimefilter(value):
    """convert a datetime to a different format."""
    tt = datetime.strptime(value, '%m/%d/%Y %H:%M:%f %p')
    return tt.strftime('%b %d - %H:%M EST')

@app.template_filter()
def urlify(value):
  return slugify(value)
