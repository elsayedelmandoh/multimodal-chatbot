---
title: Multimodal Chatbot
emoji: 🏆
colorFrom: green
colorTo: red
sdk: gradio
sdk_version: 6.5.1
app_file: app.py
pinned: false
---

# Build and Deploy a Multimodal Chatbot

## Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Setup](#setup)
  - [Clone from GitHub](#clone-from-github)
  - [Conda environment](#conda-environment)
  - [Run locally](#run-locally)
  - [Duplicate Hugging Face Space](#duplicate-hugging-face-space)
- [Contributing](#contributing)
- [Author](#author)

## Overview
This is a multimodal chatbot application that leverages advanced image analysis and computer vision capabilities. It accepts both text and image inputs, analyzing visual content in detail to understand composition, objects, and contextual elements. The chatbot processes uploaded images through state-of-the-art AI models, providing specific descriptions and insights that can be used across machine learning, computer vision, and multimodal AI applications. Perfect for tasks requiring visual understanding combined with conversational AI.

## Project Structure
```
web-search/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .gitattributes
├── .env
├── research/
│   └── notebook.ipynb
└── src/
    ├── __init__.py
    ├── config/
    │   ├── __init__.py
    │   └── settings.py
    └── utils/
        ├── __init__.py
        └── helpers.py
```

## Setup

- GitHub repo: [link](https://github.com/elsayedelmandoh/multimodal-chatbot)
- Hugging Face Space: [link](https://huggingface.co/spaces/elsayedelmandoh/multimodal-chatbot)

### Clone from GitHub
```bash
git clone https://github.com/elsayedelmandoh/multimodal-chatbot
cd multimodal-chatbot
```

### Conda environment
```bash
# create & activate
conda create -n multimodal-chatbot python=3.12 -y
conda activate multimodal-chatbot

# install pip then dependencies
conda install pip -y
pip install -r requirements.txt
```
You may use a .env loader or store vars in the Hugging Face Space secrets.

### Run locally
```bash
python app.py
```
Open the URL printed in the terminal.

### Duplicate Hugging Face Space

Hugging Face Space URL used in this project:
https://huggingface.co/spaces/elsayedelmandoh/multimodal-chatbot

1. Sign in to Hugging Face.
2. Go to the Space you want to duplicate.
3. Click the "Duplicate this Space" button.
4. Choose a new name and visibility, then Duplicate Space.
5. In the new Space settings add secrets (GEMINI_API_KEY) and push code.

## Contributing
1. Fork the repository.
2. Create a branch for your change.
3. Make changes, commit with clear messages.
4. Push to your fork and open a pull request.

## Author
Developed by Elsayed Elmandoh — NLP Engineer.  
LinkedIn: https://linkedin.com/in/elsayed-elmandoh-b5849a1b8/  
X/Twitter: https://x.com/aangpy
