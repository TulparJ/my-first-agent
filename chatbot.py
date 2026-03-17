import anthropic
import requests
import urllib.parse
import os
import subprocess

client = anthropic.Anthropic()

# 1. Define all tools
tools = [
    {
        "name": "calculator",
        "description": "Use this to perform math calculations",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The math expression to calculate, e.g. '2 + 2' or '10 * 5'"
                }
            },
            "required": ["expression"]
        }
    },
    {
        "name": "get_weather",
        "description": "Get the current weather for a city",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The name of the city, e.g. 'London' or 'New York'"
                }
            },
            "required": ["city"]
        }
    },
    {
        "name": "generate_image",
        "description": "Generate an image from a text description",
        "input_schema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "A detailed description of the image to generate"
                },
                "filename": {
                    "type": "string",
                    "description": "A short filename for the image, e.g. 'sunset' or 'robot'"
                }
            },
            "required": ["prompt", "filename"]
        }
    },
    {
        "name": "write_file",
        "description": "Write code or text to a file on the computer",
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "The filename to write to, e.g. 'hello.py' or 'index.html'"
                },
                "content": {
                    "type": "string",
                    "description": "The content to write to the file"
                }
            },
            "required": ["filename", "content"]
        }
    },
    {
        "name": "run_code",
        "description": "Run a Python file and return the output",
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "The Python filename to run, e.g. 'hello.py'"
                }
            },
            "required": ["filename"]
        }
    }
]

# 2. Calculator tool
def run_calculator(expression):
    try:
        result = eval(expression)
        return str(result)
    except:
        return "Error: invalid expression"

# 3. Weather tool
def get_weather(city):
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_response = requests.get(geo_url).json()

        if not geo_response.get("results"):
            return f"Could not find city: {city}"

        lat = geo_response["results"][0]["latitude"]
        lon = geo_response["results"][0]["longitude"]
        name = geo_response["results"][0]["name"]

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m,weathercode&temperature_unit=fahrenheit"
        weather_response = requests.get(weather_url).json()

        temp = weather_response["current"]["temperature_2m"]
        wind = weather_response["current"]["wind_speed_10m"]

        return f"Weather in {name}: {temp}°F, wind speed {wind} km/h"
    except Exception as e:
        return f"Error fetching weather: {str(e)}"

# 4. Image generation tool
def generate_image(prompt, filename):
    try:
        hf_key = os.environ.get("HF_API_KEY")
        if not hf_key:
            return "Error: HF_API_KEY not set"

        api_url = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
        headers = {"Authorization": f"Bearer {hf_key}"}
        payload = {"inputs": prompt}

        print(f"  [Generating image, please wait ~20 seconds...]")
        response = requests.post(api_url, headers=headers, json=payload, timeout=60)

        if response.status_code == 200:
            safe_filename = "".join(c for c in filename if c.isalnum() or c in "._- ")
            filepath = f"{safe_filename}.png"
            with open(filepath, "wb") as f:
                f.write(response.content)
            full_path = os.path.abspath(filepath)
            return f"Image saved as {filepath} at {full_path}"
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error generating image: {str(e)}"

# 5. Write file tool
def write_file(filename, content):
    try:
        with open(filename, "w") as f:
            f.write(content)
        return f"File '{filename}' written successfully!"
    except Exception as e:
        return f"Error writing file: {str(e)}"

# 6. Run code tool
def run_code(filename):
    try:
        result = subprocess.run(
            ["python3", filename],
            capture_output=True,
            text=True,
            timeout=10
        )
        output = result.stdout or result.stderr
        return output if output else "Code ran successfully with no output"
    except Exception as e:
        return f"Error running code: {str(e)}"

# 7. Conversation history
conversation_history = []

print("AI Agent ready! Type 'quit' to exit.\n")
print("Tools available: calculator | weather | image generation | write file | run code\n")

while True:
    user_input = input("You: ").strip()
    if not user_input:
        continue
    if user_input.lower() == "quit":
        break

    conversation_history.append({"role": "user", "content": user_input})

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        tools=tools,
        messages=conversation_history
    )

    # 8. Handle tool use
    if response.stop_reason == "tool_use":
        conversation_history.append({"role": "assistant", "content": response.content})

        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                if block.name == "calculator":
                    result = run_calculator(block.input["expression"])
                    print(f"  [Calculator used: {block.input['expression']} = {result}]")
                elif block.name == "get_weather":
                    result = get_weather(block.input["city"])
                    print(f"  [Weather fetched for {block.input['city']}]")
                elif block.name == "generate_image":
                    result = generate_image(block.input["prompt"], block.input["filename"])
                    print(f"  [Image generation complete!]")
                elif block.name == "write_file":
                    result = write_file(block.input["filename"], block.input["content"])
                    print(f"  [File written: {block.input['filename']}]")
                elif block.name == "run_code":
                    result = run_code(block.input["filename"])
                    print(f"  [Code executed: {block.input['filename']}]")

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result
                })

        conversation_history.append({"role": "user", "content": tool_results})

        # Keep looping until Claude returns a text response
        while True:
            follow_up = client.messages.create(
                model="claude-opus-4-5",
                max_tokens=1024,
                tools=tools,
                messages=conversation_history
            )

            if follow_up.stop_reason == "tool_use":
                conversation_history.append({"role": "assistant", "content": follow_up.content})
                next_results = []
                for block in follow_up.content:
                    if block.type == "tool_use":
                        if block.name == "calculator":
                            result = run_calculator(block.input["expression"])
                            print(f"  [Calculator used: {block.input['expression']} = {result}]")
                        elif block.name == "get_weather":
                            result = get_weather(block.input["city"])
                            print(f"  [Weather fetched for {block.input['city']}]")
                        elif block.name == "generate_image":
                            result = generate_image(block.input["prompt"], block.input["filename"])
                            print(f"  [Image generation complete!]")
                        elif block.name == "write_file":
                            result = write_file(block.input["filename"], block.input["content"])
                            print(f"  [File written: {block.input['filename']}]")
                        elif block.name == "run_code":
                            result = run_code(block.input["filename"])
                            print(f"  [Code executed: {block.input['filename']}]")
                        next_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result
                        })
                conversation_history.append({"role": "user", "content": next_results})
            else:
                reply = follow_up.content[0].text
                conversation_history.append({"role": "assistant", "content": reply})
                print(f"Claude: {reply}\n")
                break