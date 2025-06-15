# Use official Python base image
FROM python:3.12

# Set environment vars to prevent Python from buffering and writing .pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TRANSFORMERS_CACHE=/tmp/huggingface
ENV HF_HOME=/tmp/huggingface
ENV TRANSFORMERS_CACHE=/tmp/huggingface/transformers


# Set work directory inside container
WORKDIR /app

# Copy all files from current dir to /app in container
COPY . /app

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose port (OPTIONAL – only needed if you serve on HTTP)
EXPOSE 7860

# Run your app
CMD ["python", "main.py"]
