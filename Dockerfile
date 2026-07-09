FROM python:3.10
RUN curl -fsSL https://ollama.com/install.sh | sh
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod +x entrypoint.sh
EXPOSE 7860
CMD ["./entrypoint.sh"]