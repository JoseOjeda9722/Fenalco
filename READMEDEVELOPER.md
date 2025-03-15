Los archivos donde se realizó el desarrollo se encuentran en la ruta ./odoo/odoo/custom_addoms\excel_to_txt
Despliega las carpetas
 -controllers -> con la rutas para las peticiones
 -models -> con el modelo para el manejo y almacenamiento de los datos y ejecucion de logica de negocio
 -services -> logica que realiza la tranformacion
 -security -> archivo de acceso y acciones de los usuarios
 - views -> vista xml del para la ejecucion 

Despues de instalar python, git, vs code, wkhtmitox, si no se tiene instalar pip
    -> install pip -> py get-pip.py y agregar al PATH
    -> creo el entorno virtual en la carpeta de trabajo : py -m venv venv

Luego, creación de la base de datos
 command:
    - > "C:\Program Files\PostgreSQL\15\bin\crreateuser.exe" --createdb --pwprompt --username=postgres odoo

Clonar el repositorio odoo de git 
    -> git clone --single-branch --branch 16.0 https://github.com/odoo/odoo.git odoo

Ejecutar requirements.txt
    command: 
    -> venv\Scripts\activate
    -> en la ruta: Odoo\odoo> pip install requirements.txt
    -> considere instalar -> pip install pandas, pip install openpyxl

Ejecutar terminal en vs code -> crear el archivo odoo.conf
en la tarminal de vs code ->python odoo\odoo-bin -c odoo.conf --save

Cuando se cree el archivo modificar los campos 
db_user = odoo
db_password+ 12345
db_port 5432
bin_path = C:\Program Files\wkhtmltopdf\bin

Crear el lauch.json
En vs code -> Run and Debug -> create & launch.json file -> python debugger
En lauch.json copiar:
    {
        // Use IntelliSense to learn about possible attributes.
        // Hover to view descriptions of existing attributes.
        // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
        "version": "0.2.0",
        "configurations": [

            {
                "name": "Odoo",
                "type": "debugpy",
                "request": "launch",
                "program": "${workspaceRoot}/odoo/odoo-bin",
                "args": ["-c","${workspaceFolder}/odoo.conf"],
                "gevent": false,
                "console": "integratedTerminal",
                "justMyCode": false,
            }
        ]
    }
Guardar y ejecutar Odoo
Ya se puede correr el servidor si todo esta correctamente configurador 

Verificar de addons_path en archivo odoo.conf
Luego entrar en odoo\odoo y agregar la carpeta custom_addoms con los recursos para el modulo excel_to_txt
    Copiar la ruta donde almaceno la carpeta 

Nuevamente en odoo.conf, en addons_path no boorrar nada solo agregar
    ->addons_path = ..., ruta de custom_addons
Ejecutar nuevamente Odoo desde Run & Debug -> en el odoo web activar modo desarrollador
actualizar las aplicaciones y buscar excel_to_txt, debería aparecer en la parte superior, actualizar el modulo
Ya puede realizar las conversiones del excel
