# Kilian Rodhe - AI Image Generation Service

একটি শক্তিশালী এবং স্বয়ংক্রিয় মার্চেন্ডাইজ ডিজাইন জেনারেশন সার্ভিস যা FastAPI, Google Generative AI (Gemini 2.5), এবং AWS S3 ব্যবহার করে কাস্টম টি-শার্ট এবং মগ ডিজাইন তৈরি করে।

A powerful automated merchandise design generation service that creates custom t-shirt and mug designs using FastAPI, Google Generative AI (Gemini 2.5), and AWS S3.

---

## 🎯 প্রজেক্ট সম্পর্কে (Project Overview)

এই প্রজেক্টটি একটি AI-পাওয়ারড মার্চেন্ডাইজ ডিজাইন সার্ভিস যা ইউজারদের টেক্সট প্রম্পট এবং অপশনাল ইমেজ আপলোড করার মাধ্যমে প্রফেশনাল টি-শার্ট এবং মগ ডিজাইন তৈরি করতে দেয়।

This project is an AI-powered merchandise design service that allows users to create professional t-shirt and mug designs through text prompts and optional image uploads.

### ✨ কী কী ফিচার আছে (Key Features)

- **🎨 AI-Powered Design Generation**: Google Gemini 2.5 Flash Image মডেল ব্যবহার করে স্বয়ংক্রিয় ডিজাইন তৈরি
- **👕 T-Shirt Design**: কাস্টম টি-শার্ট ডিজাইন এবং রিয়েলিস্টিক মকআপ তৈরি
- **☕ Mug Design**: প্রফেশনাল মগ ডিজাইন এবং মকআপ জেনারেশন (স্বয়ংক্রিয়ভাবে প্রম্পট থেকে ডিটেক্ট করে)
- **📸 Optional Logo Upload**: নিজের লোগো বা ইমেজ আপলোড করে ডিজাইনে ব্যবহার করার সুবিধা
- **☁️ AWS S3 Cloud Storage**: সব জেনারেটেড ইমেজ AWS S3-তে আপলোড এবং পাবলিক URL প্রদান
- **🔄 Automatic Retry Logic**: API ব্যর্থ হলে স্বয়ংক্রিয়ভাবে পুনরায় চেষ্টা (Tenacity দিয়ে)
- **📝 Professional Logging**: সব অপারেশনের জন্য বিস্তারিত লগিং সিস্টেম
- **🚀 Fast & Efficient**: FastAPI ব্যবহার করে দ্রুত এবং অ্যাসিঙ্ক্রোনাস API

---

## 🛠️ প্রযুক্তি স্ট্যাক (Tech Stack)

### Backend Framework
- **FastAPI**: আধুনিক, দ্রুত (high-performance) Python web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation এবং settings management

### AI/ML
- **Google Generative AI (Gemini 2.5 Flash Image)**: টেক্সট এবং ইমেজ জেনারেশন
- **google-genai**: Official Google Generative AI Python SDK

### Cloud & Storage
- **AWS S3**: ক্লাউড স্টোরেজ জেনারেটেড ইমেজের জন্য
- **Boto3**: AWS SDK for Python

### Image Processing
- **Pillow (PIL)**: ইমেজ প্রসেসিং এবং manipulation
- **Python-multipart**: ফাইল আপলোড হ্যান্ডলিং

### Utilities
- **Tenacity**: Retry logic এবং error handling
- **Python-dotenv**: এনভায়রনমেন্ট ভেরিয়েবল ম্যানেজমেন্ট
- **Requests**: HTTP রিকোয়েস্ট
- **Colorama**: টার্মিনাল কালার আউটপুট

### Development Tools
- **Docker**: Containerization support
- **Docker Compose**: Multi-container orchestration

---

## 📦 ইন্সটলেশন এবং সেটআপ (Installation & Setup)

### Prerequisites

- Python 3.8+
- Google Generative AI API Key
- AWS Account with S3 access
- pip বা conda প্যাকেজ ম্যানেজার

### Installation Steps

1. **Repository Clone করুন**:

   ```bash
   git clone https://github.com/yourusername/KilianRodhe_ImageGeneration_AI.git
   cd KilianRodhe_ImageGeneration_AI
   ```

