# Chatbot-A

A minimalist chatbot application with a FastAPI backend and a simple HTML/CSS/JS frontend.

## Features

- AI-powered chat interface using OpenAI's GPT model
- User authentication with JWT
- Simple responsive UI
- Conversation history tracking

## Setup

### Backend Setup

1. Navigate to the backend directory
   ```bash
   cd chatbot-a/backend
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your configuration:
   ```
   OPENAI_API_KEY=your_openai_api_key
   SECRET_KEY=your_secret_key
   OPENAI_MODEL=gpt-4
   ```

4. Run the backend server
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. Simply open the `frontend/index.html` file in a web browser, or serve it using a web server of your choice.

## Usage

1. Open the frontend URL (e.g., http://localhost:3000 if serving the frontend on port 3000)
2. Log in with the demo credentials:
   - Username: demo
   - Password: demo
3. Start chatting with the AI!

## Development

- Backend API documentation is available at http://localhost:8000/docs
- For local development, the frontend connects to the backend at http://localhost:8000

## License

MIT 