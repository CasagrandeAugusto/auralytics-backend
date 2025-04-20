# Auralytics Backend

Este proyecto corre una API en FastAPI que recibe archivos de audio, los transcribe usando Whisper (OpenAI) y genera un informe con GPT-4.

## Cómo desplegar en Railway

1. Subí este repositorio a GitHub
2. Conectalo a Railway
3. Agregá una variable de entorno:
   - `OPENAI_API_KEY` = tu clave de OpenAI
4. Railway va a detectar el `Procfile` y crear la URL automáticamente

Endpoint:
POST /upload (archivo de audio)