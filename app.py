from flask import Flask, render_template, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Configurar las credenciales de autenticación
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('loginsheet-390618-bb07842fa3c0.json', scope)
client = gspread.authorize(creds)

# Abrir la hoja de cálculo específica
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1cHnqm05Zf8D9pWFRWdXboD_mz79SbkTBOB74zJQ8fJ8/edit?usp=sharing'
sheet = client.open_by_url(spreadsheet_url).worksheet('men')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/guardar_datos', methods=['POST'])
def guardar_datos():
    # Obtener los datos enviados desde el formulario HTML
    dato1 = request.form.get('dato1')
    dato2 = request.form.get('dato2')

    # Agregar los datos a la hoja de cálculo
    row = [dato1, dato2]
    sheet.append_row(row)

    return 'Datos guardados exitosamente!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Obtener los valores ingresados por el usuario
        username = request.form.get('username')
        password = request.form.get('password')

        # Leer los datos de la hoja de cálculo
        login_data = sheet.get_all_records()

        # Buscar una coincidencia en los datos de inicio de sesión
        for row in login_data:
            if row['username'] == username and row['password'] == password:
                # Autenticar al usuario y redirigir a una página protegida
                return 'Inicio de sesión exitoso'

        # Si no se encuentra una coincidencia, mostrar un mensaje de error
        return 'Credenciales inválidas'

    return render_template('login.html')



if __name__ == '__main__':
    app.run(port=5000, debug=True)
