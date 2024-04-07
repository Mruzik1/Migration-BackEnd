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

    def extract_code(self, response):
        pattern = r".*```(.*?)```.*"
        match = re.search(pattern, response)
        code_snippet = match.group(1) if match else response
        return code_snippet

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
    
    def describe_structure(self, files_structure_path="migrated_code.json"):
        print("Describing the file structure...")
        files_structure = self.load_code_json(files_structure_path)
        sys_message= \
        f"You will get JSON object containing files structure for {self.frameworks[0]} app. " \
        f"Generate new files structure for {self.frameworks[1]} app using provided files structure and files descriptions. " \
        "Generate files structure strictly in the same format as the provided example: ```json\n\[{\"description\": brief description of the file contents, \"filename\": path to file\}, ...]\n``` "
        message = f"```json\n{files_structure}\n```"
        response = self.model.get_response(message, sys_message)
        return response


if __name__ == "__main__":
    repo_url = "https://github.com/Mruzik1/Migration-Test.git"
    migrator = CodeMigrator(repo_url)

    code_description = migrator.describe_files()
    # print(migrator.describe_structure())