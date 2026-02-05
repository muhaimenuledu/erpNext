# 1. ALLOW PRIVILEGED ROLES OR ADMINISTRATOR TO SEE EVERYTHING
# Expanded the list to include: Admin Officer, D.R Admin, Assistant Registrar, 
# Director Finance, Registrar, Pro-VC, VC, Store Officer, and Procurement.
has_privileged_role = frappe.db.exists("Has Role", {
    "parent": frappe.session.user,
    "role": ["in", [
        "Store Officer", 
        "Director, Finance", 
        "Admin Officer", 
        "D.R Admin", 
        "Assistant Registrar", 
        "Registrar", 
        "Pro-VC", 
        "VC", 
        "Procurement"
    ]]
})

if frappe.session.user == "Administrator" or has_privileged_role:
    conditions = ""

else:
    # 2. FETCH THE *ACTIVE* USER'S DEPARTMENT
    # Added "status": "Active" to ensure we don't pick up old employee records
    user_dept = frappe.db.get_value("Employee", {
        "user_id": frappe.session.user,
        "status": "Active"
    }, "department")

    # 3. APPLY THE RESTRICTION
    if user_dept:
        # Filter: Only show records from the user's ACTIVE department
        conditions = f"department = '{user_dept}'"
    else:
        # Security Fallback: Show nothing if no active employee/department found
        conditions = "1=0"
