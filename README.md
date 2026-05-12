# AutoAesthetic: Image Ranking and Optimization Pipeline

This project performs aesthetic image ranking and optimization using vision models to help photographers efficiently select photos and experiment with new editing skills!

It supports:
- Image ranking scored by CLIP-based aesthetic model
- Automated image optimization via gradient descent
- Interactive experimentation with editing parameters

To setup the project, please follow the instructions below:

1. Create Environment/Install Backend Dependencies

```bash
conda create -n aesthetic_env python=3.12
conda activate aesthetic_env
```

2. Run backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload
```

3. Run frontend

First, open another terminal.
```bash
cd frontend
nvm install 20.19.0
nvm use 20.19.0
npm install
npm run dev
```
4. Click/go to the link provided in the frontend terminal to launch the application.
