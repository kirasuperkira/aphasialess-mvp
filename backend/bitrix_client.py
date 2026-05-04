import os
import httpx
from typing import Dict, Any, Optional

BITRIX_WEBHOOK_URL = os.getenv("BITRIX24_WEBHOOK_URL")

class Bitrix24Client:
    def __init__(self):
        self.base_url = BITRIX_WEBHOOK_URL.rstrip("/")
        self.client = httpx.AsyncClient(timeout=10.0)

    async def create_contact(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        payload = {
            "fields": {
                "NAME": patient_data.get("full_name", "").strip(),
                "PHONE": [
                    {
                        "VALUE": patient_data.get("bot_phone", ""),
                        "VALUE_TYPE": "WORK"
                    }
                ],
                "UF_CRM_APHASIA_TYPE": patient_data.get("aphasia_type", ""),
                "UF_CRM_AUTH_METHOD": patient_data.get("auth_method", ""),
                "UF_CRM_DOCTOR_ID": patient_data.get("assigned_doctor_id", ""),
                "UF_CRM_SUB_STATUS": patient_data.get("subscription_status", "Trial"),
                "UF_CRM_BOT_PHONE": patient_data.get("bot_phone", ""),
                "COMMENTS": (
                    f"Пациент создан через Aphasialess MVP (ПР-04). "
                    f"Врач ID: {patient_data.get('assigned_doctor_id')}"
                )
            }
        }

        try:
            response = await self.client.post(
                f"{self.base_url}/crm.contact.add",
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            return {
                "status": "success",
                "contact_id": result.get("result"),
                "raw_response": result
            }
        except httpx.HTTPStatusError as e:
            return {
                "status": "error",
                "code": e.response.status_code,
                "detail": e.response.text,
                "raw_response": None
            }
        except Exception as e:
            return {
                "status": "error",
                "detail": str(e),
                "raw_response": None
            }