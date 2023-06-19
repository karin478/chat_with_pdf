# PDF Question Answering Tool
##Description
This is a PDF Question-Answering tool developed using Flask, Langchain, and OpenAI embedding. In light of the significant price decrease of OpenAI embeddings, we opted to use them over the local or server embeddings that we had considered earlier. After several trials, we discovered a few issues with these alternatives:

## About Embedding
The embedding vector files were extremely large, occupying a significant amount of space.
The speed of creating the embeddings was less than ideal. Especially when calculations were done using small-scale server-side CPUs, the process was time-consuming.
Therefore, we decided to use OpenAI's embeddings for vector matching.

The operation of the program is quite simple. Users upload a PDF file which is divided into different chunks. When a user poses a question, the system computes the match between the question and the text in each chunk. The best-matching chunk is then sent along with the user's question to the Language Model (LLM), which responds based on the provided context. To make it easier for users to find the original text corresponding to their questions, we've also added a citation feature in the answer section.

## Installation Instructions
1. Set up a virtual environment using pip and install the dependencies listed in the requirements.txt file.

2. Start the Flask server and navigate to /upload to upload the PDF file for which you have questions. The system will automatically redirect you to the /chat page where you can start conversing with the PDF document.

3. Set up your .env file with openai api key

Each time question will cost about 0.02$  (test base on a 80 page pdf)
