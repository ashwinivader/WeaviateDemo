import os
import pandas
import streamlit as st
import weaviate
from langchain_community.vectorstores import Weaviate
from src.vectorisation import DataIngestion




def store_uploaded_files(uploaded_files, data_folder="data"):
    """
    Stores uploaded files with unique filenames and progress bar.

    Args:
        uploaded_files (list): A list of Streamlit `UploadedFile` objects.
        data_folder (str, optional): The desired folder to store the files in. Defaults to "data".
    """

    # Create the "data" folder if it doesn't exist
    try:
        os.makedirs(data_folder, exist_ok=True)
    except OSError as e:
        st.error(f"Error creating data folder: {e}")
        return

    for uploaded_file in uploaded_files:
        # Extract filename and extension
        filename, extension = os.path.splitext(uploaded_file.name)

        # Ensure unique filename (add numbers if necessary)
        i = 1
        while os.path.exists(os.path.join(data_folder, f"{filename}{extension}")):
            i += 1
            filename = f"{filename}-{i}"

        # Save the file with progress bar
        file_path = os.path.join(data_folder, f"{filename}{extension}")
        total_size = uploaded_file.size
        read_size = 1024  # Chunk size for reading the file
        progress = 0

        with open(file_path, "wb") as f:
            with st.spinner(f"Uploading {filename}{extension}..."):  # Show a spinner
                for data in iter(lambda: uploaded_file.read(read_size), b""):
                    f.write(data)
                    progress += read_size
                    st.progress(round(progress / total_size) * 100)

            st.success(f"File '{filename}{extension}' saved successfully!")

            # Update UI dynamically (refresh file list if applicable)
            if 'uploaded_files' in st.session_state:
                st.session_state.uploaded_files.append(filename)
                st.write(f"Uploaded files: {st.session_state.uploaded_files}")
                st.session_state.uploaded_files = []  # Clear the list after display



# Main app
def main():
    st.title("Talk to your file")
    uploaded_files = st.file_uploader("Choose files to upload", accept_multiple_files=True,)
    if uploaded_files:
        store_uploaded_files(uploaded_files)
        injestData=DataIngestion()
        injestData.load_chunk_pdf()
        


if __name__ == "__main__":
    main()