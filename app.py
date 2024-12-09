
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from fastapi.responses import JSONResponse
from typing import List

# Initialize FastAPI app
app = FastAPI()

# Allow CORS for all origins (adjust origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


model_name = "openai-community/gpt2"  
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
text_gen_model = pipeline('text-generation', model=model, tokenizer=tokenizer)  # device=0 to use GPU


def generate_ai_suggestions(input_text: str, num_suggestions: int = 3) -> List[str]:
    """
    Generate AI-based suggestions using the text generation model.

    :param input_text: Input string for generating suggestions.
    :param num_suggestions: Number of suggestions to return.
    :return: List of generated suggestions.
    """
    generated = text_gen_model(input_text, max_length=20, num_return_sequences=num_suggestions, num_beams=3)
    return [g['generated_text'].strip() for g in generated]


@app.route('/suggest', methods=["POST"])
async def suggest(request: Request):
    """
    Endpoint to provide suggestions based on user input.

    :param request: Incoming POST request with JSON data.
    :return: JSON response containing suggestions.
    """
    data = await request.json()
    user_input = data.get('input', '')

    if user_input:
        ai_suggestions = generate_ai_suggestions(user_input, num_suggestions=3)
        return JSONResponse(content={"suggestions": ai_suggestions})

    return JSONResponse(content={"suggestions": []})


@app.route('/get-first-prompt', methods=["GET"])
def get_first_prompt():
    """
    Endpoint to return the initial prompt as a placeholder.

    :return: JSON response with the first prompt.
    """
    return JSONResponse(content={"prompt": "Type something here..."})


# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
