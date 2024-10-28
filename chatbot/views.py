import mysql.connector
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django import template
from django.contrib.auth.decorators import login_required


def chatbot_index(request):
    # Loads the initial chatbot page
    return render(request, 'chatbot/chatbot.html')


def chat_assistant(request):
    from django.http import JsonResponse
    from bardapi import Bard
    import google.generativeai as genai
    import mysql.connector
    if request.method == 'POST':
        message = request.POST.get('message')
        genai.configure(api_key="AIzaSyCPBau4ZNNhZ-CiaCdlvNDCG-BxHcjovqc")
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
        }

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
        )

        database_schema = """
You are working with the following database tables:

1. `account`: Columns: (account_id, district_id, frequency, date)
2. `card`: Columns: (card_id, disp_id, type, date)
3. `disposition`: Columns: (disp_id, client_id)
4. `clientaccount`: Columns: (client_id, account_id, type)
5. `client`: Columns: (client_id, sex, fulldate, age, social, first, middle, last, phone, email, address_1, address_2, city, state, zipcode, district_id)
6. `district`: Columns: (district_id, city, state_name)
7. `state`: Columns: (state_name, state_abbrev, region, division)
8. `loan`: Columns: (loan_id, account_id, amount, duration, payments, status, date, location, purpose)
9. `CRMCallCenterLogs`: Columns: (Date received, Complaint ID, rand client, phonefinal, vru+line, call_id, priority, type, outcome, server, ser_start, ser_exit, ser_time)
10. `order`: Columns: (order_id, account_id, bank_to, account_to, amount, k_symbol)
11. `CRMEvents`: Columns: (Date received, Product, Sub-product, Issue, Sub-issue, Consumer complaint narrative, Tags, Consumer consent provided?, Submitted via, Date sent to company, Company response to consumer, Timely response?, Consumer disputed?, Complaint ID, Client_ID, createdAt, updatedAt)
12. `CRMReviews`: Columns: (reviewId, Date, Stars, Reviews, Product, district_id)
13. `transaction`: Columns: (trans_id, account_id, type, operation, amount, balance, k_symbol, bank, account, date, fulldatewithtime)

Foreign Key Relationships:
- `transaction.account_id` references `account.account_id`
- `loan.account_id` references `account.account_id`
- `CRMEvents.Client_ID` references `client.client_id`
- `CRMCallCenterLogs.Complaint ID` references `CRMEvents.Complaint ID`
- `order.account_id` references `account.account_id`
- `account.district_id` references `district.district_id`
- `card.disp_id` references `disposition.disp_id`
- `disposition.client_id` references `client.client_id`
- `client.district_id` references `district.district_id`
- `CRMReviews.district_id` references `district.district_id`
- `district.state_name` references `state.state_name`
"""

        # Function to convert user input to SQL using the AI model
        def bard_query_to_sql(natural_language_query):
            try:
                chat_session = model.start_chat(history=[])
                full_prompt = f"{database_schema}\n\nGenerate an SQL query for the following request:\n{
                    natural_language_query}"
                response = chat_session.send_message(full_prompt)

                sql_command = response.text.strip()

                # Extract only the SQL query from the response
                if '```' in sql_command:
                    sql_command = sql_command.split('```')[1].strip()

                # Clean up any extra text or 'sql' keywords in the generated query
                sql_command = sql_command.replace('sql', '', 1).strip()

                return sql_command
            except Exception as e:
                return f"An error occurred: {e}"

        # Step 3: Get the SQL query from user input
        sql_query = bard_query_to_sql(message)

        # Step 4: MySQL database configuration
        db_config = {
            'host': '0.tcp.in.ngrok.io',  # ngrok TCP host
            'port': 12370,                # ngrok TCP port
            'user': 'root',
            'password': '',
            'database': 'bankdb'
        }

        try:
            # Step 5: Connect to the MySQL database and execute the generated SQL
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Execute the generated SQL query
            cursor.execute(sql_query)
            results = cursor.fetchall()

            # Prepare the results for output
            result_list = []
            for row in results:
                result_list.append(row)

            # Step 6: Close the cursor and connection
            cursor.close()
            conn.close()

            # Return the SQL query results as a JSON response
            return JsonResponse({'sql': sql_query, 'response': result_list})
        except mysql.connector.Error as err:
            return JsonResponse({'error': str(err), 'response': str(err)})
    return render(request, 'chatbot/chatbot.html')


def dashboard(request):
    context = {'segment': 'dashboard'}

    html_template = loader.get_template('home/dashboard.html')
    return HttpResponse(html_template.render(context, request))



#@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


#@login_required(login_url="/login/")
def pages(request):
    context = {}

    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

  