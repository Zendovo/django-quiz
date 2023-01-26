import sys
sys.path.append('../')

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()

from quiz.models import Attempt
from django.db.models import Count, Avg
from django.db.models.functions import Length
import pandas
from quiz.helpers import calculate_score

from openpyxl import Workbook

path = 'utils/exports/test.xlsx'
book = Workbook()
book.save(path)
writer = pandas.ExcelWriter(path, engine = 'openpyxl')

attempts = Attempt.objects.all()

attempts_list = []
for attempt in attempts:
    at_dict = {'username': attempt.attempter.username, 'score': calculate_score(attempt) }
    attempts_list.append(at_dict)

dataframe = pandas.DataFrame(attempts_list)
dataframe.to_excel(writer, sheet_name='Attempts', index=False)

writer.close()
