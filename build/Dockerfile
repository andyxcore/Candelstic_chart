FROM python:3.10.13-slim-bullseye
RUN mkdir "/app"
COPY src /app/src/
COPY tests /app/tests/

WORKDIR app
RUN pip install pandas==1.5.3 matplotlib==3.6.3 plotly==5.16.1
#ENTRYPOINT python
CMD ["python", "main.py"]