import os


def ensure_data_folders():
    """
    Ensures that the necessary 'data' folder and its subfolders exist.
    """
    data_path = 'data'
    subfolders = [
        'base_rag_module/output',
        'base_rag_module/persist',
        'base_rag_module/source_data',
        'cv_module/output',
        'cv_module/persist',
        'cv_module/source_data',
    ]

    # Create the main 'data' directory if it doesn't exist
    os.makedirs(data_path, exist_ok=True)

    # Create each subfolder under 'data'
    for subfolder in subfolders:
        folder_path = os.path.join(data_path, subfolder)
        os.makedirs(folder_path, exist_ok=True)