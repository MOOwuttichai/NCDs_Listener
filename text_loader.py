from langchain_community.document_loaders import TextLoader
raw_documents = TextLoader('Google_ge.txt', encoding="utf8")
loader = raw_documents.load()
loader