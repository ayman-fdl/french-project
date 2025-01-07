import anthropic
import json
from correction import Correction
from dotenv import load_dotenv
import os

# import the Groq key
load_dotenv()

# Claude model
sonnet = "claude-3-5-sonnet-20241022"
opus = "claude-3-opus-20240229"

# Define the system prompt for < Claude>
system_prompt_claude = open('Prompt.txt', 'r').read()
system_val_prompt_claude = open('validation_promt.txt', 'r').read()

# Generate the analysis using < Claude >
def chat_completion(system_prompt,prompt,model_name):
    
    if prompt:
        client = anthropic.Anthropic(
        api_key=os.getenv('ANTHROPIC_API_KEY')
        )
        
        try:
            # Make the API call
            message = client.messages.create(
                model=model_name,
                max_tokens=4000, # The maximum number of tokens to generate before stopping.
                temperature=0.1,
                system=system_prompt,
                messages = [ # specify the prior conversational turns with the messages parameter
                            {"role": "user", "content": prompt}
                        ]
            )
        
            # New approach to handle response
            if message and message.content:
                # Extract text from the first content block
                response_text = message.content[0].text if message.content[0].type == 'text' else None
                
                if response_text:
                    # format the response
                    response_text = response_text.split("<answer>\n")[1]
                    response_text = response_text.split("\n</answer>")[0]
                    text_analysis = json.loads(response_text)
                    return text_analysis
                else:
                    print("Error: No text content found in response.")
                    return None
            else:
                print("Error: No content in API response.")
                return None

        except anthropic.APIConnectionError as e:
            print(f"Anthropic API error: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None
    else:
        return None

# validation step
def get_results(prompt):
    formatted_prompt = "<Text> "+ prompt + "</Text>"
        
    # Generate the result
    result_temp = chat_completion(system_prompt_claude,formatted_prompt,sonnet)

    # Format the prompt for the validation step
    formatted_prompt_val = formatted_prompt + "\n<statistiques>" + json.dumps(result_temp, ensure_ascii=False, indent=4) + "\n</statistiques>"

    # Validate the temp result and get the validation
    val = chat_completion(system_val_prompt_claude,formatted_prompt_val,sonnet)

    return val
