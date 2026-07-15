from groq import Groq

client = Groq(api_key="")

name = "Aarti"
score = 90
subject_name = "Python"

#step 1:create a prompt for the AI model
prompt =f"""
name: {name}
score: {score}/100
subject_name: {subject_name}
please provide practical study tips,it should not be more than 3 lines.
"""
#step 2: call the AI model to get the response
response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "user", 
         "content": prompt} ]
)

#step 3: print the response
tip = response.choices[0].message.content
print(tip)

