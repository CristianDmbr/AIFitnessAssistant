import os
import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key = os.getenv("OPEN_API_KEY")
)

schema_response = client.responses.create(
    model = "gpt-5.5",
    input = "Make me a 5 workout chest plan for today",
    text = {
        "format" : {
            "type" : "json_schema",
            "name" : "chest_workout",
            "strict" : True,
            "schema" : {
                "type" : "object",
                "properties" : {
                    "total_workout_duration" : {"type" : "integer"},
                    "exercises" : {
                        "type" : "array",
                        "items" : {
                            "type" : "object",
                            "properties" : {
                                "exercise" : {"type" : "string"},
                                "sets" : {"type" : "integer"},
                                "reps" : {"type" : "integer"},
                                "rest_time" : {"type" : "integer"},
                                "intensity" : {"type":"string"}
                            },
                            "required" : ["exercise","sets","reps","rest_time","intensity"],
                            "additionalProperties" : False,
                        }
                    }
                },
                "required" : ["exercises","total_workout_duration"],
                "additionalProperties" : False
            }
        }
    } 
)

response = schema_response.output_text
final = json.loads(response)
for exercise in final["exercises"]:
    print(f"Exercise  {exercise['exercise']}")
    print(f"Sets : {exercise['sets']}")
    print(f"Reps {exercise['reps']} ")
    print("-----------------")

print("Total exercises " + str(len(final["exercises"])))
print(f"First exercise {final['exercises'][0]['exercise']}")
print(f"Rest time of third exercise : {final['exercises'][2]['rest_time']}")
print(f"Last exercise name {final['exercises'][-1]['exercise']}")

all_exercises = []
for exercise in final["exercises"]:
    all_exercises.append(exercise["exercise"])
print("All Exercieses")
print(all_exercises)