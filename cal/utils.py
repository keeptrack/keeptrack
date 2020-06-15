from calendar import HTMLCalendar
from functools import partial

from hire.models import HireRequest, Event


class ModelWrapper:
	def __init__(self, year, month, model, date_from, date_to):
		self.year = year
		self.month = month
		self.model = model
		self.date_from = date_from
		self.date_to = date_to


def day_filter(day, event):
	if event.date_from.day <= day <= event.date_to.day and not event.model.is_hidden:
		return True
	else:
		return False


def recolour(event, events):
	colours = list(map(lambda x: x.model.colour, events))
	palette = ['#1abc9c', '#2ecc71', '#3498db', '#9b59b6', '#34495e', '#f1c40f', '#e67e22', '#e74c3c']
	for p in palette:
		if p not in colours:
			event.model.colour = p


class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None, events=None):
		self.year = year
		self.month = month
		self.events = events

		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
	def formatday(self, day, events):
		events_per_day = list(filter(partial(day_filter, day), events))
		colour_events = events_per_day.copy()
		d = ''
		for event in events_per_day:
			if event.model.colour == '#000000':
				recolour(event, colour_events)

			d += f'<li style="background: %s"> {event.model.get_html_url} </li>' % event.model.colour

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
			self.events.append(ModelWrapper(self.year, self.month, hire, hire.hire_from, hire.hire_to))

		for event in events:
			self.events.append(ModelWrapper(self.year, self.month, event, event.event_from, event.event_to))

		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week)}\n'
		return cal
