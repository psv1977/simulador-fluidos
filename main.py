from flask import Flask, render_template, request, jsonify
import math
import motor_fisico as mf

app = Flask(__name__)

# 1. Ruta principal: Sirve la interfaz gráfica (HTML)
@app.route('/')
def index():
    return render_template('index.html')

# 2. Ruta de la API: Recibe datos del juego y devuelve la física
@app.route('/calcular', methods=['POST'])
def calcular():
    try:
        # Recibimos los datos que el navegador envía en formato JSON
        datos = request.json
        caudal_lps = float(datos['caudal'])      # Caudal en Litros/segundo
        diametro_mm = float(datos['diametro'])   # Diámetro en milímetros
        longitud_m = float(datos['longitud'])    # Longitud en metros
        material = datos['material']             # Llave del diccionario (ej: 'pvc')
        
        # --- PREPARACIÓN DE DATOS ---
        # Convertimos a unidades del Sistema Internacional (m, m/s)
        caudal_m3s = caudal_lps / 1000.0
        diametro_m = diametro_mm / 1000.0
        area = math.pi * (diametro_m / 2.0)**2
        velocidad = caudal_m3s / area
        
        rugosidad = mf.MATERIALES.get(material, 0.000045) # Por defecto acero si hay error
        
        # --- LLAMADA AL MOTOR FÍSICO ---
        reynolds = mf.calcular_reynolds(velocidad, diametro_m)
        f_friccion = mf.calcular_factor_friccion(reynolds, rugosidad, diametro_m)
        perdida = mf.calcular_perdida_carga(f_friccion, longitud_m, diametro_m, velocidad)
        
        # Devolvemos los resultados al navegador
        return jsonify({
            "estatus": "exito",
            "velocidad_ms": round(velocidad, 2),
            "reynolds": round(reynolds, 0),
            "factor_friccion": round(f_friccion, 5),
            "perdida_carga_m": round(perdida, 2)
        })
        
    except Exception as e:
        return jsonify({"estatus": "error", "mensaje": str(e)}), 400

# Esta línea asegura que el servidor se levante al ejecutar el archivo
if __name__ == '__main__':
    # debug=True reinicia el servidor automáticamente cuando guardas cambios en el código
    app.run(debug=True, host='0.0.0.0', port=5000)

@app.route('/obtener_grafica', methods=['POST'])
def obtener_grafica():
    datos = request.json
    # Generamos una curva desde 1 L/s hasta el doble del caudal actual para dar contexto
    caudal_actual = float(datos['caudal'])
    puntos = mf.generar_curva_perdida(
        caudal_min=1, 
        caudal_max=caudal_actual * 2, 
        diametro=float(datos['diametro']),
        longitud=float(datos['longitud']),
        material=datos['material']
    )
    return jsonify(puntos)