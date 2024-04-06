from git import Repo
import os


class MigrationParser:
    def __init__(self, repo_url, repos_folder, extensions=["py", "c"]):
        self.repo_url = repo_url
        self.local_path = repo_url.split("/")[-1].replace(".git", "")
        os.makedirs(repos_folder, exist_ok=True)
        self.local_path = os.path.join(repos_folder, self.local_path)
        self.extensions = extensions

    def clone_repo(self):
        Repo.clone_from(self.repo_url, self.local_path)

    def get_filenames(self):
        filenames = []
        for root, dirs, files in os.walk(self.local_path):
            for file in files:
                if file.endswith(tuple(self.extensions)):
                    filenames.append(os.path.join(root, file))
        return filenames
    
    def read_code(self, filename):
        with open(filename, 'r') as f:
            return f.read()
    
    def parse(self):
        self.clone_repo()
        filenames = self.get_filenames()
        code = dict()
        for filename in filenames:
            code[filename] = self.read_code(filename)

        return code
