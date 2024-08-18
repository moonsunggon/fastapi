import os
import subprocess

'''
초기 폴더 생성 스크립트
'''
def create_directory(path):
    os.makedirs(path, exist_ok=True)

def create_file(path, content=''):
    with open(path, 'w') as f:
        f.write(content)

def create_project_structure(base_dir):
    # Create main project directory
    create_directory(base_dir)

    # Create app directory and its subdirectories
    app_dir = os.path.join(base_dir, 'app')
    create_directory(app_dir)
    create_file(os.path.join(app_dir, '__init__.py'))
    create_file(os.path.join(app_dir, 'main.py'), 'from fastapi import FastAPI\n\napp = FastAPI()\n')

    # Create API directory and its subdirectories
    api_dir = os.path.join(app_dir, 'api')
    create_directory(api_dir)
    create_file(os.path.join(api_dir, '__init__.py'))
    create_directory(os.path.join(api_dir, 'endpoints'))
    create_file(os.path.join(api_dir, 'endpoints', '__init__.py'))
    create_file(os.path.join(api_dir, 'endpoints', 'items.py'))
    create_file(os.path.join(api_dir, 'endpoints', 'users.py'))
    create_file(os.path.join(api_dir, 'dependencies.py'))

    # Create core directory
    core_dir = os.path.join(app_dir, 'core')
    create_directory(core_dir)
    create_file(os.path.join(core_dir, '__init__.py'))
    create_file(os.path.join(core_dir, 'config.py'))
    create_file(os.path.join(core_dir, 'security.py'))

    # Create db directory
    db_dir = os.path.join(app_dir, 'db')
    create_directory(db_dir)
    create_file(os.path.join(db_dir, '__init__.py'))
    create_file(os.path.join(db_dir, 'base.py'))
    create_file(os.path.join(db_dir, 'session.py'))

    # Create models directory
    models_dir = os.path.join(app_dir, 'models')
    create_directory(models_dir)
    create_file(os.path.join(models_dir, '__init__.py'))
    create_file(os.path.join(models_dir, 'item.py'))
    create_file(os.path.join(models_dir, 'user.py'))

    # Create schemas directory
    schemas_dir = os.path.join(app_dir, 'schemas')
    create_directory(schemas_dir)
    create_file(os.path.join(schemas_dir, '__init__.py'))
    create_file(os.path.join(schemas_dir, 'item.py'))
    create_file(os.path.join(schemas_dir, 'user.py'))

    # Create tests directory
    tests_dir = os.path.join(base_dir, 'tests')
    create_directory(tests_dir)
    create_file(os.path.join(tests_dir, '__init__.py'))
    create_directory(os.path.join(tests_dir, 'test_api'))
    create_file(os.path.join(tests_dir, 'test_api', '__init__.py'))
    create_file(os.path.join(tests_dir, 'test_api', 'test_items.py'))
    create_file(os.path.join(tests_dir, 'test_api', 'test_users.py'))
    create_file(os.path.join(tests_dir, 'conftest.py'))

    # Create alembic directory
    alembic_dir = os.path.join(base_dir, 'alembic')
    create_directory(alembic_dir)
    create_directory(os.path.join(alembic_dir, 'versions'))
    create_file(os.path.join(alembic_dir, 'env.py'))
    create_file(os.path.join(alembic_dir, 'script.py.mako'))

    # Create root level files
    create_file(os.path.join(base_dir, '.env'))
    create_file(os.path.join(base_dir, '.gitignore'), '*.pyc\n__pycache__\n.env\n')
    create_file(os.path.join(base_dir, 'requirements.txt'), 'fastapi\nuvicorn\nsqlalchemy\nalembic\npydantic\n')
    create_file(os.path.join(base_dir, 'README.md'), '# FastAPI Project\n\nThis is a FastAPI project template.\n')

    print(f"Project structure created in {base_dir}")

'''
초기 폴더 생성 스크립트로 필요시에만 주석 풀어서 사용.
'''
if __name__ == "__main__":
    # project_name = input("Enter your project name: ")
    # base_dir = os.path.join(os.getcwd(), project_name)
    # create_project_structure(base_dir)

    # # Initialize git repository
    # try:
    #     subprocess.run(['git', 'init', base_dir], check=True)
    #     print("Git repository initialized.")
    # except subprocess.CalledProcessError:
    #     print("Failed to initialize git repository. Make sure git is installed.")
    # except FileNotFoundError:
    #     print("Git is not installed or not in the system PATH.")