import mysql.connector
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django import template
from django.contrib.auth.decorators import login_required
import base64
from io import BytesIO
import re
from . import chat_utils  # Import the new module # Import the new module
import mysql.connector
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import re
from . import chat_utils


def dashbord(request):
    context = {'name': 'chathuri'}

    html_template = loader.get_template('home/dashboard.html')
    return HttpResponse(html_template.render(context, request))


def chatbot_index(request):
    # Loads the initial chatbot page
    return render(request, 'chatbot/chatbot.html')




def chat_assistant(request):
    if request.method == 'POST':
        message = request.POST.get('message')

        # Configure Bard ONCE (using a function attribute):
        if not hasattr(chat_assistant, 'bard_configured'):
            chat_utils.configure_bard()
            setattr(chat_assistant, 'bard_configured', True)

        sql_query = chat_utils.bard_query_to_sql(message)

        db_config = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': 'root',
            'database': 'bankdb'
        }

        def contains_restricted_sql(sql_query):
            restricted_commands = ["UPDATE", "DELETE", "DROP", "ALTER"]  # Added ALTER
            pattern = r'\b(?:' + '|'.join(restricted_commands) + r')\b'
            match = re.search(pattern, sql_query, re.IGNORECASE)
            return bool(match)

        if contains_restricted_sql(sql_query):
            return JsonResponse({
                'response': '<div class="restricted-cmd" style="color: red; font-weight: bold; padding: 10px; border: 1px solid red; background-color: #ffdddd;">You do not have permission to perform this operation. Please contact your database administration department.</div>',
                'visualization': None,
                'sql': sql_query
            })

        def visualize_data(df, chart_type, x_column, y_column): # added parameter for x_column and y_column
            plt.switch_backend('Agg')
            plt.figure(figsize=(10, 6))  # Create figure *before* plotting

            try:
                if chart_type == 'line':
                    sns.lineplot(data=df, x=x_column, y=y_column)
                    plt.title(f'Line Plot of {y_column} vs {x_column}')
                elif chart_type == 'bar':
                    sns.barplot(data=df, x=x_column, y=y_column)
                    plt.title(f'Bar Chart of {y_column} by {x_column}')
                elif chart_type == 'scatter':
                    sns.scatterplot(data=df, x=x_column, y=y_column)
                    plt.title(f'Scatter Plot of {y_column} vs {x_column}')
                else:
                    return "Unsupported chart type." # Return error message
            except KeyError as e:
                return f"Column not found: {e}" # Handle column not found errors
            except Exception as e:
                return f"An error occurred during visualization: {e}"

            plt.xlabel(x_column)
            plt.ylabel(y_column)
            plt.tight_layout()

            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
            plt.close() # Close the plot to release memory
            return image_base64

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute(sql_query)
            results = cursor.fetchall()
            column_names = [i[0] for i in cursor.description]

            table_html = "<table style='border-collapse: collapse; width: 100%; font-family: Arial, sans-serif;'><thead><tr>"
            for col in column_names:
                table_html += f"<th style='border: 1px solid #dddddd; padding: 8px; background-color: #f2f2f2; text-align: left;'>{col}</th>"
            table_html += "</tr></thead><tbody>"
            for row in results:
                table_html += "<tr>"
                for value in row:
                    table_html += f"<td style='border: 1px solid #dddddd; padding: 3px;'>{value}</td>"
                table_html += "</tr>"
            table_html += "</tbody></table>"

            df = pd.DataFrame(results, columns=column_names)
            image_base64 = None # Initialize to None

            if not df.empty:
                chart_type = None
                x_axis_column = None
                y_axis_column = None

                if 'linechart' in message.lower():
                    chart_type = 'line'
                    if 'vs' in message.lower():
                        match = re.search(r"(\w+)\s+vs\s+(\w+)", message, re.IGNORECASE)
                        if match:
                            x_axis = match.group(1).lower()
                            y_axis = match.group(2).lower()
                            x_axis_column = next((col for col in column_names if col.lower() == x_axis), None)
                            y_axis_column = next((col for col in column_names if col.lower() == y_axis), None)
                elif 'barchart' in message.lower():
                    chart_type = 'bar'
                    x_axis_column = column_names[0]
                    y_axis_column = column_names[1] if len(column_names) > 1 else None
                elif 'scatter' in message.lower():
                    chart_type = 'scatter'
                    x_axis_column = column_names[0]
                    y_axis_column = column_names[1] if len(column_names) > 1 else None

                if chart_type and x_axis_column and y_axis_column:
                    image_result = visualize_data(df, chart_type, x_axis_column, y_axis_column)
                    if not image_result.startswith("Column not found:") and not image_result.startswith("An error occurred during visualization:"):
                        image_base64 = image_result
                    else:
                        table_html = f"<div style='color: red;'>{image_result}</div>" + table_html #display error message in the frontend

            cursor.close()
            conn.close()

            return JsonResponse({'sql': sql_query, 'response': table_html, 'visualization': image_base64})

        except mysql.connector.Error as err:
            return JsonResponse({'error': str(err), 'response': f"<div style='color: red;'>Database Error: {err}</div>", 'visualization': None}) # Improved error handling
        except Exception as e:
            return JsonResponse({'error': str(e), 'response': f"<div style='color: red;'>An unexpected error occurred: {e}</div>", 'visualization': None}) # Catch other exceptions
    return render(request, 'chatbot/chatbot.html')





# @login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


# @login_required(login_url="/login/")
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
