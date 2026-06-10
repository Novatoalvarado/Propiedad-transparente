import firebase_admin
from firebase_admin import credentials, firestore
import uuid
import datetime
import random

# Inicializar Firebase
# Nos aseguramos de usar el archivo JSON correcto
cred = credentials.Certificate('propiedad-transparente-firebase-adminsdk-fbsvc-605fe92eb9.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

def generate_id():
    return str(uuid.uuid4())

def seed_database():
    print("Iniciando la población de la base de datos Firestore...")
    
    # 1. Crear Usuarios (Administrador y Copropietarios)
    admin_id = generate_id()
    copropietario_1_id = generate_id()
    copropietario_2_id = generate_id()
    
    users_ref = db.collection('USERS')
    
    users_data = [
        {
            "id": admin_id,
            "gov_id": "123456789",
            "full_name": "Administrador Principal",
            "email": "admin@propiedadtransparente.com",
            "role": "ADMIN",
            "phone": "3001234567",
            "created_at": datetime.datetime.now()
        },
        {
            "id": copropietario_1_id,
            "gov_id": "987654321",
            "full_name": "Ingrid Alvarado",
            "email": "ingrid@ejemplo.com",
            "role": "COPROPIETARIO",
            "phone": "3109876543",
            "created_at": datetime.datetime.now()
        },
        {
            "id": copropietario_2_id,
            "gov_id": "112233445",
            "full_name": "Carlos Gomez",
            "email": "carlos.gomez@ejemplo.com",
            "role": "COPROPIETARIO",
            "phone": "3154445555",
            "created_at": datetime.datetime.now()
        }
    ]
    
    for u in users_data:
        users_ref.document(u["id"]).set(u)
    print(f"[OK] Se insertaron {len(users_data)} usuarios.")

    # 2. Crear Propiedades
    prop_1_id = generate_id()
    prop_2_id = generate_id()
    
    props_ref = db.collection('PROPERTIES')
    props_data = [
        {
            "id": prop_1_id,
            "user_id": copropietario_1_id,
            "unit_number": "Apto 301 B",
            "type": "APARTAMENTO",
            "coefficient": 0.05
        },
        {
            "id": prop_2_id,
            "user_id": copropietario_2_id,
            "unit_number": "Apto 402 A",
            "type": "APARTAMENTO",
            "coefficient": 0.04
        }
    ]
    for p in props_data:
        props_ref.document(p["id"]).set(p)
    print(f"[OK] Se insertaron {len(props_data)} propiedades.")

    # 3. Zonas Comunes (AMENITIES)
    salon_social_id = generate_id()
    bbq_id = generate_id()
    
    amenities_ref = db.collection('AMENITIES')
    amenities_data = [
        {
            "id": salon_social_id,
            "name": "Salón Social Multipropósito",
            "max_capacity": 50,
            "cleaning_fee": 30000.00,
            "is_active": True
        },
        {
            "id": bbq_id,
            "name": "Zona BBQ Terraza",
            "max_capacity": 20,
            "cleaning_fee": 15000.00,
            "is_active": True
        }
    ]
    for a in amenities_data:
        amenities_ref.document(a["id"]).set(a)
    print(f"[OK] Se insertaron {len(amenities_data)} amenidades.")

    # 4. Reservas (RESERVATIONS)
    res_1_id = generate_id()
    res_ref = db.collection('RESERVATIONS')
    res_data = [
        {
            "id": res_1_id,
            "user_id": copropietario_1_id,
            "amenity_id": salon_social_id,
            "reservation_date": (datetime.datetime.now() + datetime.timedelta(days=7)).isoformat(),
            "status": "CONFIRMED",
            "created_at": datetime.datetime.now()
        }
    ]
    for r in res_data:
        res_ref.document(r["id"]).set(r)
    print(f"[OK] Se insertaron {len(res_data)} reservas.")

    # 5. Facturas (INVOICES)
    inv_1_id = generate_id()
    inv_2_id = generate_id()
    
    inv_ref = db.collection('INVOICES')
    inv_data = [
        {
            "id": inv_1_id,
            "user_id": copropietario_1_id,
            "concept": "Administración Mayo 2026",
            "amount": 250000.00,
            "status": "PENDING",
            "due_date": (datetime.datetime.now() + datetime.timedelta(days=15)).isoformat(),
            "created_at": datetime.datetime.now()
        },
        {
            "id": inv_2_id,
            "user_id": copropietario_1_id,
            "concept": "Alquiler Salón Social",
            "amount": 30000.00,
            "status": "PAID",
            "due_date": (datetime.datetime.now() - datetime.timedelta(days=2)).isoformat(),
            "created_at": datetime.datetime.now() - datetime.timedelta(days=10)
        }
    ]
    for i in inv_data:
        inv_ref.document(i["id"]).set(i)
    print(f"[OK] Se insertaron {len(inv_data)} facturas.")

    # 6. Audit Logs (system_audit_logs)
    logs_ref = db.collection('system_audit_logs')
    log_data = {
        "timestamp": datetime.datetime.now(),
        "actor": {
            "user_id": admin_id,
            "role": "ADMIN",
            "full_name": "Administrador Principal"
        },
        "action": {
            "module": "INVOICES",
            "operation_type": "CREATE",
            "target_entity": "INVOICES",
            "target_record_id": inv_1_id
        },
        "details": {
            "amount": 250000.00,
            "ip_address": "127.0.0.1"
        },
        "status": "SUCCESS"
    }
    logs_ref.add(log_data)
    print("[OK] Se insertó Log de Auditoría.")
    
    # 7. Documentos Generales (DOCUMENTS)
    doc_1_id = generate_id()
    doc_ref = db.collection('DOCUMENTS')
    doc_data = {
         "id": doc_1_id,
         "file_name": "Reglamento_Propiedad_Horizontal_2026.pdf",
         "document_type": "REGLAMENTO",
         "uploaded_by": admin_id,
         "uploaded_at": datetime.datetime.now()
    }
    doc_ref.document(doc_data["id"]).set(doc_data)
    print("[OK] Se insertó 1 Documento Institucional.")

    print("\n🎉 Migración exitosa. ¡La base de datos Firebase ha sido inicializada y poblada!")

if __name__ == "__main__":
    seed_database()
