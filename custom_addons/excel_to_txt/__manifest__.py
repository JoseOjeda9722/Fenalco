{
    'name': "Excel to txt",
    'version': '16.0.0.1',
    'depends': ['base'],
    'author': "Sebastián Ojeda",
    'category': 'Converter',
    'description': """
    Convertir excel a txt segúhn las reglas de negocio dadas
    """,
    'sequence': -1000,
    'data': [
        'security/ir.model.access.csv',
        'views/view_excel_converter.xml'
    ],
    'installable': True,
    'application': True,
    'autoinstall': False,
}