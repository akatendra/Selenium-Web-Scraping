import openpyxl as xl
from openpyxl.styles import NamedStyle, Font, Alignment, PatternFill, Border, \
    Side


def write_to_xlsx_file(data, file_name):
    xlsx_file_path = f'data_store/{file_name}.xlsx'
    work_book = xl.Workbook()
    work_sheet = work_book.active
    #  Write col headers
    item_ids = list(data.keys())
    print(f'Elements in data: {len(item_ids)} : {item_ids}')
    col_headers = list(data[item_ids[0]].keys())
    print('Col headers:', col_headers)
    # Put headers into xlsx-file
    work_sheet.append(col_headers)
    for item_id in item_ids:
        item_dict = data[item_id]
        row = []
        for item in item_dict:
            row.append(item_dict[item])
        # Put data into xlsx-file
        work_sheet.append(row)
    # Set styles to headers
    avito_col_header_style(work_book, work_sheet)
    # Adjust columns width according content
    xlsx_file_adjust_col_width(work_sheet)
    # Save xlsx-file
    work_book.save(xlsx_file_path)
    print(f'Data saved into file {xlsx_file_path}!')


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
