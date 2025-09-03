from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import datetime
import os.path

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def main():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("calendar", "v3", credentials=creds)

    # Datos del evento
    event = {
        "summary": "Reunión de prueba Python",
        # Ubicación de la reunión en Caracas
        "location": "Caracas",
        "description": "Evento creado desde la API de Google Calendar",
        # Fecha y hora de inicio
        "start": {
            "dateTime": "2025-09-04T10:00:00-06:00",
            "timeZone": "America/Caracas",
        },
        # Fecha y hora de fin
        "end": {
            "dateTime": "2025-09-04T11:00:00-06:00",
            "timeZone": "America/Caracas",
        },
        # Lista de asistentes
        "attendees": [
            {"email": "jdorantes@bantel.net.ve"},
        ],
        # Recordatorios
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "email", "minutes": 24 * 60},  # Un día antes
                {"method": "popup", "minutes": 10},  # Diez minutos antes
            ],
        },
    }

    event_result = (
        service.events().insert(calendarId="primary", body=event).execute()
    )  # Crear evento
    print("Evento creado:")
    print("ID:", event_result.get("id"))
    print("Resumen:", event_result.get("summary"))
    print("Inicio:", event_result["start"].get("dateTime"))
    print("Fin:", event_result["end"].get("dateTime"))


if __name__ == "__main__":
    main()
