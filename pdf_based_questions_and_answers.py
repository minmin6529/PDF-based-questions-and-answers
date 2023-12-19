# -*- coding: utf-8 -*-
"""PDF-based-questions-and-answers.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IJe-hhAJtCuCpF3WGRdOG-Qa0Umr9CQ_
"""

# 필요한 라이브러리 설치
!pip install -q openai langchain langchainhub pypdf

import os

# 허깅페이스 LLM Read Key
os.environ['HUGGINGFACEHUB_API_TOKEN'] = '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'

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough

# PDF 파일 로드
loader = PyPDFLoader("data/황순원-소나기.pdf")
document = loader.load()
document[0].page_content[:200] # 내용 추출

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
texts = text_splitter.split_documents(document)

!pip install sentence-transformers
!pip install chromadb

huggingface_model_repo = 'beomi/llama-2-ko-7b'

# 임베딩
embeddings = HuggingFaceEmbeddings()
# Chroma DB 에 저장
docsearch = Chroma.from_documents(texts, embeddings)
# retriever 가져옴
retriever = docsearch.as_retriever()

# langchain hub 에서 Prompt 다운로드 예시
# https://smith.langchain.com/hub/rlm/rag-prompt

from langchain import hub

rag_prompt = hub.pull("rlm/rag-prompt")
rag_prompt

# HuggingFaceHub 객체 생성
llm = HuggingFaceHub(
    repo_id=huggingface_model_repo,
    model_kwargs={"temperature": 0.2, "max_length": 128}
)

# pipe operator를 활용한 체인 생성
# rag_prompt = PromptTemplate.from_template("question: {question}")
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
)

result = rag_chain.invoke("이 소설의 제목은 뭐야?")
print(result)

rag_chain.invoke("이 소설의 제목은 뭐야?")

rag_chain.invoke("이 소설의 저자는 누구야?")