# Copyright (c) 2013, Alfahhad and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from calendar import monthrange
from datetime import datetime
import frappe
from frappe	import _,msgprint

def execute(filters=None):
	columns, data = [], []
	
	columns = get_columns()
	data = get_data(filters)
	
	return columns, data

def get_columns():
	return [
		_("employee_name") + ":Link/Employee:120",
		_("delay_minutes") + ":Int:120"
	]

def get_data(filters):
	month = get_month(filters["month"])
	conditions = get_conditions(filters)
	currentYear = datetime.now().year
	month_end_date = monthrange(currentYear, month)[1]
	date_of_data = str(month_end_date)+"/"+str(month)+"/"+str(currentYear)
	
	return frappe.db.sql("""
		select  
				employee_name ,
				 SUM(delay_minutes) 
		from tabAttendance T
			where docstatus = 1
			and 	(select attendance_type 
						from `tabAttendance Period`
								where `name` =(
								select attendance_period
									from `tabAttendance Data`
										where parent = T.employee
										--	and STR_TO_DATE('%s','%%d/%%m/%%Y') between start_date and IFNULL(end_date,CURDATE())
			))='Shift'
			%s
			GROUP BY employee_name
	"""
	% (date_of_data,conditions), as_list=1,debug=True)


def get_conditions(filters):
	conditions = ""
	if filters.get("month"):
		month = get_month(filters["month"])
		conditions += " and month(attendance_date) = '%s'" % month

	if filters.get("company"): conditions += " and company = '%s'" % \
		filters["company"].replace("'", "\\'")

	if filters.get("department"):
		conditions += " and (select department 	from tabEmployee	where `name` =T.employee) ='%s'" % \
		filters["department"].replace("'", "\\'")
	
	return conditions

def get_month(month):
	return ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov",
			"Dec"].index(month) + 1