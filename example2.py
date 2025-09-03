from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import datetime
import os.path

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

# ID del calendario de días festivos de Venezuela
HOLIDAY_CALENDAR_IDS = [
    "family09967166610684889287@group.calendar.google.com",
    "es.ve#holiday@group.v.calendar.google.com",
    # Agrega más IDs aquí
]


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

    # Fecha actual en formato RFC3339 y con zona horaria UTC
    now = datetime.datetime.now(datetime.timezone.utc)
    now = now.replace(microsecond=0).isoformat()
    print("Días festivos próximos en Venezuela:")
    for HOLIDAY_CALENDAR_ID in HOLIDAY_CALENDAR_IDS:
        events_result = (
            service.events()
            .list(
                calendarId=HOLIDAY_CALENDAR_ID,
                timeMin=now,
                maxResults=20,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No hay días festivos próximos encontrados.")
        for event in events:
            start = event["start"].get("date", event["start"].get("dateTime"))
            print(start, event["summary"])


if __name__ == "__main__":
    main()
