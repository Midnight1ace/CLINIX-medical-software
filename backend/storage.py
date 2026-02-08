import asyncpg
import json


class InMemoryStorage:
    def __init__(self, patients):
        self.patients = patients
        self.documents = []

    async def connect(self):
        return None

    async def close(self):
        return None

    async def init(self):
        return None

    async def seed_demo_data(self, demo_patients):
        for patient_id, patient in demo_patients.items():
            self.patients.setdefault(patient_id, patient)

    async def get_patient(self, patient_id):
        return self.patients.get(patient_id)

    async def search_patients(self, method, value):
        results = []
        if not value:
            return results

        if method in ["PATIENT_ID", "QR_CODE", "BARCODE"]:
            patient = self.patients.get(value)
            if patient:
                results.append(_build_search_result(patient, 1.0, "Exact Patient ID match"))
        elif method == "NATIONAL_ID":
            for patient in self.patients.values():
                national_id = patient.get("demographics", {}).get("national_id")
                if national_id and national_id == value:
                    results.append(_build_search_result(patient, 0.95, "National ID match"))
        elif method == "PARTIAL_NAME":
            search_term = value.lower()
            for patient in self.patients.values():
                name = patient.get("demographics", {}).get("name", "").lower()
                if search_term in name:
                    results.append(_build_search_result(patient, 0.9, "Name match"))

        return results

    async def upsert_patient(self, patient_id, patient_record):
        self.patients[patient_id] = patient_record
        return patient_record

    async def add_document(self, document):
        self.documents.append(document)
        return document


class PostgresStorage:
    def __init__(self, database_url):
        self.database_url = database_url
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(self.database_url, min_size=1, max_size=5)

    async def close(self):
        if self.pool:
            await self.pool.close()

    async def init(self):
        schema_sql = """
        CREATE TABLE IF NOT EXISTS patients (
            patient_id TEXT PRIMARY KEY,
            data JSONB NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS documents (
            id BIGSERIAL PRIMARY KEY,
            patient_id TEXT NULL REFERENCES patients(patient_id) ON DELETE SET NULL,
            filename TEXT NOT NULL,
            mime_type TEXT,
            storage_path TEXT NOT NULL,
            size_bytes INTEGER,
            extracted_data JSONB,
            ocr_text TEXT,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );

        CREATE INDEX IF NOT EXISTS idx_patients_name
            ON patients ((data->'demographics'->>'name'));
        CREATE INDEX IF NOT EXISTS idx_patients_national_id
            ON patients ((data->'demographics'->>'national_id'));
        """
        async with self.pool.acquire() as conn:
            await conn.execute(schema_sql)

    async def seed_demo_data(self, demo_patients):
        async with self.pool.acquire() as conn:
            existing = await conn.fetchval("SELECT COUNT(*) FROM patients")
            if existing and existing > 0:
                return
            for patient_id, patient in demo_patients.items():
                await conn.execute(
                    """
                    INSERT INTO patients (patient_id, data, created_at, updated_at)
                    VALUES ($1, $2::jsonb, NOW(), NOW())
                    ON CONFLICT (patient_id) DO NOTHING
                    """,
                    patient_id,
                    json.dumps(patient)
                )

    async def get_patient(self, patient_id):
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT data FROM patients WHERE patient_id = $1",
                patient_id
            )
            return row["data"] if row else None

    async def search_patients(self, method, value):
        results = []
        if not value:
            return results

        async with self.pool.acquire() as conn:
            if method in ["PATIENT_ID", "QR_CODE", "BARCODE"]:
                row = await conn.fetchrow(
                    "SELECT data FROM patients WHERE patient_id = $1",
                    value
                )
                if row:
                    results.append(_build_search_result(row["data"], 1.0, "Exact Patient ID match"))
            elif method == "NATIONAL_ID":
                rows = await conn.fetch(
                    """
                    SELECT data FROM patients
                    WHERE data->'demographics'->>'national_id' = $1
                    """,
                    value
                )
                for row in rows:
                    results.append(_build_search_result(row["data"], 0.95, "National ID match"))
            elif method == "PARTIAL_NAME":
                rows = await conn.fetch(
                    """
                    SELECT data FROM patients
                    WHERE data->'demographics'->>'name' ILIKE '%' || $1 || '%'
                    LIMIT 50
                    """,
                    value
                )
                for row in rows:
                    results.append(_build_search_result(row["data"], 0.9, "Name match"))

        return results

    async def upsert_patient(self, patient_id, patient_record):
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO patients (patient_id, data, created_at, updated_at)
                VALUES ($1, $2::jsonb, NOW(), NOW())
                ON CONFLICT (patient_id)
                DO UPDATE SET data = EXCLUDED.data, updated_at = NOW()
                """,
                patient_id,
                json.dumps(patient_record)
            )
        return patient_record

    async def add_document(self, document):
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO documents
                (patient_id, filename, mime_type, storage_path, size_bytes, extracted_data, ocr_text, created_at)
                VALUES ($1, $2, $3, $4, $5, $6::jsonb, $7, NOW())
                """,
                document.get("patient_id"),
                document.get("filename"),
                document.get("mime_type"),
                document.get("storage_path"),
                document.get("size_bytes"),
                json.dumps(document.get("extracted_data") or {}),
                document.get("ocr_text")
            )
        return document


def _build_search_result(patient, match_score, match_reason):
    demographics = patient.get("demographics", {})
    return {
        "patient_id": patient.get("patient_id", "Unknown"),
        "name": demographics.get("name", "Unknown"),
        "date_of_birth": demographics.get("date_of_birth", "Unknown"),
        "age": demographics.get("age", "Unknown"),
        "gender": demographics.get("gender", "Unknown"),
        "match_score": match_score,
        "match_reason": match_reason
    }
