Google Meet Instant Meeting App
Această aplicație permite crearea unui meeting instant Google Meet folosind Google Calendar API. Poți trimite o listă de email-uri și, dacă este specificată o dată, întâlnirea va fi programată pentru acea dată, altfel se va crea un meeting imediat.

Pași pentru instalare și rulare
1. Clonează acest repository
Clonează repository-ul folosind Git:

bash
Copy
git clone <URL_REPO>
cd <FOLDER_NAME>
2. Creează un mediu virtual (opțional, dar recomandat)
Este recomandat să folosești un mediu virtual pentru a izola dependențele proiectului.

Pentru Windows:
bash
Copy
python -m venv venv
Pentru macOS/Linux:
bash
Copy
python3 -m venv venv
3. Activează mediul virtual
Pentru Windows:
bash
Copy
venv\Scripts\activate
Pentru macOS/Linux:
bash
Copy
source venv/bin/activate
4. Instalează dependențele
Asigură-te că te afli în directorul proiectului și instalează toate dependențele necesare din fișierul requirements.txt:

bash
Copy
pip install -r requirements.txt
5. Obține credentials.json pentru autentificarea cu Google API
Pentru a folosi Google Calendar API, trebuie să creezi un proiect în Google Cloud Console, să obții un fișier credentials.json și să îl plasezi în directorul rădăcină al proiectului. Urmează pașii de mai jos:

Mergi la Google Cloud Console.
Creează un proiect nou sau selectează unul existent.
Activează API-ul Google Calendar:
Mergi la API & Services > Library.
Căută "Google Calendar API" și activează-l.
Creează credențiale pentru aplicația ta:
Mergi la API & Services > Credentials.
Apasă pe Create Credentials și selectează OAuth 2.0 Client ID.
Alege Web application și configurează-ți redirect-urile.
Descarcă fișierul credentials.json și plasează-l în directorul rădăcină al proiectului tău.
6. Rulează aplicația
După ce ai instalat dependențele și ai configurat credențialele, poți rula aplicația Flask:

bash
Copy
python app.py
Serverul va fi disponibil la adresa http://127.0.0.1:5000/.

7. Testează API-ul
Poți testa endpoint-ul POST folosind un client HTTP precum Postman sau utilizând curl din linia de comandă. Iată exemplele de requesturi:

Request cu dată specificată:
json
Copy
{
    "emails": ["email1@example.com", "email2@example.com"],
    "datetime": "2025-03-07T15:00:00"
}
Request fără dată specificată (întâlnire instant):
json
Copy
{
    "emails": ["email1@example.com", "email2@example.com"]
}
Exemplu de request curl pentru a crea întâlnirea:

bash
Copy
curl -X POST http://127.0.0.1:5000/create_meeting \
-H "Content-Type: application/json" \
-d '{"emails": ["email1@example.com", "email2@example.com"], "datetime": "2025-03-07T15:00:00"}'
8. Alte informații
Portul implicit pentru aplicația Flask este 5000, dar poate fi modificat prin modificarea parametrului port în metoda app.run().
Dacă întâmpini erori de autentificare cu Google API, asigură-te că fișierul credentials.json este corect configurat și că ai acces la API-ul Google Calendar.

Fișiere și directoare importante
app.py: Codul aplicației care gestionează logica pentru crearea întâlnirii și serverul Flask.
requirements.txt: Lista dependențelor necesare pentru a rula aplicația.
credentials.json: Fișierul de autentificare pentru accesul la Google Calendar API (acest fișier nu este inclus în repository din motive de securitate).
token.json: Fișierul care stochează token-ul de acces și refresh token-ul pentru API-ul Google Calendar, creat automat în urma primei autentificări.