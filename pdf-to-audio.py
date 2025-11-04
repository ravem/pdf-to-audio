import asyncio
import edge_tts
import fitz  # PyMuPDF

def pdf_to_text(pdf_file):
    """Estrae tutto il testo da un file PDF, aggiungendo micro-pause e pause tra paragrafi."""
    text = ''
    with fitz.open(pdf_file) as doc:
        for page in doc:
            page_text = page.get_text("text").strip()
            for paragraph in page_text.split('\n'):
                line = paragraph.strip()
                if line:
                    # micro-pause dopo punteggiatura
                    line = line.replace('.', '. …').replace(',', ', …').replace(';', '; …').replace(':', ': …')
                    # pausa più lunga tra paragrafi
                    if len(line) < 50:
                        text += line + '\n'
                    elif len(line) < 150:
                        text += line + '\n\n'
                    else:
                        text += line + '\n\n\n'
    return text.strip()

async def text_to_speech_edge(text, output_file, voice="it-IT-IsabellaNeural", rate="+0%"):
    """Usa edge-tts per creare il file MP3."""
    communicate = edge_tts.Communicate(text, voice=voice, rate=rate)
    await communicate.save(output_file)
    print(f"✅ Audio generato: {output_file}")

if __name__ == "__main__":
    pdf_file = "1.pdf"
    output_file = "1.mp3"
    text_content = pdf_to_text(pdf_file)
    # Esegui l’async
    asyncio.run(text_to_speech_edge(text_content, output_file, voice="it-IT-IsabellaNeural", rate="+10%"))