2. **Dependencies Install করুন**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration**:
   
   প্রজেক্ট রুট ডিরেক্টরিতে একটি `.env` ফাইল তৈরি করুন:

   ```env
   # Google Gemini API
   GEMINI_API_KEY=your_gemini_api_key_here

   # AWS S3 Configuration
   AWS_ACCESS_KEY_ID=your_aws_access_key_id
   AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
   AWS_REGION=us-east-1
   AWS_S3_BUCKET_NAME=your_bucket_name
   ```

4. **Application Run করুন**:

   ```bash
   uvicorn main:app --reload
   ```

   অথবা production এর জন্য:

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

5. **Docker দিয়ে Run করুন** (Optional):

   ```bash
   docker-compose up --build
   ```

6. **API Documentation Access করুন**:
   - Swagger UI: http://127.0.0.1:8000/docs
   - ReDoc: http://127.0.0.1:8000/redoc

---

## 🔌 API Endpoints

### 1. Root Endpoint

**Endpoint**: `GET /`

**Description**: API service এর স্ট্যাটাস চেক করার জন্য

**Response**:

```json
{
  "message": "Welcome to the Kilian Rodhe API.Image Generation Service and project name is: Kilian_Rodhe"
}
```

---

### 2. Generate Merchandise Design

**Endpoint**: `POST /generate_merchandise`

**Description**: টেক্সট প্রম্পট এবং অপশনাল ইমেজ ব্যবহার করে টি-শার্ট বা মগ ডিজাইন এবং মকআপ তৈরি করে।

**Request Type**: `multipart/form-data`

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | string (Form) | ✅ Yes | ডিজাইনের বিস্তারিত বর্ণনা (e.g., "A cool gaming logo with neon colors") |
| `img_file` | file (File) | ❌ No | অপশনাল লোগো/ইমেজ ফাইল (JPEG, PNG, BMP) |

**Request Example**:

```bash
curl -X POST "http://127.0.0.1:8000/generate_merchandise" \
  -H "Content-Type: multipart/form-data" \
  -F "prompt=A minimalist coffee mug design with mountain silhouette" \
  -F "img_file=@/path/to/your/logo.png"
```

**Response Example**:

```json
{
  "generated_design_url": "https://your-bucket.s3.us-east-1.amazonaws.com/generated_images/20260204_143025_a1b2c3d4.png",
  "mockup_url": "https://your-bucket.s3.us-east-1.amazonaws.com/generated_images/20260204_143028_e5f6g7h8.png"
}
```

**Response Fields**:
- `generated_design_url`: প্রিন্ট-রেডি ডিজাইন ইমেজের AWS S3 URL
- `mockup_url`: রিয়েলিস্টিক প্রোডাক্ট মকআপের AWS S3 URL

**Supported File Types**:
- `image/jpeg` (.jpg, .jpeg)
- `image/png` (.png)
- `image/bmp` (.bmp)

**Error Responses**:

```json
// Invalid file type
{
  "detail": "Only Image file are acceptable."
}

// File not found
{
  "detail": "File not found."
}
```

---

## 🗂️ প্রজেক্ট স্ট্রাকচার (Project Structure)

```
KilianRodhe_ImageGeneration_AI/
│
├── main.py                     # FastAPI অ্যাপ্লিকেশন এন্ট্রি পয়েন্ট
├── requirements.txt            # Python dependencies
├── pyproject.toml             # Project metadata
├── Dockerfile                 # Docker containerization
├── docker-compose.yml         # Docker compose configuration
├── .env                       # Environment variables (not in repo)
├── README.md                  # এই ফাইল
│
├── app/                       # Main application package
│   ├── __init__.py
│   ├── config.py              # Configuration এবং constants
│   │
│   ├── api/                   # API routes
│   │   ├── __init__.py
│   │   └── v1/                # API version 1
│   │       ├── __init__.py
│   │       └── endpoints/     # API endpoint modules
│   │           ├── __init__.py
│   │           └── t_shirt_endpoint.py  # Merchandise generation endpoint
│   │
│   ├── services/              # Business logic services
│   │   ├── __init__.py
│   │   └── t_shirt/           # T-shirt/merchandise service
│   │       ├── __init__.py
│   │       └── shirt.py       # TShirt class - main design logic
│   │
│   ├── schemas/               # Pydantic models
│   │   ├── __init__.py
│   │   └── schema.py          # Data validation schemas
│   │
│   └── utils/                 # Utility functions
│       ├── __init__.py
│       ├── helper.py          # Helper functions (S3 upload, image processing)
│       └── logger.py          # Logging configuration
│
├── data/                      # Generated images temporary storage
├── logs/                      # Application logs
└── temp/                      # Temporary uploaded files
```

