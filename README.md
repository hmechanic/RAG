# Retrieval-Augmented Generation techniques 

**RAG** is a powerful AI tool designed for **real-life applications**. It supports the integration of state-of-the-art large language models (LLMs), including both **open-source** and subscription-based options. Additionally, it allows the implementation of advanced reasoning and foundation models to generate responses based on your **own data**.

To develop AI applications, we use **LlamaIndex** as the data orchestration framework. We also explore tools like **Groq**, which provides high-performance language processing units and free access to powerful open-source models.


## 1. Parsing Unstructured Files
There are several libraries to parse documents, each one can be used for a specific use case. 

### Nougat (Meta AI)
Trained to parse scientific documents (especially PDFs, even image-based ones) into a structured Markdown format (.mmd). It excels at recognizing and correctly formatting mathematical equations (LaTeX).

````
pip install nougat-ocr
````

### Markers PDF
**Optional (for GPU acceleration):**
- An NVIDIA GPU.
- CUDA Toolkit installed.
- PyTorch installed with CUDA support. Marker will automatically use the GPU if PyTorch detects one.
https://github.com/tesseract-ocr/tesseract?tab=readme-ov-file

#### Installation

```
pip install marker-pdf
```

-   **To include OCR capabilities (with Tesseract):**  
    You might need to install Tesseract OCR engine separately on your system first.
    
    -   On Ubuntu/Debian: sudo apt install tesseract-ocr libtesseract-dev tesseract-ocr-all (for all language packs)
        
    -   On macOS (using Homebrew): brew install tesseract tesseract-lang
        
    -   On Windows: Download the installer from the Tesseract GitHub page.  
        Then, when installing Marker, you might need an extra if specified by the documentation (though often Marker's dependencies might pull in pytesseract which interfaces with a system-installed Tesseract). For Marker, it seems to bundle its OCR dependencies more directly.

