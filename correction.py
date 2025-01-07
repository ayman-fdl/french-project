from groq import Groq
from typing import Dict, List
from dotenv import load_dotenv
import os

# import the Groq key
load_dotenv()
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

# Define the Llama models 
LLAMA3_70B_INSTRUCT = "llama-3.1-70b-versatile"
LLAMA3_8B_INSTRUCT = "llama3.1-8b-instant"

DEFAULT_MODEL = LLAMA3_70B_INSTRUCT

# Define the user and the assistant roles
def assistant(content: str):
    return { "role": "assistant", "content": content }

def user(content: str):
    return { "role": "user", "content": content }


# Creat the chat to interact with Llama 
def chat_completion(
    messages: List[Dict],
    model = DEFAULT_MODEL,
    temperature: float = 0.2,
    top_p: float = 0.9,
) -> str:
    response = client.chat.completions.create(
        messages=messages,
        model=model,
        temperature=temperature,
        top_p=top_p,
    )
    return response.choices[0].message.content

# The Correction function
def Correction(text):
    # Check if the text is in french
    is_french = chat_completion(messages=[
    user("Tu es un expert en linguistique française spécialisé dans l'analyse de texte. Ta tâche est de déterminer si un texte est écrit en français ou non. Réponds uniquement par 'Oui' si le texte est écrit en français, sinon réponds 'Non'."),
    user("Je vais au magasin acheter des légumes et du pain demain."),
    assistant("Oui"),
    user("Elle a oublié ses clés sur la table avant de sortir."),
    assistant("Oui"),
    user("This text is written in English."),
    assistant("Non"),
    user("Ich gehe morgen zum Markt, um Gemüse und Brot zu kaufen."),
    assistant("Non"),
    user(text),
    ])

    # Correct the prompt
    
    if is_french == "Oui":
        correct = chat_completion(messages=[
        user("Tu es un expert en linguistique française spécialisé dans la correction des textes. Pour chaque texte, corrige les erreurs grammaticales, orthographiques, syntaxiques et de ponctuation. Assure-toi de conserver la signification d'origine du texte tout en le rendant clair et grammaticalement correct. Retourner uniquement le texte corrigé, propre et bien formaté, sans aucune analyse supplémentaire. Pour chaque texte extrait uniquement le texte sans la question."),
        user("Voici le texte : Je vais magasin acheter des legume et du pain demain."),
        assistant("Je vais au magasin acheter des légumes et du pain demain."),
        user("Texte: Elle a oubliée ses cles sur la table avant de sortir."),
        assistant("Elle a oublié ses clés sur la table avant de sortir."),
        user("Elle a mangé des pommes et des bananes."),
        assistant("Elle a mangé des pommes et des bananes."),
        user("Je mappelle Angélica Summer, jai 12 ans etje suis canadienne Il y a 5 ans, ma famille et moi avons deménagé dans le sud de la France."),
        assistant("Je m'appelle Angélica Summer, j'ai 12 ans et je suis canadienne. Il y a 5 ans, ma famille et moi avons déménagé dans le sud de la France."),
        user(text),
        ])
        return correct
    else:
        return None