---

## 🎨 কীভাবে কাজ করে (How It Works)

### Design Generation Flow:

1. **User Input**: ইউজার টেক্সট প্রম্পট দেয় এবং অপশনালি একটি লোগো/ইমেজ আপলোড করে
2. **Image Upload**: যদি ইমেজ থাকে, তা temporary folder-এ সেভ হয়
3. **AI Processing**: 
   - Google Gemini 2.5 মডেল ব্যবহার করে প্রিন্ট-রেডি ডিজাইন তৈরি হয়
   - যদি ইমেজ দেওয়া থাকে, সেটি মূল লোগো হিসেবে preserve করা হয়
   - প্রম্পট অনুযায়ী কমপ্লিমেন্টারি এলিমেন্ট যোগ করা হয়
4. **Mockup Generation**:
   - প্রম্পট বিশ্লেষণ করে টি-শার্ট বা মগ ডিটেক্ট করা হয়
   - উপযুক্ত মকআপ তৈরি করা হয় (realistic product photography)
5. **S3 Upload**: উভয় ইমেজ AWS S3-এ আপলোড হয়
6. **Response**: পাবলিক URL-গুলো রিটার্ন করা হয়
7. **Cleanup**: Temporary ফাইল ডিলিট করা হয় (background task)

### Automatic Product Detection:

সিস্টেম স্বয়ংক্রিয়ভাবে বুঝে নেয় কোন ধরনের মকআপ তৈরি করতে হবে:
- প্রম্পটে **"mug"**, **"cup"**, বা **"ceramic"** থাকলে → Mug Mockup
- অন্যথায় → T-Shirt Mockup

### Retry Mechanism:

- API ব্যর্থ হলে স্বয়ংক্রিয়ভাবে **3 বার** পুনরায় চেষ্টা করে
- Exponential backoff ব্যবহার করে (4s, 8s, 10s)
- Server errors (500) এবং service unavailable errors হ্যান্ডল করে

---

## 📝 কোড আর্কিটেকচার (Code Architecture)

### Service Layer (`app/services/t_shirt/shirt.py`)

**TShirt Class** - মূল বিজনেস লজিক:

```python
class TShirt:
    - __init__(prompt): Constructor
    - model_client(): Gemini API client setup
    - generate_shirt_design(): প্রিন্ট-রেডি ডিজাইন তৈরি
    - generate_shirt_mockup(): টি-শার্ট mockup তৈরি
    - generate_mug_mockup(): মগ mockup তৈরি
    - generate_mockup(): স্বয়ংক্রিয় mockup সিলেকশন
    - _mockup_target(): প্রম্পট থেকে product type ডিটেক্ট
```

### API Layer (`app/api/v1/endpoints/t_shirt_endpoint.py`)

**Endpoints**:
- `POST /generate_merchandise`: মেইন API endpoint
  - Request validation
  - File upload handling
  - Service orchestration
  - Background task management
  - Error handling

### Utility Layer (`app/utils/helper.py`)

**Key Functions**:
- `s3_file_upload()`: AWS S3-এ ফাইল আপলোড
- `upload_image()`: ইমেজ file-কে API format-এ convert
- `response_data_img()`: API response থেকে ইমেজ extract এবং save
- `delete_file()`: Temporary ফাইল cleanup

### Configuration (`app/config.py`)

**Settings**:
- API keys এবং credentials
- Model configuration (Gemini 2.5 Flash Image)
- AWS S3 setup
- Paths এবং constants
- Prompt templates

---

## 🚀 ব্যবহারের উদাহরণ (Usage Examples)

### Example 1: Simple T-Shirt Design (Without Image)

