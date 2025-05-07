import os


def detect_language(repo_path):
    """
    Detect the primary programming language of a repository based on file extensions.

    :param repo_path: Path to the cloned repository.
    :type repo_path: str
    :return: The detected programming language.
    :rtype: str
    """
    language_count = {}

    for root, _, files in os.walk(repo_path):
        for file in files:
            _, ext = os.path.splitext(file)
            if ext:
                language = get_language_from_extension(ext)
                if language:
                    language_count[language] = language_count.get(language, 0) + 1

    if language_count:
        return max(language_count, key=language_count.get)
    
    return "Unknown"


def get_language_from_extension(extension):
    """
    Map file extensions to programming languages.

    :param extension: File extension (e.g., '.py').
    :type extension: str
    :return: The corresponding programming language.
    :rtype: str
    """
    extension_to_language = {
        ".py": "Python",
        ".js": "JavaScript",
        ".java": "Java",
        ".cpp": "C++",
        ".c": "C",
        ".rb": "Ruby",
        ".go": "Go",
        ".php": "PHP",
        ".html": "HTML",
        ".css": "CSS",
    }

    return extension_to_language.get(extension)
