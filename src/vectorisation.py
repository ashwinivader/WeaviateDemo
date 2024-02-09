import  src.utils as utils
import os
import sys
import langchain
import langchain_community
from dataclasses import dataclass
from src.logger import logging
from src.exception import CustomException
#from langchain.document_loaders import PyPDFDirectoryLoader
from langchain_community.document_loaders import PyPDFDirectoryLoader
#rom langchain_community.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter



@dataclass
class EnvParams :

      utils.loadEnv()
      openai_key=os.getenv("OPENAI_KEY")
      weaviate_key=os.getenv("weaviate_key")
      weaviate_cluster=os.getenv("weaviate_cluster")
      weaviate_url=os.getenv("weaviate_url")
      weaviate_key1=os.getenv("weaviate_key1")
      weaviate_cluster1=os.getenv("weaviate_cluster1")
      weaviate_url1=os.getenv("weaviate_url1")


class DataIngestion:
    def __init__(self):
      self.ingestion_config=utils.loadEnv() 

    def chunk_data(self,docs,chunk_size=500,chunk_overlap=50):
        logging.info("Entered the data chunk method or component")
        text_splitter=RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=50)
        doc=text_splitter.split_documents(docs)
        logging.info("Numer of chunks")
        logging.info(len(doc))
        return doc


    def load_chunk_pdf(self):
      logging.info("Entered the data ingestion method or component")
      #try:
      dir_loader=PyPDFDirectoryLoader("data/")
      documents=dir_loader.load()
      logging.info("Numer of documents")
      logging.info(len(documents))
      self.chunk_data(docs=documents)
      return(documents)
      
      #except Exception as e:
      #      raise CustomException(e,sys)
      



