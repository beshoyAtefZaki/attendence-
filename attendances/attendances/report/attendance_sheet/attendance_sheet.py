# Copyright (c) 2013, Alfahhad and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

from erpnext.hr.doctype.employee.employee import get_holiday_list_for_employee
from erpnext.hr.report.monthly_attendance_sheet.monthly_attendance_sheet import get_holiday, get_employee_details
from frappe import _
import frappe
from frappe.utils import cstr


def execute(filters=None):
	if not filters: filters = {}
	# columns, data = [], []
	
	columns = getcolumns()
	data = get_employees(filters)
	
	return columns, data

def getcolumns():
	return [
		_("attendance_date") + ":Date:120",
		_("status") + ":Data:70",
		_("leave_type") + ":Link/Leave Type:120",
		_("attend_time") + ":Time:80",
		_("leave_time") + ":Time:80",
		_("delay_minutes") + ":Int/delay_minutes:100",
		_("daily_hours") + ":Data:120",
		_("notes") + ":Data:300"
		
	]

def get_employees(filters):
	holiday_list = get_holidays_for_employee(filters["employee"],filters["month"])

	conditions = get_conditions(filters)
	att_data = frappe.db.sql("""
		select  
				attendance_date ,
				`status` ,
				leave_type ,
				attend_time ,
				leave_time ,
				delay_minutes ,
				daily_hours,
				notes 
		from tabAttendance T
			where docstatus = 1
			%s
	"""
	% conditions, as_list=1)
	att_data.extend(holiday_list)
	final_att_data = sorted(att_data, key=lambda k: k[0])
	return final_att_data


def get_conditions(filters):
	conditions = ""
	if filters.get("month"):
		month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov",
			"Dec"].index(filters["month"]) + 1
		conditions += " and month(attendance_date) = '%s'" % month

	if filters.get("company"): conditions += " and company = '%s'" % \
		filters["company"].replace("'", "\\'")

	if filters.get("employee"): conditions += " and employee = '%s'" % \
		filters["employee"].replace("'", "\\'")

	if filters.get("department"):
		conditions += " and (select department 	from tabEmployee	where `name` =T.employee) ='%s'" % \
		filters["department"].replace("'", "\\'")
	return conditions


def get_holidays_for_employee(employee,curr_month):
	holiday_list = get_holiday_list_for_employee(employee)
	month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov",
			 "Dec"].index(curr_month) + 1
	holidays = frappe.db.sql('''select
 		TH.holiday_date as attendance_date,
		'Holiday' as status,
		NULL as leave_type ,
		NULL as attend_time ,
		NULL as leave_time ,
		0 as delay_minutes ,
		NULL as daily_hours,
		NULL as notes
	    from `tabHoliday` TH
	    LEFT JOIN `tabAttendance` T
	    ON TH.holiday_date = T.attendance_date
		WHERE 
			T.attendance_date is null
			and TH.parent=%(holiday_list)s
			and month (TH.holiday_date) = %(month)s ''', {
		"holiday_list": holiday_list,
		"month": month,
	},as_list=1,debug=True)
	return holidays