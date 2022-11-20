import frappe
import requests
import json
import traceback
from ast import literal_eval

@frappe.whitelist()
def click_to_call(agent,customer):
    
    '''calling api form agent to client'''
    # frappe.msgfrappe.log_error(str(frappe.session.User))
    # frappe.prompt([{'fieldname': 'birth', 'fieldtype': 'Date', 'label': 'Birth Date', 'reqd': 1}],
    subject = frappe.db.get_value('User', agent , 'phone')
    doc = frappe.get_doc('Knowlarity Settings')
    url = doc.url
    payload = json.dumps({
    "k_number": doc.sr_number,
    "agent_number": f"+91{str(subject)}",
    "customer_number": f"+91{str(customer)}"
    })
    headers = {
    'x-api-key': doc.x_api_key,
    'Authorization': doc.authorization,
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    frappe.log_error("click_to_call",response)
    frappe.log_error(response.text)


@frappe.whitelist()
def inbound_handler():
    authorization = frappe.db.get_single_value('Knowlarity Settings', 'authorization')
    stream_url = 'https://konnect.knowlarity.com:8100/update-stream/' + authorization + '/konnect'
    while frappe.local.conf.get('knowlarity_stream'):
        try:
            request = requests.get(,stream=True)
            if(request.status_code == 200):
                for line in request.iter_lines():
                    if(line and frappe.local.conf.get('knowlarity_stream')):
                        if(line.startswith(b'data:')):
                            line = line.decode('UTF-8').split('data:')[1].strip().replace('null', 'None')
                            line = literal_eval(line)
                            frappe.log_error('Stream data', line)
                    else:
                        frappe.log_error('closing connection', 'closing connection')
                        request.close()
                        break
            else:
                frappe.log_error('StatusCode !200: knowlarity stream', request.text)
                break
        except:
            frappe.log_error('Error: Knowlarity Connection Closed', traceback.print_exc())
            break