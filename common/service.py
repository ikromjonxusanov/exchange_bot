import openpyxl
from openpyxl.styles import Alignment, Side, Border, Font

from account.models import BotUser


def get_user_for_excel(file_name: str = "test"):
    wb = openpyxl.Workbook()
    sheet = wb.active
    users = BotUser.objects.all().filter(is_active=True).values_list('tg_id', "full_name", "phone")
    sheet.append(["ID", "TELEGRAM ID", "FISH", "TELEFON NOMER"])
    sheet.column_dimensions["A"].width = 25
    sheet.column_dimensions["B"].width = 30
    sheet.column_dimensions["C"].width = 40
    sheet.column_dimensions["D"].width = 20
    for i in range(2, len(users) + 2):
        sheet.append([i - 1] + list(users[i - 2]))

    thin = Side(border_style="thin", color="303030")
    black_border = Border(top=thin, left=thin, right=thin, bottom=thin)
    align = Alignment(horizontal="right", wrap_text=True, vertical="center")
    align_center = Alignment(horizontal="center", wrap_text=True, vertical="center")
    font = Font(name='Calibri', size=13, bold=True, color='07101c')

    for label in ["A", "B", "C", "D"]:
        for col_idx in range(len(users) + 1):
            idx = label + str(col_idx + 1)
            sheet[idx].alignment = align
            sheet[idx].border = black_border
            if col_idx == 0:
                sheet[idx].font = font
                sheet[idx].alignment = align_center
    file_name = file_name.rstrip(".xlsx")+".xlsx"
    wb.save("uploads/" + file_name)
    return file_name


def get_exchange_for_excel(file_name: str = "test"):
    wb = openpyxl.Workbook()
    sheet = wb.active
    users = BotUser.objects.all().filter(is_active=True).values_list('tg_id', "full_name", "phone")
    sheet.append(["ID", "TELEGRAM ID", "FISH", "TELEFON NOMER"])
    sheet.column_dimensions["A"].width = 25
    sheet.column_dimensions["B"].width = 30
    sheet.column_dimensions["C"].width = 40
    sheet.column_dimensions["D"].width = 20
    for i in range(2, len(users) + 2):
        sheet.append([i - 1] + list(users[i - 2]))

    thin = Side(border_style="thin", color="303030")
    black_border = Border(top=thin, left=thin, right=thin, bottom=thin)
    align = Alignment(horizontal="right", wrap_text=True, vertical="center")
    align_center = Alignment(horizontal="center", wrap_text=True, vertical="center")
    font = Font(name='Calibri', size=13, bold=True, color='07101c')

    for label in ["A", "B", "C", "D"]:
        for col_idx in range(len(users) + 1):
            idx = label + str(col_idx + 1)
            sheet[idx].alignment = align
            sheet[idx].border = black_border
            if col_idx == 0:
                sheet[idx].font = font
                sheet[idx].alignment = align_center
    file_name = file_name.rstrip(".xlsx")+".xlsx"
    wb.save("uploads/" + file_name)
    return file_name