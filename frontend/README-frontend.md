Frontend (React) quick start

1. Install dependencies:

```bash
cd frontend
npm install
```

2. Start dev server:

```bash
npm start
```

This will run the React dev server on http://localhost:3000 by default. To connect it to the Django backend (running on port 8000), either:
- use a proxy in `package.json` (add "proxy": "http://localhost:8000"), or
- run both and call the backend explicitly (set full URL in `axios.post`).
