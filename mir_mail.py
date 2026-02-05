# Check if the requisition is made 'On Behalf' and an ID is provided
if doc.requisition_for == "On Behalf" and doc.id:
    
    # Fetch the employee's email address from the Employee record
    recipient_email = frappe.db.get_value("Employee", doc.id, "user_id")

    if recipient_email:
        # 1. Build Item Rows using simple addition
        items_rows = ""
        for item in doc.items:
            items_rows = items_rows + "<tr>"
            items_rows = items_rows + '<td style="border: 1px solid #ddd; padding: 8px;">' + (item.item_name or "") + '</td>'
            items_rows = items_rows + '<td style="border: 1px solid #ddd; padding: 8px;">' + (item.description or "") + '</td>'
            items_rows = items_rows + '<td style="border: 1px solid #ddd; padding: 8px;">' + str(item.quantity or 0) + '</td>'
            items_rows = items_rows + "</tr>"
        
        # 2. Build Subject using simple addition
        subject = "Material Issue Request Submitted on Your Behalf: " + str(doc.name)
        
        # 3. Build Message Body using simple addition
        msg = "<p>Hello " + str(doc.name1) + ",</p>"
        msg = msg + "<p>A new Material Issue Request (<b>" + str(doc.name) + "</b>) has been submitted on your behalf by " + str(doc.owner) + ".</p>"
        msg = msg + "<p><b>Details:</b></p>"
        msg = msg + "<ul>"
        msg = msg + "<li><b>Date:</b> " + str(doc.request_date) + "</li>"
        msg = msg + "<li><b>Request Type:</b> " + str(doc.request_for) + "</li>"
        msg = msg + "</ul>"
        msg = msg + "<p><b>Items Requested:</b></p>"
        msg = msg + '<table style="border-collapse: collapse; width: 100%; border: 1px solid #ddd;">'
        msg = msg + '<thead><tr style="background-color: #f2f2f2;">'
        msg = msg + '<th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Item Name</th>'
        msg = msg + '<th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Description</th>'
        msg = msg + '<th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Quantity</th>'
        msg = msg + '</tr></thead><tbody>'
        msg = msg + items_rows
        msg = msg + '</tbody></table>'
        msg = msg + '<p>You can view the request here: <a href="/app/material-issue-request/' + str(doc.name) + '">View Request</a></p>'

        # 4. Send the email
        frappe.sendmail(
            recipients=[recipient_email],
            subject=subject,
            message=msg,
            reference_doctype=doc.doctype,
            reference_name=doc.name
        )
