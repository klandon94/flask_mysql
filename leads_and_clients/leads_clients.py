from flask import Flask, render_template, request, session, redirect, url_for
from mysqlconnection import connectToMySQL
from datetime import datetime,date

app = Flask(__name__)
app.secret_key = "ThisIsSecret"

mysql = connectToMySQL('lead_gen_business')

@app.route('/')
def index():
    if 'dateparams' not in session:
        session['dateparams'] = ''
    query = f'select concat(clients.first_name, " ", clients.last_name) as client_name, count(*) as num_leads from clients join sites on clients.client_id = sites.client_id join leads on sites.site_id = leads.site_id where (clients.client_id = 1 or clients.client_id = 2 or clients.client_id = 3 or clients.client_id = 4 or clients.client_id=5) {session["dateparams"]} group by clients.client_id;'
    # data = {'dateparam': session['dateparams']} <---- can't figure out how to avoid SQL injection
    leads_clients = mysql.query_db(query)
    # and (registered_datetime >= "2011/01/01" and registered_datetime <= "2013/12/31") --> sets the date parameter (records are from 2011 to 2013)
    return render_template('leads_clients.html', leads_clients = leads_clients)

@app.route('/change_date', methods=['POST'])
def change_date():
    dates = request.form 
    session['from'] = dates['from']
    session['until'] = dates['until']
    print(datetime.strptime(dates['from'], '%m/%d/%Y').strftime('%Y/%m/%d'))
    print(datetime.strptime(dates['until'], '%m/%d/%Y').strftime('%Y/%m/%d'))
    session['dateparams'] = f"and (registered_datetime >= '{datetime.strptime(dates['from'], '%m/%d/%Y').strftime('%Y/%m/%d')}' and registered_datetime <= '{datetime.strptime(dates['until'], '%m/%d/%Y').strftime('%Y/%m/%d')}')"
    return redirect('/')

@app.route('/reset')
def reset():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)


# // [ THE JINJA WAY...
# 					// {% for x in range((leads_clients) | length - 1) %}
# 					// 	{ y: {{ leads_clients[x]['num_leads'] }}, name: "{{leads_clients[x]['client_name']}}"},
# 					// {% endfor %}
# 					// 	{ y: {{ leads_clients[(leads_clients) | length - 1]['num_leads'] }}, name: "{{leads_clients[(leads_clients)|length-1]['client_name']}}", exploded: true}
# 					// ]
# 					// { y:{{leads_clients[0]['num_leads']}}, name:'{{leads_clients[0]['client_name']}}'},
# 					// { y:{{leads_clients[1]['num_leads']}}, name:'{{leads_clients[1]['client_name']}}'},
#					// { y:{{leads_clients[2]['num_leads']}}, name:'{{leads_clients[2]['client_name']}}'},
# 					// { y:{{leads_clients[3]['num_leads']}}, name:'{{leads_clients[3]['client_name']}}'}

# 					// { y: 20, name: "Medical Aid" },
# 					// { y: 5, name: "Debt/Capital" },
# 					// { y: 3, name: "Elected Officials" },