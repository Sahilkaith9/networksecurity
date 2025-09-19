from setuptools import setup,find_packages

def get_installs(file_path):
    
    with open(file_path,'r') as file:
        requirenments=file.readlines()
        requirenments=[req.replace("\n"," ") for req in requirenments]
        
        if "-e ." in requirenments:
            requirenments.remove('-e .')
    return requirenments




setup(
    name="networksecurity",
    version="0.0.1",
    author="Sahil kaith",
    author_email="sahilkaith095@gmail.com",
    packages=find_packages(),
    install_requires=get_installs('requirenments.txt')
)
