import os
import sys
import re
import openai
import subprocess

filename = sys.argv[1]
proc = subprocess.Popen(["python3", filename], stderr=subprocess.PIPE)
proc.wait()

error = proc.stderr.read().decode()
if not error:
    sys.exit(0)

print(error)

with open(filename, 'r') as file:
    code = file.read()

openai.api_key = os.getenv('OPENAI_API_KEY')

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "あなたはプログラミングのコーチです。コードとエラーメッセージが2回に分けて入力されるので、エラーの原因と解決方法をわかりやすく説明してください。"},
        {"role": "user", "content": code},
        {"role": "user", "content": error}
    ],
    top_p=0
)

for choice in response.choices:
    print(choice.message.content)
