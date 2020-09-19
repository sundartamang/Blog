import datetime
import re

from django.utils.html import strip_tags

def count_words(html_string):
    word_String = strip_tags(html_string)
    matching_word = re.findall(r'/w',word_String)
    count = len(matching_word)
    return count

def get_read_time(html_string):
    count = count_words(html_string)
    read_time_min = (count/200) #assuming 200wpm reading
    read_time_sec = read_time_min * 60
    read_time = str(datetime.timedelta(seconds=read_time_sec))
    return read_time