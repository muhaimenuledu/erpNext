frappe.ui.form.on('Material Issue Request', {
    refresh: function(frm) {
        // 1. Only run for Director, Finance (Skip for Administrator)
        if (frappe.user_roles.includes("Director, Finance") && frappe.session.user !== "Administrator") {
            
            // 2. Get User Department from their Employee profile
            frappe.db.get_value('Employee', { 'user_id': frappe.session.user }, 'department', (r) => {
                if (r && r.department) {
                    let user_dept = r.department;
                    
                    // 3. Compare with the Document's department
                    if (frm.doc.department !== user_dept) {
                        
                        // 4. Force 'display: none' on the Actions button group
                        // We use a timeout to wait for the Workflow engine to finish rendering
                        setTimeout(() => {
                            // Target the class you found in the inspector: .actions-btn-group
                            $('.actions-btn-group').css('display', 'none');
                            
                            // Optional: Hide the mobile version/standard dropdown too
                            $('.menu-btn-group').hide(); 
                        }, 200);
                    }
                }
            });
        }
    }
});
