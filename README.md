# AI Chat Engine – Backend

This is the **backend API** for the AI Chat Engine project, built using **Django REST Framework**.  
It handles **user authentication, chat sessions, AI profile management, and real-time AI responses** by integrating **LangChain**, **Groq**, and **LLMs**.

---

## 🚀 Features

- **Authentication API**
  - Login/Signup with Email & Password
  - Google OAuth integration
  - JWT-based authentication

- **User Chat API**
  - Create and manage chat sessions
  - Get responses from different AI profiles (e.g., Interview Assistant)

- **AI Profile API**
  - Manage multiple AI profiles dynamically
  - Assign profiles to chat sessions

- **Admin Dashboard APIs**
  - View total sessions, chats, users, and AI profiles
  - Get system-level usage insights

- **AI Layer**
  - Uses **LangChain** for orchestration
  - Integrates **Groq** and LLM models for fast inference
  - Stores data in **MongoDB**

---

## 🛠️ Tech Stack

- **Framework**: [Django REST Framework](https://www.django-rest-framework.org/)  
- **Database**: [MongoDB](https://www.mongodb.com/)  
- **AI Layer**: [LangChain](https://www.langchain.com/), [Groq](https://groq.com/), LLMs  
- **Authentication**: JWT & Google OAuth  
- **Environment Management**: Python `venv` or `pipenv`

---

## 📂 Related Repositories

- **Hub (Project Overview)**: [ai-chat-engine-hub ↗](https://github.com/Sakthivel1122/ai-chat-engine-hub)  
- **Frontend UI**: [ai-chat-engine-frontend ↗](https://github.com/Sakthivel1122/ai-chat-engine-frontend)  
