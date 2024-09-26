import base64
import io
import re
import html
from email.header import Header

from docutils.nodes import header
from docutils.parsers.rst.directives.tables import align

from odoo import api,models,fields

class SaleReportXlsx(models.AbstractModel):
    _name = 'report.school_management.sale_order_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, orders):
        sheet = workbook.add_worksheet(orders.partner_id.name)

        # Hide gridlines (0: show gridlines, 1: hide printed gridlines, 2: hide screen gridlines)
        sheet.hide_gridlines(2)  # Hides both printed and screen gridlines

        bold = workbook.add_format({'bold': True})
        title_format = workbook.add_format({'bold': True, 'font_size': 14, 'align': 'right', 'valign': 'vcenter','color':'#004269'})
        header_format= workbook.add_format({'bold':True , 'border': 1, 'bg_color':'#0070C0','color':'white',
                                            'align':'center', 'valign':'vcenter'})
        date_format = workbook.add_format({'border':1,'num_format': 'DD-MM-YYYY','align':'center', 'valign':'vcenter'})
        border_text_format = workbook.add_format(
            {'align': 'left', 'border': 1, 'num_format': 'dd/mm/yyyy', 'valign': 'vcenter'})
        border_format = workbook.add_format({'border':1,'align':'center','valign':'vcenter'})

        row =0
        col =0
        sheet.set_column('A:A',18)
        sheet.set_column('B:B',18)
        for obj in orders:
            # Fetch the company logo
            if obj.company_id.logo:
                company_logo = io.BytesIO(base64.b64decode(obj.company_id.logo))
                # Insert the image into the Excel sheet
                sheet.insert_image(row,col,'image.png',{"image_data":company_logo, 'x_scale':1.0,'y_scale':0.8})

            # Determine the label for the sales order based on the state
            sales_state_label = (
                'Quotation' if obj.state in ['draft', 'sent'] else
                'Sales Order' if obj.state == 'sale' else
                'Cancelled'
            )
            # Merge cells for the title
            sheet.merge_range('H3:J3', sales_state_label, title_format)


            row = row + 6
            sheet.merge_range(row,col,row,col+2,obj.company_id.street)
            row=row+1
            sheet.write(row,col,obj.company_id.city)
            row=row+1
            sheet.write(row,col,obj.company_id.state_id.name)
            row=row+1
            sheet.write(row,col,obj.company_id.zip)
            row = row + 1
            sheet.write(row, col, obj.company_id.website)

           # Date and Expiration date and Order
            sheet.set_column('J7:J7',13)
            sheet.merge_range('H7:I7', 'Date :')
            sheet.write('J7',obj.date_order,border_text_format)
            sheet.merge_range('H8:I8', 'Order # :')
            sheet.write('J8', obj.name,border_text_format)
            sheet.merge_range('H9:I9', 'Valid Until :')
            sheet.write('J9', obj.validity_date,border_text_format)

            # format for invoice  and shipping headings
            format_head = workbook.add_format({'bold':True , 'border': 1, 'bg_color':'#0070C0','color':'white',
                                            'align':'left', 'valign':'vcenter'})
           # Invoicing address  and  shipping address headers
            sheet.merge_range('A13:B13','Invoice Address',format_head)
            sheet.merge_range('H13:J13','Shipping Address',format_head)

            # Invoice address
            sheet.write('A15',obj.partner_invoice_id.name)
            sheet.write('A16',obj.partner_invoice_id.street)
            sheet.write('A17',obj.partner_invoice_id.city)
            sheet.write('A18',obj.partner_invoice_id.country_id.name)

            # Shipping Address
            sheet.write('H15', obj.partner_shipping_id.name)
            sheet.write('H16', obj.partner_shipping_id.street)
            sheet.write('H17', obj.partner_shipping_id.city)
            sheet.write('H18', obj.partner_shipping_id.country_id.name)

            # Table Headers for Sales Information
            sheet.write('A21','Sales Person',header_format)
            sheet.write('B21','Shipping Method',header_format)
            sheet.merge_range('C21:D21','Shipping Terms',header_format)
            sheet.merge_range('E21:F21','Payment Terms',header_format)
            sheet.merge_range('G21:H21','Due Date',header_format)
            sheet.merge_range('I21:J21','Delivery Date',header_format)

            # Salesperson and other information
            sheet.merge_range('A22:A23', obj.user_id.name, border_format)
            sheet.merge_range('B22:B23', obj.carrier_id.name, border_format)
            sheet.merge_range('C22:D23',obj.shipping_terms, border_format)
            sheet.merge_range('E22:F23', obj.payment_term_id.name, border_format)
            sheet.merge_range('G22:H23', obj.due_date, date_format)
            sheet.merge_range('I22:J23', obj.commitment_date, date_format)

            # Table Headers for Line Items
            sheet.write('A25', 'Product', header_format)
            sheet.merge_range('B25:C25', 'Description', header_format)
            sheet.merge_range('D25:E25', 'Qty', header_format)
            sheet.merge_range('F25:G25', 'Unit Price', header_format)
            sheet.write('H25', 'Taxes', header_format)
            sheet.merge_range('I25:J25', 'Total', header_format)

            row_number=26
            for line in obj.order_line:
                sheet.write(f'A{row_number}',line.product_template_id.name,border_text_format)
                # mutliple descriptions to store the description field
                description = line.name.split('\n')    # Split the descriptions by new line
                formatted_description = ""
                if  len(description) > 1:
                    for idx,rec in enumerate(description):
                        if idx == 0:
                            formatted_description += '*' + rec   # First description without a newline
                        else:
                            formatted_description += "\n" + "*" +rec
                else:
                    # If there's only one description, keep it as is
                    formatted_description = description[0]

                sheet.merge_range(f'B{row_number}:C{row_number}',formatted_description,border_text_format)
                sheet.merge_range(f'D{row_number}:E{row_number}',line.product_uom_qty,border_format)
                sheet.merge_range(f'F{row_number}:G{row_number}',line.price_unit,border_format)
                tax_names = []
                # Loop through all taxes in the line's tax_id field
                for tax in line.tax_id:
                    tax_names.append(tax.name)  # Collect the name of the tax
                # Join the tax names into a string to display in one cell
                taxes_display = ', '.join(tax_names)
                sheet.write(f'H{row_number}',taxes_display,border_format)
                sheet.merge_range(f'I{row_number}:J{row_number}',line.price_total,border_format)
                row_number = row_number+1

            # Increment the row number for the content below the header
            special_note = row_number+2
            sheet.merge_range(f'A{special_note}:F{special_note}','Special Notes and Instructions',header_format)

            # Remove HTML tags and unescape HTML entities from obj.note
            clean_note = re.sub('<.*?>', '', obj.note)
            clean_note_text = html.unescape(clean_note)
            sheet.merge_range(f'A{special_note+1}:F{special_note+2}',clean_note_text,border_format)

            # fetch the subtotal and taxes and total amount
            sheet.write(f'H{special_note}','Sub total')
            sheet.write(f'J{special_note}',obj.amount_untaxed)
            sheet.write(f'H{special_note+1}','Taxes')
            sheet.write(f'J{special_note+1}',obj.amount_tax)
            sheet.write(f'H{special_note+2}','Total',bold)
            sheet.write(f'J{special_note+2}',obj.amount_total,bold)

            # Fetch the currency symbol from the sale order
            currency_symbol = obj.currency_id.symbol
            # align symbol right end
            align_right= workbook.add_format({'align':'right','valign':'vcenter'})
            sheet.write(f'I{special_note }', currency_symbol,align_right)
            sheet.write(f'I{special_note + 1}', currency_symbol,align_right)
            sheet.write(f'I{special_note + 2}', currency_symbol,align_right)


            # Footer Section
            text_center_format= workbook.add_format({'bold':True,'align':'center','valign':'vcenter'})
            text_center_format2= workbook.add_format({ 'align': 'center', 'valign': 'vcenter'})
            dotted_top_format=workbook.add_format({'top':1,'top_color':'##2c2e80','align':'center','valign':'vcenter','text_wrap':True})

            sheet.merge_range(f'A{special_note + 8}:J{special_note + 8}', 'Thank you for your business!',text_center_format)
            sheet.merge_range(f'A{special_note + 9}:J{special_note + 10}', f'Should you have any inquiries concerning this quotation, please contact : {obj.user_id.name} on  {obj.user_id.phone}.',text_center_format2)
            sheet.merge_range(f'A{special_note + 11}:J{special_note + 13}', f'{obj.company_id.street} , {obj.company_id.city} , {obj.company_id.country_id.name} \n Phone: {obj.company_id.phone}      Email: {obj.company_id.email}      Website: {obj.company_id.website}  ',dotted_top_format)












