# tools/transcribe_audio.py
from langchain_core.tools import tool
import os
import subprocess

@tool
def transcribe_audio(filename: str, model: str = "small") -> str:
    """
    Transcribe an audio file (.opus/.wav) to lowercase text using Whisper.
    """
    try:
        # LAZY IMPORT - Only when tool is called
        import whisper
        
        # Check ffmpeg
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        
        # File existence check
        if not os.path.exists(filename):
            alt_path = os.path.join("LLMFiles", filename)
            if os.path.exists(alt_path):
                filename = alt_path
            else:
                return f"Error: file '{filename}' not found (checked LLMFiles/)"
        
        # Convert opus/ogg to wav
        base, ext = os.path.splitext(filename)
        if ext.lower() in ['.opus', '.ogg']:
            wav_path = base + '.wav'
            cmd = ['ffmpeg', '-y', '-i', filename, '-ar', '16000', '-ac', '1', wav_path]
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            filename = wav_path
        
        # Transcribe
        model_obj = whisper.load_model(model)
        result = model_obj.transcribe(filename)
        text = result['text'].strip().lower()
        print(f"✓ Transcribed '{filename}': {text}")
        return text
        
    except ImportError:
        return "Error: openai-whisper not installed. Run: pip install openai-whisper torch torchaudio --extra-index-url https://download.pytorch.org/whl/cpu"
    except FileNotFoundError:
        return "Error: ffmpeg not found. Install ffmpeg system-wide."
    except subprocess.CalledProcessError as e:
        return f"ffmpeg error: {e.stderr.decode('utf-8', errors='ignore')}"
    except Exception as e:
        return f"Transcription failed: {str(e)}"