```bash
curl -X POST "http://127.0.0.1:8000/generate_merchandise" \
  -F "prompt=Cool gaming t-shirt with neon RGB colors and futuristic elements"
```

### Example 2: T-Shirt with Logo

```bash
curl -X POST "http://127.0.0.1:8000/generate_merchandise" \
  -F "prompt=Professional corporate t-shirt design, minimalist style" \
  -F "img_file=@company_logo.png"
```

### Example 3: Coffee Mug Design

```bash
curl -X POST "http://127.0.0.1:8000/generate_merchandise" \
  -F "prompt=Coffee mug with mountain landscape and inspirational quote"
```

### Example 4: Mug with Custom Logo

```bash
curl -X POST "http://127.0.0.1:8000/generate_merchandise" \
  -F "prompt=Ceramic mug design with vintage aesthetic" \
  -F "img_file=@vintage_logo.png"
```

### Python Example:

```python
import requests

url = "http://127.0.0.1:8000/generate_merchandise"

# Without image
data = {
    "prompt": "Minimalist tech startup t-shirt with geometric patterns"
}
response = requests.post(url, data=data)
print(response.json())

# With image
files = {
    "img_file": open("logo.png", "rb")
}
data = {
    "prompt": "Modern t-shirt design incorporating the uploaded logo"
}
response = requests.post(url, data=data, files=files)
print(response.json())
```

---

## 🛡️ Error Handling

প্রজেক্টে বিভিন্ন লেভেলে error handling implement করা হয়েছে:

### API Level Errors:
- Invalid file type → HTTP 404
- File not found → HTTP 400
- General exceptions → HTTP 500

### Service Level Errors:
- Google API failures → Automatic retry (3 attempts)
- S3 upload failures → ClientError exception
- Image processing errors → ValueError

### Logging:
সব error এবং operation `logs/` ডিরেক্টরিতে log করা হয়:
- Info level: Normal operations
- Error level: Exceptions এবং failures
- Retry attempts ট্র্যাক করা হয়

---

## 🔧 Configuration Options

### Environment Variables:

```env
# Google Gemini API
GEMINI_API_KEY=your_key_here

# AWS S3
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1
AWS_S3_BUCKET_NAME=your_bucket_name
```

### Model Configuration (`app/config.py`):

```python
MODEL_NAME = "gemini-2.5-flash-image"
TEMPERATURE = 1.0  # Creativity level (0.0-2.0)
```

### Customizable Prompts:

`CLOTHING_DESIGN_PROMPT` ভেরিয়েবল এডিট করে ডিজাইন style কাস্টমাইজ করা যায়।

---

## 📊 Features Breakdown

### ✅ Implemented Features:

1. **AI-Powered Design Generation**
   - Text-to-image using Gemini 2.5
   - Logo preservation এবং integration
   - Print-ready output (transparent background)

2. **Multiple Product Support**
   - T-shirt designs এবং mockups
   - Mug designs এবং mockups
   - Automatic product detection

3. **File Upload & Processing**
   - JPEG, PNG, BMP support
   - Image validation
   - Temporary file management

4. **Cloud Storage Integration**
   - AWS S3 upload
   - Unique filename generation
   - Public URL generation

5. **Robust Error Handling**
   - Retry logic with exponential backoff
   - Comprehensive logging
   - Graceful degradation

6. **API Documentation**
   - Auto-generated Swagger UI
   - ReDoc documentation
   - Request/response examples

### 🔄 Workflow Features:

- **Background Tasks**: Temporary file cleanup
- **CORS Support**: Cross-origin requests enabled
- **Async Operations**: FastAPI async endpoints
- **Type Safety**: Pydantic validation

---

## 🐳 Docker Support

### Build and Run:

```bash
# Build image
docker build -t kilian-rodhe-api .

# Run container
docker run -p 8000:8000 --env-file .env kilian-rodhe-api

# Using docker-compose
docker-compose up -d
```

---

## 📈 Future Enhancements (Possible)

- [ ] More product types (hoodies, posters, phone cases)
- [ ] Batch processing multiple designs
- [ ] Design style presets
- [ ] User authentication এবং API keys
- [ ] Design history এবং favorites
- [ ] Advanced image editing options
- [ ] Custom mockup backgrounds
- [ ] PDF export for printing

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Soudeep Sarkar**

