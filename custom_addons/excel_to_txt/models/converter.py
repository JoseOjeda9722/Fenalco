from odoo import models, fields, api
import base64
import tempfile
import os
from odoo.exceptions import UserError
from ..services.excel_convertidor_servicio import ExcelConvertirdorServicio


class CargaExcel(models.Model):
    _name = "excel.upload"
    _description = "Carga y conversión del archivo"

    name = fields.Char(string = "Nombre archivo", required=True)
    excel_archivo = fields.Binary(string = "Archivo", required=True, attachment=True)
    convertido_archivo = fields.Text(string = "Datos convertidos", readonly=True)

    # -> para la descarga del archivo transformado
    archivo_tranformado = fields.Binary(string="Archivo tranformado", readonly=True, attachment=True, store=True)
    archivo_tranformado_name = fields.Char(string="Nombre archivo tranformado", readonly=True, store=True)


    def get_file_process(self):
        """
        Método que proceso el archivo excel cargado y guarda el archivo transformado en convertido_archivo.
        Luego genera el archivo txt con los datos tranformados 

        """
        # if not self.file: return
        if not self.excel_archivo: raise UserError("No se cargó el archivo excel.")

        # -> Decodifico el excel y lo guardo en archivo tempral mientras lo proceso
        contenido_excel = base64.b64decode(self.excel_archivo) 
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as archivo_temporal:
            archivo_temporal.write(contenido_excel)
            ruta_archivo_temporal = archivo_temporal.name
        
        try:
            #-> conversión según reglas de negocio
            convertidor_datos = ExcelConvertirdorServicio.conversor_excel(ruta_archivo_temporal)
            print(convertidor_datos)
            if not convertidor_datos:
                raise UserError("La conversión del archivo no generó datos.")

            texto_convertido = "\n".join(convertidor_datos)
            print(texto_convertido)
            self.write({'convertido_archivo': texto_convertido})

            #-> guardo en archivo txt
            data_txt = "\n".join(convertidor_datos)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as archivo_txt:
                archivo_txt.write(data_txt.encode("utf-8"))
                ruta_archivo_txt = archivo_txt.name

            #- > leo el archivo y lo paso base64 -> guado en odoo
            with open(ruta_archivo_txt,"rb") as file:
                archivo_tranformado_binary = base64.b64encode(file.read())

            self.write({
                'archivo_tranformado': archivo_tranformado_binary,
                'archivo_tranformado_name': self.name.replace(".xlsx", ".txt"),
            })

            #self.archivo_tranformado_name = self.name.replace(".xlsx", ".txt")

        finally:
            # -> Borro el archivo excel y txt temporal
            if os.path.exists(ruta_archivo_temporal):
                os.remove(ruta_archivo_temporal)
            if os.path.exists(ruta_archivo_txt):
                os.remove(ruta_archivo_txt) 

    

    def download_tranformed_file(self):
        """
        Método que redirige a la descarga del archivo txt.
        """
        self.ensure_one()
        if not self.archivo_tranformado:
            raise UserError("No se encontró arhicvo para descarga.")

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s/archivo_tranformado?download=true' % self.id, 
            'target': 'self',
        }
