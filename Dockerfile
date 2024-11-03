FROM python:3.11-alpine

COPY bot /bot
WORKDIR /bot

# Set environment variables to suppress pip and Python warnings
ENV PYTHONWARNINGS="ignore"
ENV PIP_NO_WARN_SCRIPT_LOCATION=1

# Install dependencies with suppressed location warnings
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt --no-warn-script-location

CMD ["python3", "-u", "main.py"]
