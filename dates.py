#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import csv
import getopt
from datetime import datetime, timedelta
import calendar

now = datetime.now()

year_to_build = now.year

date_format = '%d/%m/%Y'
date_format_name_output = '%Y-%m-%d'

headers =['year', 'month', 'week_nbr', 'start_date', 'end_date', 'name']

months = {
			1 : 'Janvier',
			2 : 'Février',
			3 : 'Mars',
			4 : 'Avril',
			5 : 'Mai',
			6 : 'Juin',
			7 : 'Juillet',
			8 : 'Août',
			9 : 'Septembre',
			10 : 'Octobre',
			11 : 'Novembre',
			12 : 'Décembre'
		}

output_file = 'weeks_in_year.csv'

monday_weekday_index = 0
friday_weekday_index = 4

help_msg = "dates.py -o <output_file> -y <year>"


def main(argv):

	try:
		opts, args = getopt.getopt(argv, "ho:s:y:", ["output_file=", "year="])
	except getopt.GetoptError:
		print(help_msg)
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print(help_msg)
			sys.exit(2)
		elif opt in ("-o", "--output_file"):
			global output_file 
			output_file = arg
		elif opt in ("-y", "--year"):
			global year_to_build 
			year_to_build = arg

	get_all_weeks_in_year(year_to_build, output_file)


def get_day_of_week(date):
	return datetime.strptime(date, date_format)

def get_all_days_in_week(week_start_date):
	dates = [week_start_date + timedelta(days=i) for i in range(0 - week_start_date.weekday(), 7 - week_start_date.weekday())]
	return dates

def get_youngest_date(week_dates):
	youngest = max(week_dates)
	return youngest

def get_week_boundaries(week_dates):
	out = dict()

	for idx, day in enumerate(week_dates):
		if day.month not in out:
			out[day.month] = dict()
			range_dates = calendar.monthrange(day.year, day.month)
			range_dates = (1, range_dates[1])

		if (day.day == range_dates[0] and day.weekday() <= friday_weekday_index):
			out[day.month]['Start'] = day
		
		if (day.weekday() == monday_weekday_index):
			out[day.month]['Start'] = day

		if (day.day == range_dates[1] and day.weekday() <= friday_weekday_index):
			out[day.month]['End'] = day
		
		if (day.weekday() == friday_weekday_index):
			out[day.month]['End'] = day

	return out

def get_all_weeks_in_year(year_to_build, output_file):
	start_day = '01/01/' + str(year_to_build)
	end_day = '31/12/' + str(year_to_build)

	start_dt = datetime.strptime(start_day, date_format)
	end_dt = datetime.strptime(end_day, date_format)

	current_date = start_dt
	
	weeks_to_write = []

	while current_date < end_dt:

		dates_in_week = get_all_days_in_week(current_date)
		youngest_date = get_youngest_date(dates_in_week)
		current_date = youngest_date + timedelta(days=1)

		weeks_boundaries = get_week_boundaries(dates_in_week)

		for key, week in weeks_boundaries.iteritems():
			if week.has_key("Start") and week.has_key("End"):
				week_start_date = week['Start']
				week_end_date = week['End']
				weeks_to_write.append([week_start_date.year, months[week_start_date.month], week_start_date.isocalendar()[1], week_start_date.strftime(date_format), week_end_date.strftime(date_format), week_start_date.strftime(date_format_name_output) + "_" +week_end_date.strftime(date_format_name_output)])
		


	with open(output_file, 'a') as csvfile:
		datewriter = csv.writer(csvfile, delimiter = ',')
		datewriter.writerow(headers)
		datewriter.writerows(weeks_to_write)


if __name__ == "__main__":
	main(sys.argv[1:])
