import io

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from plotly.offline import plot
import plotly.graph_objs as graphs
import xlsxwriter

from .utils import get_books_read_by_month, get_books_read

@login_required
def profile(request):
    user = request.user
    permissions = user.get_all_permissions()
    # Get the books read in different months this year
    books_read_by_month = get_books_read_by_month(user.username)

    # Initialize the Axis for the graphs, X-Axis is months, Y-Axis is books read
    months = [i+1 for i in range(12)]
    books_read = [0 for _ in range(12)]
    
    # Set the value for books read per month on Y-Axis 
    for num_books_read in books_read_by_month:
        list_index = num_books_read['date_created__month'] - 1
        books_read[list_index] = num_books_read['book_count']

    # Generate a scatter plot HTML
    figure = graphs.Figure()
    scatter = graphs.Scatter(x=months, y=books_read)
    figure.add_trace(scatter)
    figure.update_layout(xaxis_title="Month", yaxis_title="No. of books read")
    plot_html = plot(figure, output_type='div')
    
    return render(request, 'profile.html', {
        'user': user,
        'permissions': permissions,
        'books_read_plot': plot_html
    })

@login_required
def reading_history(request):
    user = request.user
    books_read = get_books_read(user.username)

    # in-memory file to store data
    output = io.BytesIO()

    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    for row, book_read in enumerate(books_read):
        worksheet.write(row, 0, book_read['title'])

    # Close the workbook before sending the data.
    workbook.close()

    # Rewind the buffer
    # output.seek(0)

    # Set up the Http response.
    filename = 'reading_history.xlsx'
    response = HttpResponse(
        output.getvalue(),
        content_type="application/vnd.ms-excel"
    )
    response["Content-Disposition"] = 'attachment; filename=reading_history.xlsx'

    return response