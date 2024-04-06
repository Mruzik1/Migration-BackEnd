import re
from parse_repo import MigrationParser
from model import Model
from tqdm import tqdm


class CodeMigrator:
    def __init__(self, github_url, frameworks=["Vue.js", "React"],
                 model_url="http://10.0.4.174:5555/v1", repos_folder="Repos"):
        if len(frameworks) != 2:
            raise ValueError("Please provide exactly two frameworks to migrate between.")

        extensions = self.define_extensions(frameworks)
        self.frameworks = frameworks
        self.parser = MigrationParser(github_url, repos_folder, extensions=extensions)
        self.model = Model(model_url)

    def define_extensions(self, frameworks):
        extensions = []
        if "react" == frameworks[0].lower():
            extensions.extend(["jsx", "tsx"])
        if "vue.js" == frameworks[0].lower():
            extensions.append(".vue")
        if "angular" == frameworks[0].lower():
            extensions.append([".ts", ".html", ".css"])
        return extensions

    def extract_code(self, response):
        pattern = r".*```(.*?)```.*"
        match = re.search(pattern, response)
        code_snippet = match.group(1) if match else response
        return code_snippet

    def migrate(self):
        print("Parsing the repository...")
        code = self.parser.parse()
        from_framework, to_framework = self.frameworks
        instructions = f"""
        Act as a code translator.
        Rewrite this source code from {from_framework} framework to {to_framework}:
        """

        print("Migrating the code...")
        pbar = tqdm(code, total=len(code))
        code_snippets = []
        for filename in pbar:
            pbar.set_description(f"Processing {filename}")
            prompt = instructions + code[filename]
            response = self.model.get_response(prompt)
            code_snippet = self.extract_code(response)
            code_snippets.append({
                "lang": filename.split(".")[-1],
                "value": code_snippet,
                "filename": filename
            })
        return code_snippets


if __name__ == "__main__":
    repo_url = "https://github.com/Mruzik1/Migration-Test.git"
    migrator = CodeMigrator(repo_url)

    codes = migrator.migrate()
    print(codes)