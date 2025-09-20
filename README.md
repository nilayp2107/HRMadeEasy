# HRMadeEasy
A project aimed at developing an AI Agent to Handle work related to Human Resource Management.

## HR Assistant
Answer questions about leave, policies and benefits
<br>
<br>
Basic Principal: Retrieval Augmented Generation with Vector DB and carefully constructing prompts from the context to feed to an LLM.

### Technologies Used
AI Model used: gpt-oss-20b
<br>
Database: Milvus
<br>
UI: Flask
<br>
Coding Language: Python
<br>
Documents fetched: V11_leave.pdf, V11_policies.pdf, V11_benefits.pdf

### Working Principal
Input: Human user Queries in Text format
<br>
Output: LLM generated text
<br>
<br>
Query(text) -> Vector_embeddings -> Similarity Search (Vector DB) -> Top k contexts -> Prompt Construction -> Feeding an LLM -> LLM Response
