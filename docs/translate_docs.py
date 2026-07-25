import os
import polib
from google import genai
from google.genai import types

def translate_po_file(po_file_path, target_language):
    po = polib.pofile(po_file_path)
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print(f"Skipping {po_file_path}: GEMINI_API_KEY not set. Add it to GitHub Secrets.")
        return
        
    client = genai.Client() # Requires GEMINI_API_KEY environment variable
    
    system_instruction = (
        f"You are a technical translator specializing in solar energy, inverters (Huawei SUN2000), and software engineering. "
        f"Translate the following text from Ukrainian to {target_language}. "
        f"Preserve all markdown formatting (like *, _, `), placeholders, and technical terms. "
        f"Do not add any extra conversational text, output only the translation."
    )
    
    modified = False
    for entry in po:
        # Translate only if msgstr is empty
        if not entry.msgstr:
            print(f"Translating to {target_language}: {entry.msgid[:50]}...")
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=entry.msgid,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                    )
                )
                entry.msgstr = response.text.strip()
                modified = True
            except Exception as e:
                print(f"Error translating: {e}")
                
    if modified:
        po.save(po_file_path)
        print(f"Saved translations to {po_file_path}")
    else:
        print(f"No new translations needed for {po_file_path}")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    locale_dir = os.path.join(base_dir, 'locale')
    
    languages = {'en': 'English', 'zh_CN': 'Simplified Chinese'}
    
    for lang, lang_name in languages.items():
        lang_dir = os.path.join(locale_dir, lang, 'LC_MESSAGES')
        if not os.path.exists(lang_dir):
            continue
            
        for filename in os.listdir(lang_dir):
            if filename.endswith('.po'):
                po_path = os.path.join(lang_dir, filename)
                print(f"Processing {po_path} for {lang_name}")
                translate_po_file(po_path, lang_name)

if __name__ == "__main__":
    main()
