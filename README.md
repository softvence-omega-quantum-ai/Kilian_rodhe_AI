# PartyPlaneGenerator

Generate personalized birthday invitation cards and custom t-shirt designs using FastAPI, AI, and image processing.

## Features

- **Birthday Card Generation:** Create invitation cards with custom themes, messages, and images.
- **T-Shirt Design:** Generate t-shirt mockups based on user input and optional images.
- **Cloudinary Integration:** Upload and manage generated images.
- **AI-Powered:** Uses Google Generative AI for text and image generation.

## Tech Stack

- FastAPI
- Uvicorn
- Pillow
- Cloudinary
- Google Generative AI
- ONNX Runtime
- Tenacity

## Installation

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd PartyPlaneGenerator
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure environment variables and `config/config.yaml` as needed.

## Usage

Run the FastAPI server:

```bash
uvicorn main:app --reload
```

Access the API docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## API Endpoints

### 1. Generate Birthday Card

- **POST** `/api/v1/generate-card`
  - Request Body: JSON (see `app/schemas/invite.py`)
  - Response: Invitation text and image URLs

### 2. Generate T-Shirt Design

- **POST** `/t_shirt_generate`
  - Form Data: t-shirt type, size, gender, color, age, theme, optional description, optional image file
  - Response: Generated t-shirt mockup image URL

## Project Structure

```
PartyPlaneGenerator/
├── app/
│   ├── api/v1/endpoints/      # API endpoints
│   ├── schemas/              # Pydantic models
│   ├── services/             # Business logic
│   ├── utils/                # Helpers & logging
│   └── config.py             # App config
├── config/                   # YAML config
├── data/                     # Sample images
├── generated_cards/          # Output images
├── logs/                     # Log files
├── main.py                   # FastAPI entrypoint
├── requirements.txt          # Python dependencies
├── README.md                 # Project info
└── pyproject.toml            # Project metadata
```

## License

MIT

## Author

Roksana18cse04
