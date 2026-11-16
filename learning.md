# Learning

# Normally client responses are read as <response.output_text> but we want it as a JSON structure so we can access individual information and use it for database records or REACT components.
- We need to define the JSON Schema we want, e.g. :
  - Define the fields, data types

I have made the same prompt of "Create me a muscle building workout excerise for a beginner"
The non schema has output a lot of text and pretty much made me a weekly 3 days plan.
Whereas the Schema response only replied with the fields I asked for.

# Why did the first response generate an entire workout plan?

e.g. No Schema
<default_response = client.responses.create(
    model="gpt-5.5",
    input="Create me a muscle building workout exercise for a beginner"
)>
- This is a natural language instruction, no predefined structure, no specified number of fields and no restrictions oh how to organse its answer. The model on its own decides that the best answer would be a Weekly training plan, advice and the different exercises. (It had more freedome over the response format and content).
  
e.g. With Schema
Schema : Standard for describing the structure and rules of JSON data.
<response = client.responses.create(
    model="gpt-5.5",
    input="Create me a muscle building workout excerise for a beginner",
    ########  text is the configurations of how the general response should be formatted
    text = {
        ######## Desired model's response
        "format" : {
            ######## the reason its json_schema and not regular json is because JSON schema allows us to define rules of which fields must exist, data types, overall structure the response must follow
            "type" : "json_schema",
            ######## Name is not for this response API but its the identifier for this JSON Schema Format. Names are used to distinguish between different schemas.
            "name" : "workout_exercise",
            ######## Indicates to JSON to enforce the contraints e.g. sets shoud be 3 not three.
            "strict" : True,
            ######## Actual JSON structure definition
            "schema" : {
                ########  Object allows us to do response["exercise"] once we have converted the response into JSON
                "type" : "object",
                "properties" : {
                    ######## Definition describing its expected data type.
                    "exercise" : {"type" : "string"},
                    "sets" : {"type" : "integer"},
                    "reps" : {"type" : "integer"},
                    "rest_seconds" : {"type":"integer"}
                },
                ########  Indicates which properties must be present in the response, if there is a property that is not mentioned, the property being filled is optional and not a priority.
                "required" : ["exercise","sets","reps","rest_seconds"],
                ######## Additional properties is if the model decides to give a property because it thinks its useful e.g. difficulty. If we set it to False then we don't expect another property from the API so just the described properties are included.
                "additionalProperties" : False
            }
        }
    }
)>

With the text : { "strict" : True } we instruct that whatever it generates it need to fit this predefined structure.
"properties": {
    "exercise": {"type": "string"},
    "sets": {"type": "integer"},
    "reps": {"type": "integer"},
    "rest_seconds": {"type": "integer"}
}
Output : {'exercise': 'Goblet Squat', 'sets': 3, 'reps': 10, 'rest_seconds': 90}
And it can we accessed as an object because of the type : "object" <print("Specific workout " + workout["exercise"])>