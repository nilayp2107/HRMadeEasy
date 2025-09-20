from transformers import AutoModelForCausalLM, AutoTokenizer
import os

# Use full repo_id (downloads from HF cache if already present)
BASE_DIR = os.path.dirname(__file__)
model_path = os.path.join(BASE_DIR, "Mistral-7B-v0.1")

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Load model
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype="float16",   # safer for macOS/MPS
    low_cpu_mem_usage=True,
    device_map="auto"             # GPU if available, else CPU
)

def llm_response(context, query, max_new_tokens=300):
    """
    Generate a response from the local GPT-OSS-20B LLM.
    """
    prompt = f"""
    You are a helpful assistant. Use the following contexts to answer the query. Make only a short paragraph
    and no points, unlesss stated in the query

    Context:
    {context}

    Query:
    {query}

    Answer:
    """

    # Tokenize
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    # Generate
    outputs = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        temperature=0.7,
        do_sample=True,
        top_p=0.9,
    )

    # Decode
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Try to split on "Answer:"
    if "Answer:" in response:
        answer = response.split("Answer:")[-1].strip()
    else:
        answer = response.strip()

    return answer


# Test
#print(llm_response("Hello how are you?", "What is earth?"))
