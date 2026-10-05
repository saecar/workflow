import os
import google.generativeai as genai

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY tidak ditemukan!")

genai.configure(api_key=api_key)

def get_project_structure(path="."):
    ignore_dirs = {".git", "__pycache__", "node_modules", "venv", "env", ".next", "dist", "build"}
    structure = []
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for file in files:
            if file == "generate_readme.py": 
                continue
            relative_path = os.path.relpath(os.path.join(root, file), path)
            structure.append(relative_path)
    return "\n".join(structure[:100])

file_list = get_project_structure()

prompt = f"""
Kamu adalah seorang Technical Writer dan Senior Software Engineer. 
Berdasarkan daftar file proyek berikut ini, buatkan file `README.md` yang sangat profesional, rapi, dan terstruktur dalam format Markdown.

Struktur file dalam proyek ini:
{file_list}

README.md harus mencakup:
1. Judul Proyek & Deskripsi Singkat yang menarik.
2. Tech Stack / Teknologi yang digunakan.
3. Fitur Utama (Key Features).
4. Panduan Instalasi & Konfigurasi (Step-by-step yang baik dan benar).
5. Cara Menjalankan Proyek.

Gunakan bahasa Indonesia, gunakan emoji secukupnya, dan pastikan bersih tanpa teks penjelasan di luar format Markdown.
"""

model = genai.GenerativeModel("gemini-2.5-flash")
response = model.generate_content(prompt)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(response.text)

print("README.md berhasil di-generate secara otomatis oleh AI!")