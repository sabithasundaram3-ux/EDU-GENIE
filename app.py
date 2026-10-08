from flask import Flask, render_template, request
from google import genai

app = Flask(__name__)

client = genai.Client(api_key="AQ.Ab8RN6LaqTTYfHTF2GVcK_KlWTCwT61NwcwRmz_X3HPAj88n6g") 


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    user_query = request.form.get('user_query')

    try:
        system_instruction = (
            "You are an AI tutor. If the user asks for a quiz, return the output "
            "formatted as clean HTML with interactive elements. Provide question "
            "options using HTML buttons or radio inputs. Include inline onclick "
            "JavaScript functions that check if the selected option is correct, "
            "changing its color to green for correct and red for incorrect, "
            "and showing an instant explanation."
        )

        full_prompt = f"{system_instruction}\n\nUser request: {user_query}"

        response = client.models.generate_content(
            model="gemini-3.5-flash", 
            contents=full_prompt
        )

        result_text = response.text

    except Exception as e:
        result_text = f"An error occurred: {str(e)}"

    return render_template(
        'index.html',
        result=result_text,
        query=user_query
    )


if __name__ == '__main__':
    app.run(debug=True)