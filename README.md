# Limbu Transliteration System

This repository hosts a **Limbu Transliteration System**, enabling seamless conversion between the Limbu, Devanagari, and Roman scripts. Designed to bridge linguistic gaps, this project leverages **Natural Language Processing (NLP)** techniques to preserve the Limbu language and make it more accessible to diverse audiences.

---

## Features

- **Multi-Script Transliteration**:
  - Limbu ↔ Roman
  - Limbu ↔ Devanagari
- **Round-Trip Fidelity**
- **Collision Handling**
- **Reverse Mapping**

---

## Project Motivation

The **Limbu language** is spoken by approximately 410,000 people, primarily in Nepal, India, and Bhutan. With no existing transliteration service for this language, the project aims to:

1. **Preserve Linguistic Heritage**: Enable wider digital usage of the Limbu script.
2. **Bridge Cultural Gaps**: Facilitate communication between communities using different scripts.
3. **Empower Research and Education**: Provide tools for linguists and educators to explore the Limbu language.

---

## Installation

### Prerequisites
- Python 3.8 or higher
- Flask

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/limbu-transliteration.git
   cd limbu-transliteration
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask app:
   ```bash
   python app.py
   ```

4. Access the application in your browser at `http://127.0.0.1:5000`.

---

## Usage

1. **Select Transliteration Mode**:
   - Limbu → Roman
   - Limbu → Devanagari
   - Devanagari → Limbu
   - Roman → Limbu

2. **Enter Text**:
   - Use the provided text area to input Limbu, Devanagari, or Roman text.

3. **Submit and View Output**:
   - The transliterated text will appear along with debugging logs (optional).

---

## Technical Overview

### Architecture
1. **Core Logic (`transliteration.py`)**:
   - Contains mappings and algorithms for transliteration between scripts.
2. **Web Application (`app.py`)**:
   - Flask-based API for handling user input and calling transliteration functions.
3. **Front-End Interface (`index.html`)**:
   - Simple UI for selecting transliteration modes and testing the system.

### Fonts Used
The following fonts are utilized to ensure proper rendering of the Limbu script:

- **Namdhinggo Font**: Self-hosted under `static/fonts` for accurate representation of Limbu characters.
- **Noto Sans Limbu**: Available on Google Fonts for additional compatibility.

---

## Future Enhancements

- **Optical Character Recognition (OCR)**:
  - Support for recognizing Limbu script in scanned documents.
- **Computer Vision**:
  - Context-aware recognition of handwritten or stylized Limbu text.
- **Enhanced NLP Tools**:
  - Improved tokenization and transliteration accuracy.
- **Community Collaboration**:
  - Contributions from linguists, educators, and developers to refine the system.

---

## Acknowledgments

This project draws inspiration and references from the detailed research available at [Omniglot - Limbu Writing System](https://www.omniglot.com/writing/limbu.htm). A special thanks to the creators of such valuable linguistic resources.

---

## License

This project is licensed under the MIT License.
