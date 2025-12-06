import docx
import fitz  
import re
import nltk
from nltk.corpus import wordnet
from collections import Counter

try:
    nltk.data.find('corpora/wordnet.zip')
except LookupError:
    nltk.download('wordnet')

def read_txt(file):
    """Membaca file teks biasa (.txt)"""
    try:
        return file.read().decode("utf-8")
    except Exception as e:
        raise Exception(f"Gagal membaca TXT: {str(e)}")

def read_docx(file):
    """Membaca file Word (.docx)"""
    try:
        doc = docx.Document(file)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    full_text.append(cell.text)
        return '\n'.join(full_text)
    except Exception as e:
        raise Exception(f"Gagal membaca DOCX: {str(e)}")

def read_pdf(file):
    """
    Membaca file PDF menggunakan PyMuPDF (fitz).
    """
    try:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        full_text = []
        
        for page in doc:
            full_text.append(page.get_text())
            
        return '\n'.join(full_text)
    except Exception as e:
        raise Exception(f"Gagal membaca PDF: {str(e)}")

def count_word_occurrences(text, word):
    """
    Menghitung jumlah kemunculan satu kata/frasa.
    Menggunakan regex yang efisien.
    """
    if not word or not text:
        return 0
    escaped_word = re.escape(word.strip())
    pattern = r'\b' + escaped_word + r'\b'
    matches = re.findall(pattern, text, re.IGNORECASE)
    return len(matches)

def count_multiple_words(text, words_list):
    """
    Menghitung jumlah kemunculan untuk banyak kata target sekaligus.
    
    Args:
        text (str): Teks dokumen.
        words_list (list): List kata/frasa yang ingin dihitung.
        
    Returns:
        dict: Dictionary dengan key kata dan value jumlah kemunculan.
    """
    results = {}
    for word in words_list:
        results[word] = count_word_occurrences(text, word)
    return results

def get_top_words(text, top_n=5):
    """
    Mengambil kata terbanyak muncul untuk saran input.
    Hanya memproses 100.000 karakter pertama untuk kecepatan.
    """
    if not text: return []
    
    sample_text = text[:100000] 
    
    words = re.findall(r'\b\w{4,}\b', sample_text.lower())
    return [word for word, count in Counter(words).most_common(top_n)]

def get_synonyms(word):
    """Mendapatkan sinonim kata menggunakan NLTK"""
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            clean_lemma = lemma.name().replace('_', ' ')
            if clean_lemma.lower() != word.lower():
                synonyms.add(clean_lemma)
    return list(synonyms)[:5]

def format_results_for_download(target_data, results_data=None, format_type="csv"):
    """
    Memformat hasil untuk diunduh.
    
    Args:
        target_data: Bisa berupa string (single word) atau list (multi word dari input awal).
        results_data: Bisa berupa int (single count) atau dict (multi count).
        format_type: 'csv' atau 'txt'.
        
    Returns:
        str: String data yang siap didownload.
    """
    output = ""
    
    data_to_process = {}
    if isinstance(results_data, dict):
        data_to_process = results_data
    else:
        data_to_process = {str(target_data): results_data}

    if format_type == "csv":
        output = "Word,Count\n"
        for word, count in data_to_process.items():
            output += f"{word},{count}\n"
            
    elif format_type == "txt":
        output = "WORD COUNT ANALYSIS REPORT\n"
        output += "==========================\n\n"
        for word, count in data_to_process.items():
            output += f"Word: {word}\nCount: {count}\n--------------------------\n"
            
    return output