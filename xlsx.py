import openpyxl as xl
from openpyxl.styles import NamedStyle, Font, Alignment, Border, Side
import logging
import logging.config

# Set up logging
logging.config.fileConfig("logging.ini", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def write_to_xlsx_file(data, file_name):
    wb = xl.Workbook()
    ws = wb.active
    #  Write col headers
    item_ids = list(data.keys())
    logging.getLogger(f'Elements in data: {len(item_ids)} : {item_ids}')
    col_headers = list(data[item_ids[0]].keys())
    logging.getLogger(f'Col headers: {col_headers}')
    # Put headers into xlsx-file
    ws.append(col_headers)
    for item_id in item_ids:
        item_dict = data[item_id]
        row = []
        for item in item_dict:
            row.append(item_dict[item])
        # Put data into xlsx-file
        ws.append(row)
    # Set styles to headers
    avito_col_header_style(wb, ws)
    # Adjust columns width according content
    xlsx_file_adjust_col_width(ws)
    # Save xlsx-file
    wb.save(file_name)
    logging.getLogger(f'Data saved into file {file_name}!')


def append_xlsx_file(data, file_name, page):
    # Open a xlsx for reading
    wb = xl.load_workbook(filename=file_name)
    # Get the current Active Sheet
    ws = wb.active
    # You can also select a particular sheet
    # based on sheet name
    # ws = wb.get_sheet_by_name("Sheet1")

    # Put data into xlsx-file
    item_ids = list(data.keys())
    logging.getLogger(f'Elements in data: {len(item_ids)}')
    for item_id in item_ids:
        item_dict = data[item_id]
        row = []
        for item in item_dict:
            row.append(item_dict[item])
        # Put data into xlsx-file
        ws.append(row)
    # Set styles to headers

    xlsx_file_adjust_col_width(ws)
    # Save xlsx-file
    wb.save(file_name)
    logging.getLogger(f'Data of page {page} saved into file {file_name}!')


def xlsx_file_adjust_col_width(work_sheet):
    dims = {}
    for row in work_sheet.rows:
        for cell in row:
            if cell.value:
                dims[cell.column_letter] = max(
                    (dims.get(cell.column_letter, 0), len(str(cell.value))))
    for col, value in dims.items():
        work_sheet.column_dimensions[col].width = value * 1.2


def avito_col_header_style(work_book, work_sheet):
    if 'avito_col_header' not in work_book.named_styles:
        col_header_style = NamedStyle(name='avito_col_header')
        col_header_style.font = Font(bold=True, size=12)
        col_header_style.alignment = Alignment(horizontal='center')
        col_header_style.border = Border(
            left=Side(border_style='hair', color='FF000000'),
            right=Side(border_style='hair', color='FF000000'),
            top=Side(border_style='hair', color='FF000000'),
            bottom=Side(border_style='hair', color='FF000000'))
        work_book.add_named_style(col_header_style)
        # Set NamedStyle to 1st row
        for cell in work_sheet['1:1']:
            cell.style = 'avito_col_header'
