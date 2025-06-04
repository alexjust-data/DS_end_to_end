# 🏗️ Project Architecture

```
[ATAS Screens]
     ↓
🐍 Python Worker (capture + pattern recognition)
     ↓
⚙️ FastAPI Backend (alerts via WebSocket)
     ↓
🌐 React Frontend (alert visualization)
```

Each layer is decoupled for flexibility, scalability, and ease of maintenance.
