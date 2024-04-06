from git import Repo
import os
from pathlib import Path


class MigrationParser:
    def __init__(self, repo_url, repos_folder, ignore_list=["node_modules"]):
        self.repo_url = repo_url
        self.local_path = repo_url.split("/")[-1].replace(".git", "")
        os.makedirs(repos_folder, exist_ok=True)
        self.local_path = os.path.join(repos_folder, self.local_path)
        self.ignore_list = ignore_list

    def clone_repo(self):
        if os.path.exists(self.local_path):
            print("Repo already exists.")
            return
        Repo.clone_from(self.repo_url, self.local_path)

    def get_filenames(self):
        filenames = []
        for root, dirs, files in os.walk(self.local_path):
            for file in files:
                relative_path = os.path.relpath(os.path.join(root, file), start=self.local_path)
                if not any(ignore in relative_path for ignore in self.ignore_list):
                    relative_path = os.path.join(self.local_path, relative_path)
                    filenames.append(relative_path)
        return filenames
    
    def read_code(self, filename):
        with open(filename, 'r') as f:
            return f.read()
    
    def parse(self):
        self.clone_repo()
        filenames = self.get_filenames()
        code = dict()
        for filename in filenames:
            key_filename = filename.split(self.local_path)[1]
            key_filename = str(Path(key_filename).as_posix())
            try:
                code[key_filename] = self.read_code(filename)
            except UnicodeDecodeError as e:
                code[key_filename] = "Not Code"

        return code
    

if __name__ == "__main__":
    ignore_list = ['node_modules', '.git', 'venv']
    parser = MigrationParser("https://github.com/Mruzik1/Migration-Test.git", "Repos", ignore_list=ignore_list)
    code = parser.parse()
    print(code.keys())