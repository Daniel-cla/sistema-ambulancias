from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': 'localhost:3306',
    'user': 'roor',
    'password': 'root',
    'database': 'sistema_ambulancias'
}

# Ruta para registrar un accidente
@app.route('/api/accidentes', methods=['POST'])
def registrar_accidente():
    data = request.get_json()
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO accidentes (nombre, telefono, descripcion, latitud, longitud)
        VALUES (%s, %s, %s, %s, %s)
    ''', (data['nombre'], data['telefono'], data['descripcion'], data['latitud'], data['longitud']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Accidente registrado correctamente'}), 201

# Ruta para obtener todos los accidentes
@app.route('/api/accidentes', methods=['GET'])
def obtener_accidentes():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM accidentes')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    accidentes = []
    for row in rows:
        accidentes.append({
            'id': row[0],
            'nombre': row[1],
            'telefono': row[2],
            'descripcion': row[3],
            'latitud': row[4],
            'longitud': row[5]
        })
    return jsonify(accidentes)

if __name__ == '__main__':
    app.run(debug=True)
