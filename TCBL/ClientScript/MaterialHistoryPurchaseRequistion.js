frappe.ui.form.on('Material Request Item', {
    item_code: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];

        if (row.item_code) {
            frappe.call({
                method: "tcbl_customizations.api.get_logged_in_employee_history",
                args: { item_code: row.item_code },
                callback: function(r) {
                    if (r.message) {
                        let d = r.message;

                        // DEBUG CONSOLE MESSAGE
                        console.log(`--- Avg Usage Detail for ${row.item_code} ---`);
                        console.log(`Total Qty Requested: ${d.debug_total_qty}`);
                        console.log(`Months since first request: ${d.debug_months}`);
                        console.log(`Calculation: ${d.debug_total_qty} / ${d.debug_months} = ${d.avg_usage}`);
                        console.log(`-------------------------------------------`);

                        frappe.model.set_value(cdt, cdn, {
                            "mrid": d.last_mr_id === "No History Found" ? "" : d.last_mr_id,
                            "custom_last_requisition_date": d.last_date,
                            "custom_last_requisition_qty": d.last_qty,
                            "custom_last_purchase_rate": d.last_rate,
                            "custom_last_supplier": d.last_supplier,
                            "custom_avergare_monthly_usage": d.avg_usage 
                        });
                        frm.fields_dict['items'].grid.refresh();
                    }
                }
            });
        }
    }
});
