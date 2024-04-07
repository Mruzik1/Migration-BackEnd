from flask import Flask, request, jsonify
from code_migrator2 import CodeMigrator

app = Flask(__name__)


@app.route('/code_migrator', methods=['POST'])
def code_migrator():
    repo_url = request.get_json()['repo_url']
    frameworks = [request.get_json()['from_lang'], request.get_json()['to_lang']]
    task_type = request.get_json()['task_type']
    migrator = CodeMigrator(repo_url, frameworks)

    if task_type == "describe_files":
        # code_description = migrator.describe_files()
        code_description = migrator.load_code_json(filename="migrated_code3.json")
        return jsonify(code_description)
    elif task_type == "generate_structure":
        # new_structure = migrator.generate_structure(files_structure_path="migrated_code3.json")
        new_structure = migrator.load_code_json(filename="new_structure.json")
        return jsonify(new_structure)
    elif task_type == "generate_code":
        # generated_code = migrator.generate_code(files_structure_path="migrated_code3.json")
        generated_code = migrator.load_code_json(filename="generated_code.json")
        return jsonify(generated_code)


if __name__ == '__main__':
    app.run(host='10.0.5.217', port=7676, debug=True)
