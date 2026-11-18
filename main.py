import os
import json
import openai

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key = os.getenv("OPEN_API_KEY")
)

def muscle_specific_workout(muscle):
    try:
        response = client.responses.create(
        model = "gpt-5.5",
        input = f"Generate me a 5 exercise plan to train {muscle} today.",
        text = {
            "format" : {
                "type" : "json_schema",
                "name" : "muscle_specific_workout",
                "strict" : True,
                "schema" : {
                    "type" : "object",
                    "properties" : {
                        "workout_duration_in_minutes" : {"type" : "integer"},
                        "exercises" : {
                            "type" : "array",
                            "items" : {
                                "type" : "object",
                                "properties" : {
                                    "exercise" : {"type" : "string"},
                                    "sets" : {"type" : "integer"},
                                    "reps" : {"type" : "integer"},
                                    "intensity" : {"type" : "string"},
                                    "rest_between_sets" : {"type" : "integer"}
                                },
                                "required" : ["exercise","sets","reps","intensity","rest_between_sets"],
                                "additionalProperties" : False
                            }
                        }
                    },
                    "required" : ["workout_duration_in_minutes","exercises"],
                    "additionalProperties" : False
                }
            }
        }
        )

        text_output = response.output_text
        final_version = json.loads(text_output)

        all_exercises = []
        for exercise in final_version["exercises"]:
            all_exercises.append(exercise["exercise"])
        
        print(f"Workout duration : {final_version['workout_duration_in_minutes']} minutes.")
        print("All Exercises : ")
        print(all_exercises)
    except openai.AuthenticationError:
        print("Invalid API key. Please check credentials")
    except openai.APIConnectionError:
        print("Unable to connect. Check internet Connection")
    except openai.APITimeoutError:
        print("The API request timed out. Please try again")
    except openai.RateLimitError as e:
        print(f"API rate or usage limit reached {e}")
    except openai.APIStatusError as e:
        print(f"OpenAI API erorr. Status code {e.status_code}")
    
    except json.JSONDecodeError:
        print("Unable parse as valid JSON")

muscle_specific_workout("chest")