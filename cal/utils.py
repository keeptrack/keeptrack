from calendar import HTMLCalendar
from functools import partial

from hire.models import HireRequest, Event


class ModelWrapper:
	def __init__(self, year, month, model, date_from):
		self.year = year
		self.month = month
		self.model = model
		self.date_from = date_from


def day_filter(day, event):
	if day == event.date_from.day:
		return True
	else:
		return False


class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None, events=None):
		self.year = year
		self.month = month
		self.events = events

		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
	def formatday(self, day, events):
		events_per_day = filter(partial(day_filter, day), events)
		d = ''
		for event in events_per_day:
			d += f'<li> {event.model.get_html_url} </li>'

		if day != 0:
			return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
		return '<td></td>'

	# formats a week as a tr
	def formatweek(self, theweek):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, self.events)
		return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, theyear, themonth, withyear=True):
		hires = HireRequest.objects.filter(hire_from__year=self.year, hire_from__month=self.month)
		events = Event.objects.filter(event_from__year=self.year, event_from__month=self.month)
		self.events = []

		for hire in hires:
			self.events.append(ModelWrapper(self.year, self.month, hire, hire.hire_from))

		for event in events:
			self.events.append(ModelWrapper(self.year, self.month, event, event.event_from))

		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week)}\n'
		return cal
