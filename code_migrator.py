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
        
    def check_code_json(self, code_filename, filename="migrated_code.json"):
        with open(filename, "r") as f:
            code_description = json.load(f)
        return any(code_filename in code["filename"] for code in code_description)

    def describe_files(self):
        def get_instructions(f, code):
            instructions = f"""
            Describe code in a file {f} very briefly - 2-3 sentences: {code}.
            """
            return instructions

        print("Describing the application...")
        pbar = tqdm(self.application, total=len(self.application))
        code_descriptions = []
        for filename in pbar:
            if os.path.exists("migrated_code.json") and self.check_code_json(filename):
                continue
            pbar.set_description(f"Processing {filename}")
            prompt = get_instructions(filename, self.application[filename])
            response = self.model.get_response(prompt)
            code_snippet = self.extract_code(response)
            code_descriptions.append({
                "value": code_snippet,
                "filename": filename
            })
            self.save_code_json(code_descriptions)
        return code_descriptions


if __name__ == "__main__":
    repo_url = "https://github.com/Mruzik1/Migration-Test.git"
    migrator = CodeMigrator(repo_url)

    codes = migrator.describe_files()
    print(codes)