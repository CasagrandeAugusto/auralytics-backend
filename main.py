from fastapi import FastAPI, File, UploadFile
import openai
import shutil
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    with open("audio.mp3", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    audio_file = open("audio.mp3", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)

    prompt = f"""
Actuá como un analista de conversaciones. Generá un informe con:
1. Resumen (máx. 5 líneas)
2. Objeciones o temas clave
3. Tareas o próximos pasos
4. Tono emocional

Texto: {transcript['text']}
    """
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "transcripcion": transcript["text"],
        "informe": completion.choices[0].message["content"]
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=port)