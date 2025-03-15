import base64
import json
from odoo import http
from odoo.http import request

class ExcelCargaController(http.Controller):

    @http.route('/upload_excel', type='http', auth="public", methods=['POST'], csrf=False)
    def upload_excel(self, **post):
        """
        Endpoint tipo POST que permite la carga del archivo excel desde odoo.
        """
        file = post.get('file')
        if not file:
            return json.dumps({"error": "No se encontró el archivo"})

        file_content = file.read()
        file_base64 = base64.b64encode(file_content).decode('utf-8')

        # -> Creo nuevo registro en el modelo
        excel_record = request.env['excel.upload'].sudo().create({
            'name': file.filename,
            'excel_archivo': file_base64
        })

        # -> Proceso el archivo
        excel_record.get_file_process()

        return json.dumps({"message": "Archivo cargado y convertido exitosamente", "id": excel_record.id})
    

    @http.route('/download_tranformed/<int:record_id>', type='http', auth="user")
    def download_transformed(self, record_id, **kwargs):
        """
        Método para descargar el archivo txt transformado.
        """
        record = request.env['excel.upload'].sudo().browse(record_id)
        if not record or not record.archivo_tranformado:
            return request.not_found()

        file_content = base64.b64decode(record.archivo_tranformado)
        filename = record.archivo_tranformado_name or "archivo_transformado.txt"

        return request.make_response(file_content, [
            ('Content-Type', 'text/plain; charset=utf-8'),
            ('Content-Disposition', 'attachment; filename="%s"' % filename)
        ])