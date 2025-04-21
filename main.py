from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from openai import OpenAI
import shutil
import os
import logging

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

logging.basicConfig(level=logging.INFO)

@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    try:
        # Guardar el archivo en disco temporalmente
        temp_file_path = "temp_audio.mp3"
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        with open(temp_file_path, "rb") as audio_file:
            # Asegurarse de que el archivo tiene nombre
            audio_file.name = file.filename

            # Transcripción con Whisper
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )

        # Armar el prompt para GPT
        prompt = f"""
Actuá como un analista de conversaciones. Generá un informe con:
1. Resumen (máx. 5 líneas)
2. Objeciones o temas clave
3. Tareas o próximos pasos
4. Tono emocional

Texto: {transcript.text}
        """

        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )

        return {
            "transcripcion": transcript.text,
            "informe": completion.choices[0].message.content
        }

    except Exception as e:
        logging.exception("Error procesando el audio")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)