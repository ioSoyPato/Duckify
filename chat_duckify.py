from dotenv import load_dotenv, find_dotenv
from langchain.chat_models import ChatOpenAI
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
import os
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
import gradio as gr


_=load_dotenv(find_dotenv())

text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap=0)


def process_files_in_folder(folder_path):
    if not os.path.isdir(folder_path):
        print("The provided path is not a valid folder.")
        return None

    data = []
    # Iterate through the files in the directory
    for filename in os.listdir(folder_path):
        if filename.startswith('.') or not filename.endswith('.txt'):
            continue  # Skip hidden files and non-txt files

        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            try:
                # Load the file content using the TextLoader
                loader = TextLoader(file_path)
                doc = loader.load()
                splits = text_splitter.split_documents(doc)
                data.append(splits)
            except UnicodeDecodeError:
                print(f"Skipping file due to encoding error: {filename}")
            except Exception as e:
                print(f"Error processing file {filename}: {str(e)}")

    return data

# Specify the path to the folder containing the files
folder_path = "files"

# Call the function to process the files
processed_data = process_files_in_folder(folder_path)

total_splits = []
for document in processed_data:
    for split in document:
        total_splits.append(split)


total_splits = []
for document in processed_data: # Crear un solo documento con todos los splits
    total_splits.extend(document)


vectorstore = Chroma.from_documents(total_splits, embedding=OpenAIEmbeddings())



llm = ChatOpenAI(temperature=0.0)
retriever = vectorstore.as_retriever()
memory = ConversationBufferMemory(
    llm=llm,
    memory_key= "chat_history",
    return_messages=True
)

qa = ConversationalRetrievalChain.from_llm(
    llm,
    retriever = retriever,
    memory = memory
    
)


def chatbot(input_text):
    response = qa(input_text)
    return response["answer"]


with gr.Blocks() as demo:
        gr.Markdown(
    """
    # Empieza a chattear con el gymbot!
    """)

chatbot_interface = gr.Interface(fn=chatbot, 
                                 inputs="textbox", 
                                 outputs="textbox",
                                 description="Music recommendations",
                                 theme="huggingface",
                                 title="Music Chatbot")

chatbot_interface.launch(share=True)



