import re
from parse_repo import MigrationParser
from model import Model


class CodeMigrator:
    def __init__(self, github_url, repos_folder, frameworks=["React", "Vue.js"],
                 model_url="http://10.0.4.174:5555/v1"):
        if len(frameworks) != 2:
            raise ValueError("Please provide exactly two frameworks to migrate between.")

        extensions = self.define_extensions(frameworks)
        self.frameworks = frameworks
        self.parser = MigrationParser(github_url, repos_folder, extensions=extensions)
        self.model = Model(model_url)

    def define_extensions(self, frameworks):
        extensions = []
        if "React" == frameworks[0]:
            extensions.extend(["jsx", "tsx"])
        if "Vue.js" in frameworks[0]:
            extensions.append(".vue")
        if "Angular" in frameworks[0]:
            extensions.append([".ts", ".html", ".css"])
        return extensions

    def extract_code(self, response):
        pattern = r".*```(.*?)```.*"
        match = re.search(pattern, response)
        code_snippet = match.group(1) if match else response
        return code_snippet

    def migrate(self):
        code = self.parser.parse()
        from_framework, to_framework = self.frameworks
        instructions = f"""
        Act as a code translator.
        Rewrite this source code from {from_framework} framework to {to_framework}. """

        for contents in code:
            prompt = instructions + contents
            response = self.model.get_response(prompt)
            print("Response: ", response)
            code_snippet = self.extract_code(response)
            print(code_snippet)