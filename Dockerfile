# Use a Node 17 base image
FROM node:18-alpine as builder
# Copy webapp files
COPY /my_vue /my_vue
# Set the working directory to /app inside the container
WORKDIR /my_vue
# ==== BUILD =====
# Install dependencies (npm ci makes sure the exact versions in the lockfile gets installed)
RUN npm install
# Build the app
RUN npm run build

# start by pulling the python image
FROM python:latest
# copy the requirements file into the image
COPY /api .

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

COPY --from=builder /my_vue/dist /my_vue/build

EXPOSE 8080

# make sure all messages always reach console
ENV PYTHONUNBUFFERED=1

# run server
CMD ["gunicorn"  , "-b", "0.0.0.0:8080", "app:app"]
