# Diseño de Base de Datos Arquitectura Híbrida (Relacional + NoSQL)

Este documento define la estructura de bases de datos para todas las funcionalidades del sistema "Propiedad Transparente". Utiliza un modelo de persistencia políglota: **Base de datos Relacional (SQL)** para integridad transaccional e identidad, y una **Base de datos NoSQL** para alto volumen de registros de auditoría y trazas (Logs).

## 1. Diseño Relacional (SQL)
Ideado para el Core Transaccional. Soporta inicio de sesión mediante credenciales clásicas y OAuth (Google/Microsoft), separa claramente los dos roles y almacena comprobantes documentales incluso para facturación.

```mermaid
erDiagram
    USERS ||--o{ PROPERTIES : "ocupa"
    USERS ||--o{ RESERVATIONS : "realiza"
    USERS ||--o{ INVOICES : "debe"
    USERS ||--o{ NOTIFICATIONS : "recibe"
    USERS ||--o{ VOTES : "emite"
    USERS ||--o{ CHAT_SESSIONS : "inicia"
    
    AMENITIES ||--o{ RESERVATIONS : "tiene"
    
    INVOICES ||--o{ PAYMENTS : "abonado_con"
    RESERVATIONS ||--o| INVOICES : "genera"
    
    VOTINGS ||--o{ VOTES : "registra"
    
    CHAT_SESSIONS ||--o{ CHAT_MESSAGES : "contiene"

    USERS {
        uuid id PK
        string gov_id "Cédula / Identificación"
        string full_name
        string email
        string password_hash "Nulo si usa OAuth"
        enum role "ADMIN | COPROPIETARIO"
        string oauth_provider "Ej: google, microsoft, null"
        string oauth_id "ID del token OAuth externo"
        string phone
        string mobile_phone
        string emergency_contact "Nombre y celular"
        datetime birth_date
        datetime created_at
    }

    PROPERTIES {
        uuid id PK
        uuid user_id FK
        string unit_number "Ej: Apto 301, Local 2"
        enum type "APARTAMENTO | CASA | LOCAL"
        decimal coefficient "Coeficiente de copropiedad"
    }

    DOCUMENTS {
        uuid id PK
        string file_name
        string file_bucket_url "S3, Blob Storage"
        enum document_type "REGLAMENTO | FACTURACION | ASAMBLEA"
        uuid uploaded_by FK "Solo Admins"
        datetime uploaded_at
    }

    AMENITIES {
        uuid id PK
        string name "Ej: Salón Social"
        int max_capacity
        decimal cleaning_fee
        boolean is_active
    }

    RESERVATIONS {
        uuid id PK
        uuid user_id FK
        uuid amenity_id FK
        date reservation_date
        enum status "PENDING | CONFIRMED | CANCELED"
        datetime created_at
    }

    INVOICES {
        uuid id PK
        uuid user_id FK
        uuid reservation_id FK "Opcional"
        string concept "Ej: Alquiler Salón, Admin Mensual"
        decimal amount
        string invoice_file_url "PDF Factura física a pagar"
        enum status "PENDING | PAID | OVERDUE"
        date due_date
        datetime created_at
    }

    PAYMENTS {
        uuid id PK
        uuid invoice_id FK
        decimal amount_paid
        string receipt_url "Soporte de transferencia subido"
        enum payment_method "TARJETA | TRANSFERENCIA | EFECTIVO"
        datetime payment_date
    }

    NOTIFICATIONS {
        uuid id PK
        uuid user_id FK
        string title
        text description
        boolean is_read
        string redirect_url "Ruta en app"
        datetime created_at
    }

    VOTINGS {
        uuid id PK
        string title
        text description
        datetime end_date
        boolean is_active
    }

    VOTES {
        uuid id PK
        uuid voting_id FK
        uuid user_id FK
        string selected_option
        datetime voted_at
    }

    CHAT_SESSIONS {
        uuid id PK
        uuid user_id FK
        datetime started_at
        datetime ended_at
    }

    CHAT_MESSAGES {
        uuid id PK
        uuid session_id FK
        enum sender "USER | AI_ASSISTANT | ADMIN"
        text message_content
        datetime sent_at
    }
```

---

## 2. Modelado de Logs y Auditoría No Relacional (NoSQL)
Para garantizar el rendimiento de la Base de Datos transaccional y la capacidad de absorber miles de eventos por segundo que rastrean cada paso que dan el Administrador y el Copropietario de forma independiente, implementaremos una colección NoSQL (ej. en **MongoDB** o **AWS DynamoDB**).

### Colección: `system_audit_logs`

Este bloque almacena documentos libres (JSON) registrando el 100% de los movimientos para posibles auditorías de seguridad, trazabilidad de fallos o informes gerenciales.

**Estructura de Documento Json:**
```json
{
  "_id": "ObjectId('64ae9f02b3c...)",
  "timestamp": "2026-04-18T18:15:30Z",
  "actor": {
    "user_id": "uuid-referencia-base-sql",
    "role": "ADMIN", 
    "full_name": "Ingrid Alvarado"
  },
  "action": {
    "module": "CARGUE_ARCHIVOS",
    "operation_type": "UPLOAD",
    "target_entity": "DOCUMENTS",
    "target_record_id": "uuid-document-134"
  },
  "details": {
    "file_name": "factura_servicios_abril.pdf",
    "impact_areas": ["INVOICES", "DASHBOARD"],
    "ip_address": "190.24.55.12",
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64;...) Chrome/122"
  },
  "status": "SUCCESS"
}
```

### Casos de uso de generación de LOGS (Ejemplos):
- **Oauth Login:** Se registrará un log tipo `AUTH` detallando proveedor (Google/MS) y si la IP del copropietario es inusual.
- **Cambio de Estados:** Si el Admin marca una factura como "PENDIENTE" a "PAGA", saltará un log registrando el cambio `{"old_status": "PENDIENTE", "new_status": "PAID"}`.
- **Reservas de Calendario:** Si el copropietario selecciona un día en Zonas Comunes, el evento registra el mes, año y área elegida.
