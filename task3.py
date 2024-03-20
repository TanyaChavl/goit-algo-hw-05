import timeit
from docx import Document
from difflib import SequenceMatcher

# Функція для екстракції тексту з файлу .docx
def read_docx(file_path):
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

# Читання тексту з обох статей
article1_text = read_docx("documents/стаття_1.docx")
article2_text = read_docx("documents/стаття_2.docx")

# Перевірка чи були зчитані файли
len(article1_text), len(article2_text)

# Функції алгоритмів пошуку підрядка

# Алгоритм Кнута-Морріса-Пратта для пошуку підрядка
def knuth_morris_pratt(text, pattern):
    def compute_lps_array(pattern):
        length = 0
        lps = [0] * len(pattern)
        i = 1
        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length-1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

    lps = compute_lps_array(pattern)
    i = j = 0
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == len(pattern):
            return i - j  # Підрядок знайдено
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j-1]
            else:
                i += 1
    return -1  # Підрядок не знайдено


# Алгоритм Рабіна-Карпа для пошуку підрядка
def rabin_karp(text, pattern):
    d = 256
    q = 101
    M = len(pattern)
    N = len(text)
    i = j = 0
    p = t = 0  # hash value for pattern and text
    h = 1
    for i in range(M-1):
        h = (h * d) % q
    for i in range(M):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q
    for i in range(N-M+1):
        if p == t:
            for j in range(M):
                if text[i+j] != pattern[j]:
                    break
            j += 1
            if j == M:
                return i  # Підрядок знайдено
        if i < N-M:
            t = (d*(t-ord(text[i])*h) + ord(text[i+M])) % q
            if t < 0:
                t = t+q
    return -1  # Підрядок не знайдено


# Алгоритм Боєра-Мура
def boyer_moore_horspool(text, pattern):
    m = len(pattern)
    n = len(text)
    if m > n:
        return -1
    skip = {pattern[i]: m - i - 1 for i in range(m - 1)}
    skip_default = m
    i = 0
    while i <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[i + j]:
            j -= 1
        if j < 0:
            return i  # Підрядок знайдено
        i += skip.get(text[i + m - 1], skip_default)
    return -1  # Підрядок не знайдено

# Підрядки для пошуку в статтях
patterns = ["рекомендаційної системи", "гіпотетичний алгоритм"]
texts = [article1_text, article2_text]
algorithms = [knuth_morris_pratt, rabin_karp, boyer_moore_horspool]

# Вимірювання часу
results = {}
for text_index, text in enumerate(texts, start=1):
    for pattern in patterns:
        for algorithm in algorithms:
            time_taken = timeit.timeit(lambda: algorithm(text, pattern), number=10)
            results[(text_index, pattern, algorithm.__name__)] = time_taken

print(results)
