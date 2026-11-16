import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialise the OpenAI client
client = OpenAI(
    api_key=os.getenv("OPEN_API_KEY")
)

default_response = client.responses.create(
    model = "gpt-5.5",
    input = "Create me a muscle building workout excerise for a beginner"
)

print("Default no Schema " + default_response.output_text)

# Send a request to the AI model
response = client.responses.create(
    model="gpt-5.5",
    input="Create me a muscle building workout excerise for a beginner",
    text = {
        "format" : {
            "type" : "json_schema",
            "name" : "workout_exercise",
            "strict" : True,
            "schema" : {
                "type" : "object",
                "properties" : {
                    "exercise" : {"type" : "string"},
                    "sets" : {"type" : "integer"},
                    "reps" : {"type" : "integer"},
                    "rest_seconds" : {"type":"integer"}
                },
                "required" : ["exercise","sets","reps","rest_seconds"],
                "additionalProperties" : False
            }
        }
    }
)

json_text = response.output_text
print("Jason Text : " + json_text)

# Convert JSON text into a Python Dictionary
workout = json.loads(json_text)
print(workout)
print("Specific workout " + workout["exercise"])