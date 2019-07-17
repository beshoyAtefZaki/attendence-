# -*- coding: utf-8 -*-
# Copyright (c) 2018, Alfahhad and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from zk import ZK
from datetime import datetime, date
from struct import pack, unpack
class Device(Document):
	pass


@frappe.whitelist()
def test_conn(ip=None,port=None):
	conn = None
	zk = ZK(ip, port=int(port), timeout=5)
	try:
		print 'Connecting to device {0} on port {1}'.format(ip,port)
		conn = zk.connect()
		return 'success'
	except Exception, e:
		print "Process terminate : {}".format(e)
		return 'error'
	finally:
		if conn:
			conn.disconnect()

@frappe.whitelist()
def set_time(ip=None,port=None):
	conn = None
	zk = ZK(ip, port=int(port), timeout=5)
	try:
		conn = zk.connect()
		response = conn.set_time(str(datetime.now()))
		if response:
			return 'success'
	except Exception, e:
		print "Process terminate : {}".format(e)
		return 'error'
	finally:
		if conn:
			conn.disconnect()

@frappe.whitelist()
def get_log(ip=None,port=None,device_name=None):
	conn = None
	zk = ZK(ip, port=int(port), timeout=5)
	try:
		conn = zk.connect()
		response = conn.get_attendance()
		print response
		for attendance in response :
			print "attendance {0} time:{1} status {2}".format(attendance.user_id,attendance.timestamp,attendance.status)

			if attendance.status == 0 :
				status='Check In'
			elif attendance.status == 1:
				status = 'Check Out'
			else:
				status = 'Undefined'
			stored_attendance_log = frappe.db.get_value("Attendance Log",{"timestamp": attendance.timestamp,"user_id":attendance.user_id}, "*")
			if not stored_attendance_log:
				attendance_log = frappe.new_doc("Attendance Log")
				attendance_log.user_id = attendance.user_id
				emp =  get_emp(attendance.user_id)
				if emp:
					attendance_log.employee = emp
				attendance_log.timestamp = attendance.timestamp
				attendance_log.data_retrieve__time = datetime.now()
				attendance_log.status = status
				attendance_log.device = device_name
				attendance_log.save()

		if response:
			return 'success'
	except Exception, e:
		print "Process terminate : {}".format(e)
		return 'error'
	finally:
		if conn:
			conn.disconnect()

def get_emp(user_id):
	try:
		emp_name = frappe.db.get_value("Employee",{"finger_print_number": user_id}, "name")
		return emp_name
	except frappe.LinkValidationError:
		return False
