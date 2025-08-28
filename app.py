import streamlit as st
import random
from openai import OpenAI
import os
from dotenv import load_dotenv

# --- Load environment variables FIRST ---
load_dotenv()

# --- Setup LLM for text generation with OpenRouter API ---
try:
    # Fix: Get API key from environment variable and check if it exists
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    if not openrouter_api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable not found.")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=openrouter_api_key,
    )
except ValueError as e:
    st.error(f"Configuration Error: {e}")
    client = None
except Exception as e:
    st.error(f"Error connecting to OpenRouter: {e}")
    client = None


# --- Streamlit UI Components ---
st.title("🧙‍♂️ Creative AI Image Prompt Generator")
st.markdown("Enter a simple idea, and I'll create a detailed, amazing prompt for you.")

# User input text area
user_idea = st.text_input("Your Idea:", "A wise old wizard in a magical forest")

# LLM-generated components
def generate_creative_prompt(idea):
    """
    This function prompts the LLM to generate a full image prompt.
    """
    if not client:
        return {"positive_prompt": "API client not loaded.", "negative_prompt": "API client not loaded."}
    
    llm_prompt = f"""
    As an expert image prompt engineer, your task is to take a simple idea and transform it into a highly detailed, creative, and effective prompt for a state-of-the-art AI image generator.

    **Instructions:**
    - Expand the simple idea into a complex, descriptive prompt.
    - Include specific details about lighting, style, camera angle, and mood.
    - The final output should be a single, continuous sentence.
    - Start the final prompt with the phrase "**Amazing Prompt:**"

    **Simple Idea:** {idea}
    """
    
    try:
        response = client.chat.completions.create(
            model="openrouter/google/gemini-pro-1.5",
            messages=[
                {"role": "user", "content": llm_prompt},
            ],
            temperature=0.7,
            max_tokens=256,
        )
        
        positive_prompt = response.choices[0].message.content.strip()

        # Extract only the generated prompt section
        positive_prompt = positive_prompt.split("**Amazing Prompt:**")[-1].strip()

        negative_prompts = [
            "blurry, malformed, deformed, bad anatomy, ugly, low quality, cartoon, simple, out of frame, watermark, text"
        ]
        
        return {
            "positive_prompt": positive_prompt,
            "negative_prompt": random.choice(negative_prompts)
        }
    except Exception as e:
        return {"positive_prompt": f"Error during generation: {e}", "negative_prompt": "Error."}

# Button to generate the prompt
if st.button("✨ Create My Prompt"):
    if user_idea:
        with st.spinner("Generating an amazing prompt..."):
            result = generate_creative_prompt(user_idea)
            
            st.subheader("🎉 Your Prompts are Ready!")
            st.success("**Positive Prompt**")
            st.code(result["positive_prompt"])
            
            st.success("**Negative Prompt**")
            st.code(result["negative_prompt"])
            
            st.markdown("---")
            st.info("💡 **Pro-Tip:** Copy these prompts directly into your favorite AI image generator!")