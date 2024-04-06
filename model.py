from openai import OpenAI


class Model:
	def __init__(self, url="http://10.0.4.174:5555/v1"):
		self.client = OpenAI(base_url=url, api_key="lm-studio")

	def get_completion(self, model, message, temperature=0.7):
		completion = self.client.chat.completions.create(
			model=model,
			messages=[
				{"role": "user", "content": message}
			],
			temperature=temperature,
		)

		return completion.choices[0]
	
	def get_response(self, message):
		model_name = "TheBloke/deepseek-coder-6.7B-instruct-GGUF/deepseek-coder-6.7b-instruct.Q8_0.gguf"
		completion = self.get_completion(model_name, message)
		return completion.message.content


if __name__ == "__main__":
	model = Model()
	response = model.get_response("import numpy as np")
	print(response)