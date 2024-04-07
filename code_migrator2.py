import re
from parse_repo import MigrationParser
from model import Model
from tqdm import tqdm
import json
import os


class CodeMigrator:
    def __init__(self, github_url, frameworks=["Vue.js", "React"],
                 model_url="http://10.0.4.174:5555/v1", repos_folder="Repos"):
        if len(frameworks) != 2:
            raise ValueError("Please provide exactly two frameworks to migrate between.")

        ignore_list = self.define_ignored(frameworks)
        self.frameworks = frameworks
        self.parser = MigrationParser(github_url, repos_folder, ignore_list=ignore_list)
        self.model = Model(model_url)

        print("Parsing the repository...")
        self.application = self.parser.parse()

    def define_ignored(self, frameworks):
        ignore_list = ['node_modules', '.git', 'venv', ".json", ".md", ".config", ".ico"]
        if "react" == frameworks[0].lower():
            pass
        if "vue.js" == frameworks[0].lower():
            pass
        if "angular" == frameworks[0].lower():
            pass
        return ignore_list

    def extract_json_text(self, input_string):
        pattern = r"```json\n(.*?)\n```"
        matches = re.findall(pattern, input_string, re.DOTALL)
        return matches

    def save_code_json(self, code_description, filename="migrated_code.json"):
        with open(filename, "w") as f:
            json.dump(code_description, f)

    def load_code_json(self, filename="migrated_code.json"):
        if not os.path.exists(filename):
            return []
        with open(filename, "r") as f:
            code_description = json.load(f)
        return code_description
        
    def check_code_json(self, code_filename, filename="migrated_code.json"):
        with open(filename, "r") as f:
            code_description = json.load(f)
        return any(code_filename in code["filename"] for code in code_description)

    def describe_files(self):
        def get_instructions(f, code):
            instructions = f"""Describe code in file {f}: {code}."""
            return instructions

        print("Describing the application...")
        sys_message = "Write a brief description of the code in the provided file (3-5 sentences). " \
                      "The description must describe what code DOES, not the code itself."
        pbar = tqdm(self.application, total=len(self.application))
        code_descriptions = []
        for filename in pbar:
            if os.path.exists("migrated_code.json") and self.check_code_json(filename):
                continue
            pbar.set_description(f"Processing {filename}")
            message = get_instructions(filename, self.application[filename])
            response = self.model.get_response(message, sys_message)
            code_snippet = self.extract_code(response)
            code_descriptions.append({
                "description": code_snippet,
                "filename": filename
            })
            self.save_code_json(code_descriptions)
        return code_descriptions
    
    def generate_structure(self, files_structure_path="migrated_code.json"):
        print("Describing the file structure...")
        files_structure = self.load_code_json(files_structure_path)
        sys_message = \
        f"You will get JSON object containing files structure for {self.frameworks[0]} app. Your output will be another JSON object. " \
        f"Generate new files structure for {self.frameworks[1]} app using provided files structure and files descriptions. " \
        "Generate files structure strictly in the same format as the provided example: ```json\n\[{\"description\": brief description of the file contents, \"filename\": path to file\}, ...]\n``` "
        message = f"```json\n{files_structure}\n```"
        response = self.model.get_response(message, sys_message)
        with open("new_structure.txt", "w") as f:
            f.write(response)
        return self.extract_json_text(response)

    def generate_code(self, files_structure_path="migrated_code.json"):
        print("Generating code based on code description")
        code_description = self.load_code_json(files_structure_path)
        sys_message = \
        "You will get JSON object containing file desciption. Your output will be another JSON object. " \
        "Generate code based on provided file descriptions as follows (STRICTLY): ```json\n\[{\"code\": generated code based on description, \"filename\": path to file\}]\n``` "
        message = f"```json\n{code_description}\n```"
        pbar = tqdm(enumerate(code_description), total=len(code_description))
        codes = []
        for i, desc_file in pbar:
            filename, description = desc_file["filename"], desc_file["description"]
            pbar.set_description(f"Processing {filename}")
            json_object = {"description": description, "filename": filename}
            message = f"```json\n{json_object}\n```"
            response = self.model.get_response(message, sys_message)
            with open(f"code{i}.txt", "w") as f:
                f.write(response)
            codes.append(self.extract_json_text(response))
        return codes
        

if __name__ == "__main__":
    repo_url = "https://github.com/Mruzik1/Migration-Test.git"
    migrator = CodeMigrator(repo_url)

    # code_description = migrator.describe_files()
    # new_structure = migrator.generate_structure(files_structure_path="migrated_code3.json")
    # migrator.save_code_json(new_structure, filename="new_structure.json")
    converted_code = migrator.generate_code(files_structure_path="migrated_code3.json")
    migrator.save_code_json(converted_code, filename="generated_code.json")
    