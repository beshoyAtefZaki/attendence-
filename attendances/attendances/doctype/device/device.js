// Copyright (c) 2018, Alfahhad and contributors
// For license information, please see license.txt

frappe.provide("attendances.device");

frappe.ui.form.on('Device', {
	refresh: function(frm) {

		frm.add_custom_button(__('Get Attendances'),
				function () {
					return cur_frm.call({
						method: "get_log",
						async: false,
						args: {ip: cur_frm.doc.ip,port:cur_frm.doc.port,device_name:cur_frm.doc.name},
						callback: function(r) {
							if (r.message === 'success'){
								frappe.show_alert('Successfully Stored Attendance Records on db')
							}else {
								msgprint('Error')
							}
						  }
					});
				}
		);

		frm.add_custom_button(__('Set Time'),
				function () {
					return cur_frm.call({
						method: "set_time",
						args: {ip: cur_frm.doc.ip,port:cur_frm.doc.port},
						callback: function(r) {
							if (r.message === 'success'){
								frappe.show_alert('Success')
							}else {
								msgprint('Error during set time')
							}
						  }
					});
				}
			);
		frm.add_custom_button(__('Test Connection'),
				function () {
					return cur_frm.call({
						method: "test_conn",
						async: false,
						args: {ip: cur_frm.doc.ip,port:cur_frm.doc.port},
						callback: function(r) {
							console.log(r);
							if (r.message === 'success'){
								frappe.show_alert('Success')
							}else {
								msgprint('Can not connect')
							}
						  }
					});
				}
			);
	}
});
