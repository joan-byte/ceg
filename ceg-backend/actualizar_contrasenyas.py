from app.database import SessionLocal
from app.models import Socio  # Asegúrate de importar el modelo correcto
from app.auth import get_password_hash  # Importa la función de hashing utilizada en la aplicación

# Crea una sesión de la base de datos
db = SessionLocal()

def actualizar_contrasenas():
    try:
        # Obtiene todos los socios cuyas contraseñas no están hasheadas
        socios = db.query(Socio).filter(
            (Socio.hashed_password != None) & (Socio.hashed_password != '') & (Socio.hashed_password.ilike('%$2b%') == False)
        ).all()

        for socio in socios:
            if socio.hashed_password:  # Si la contraseña no está vacía
                # Aplica hashing a la contraseña actual
                hashed_password = get_password_hash(socio.hashed_password)
                
                # Actualiza el campo de hashed_password con la contraseña hasheada
                socio.hashed_password = hashed_password

                # Guarda los cambios en la base de datos
                db.add(socio)

        # Commit de la transacción para guardar los cambios
        db.commit()
        print(f"Contraseñas de {len(socios)} socios actualizadas correctamente.")

    except Exception as e:
        print(f"Error al actualizar las contraseñas: {e}")
        db.rollback()
    finally:
        # Cierra la sesión de la base de datos
        db.close()

# Ejecuta la función para actualizar contraseñas
if __name__ == "__main__":
    actualizar_contrasenas()