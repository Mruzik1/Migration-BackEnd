from openai import OpenAI


class Model:
	def __init__(self, url="http://localhost:5555/v1"):
		self.url = url

	def get_completion(self, model, msg, sys_msg, temperature=0.3):
		client = OpenAI(base_url="http://localhost:5555/v1", api_key="lm-studio")
		completion = client.chat.completions.create(
			model=model,
			messages=[
				{"role": "system", "content": sys_msg},
    			{"role": "user", "content": msg}
			],
			temperature=temperature,
		)

		return completion.choices[0]
	
	def get_response(self, msg, sys_msg):
		# model_name = "second-state/StarCoder2-7B-GGUF/starcoder2-7b-Q8_0.gguf"
		# model_name = "TheBloke/deepseek-llm-7B-chat-GGUF/deepseek-llm-7b-chat.Q8_0.gguf"
		model_name = "TheBloke/deepseek-coder-6.7B-instruct-GGUF"
		completion = self.get_completion(model_name, msg, sys_msg)
		return completion.message.content


if __name__ == "__main__":
	model = Model()
	response = model.get_response("import numpy as np")
	print(response)