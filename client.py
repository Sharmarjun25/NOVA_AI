from openai import OpenAI
client = OpenAI()

api_key= "YOUR API KEY"

completion = client.chat.completions.create(
    model= "gpt -3.5-turbo",
    messages=[
        {"role":"system" , "content":"You are a virtual assistant named Nova skilled in general tasks like Alexa and google Cloud "},
        {"role": "user","content":"What is coding "}
    ]
)
print(completion.choices[0].message)



#print(response.output_text);
#  THIS WAS INITIALLY ADDED BUT ACCORDING TO OPENAI API COSTS IT WAS NOT CONSIDERED