---

## 📞 Support

For issues and questions:
- Create an issue in the repository
- Contact: [your-email@example.com]

---

## 🙏 Acknowledgments

- Google Generative AI for Gemini 2.5 model
- FastAPI framework
- AWS S3 for cloud storage
- Open source community

---

**Made with ❤️ for automated merchandise design generation**

### 3. Party Planning

**Endpoint**: `POST /party_generate`

**Description**: Generates comprehensive party plans with gift suggestions and product recommendations.

**Request Body**:

```json
{
  "person_name": "John",
  "person_age": 8,
  "budget": 1500.0,
  "num_guests": 15,
  "party_date": "2025-12-15",
  "location": "Home",
  "party_details": {
    "theme": "Superhero",
    "favorite_activities": ["games", "dancing", "crafts"]
  },
  "num_product": 5
}
```

**Response**:

```json
{
  "party_plan": {
    "🎨 Theme & Decorations": ["decoration suggestions"],
    "🎉 Fun Activities": ["activity list"],
    "🍔 Food & Treats": ["food suggestions"],
    "🛍️ Party Supplies": ["supply list"],
    "⏰ Party Timeline": ["timeline with emojis"],
    "🎁 Suggested Gifts": ["gift suggestions"],
    "🌟 New Adventure Ideas": ["adventure ideas"]
  },
  "suggest_gifts": ["product recommendations"],
  "all_product": ["available products"]
}
```

## Project Structure

```
PartyPlaneGenerator/
├── app/
│   ├── api/v1/endpoints/          # API route handlers
│   │   ├── generate_card.py       # Birthday card endpoints
│   │   ├── t_shirt_endpoint.py    # T-shirt design endpoints
│   │   └── generate_party.py      # Party planning endpoints
│   ├── schemas/                   # Pydantic models
│   │   ├── invite.py             # Birthday card schemas
│   │   └── schema.py             # T-shirt and party schemas
│   ├── services/                  # Business logic
│   │   ├── generator.py          # Card generation service
│   │   ├── t_shirt/shirt.py      # T-shirt generation service
│   │   └── party/party.py        # Party planning service
│   ├── utils/                     # Utilities
│   │   ├── helper.py             # Helper functions
│   │   └── logger.py             # Logging configuration
│   └── config.py                 # Application configuration
├── config/                        # Configuration files
├── data/                         # Sample/reference images
├── generated_cards/              # Generated card outputs
├── logs/                         # Application logs
├── main.py                       # FastAPI application entry point
└── requirements.txt              # Python dependencies
```

## Configuration

### Environment Variables

| Variable                | Description                  | Required |
| ----------------------- | ---------------------------- | -------- |
| `GEMINI_API_KEY`        | Google Generative AI API key | Yes      |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary cloud name        | Yes      |
| `CLOUDINARY_API_KEY`    | Cloudinary API key           | Yes      |
| `CLOUDINARY_API_SECRET` | Cloudinary API secret        | Yes      |

### Application Settings

Key configuration constants in `app/config.py`:

- `MODEL_NAME`: "gemini-2.5-flash-image-preview"
- `PRODUCT_MODEL`: "gemini-2.5-flash"
- `TEMPERATURE`: 1.0
- `PRODUCT_API`: External product API endpoint

## Error Handling

The API implements comprehensive error handling:

- **400**: Bad Request (invalid file types, missing files)
- **404**: Not Found (file not found)
- **500**: Internal Server Error (AI generation failures, processing errors)

Retry logic is implemented for AI API calls with exponential backoff.

## Logging

Application logs are stored in the `logs/` directory with timestamps. Logs include:

- Request processing information
- AI generation status
- Error details and stack traces
- Retry attempts

## Development

### Running in Development Mode

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Testing

The application includes test files and sample data in the `data/` directory for development and testing purposes.

## Deployment

The application is configured for production deployment with:

- CORS middleware for cross-origin requests
- Async request handling
- Background task processing
- Automatic cleanup of temporary files

## License

MIT

## Author

Roksana18cse04

---
