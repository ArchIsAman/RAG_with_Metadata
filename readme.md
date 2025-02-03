# RAG Model – README

## Overview
This project implements a **Retrieval-Augmented Generation (RAG) Model** that enhances text generation by retrieving relevant documents based on similarity search which uses metadata for each document for source citation and data validation. It uses **cosine similarity** for retrieval and uses the **mxbai-embed-large** tokenizer . The model is hosted using **Streamlit** for an interactive and user-friendly experience.

## Features
- **Document Uploading**: Supports PDFs, plain text files, and website links.
- **Web Scraping**: Uses **BeautifulSoup** to extract content from provided URLs.
- **Metadata Storage**: Keeps track of document details for efficient retrieval.
- **Retrieval Mechanism**: Uses **cosine similarity** to fetch relevant content.
- **Citation of Sources**: Displays the source of retrieved information in responses.
- **Conversation History**: Maintains chat history for continuity.


## Usage
1. **Upload a Document** (`PDF/Text/URL`) using upload.py.
2. **Enter a Query** in the chat interface.
3. **Retrieve and Generate** an answer with cited sources.
4. **Continue the Conversation** while maintaining history.


## Future Improvements
- Implementing **vector databases** for efficient large-scale retrieval.
- Adding **multi-document summarization** for better contextual understanding.
- Enhancing **conversation memory** with longer-term storage.

## License
This project is licensed under the MIT License.
