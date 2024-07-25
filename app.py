from flask import Flask, request, render_template  
import requests  # 导入requests库以便进行API调用  

app = Flask(__name__)  

# 示例天气API  
WEATHER_API = "https://api.openweathermap.org/data/2.5/weather"  
API_KEY = "4ac39d7c8e27018192a86ec1fbae5804"  # **使用的API密钥**  

# 示例AI文本生成API（请替换为您的AI接口）  
AI_API_ENDPOINT = "https://api.openai.com/v1/engines/davinci/completions"  # **AI API接口**  
AI_API_KEY = "AIzaSyA644cQ_NoWSYnyIQ-4CjkFU_o-zHXNg_o"  # **AI API密钥**  

def get_ai_explanation(weather_description):  
    headers = {  
        'Authorization': f'Bearer {AI_API_KEY}',  
        'Content-Type': 'application/json'  
    }  

    # AI请求生成的文本  
    data = {  
        "prompt": f"请给出关于天气描述 '{weather_description}' 的解释。",  
        "max_tokens": 50  
    }  
    
    response = requests.post(AI_API_ENDPOINT, headers=headers, json=data)  
    ai_response = response.json()  

    # 检查生成的文本  
    explanation = ai_response['choices'][0]['text'].strip() if 'choices' in ai_response else "无解释可用"  
    return explanation  

@app.route('/')  
def home():  
    return render_template('index.html')  

@app.route('/get_weather', methods=['POST'])  
def get_weather():  
    city = request.form['city']  
    # **调用天气API**  
    response = requests.get(f"{WEATHER_API}?q={city}&appid={API_KEY}")  
    weather_data = response.json()  
    
    # 处理API返回的数据  
    if weather_data.get("main"):  
        temperature = weather_data["main"]["temp"]  
        description = weather_data["weather"][0]["description"]  
        
        # 使用AI解释天气描述  
        ai_explanation = get_ai_explanation(description)  
        return render_template('weather.html', temperature=temperature, description=description, ai_explanation=ai_explanation)  
    else:  
        return render_template('weather.html', error="City not found.")  

if __name__ == '__main__':  
    app.run(debug=True)
