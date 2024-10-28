# Personal_FastAPIPythonBackend
Servidor para gestionar acciones, registros y usuarios de diversos proyectos personales.

Se necesita generar un .env

SUPABASE_URL="https://***.supabase.co"
SUPABASE_KEY="***"

Inicializar

python -m venv venv //  py -m venv venv 
venv\Scripts\activate (Windows) o source venv/bin/activate (Mac)
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload


http://localhost:8000/

Extras

npm i -g vercel