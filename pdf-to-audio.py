import asyncio
import fitz  # PyMuPDF
import edge_tts
from langdetect import detect


# --------------------------------------------------
# Estrazione testo dal PDF con pause naturali
# --------------------------------------------------
def pdf_to_text(pdf_file):
    """Estrae il testo da un PDF aggiungendo micro-pause e pause tra paragrafi."""
    text = ""

    with fitz.open(pdf_file) as doc:
        for page in doc:
            page_text = page.get_text("text")
            for paragraph in page_text.split("\n"):
                line = paragraph.strip()
                if not line:
                    continue

                # micro-pause dopo punteggiatura
                line = (
                    line.replace(".", ". …")
                        .replace(",", ", …")
                        .replace(";", "; …")
                        .replace(":", ": …")
                )

                # pause dinamiche
                if len(line) < 50:
                    text += line + "\n"
                elif len(line) < 150:
                    text += line + "\n\n"
                else:
                    text += line + "\n\n\n"

    return text.strip()


# --------------------------------------------------
# Rilevamento lingua dominante
# --------------------------------------------------
def detect_language(text):
    """Rileva la lingua principale del testo e restituisce la voce edge-tts."""
    try:
        lang = detect(text[:1000])
    except Exception:
        lang = "it"

    voices = {
        "it": "it-IT-IsabellaNeural",
        "en": "en-GB-LibbyNeural",
        "fr": "fr-FR-DeniseNeural",
        "es": "es-ES-ElviraNeural",
        "de": "de-DE-KatjaNeural",
    }

    voice = voices.get(lang, "it-IT-IsabellaNeural")
    print(f"🌍 Lingua rilevata: {lang} → Voce: {voice}")
    return voice


# --------------------------------------------------
# Suddivisione testo in blocchi compatibili con edge-tts
# --------------------------------------------------
def split_text(text, max_chars=4000):
    """Divide il testo in blocchi sicuri per edge-tts."""
    chunks = []
    current = ""

    for line in text.splitlines():
        if len(current) + len(line) < max_chars:
            current += line + "\n"
        else:
            chunks.append(current.strip())
            current = line + "\n"

    if current.strip():
        chunks.append(current.strip())

    return chunks


# --------------------------------------------------
# Generazione audio MP3
# --------------------------------------------------
async def text_to_speech_edge(text, output_file, voice, rate="+10%"):
    chunks = split_text(text)
    print(f"🔊 Testo diviso in {len(chunks)} parti")

    with open(output_file, "wb") as f:
        for i, chunk in enumerate(chunks, 1):
            print(f"▶️ Generazione parte {i}/{len(chunks)}")
            communicate = edge_tts.Communicate(
                chunk,
                voice=voice,
                rate=rate
            )
            async for data in communicate.stream():
                if data["type"] == "audio":
                    f.write(data["data"])

    print(f"✅ Audio generato: {output_file}")


# --------------------------------------------------
# MAIN
# --------------------------------------------------
if __name__ == "__main__":
    pdf_file = "1.pdf"
    output_file = "1.mp3"

    text_content = pdf_to_text(pdf_file)
    voice = detect_language(text_content)

    asyncio.run(
        text_to_speech_edge(
            text_content,
            output_file,
            voice=voice,
            rate="+10%"
        )
    )
