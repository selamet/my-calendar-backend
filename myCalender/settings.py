from myCalender.default_settings import *
import os

env = os.environ.get('ENV')

try:
    if env == 'local':
        from myCalender.local_settings import *
    else:
        from myCalender.product_settings import *
except ImportError:
    pass
