import os.path
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Alcance para Google Tasks
SCOPES = ["https://www.googleapis.com/auth/tasks.readonly"]


def main():
    creds = None
    # El archivo token.pickle almacena el token de acceso del usuario.
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # Si no hay credenciales válidas, el usuario debe iniciar sesión.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Guarda las credenciales para la próxima vez
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("tasks", "v1", credentials=creds)

    # Obtener las listas de tareas
    results = service.tasklists().list(maxResults=10).execute()
    items = results.get("items", [])

    if not items:
        print("No se encontraron listas de tareas.")
        return

    for tasklist in items:
        print(f"\nLista: {tasklist['title']}")
        tasks = service.tasks().list(tasklist=tasklist["id"]).execute().get("items", [])
        if not tasks:
            print("  No hay tareas en esta lista.")
        else:
            from datetime import datetime

            for task in tasks:
                status = task.get("status", "unknown")
                title = task.get("title", "(Sin título)")
                due = task.get("due")
                if due:
                    # due puede ser 'YYYY-MM-DD' o 'YYYY-MM-DDTHH:MM:SS.sssZ'
                    try:
                        if "T" in due:
                            dt = datetime.fromisoformat(due.replace("Z", "+00:00"))
                            fecha = dt.strftime("%Y-%m-%d")
                            hora = dt.strftime("%H:%M:%S")
                            due_str = f"{fecha} {hora}"
                        else:
                            due_str = due
                    except Exception:
                        due_str = due
                else:
                    due_str = "Sin fecha"
                print(f"  - {title} | Estado: {status} | Fecha límite: {due_str}")


if __name__ == "__main__":
    main()

# Si modificas estos alcances, elimina el archivo token.pickle.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
