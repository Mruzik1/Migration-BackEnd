# Example: reuse your existing OpenAI setup
from openai import OpenAI
import re
from parse_repo import MigrationParser

repo_url = "https://github.com/Mruzik1/Migration-Test.git"
repos_folder = "Repos"
parser = MigrationParser(repo_url, repos_folder)
code = parser.parse()

print('Executing...')

# Point to the local server
client = OpenAI(base_url="http://localhost:5555/v1", api_key="lm-studio")

frameworks = ['React', 'Vue.js', 'Angular']

from_framework = frameworks[1]
to_framework = frameworks[0]

instructions = f"""
Act as a code translator.
Rewrite this source code from {from_framework} framework to {to_framework}.
YOUR ANSWER MUST CONTAINT ONLY CODE, NO FUNTHER EXPLALNATIONS. 
IMAGINE THIS AS I HAVE OPENED A FILE WITH CODE.
NO TEXT CAN BE WRITTEN AFTER THE CODE. DO NOT MARK THE END OF CODE IN ANY COMMMENTS.
KEEP IN MIND THAT THIS EXACT TEXT WILL BE EXECUTED AS SOURCE CODE.
"""

# Iterate through the dictionary of files
for contents in code:
  prompt = instructions + contents

  completion = client.chat.completions.create(
    model="TheBloke/deepseek-coder-6.7B-instruct-GGUF/deepseek-coder-6.7b-instruct.Q8_0.gguf",
    messages=[
      {"role": "user", "content": prompt }
    ],
    temperature=0.1,
  )

  response = completion.choices[0].message.content

  # Use regular expression to extract the code snippet
  pattern = r".*```(.*?)```.*"
  match = re.search(pattern, response)

  if match:
      code_snippet = match.group(1)  # Get the captured group inside the parentheses
  else:
      code_snippet = response
  print(code_snippet)