import pyrebase
from datetime import datetime

# ========== CONFIGURACIÓN DE FIREBASE ==========
# ESTOS SON TUS VALORES - YA LOS TIENES
firebaseConfig = {
    "apiKey": "AIzaSyByHS8WqO4LSMJd7F6NeVdyHgPcDqHIvn8",
    "authDomain": "smartstorepymes.firebaseapp.com",
    "databaseURL": "https://smartstorepymes-default-rtdb.firebaseio.com",
    "projectId": "smartstorepymes",
    "storageBucket": "smartstorepymes.firebasestorage.app",
    "messagingSenderId": "904588703784",
    "appId": "1:904588703784:web:b940c18f0d094505bb5d1d",
    "measurementId": "G-E02N0HR0BZ"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
auth = firebase.auth()

def inicializar_bd():
    # Crear estructura inicial si no existe
    if db.child("tiendas").child("principal").get().val() is None:
        db.child("tiendas").child("principal").set({
            "nombre": "",
            "whatsapp": "",
            "clave": "",
            "pregunta": "",
            "respuesta": "",
            "tasa_cambio": 36.5
        })
    print("Firebase conectado")

def obtener_usuario(correo, contraseña):
    try:
        user = auth.sign_in_with_email_and_password(correo, contraseña)
        uid = user['localId']
        datos = db.child("usuarios").child(uid).get().val()
        if datos:
            return (uid, datos.get('nombre', ''), correo)
        return None
    except:
        return None

def registrar_usuario(nombre, correo, telefono, fecha_nac, contraseña):
    try:
        user = auth.create_user_with_email_and_password(correo, contraseña)
        uid = user['localId']
        db.child("usuarios").child(uid).set({
            "nombre": nombre,
            "correo": correo,
            "telefono": telefono,
            "fecha_nacimiento": fecha_nac
        })
        return True
    except:
        return False

def obtener_tienda():
    tienda = db.child("tiendas").child("principal").get().val()
    if tienda:
        return (1, 
                tienda.get('nombre', ''), 
                tienda.get('whatsapp', ''), 
                tienda.get('clave', ''), 
                tienda.get('pregunta', ''), 
                tienda.get('respuesta', ''), 
                tienda.get('tasa_cambio', 36.5))
    return None

def guardar_tienda(nombre, whatsapp, clave, pregunta, respuesta, tasa_cambio):
    db.child("tiendas").child("principal").set({
        "nombre": nombre,
        "whatsapp": whatsapp,
        "clave": clave,
        "pregunta": pregunta,
        "respuesta": respuesta,
        "tasa_cambio": tasa_cambio
    })

def registrar_producto(nombre, marca, talla, precio_cordobas, precio_dolares, stock):
    productos = db.child("productos").get().val() or {}
    nuevo_id = str(len(productos) + 1)
    db.child("productos").child(nuevo_id).set({
        "nombre": nombre,
        "marca": marca,
        "talla": talla,
        "precio_cordobas": precio_cordobas,
        "precio_dolares": precio_dolares,
        "stock": stock
    })

def obtener_productos():
    productos = db.child("productos").get().val() or {}
    resultado = []
    for pid, p in productos.items():
        resultado.append((pid, 
                         p.get('nombre', ''), 
                         p.get('marca', ''), 
                         p.get('talla', ''), 
                         p.get('precio_cordobas', 0), 
                         p.get('precio_dolares', 0), 
                         p.get('stock', 0)))
    return resultado

def obtener_productos_por_nombre(nombre_filtro):
    productos = obtener_productos()
    if not nombre_filtro:
        return productos
    return [p for p in productos if nombre_filtro.lower() in p[1].lower()]

def obtener_stock_total():
    productos = obtener_productos()
    return sum(p[6] for p in productos)

def agregar_reserva(usuario_id, producto_id, cantidad):
    reservas = db.child("reservas").child(usuario_id).get().val() or {}
    nuevo_id = str(len(reservas) + 1)
    db.child("reservas").child(usuario_id).child(nuevo_id).set({
        "producto_id": producto_id,
        "cantidad": cantidad,
        "fecha": str(datetime.now()),
        "estado": "Reservado"
    })

def obtener_reservas_usuario(usuario_id):
    reservas = db.child("reservas").child(usuario_id).get().val() or {}
    productos = obtener_productos()
    productos_dict = {p[0]: p for p in productos}
    resultado = []
    for rid, r in reservas.items():
        pid = r.get('producto_id')
        if pid in productos_dict:
            p = productos_dict[pid]
            resultado.append((rid, p[1], r.get('cantidad', 0), p[4], p[5], r.get('estado', 'Reservado')))
    return resultado

def eliminar_reserva(reserva_id):
    pass

def confirmar_reserva(reserva_id):
    pass