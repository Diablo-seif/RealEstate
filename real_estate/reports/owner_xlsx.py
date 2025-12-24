from ast import literal_eval
from odoo import http
from odoo.http import request
import xlsxwriter
import io


class XlsxOwnerReport(http.Controller):
    @http.route('/owner/excel/report/<string:owner_ids>',type='http',auth='user', methods=['GET'], csrf=False)
    def download_owner_excel_report(self,owner_ids):
        owner_ids = request.env['owner'].browse(literal_eval(owner_ids))

        output     = io.BytesIO()
        workbook   = xlsxwriter.Workbook(output, {'in_memory':True})
        worksheet  = workbook.add_worksheet('owners')

        head_format   = workbook.add_format({'bold':True,'bg_color':"#D3D3D3",'border': 1 , 'align': 'center'})
        string_format = workbook.add_format({'border': 1 , 'align': 'center'})
        row_num = 1

        headers=['Name','Property ID','Title Property ']
        for col_num , header in enumerate(headers) :
            worksheet.write(0, col_num, header, head_format)

        for owner_id in owner_ids :
            num_owner = len(owner_id.property_ids)
            worksheet.write(row_num, 0, owner_id.name, string_format)
            worksheet.write(row_num, 1, num_owner, string_format)
            worksheet.write(row_num, 2, str(owner_id.property_ids.mapped('name')) , string_format)
            row_num += 1

        workbook.close()
        output.seek(0)
        file_name='Owner Report.xlsx'

        return request.make_response(
            output.getvalue(),
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', f'attachment; filename={file_name}')
        ]
        )