# Use the official Python image from Docker Hub as the base image
FROM python:3.10-slim
# Set working directory
WORKDIR /usr/src/app

# Install Dependencies
COPY requirements.txt  .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

#Configure TKinter


# Copy
COPY main.py .
COPY Audio.py  .
COPY Database.py  .
COPY DecisionPoints.py  .
COPY Game.py  .
COPY GameAssetVerification.py  .
COPY GameSession.py  .
COPY GraphicsUtilities.py  .
COPY HostSession.py  .
COPY image_handler.py  .
COPY JoinSession.py  .
COPY network.py  .
COPY story_builder.py  .
COPY story_node.py  .
COPY TestCases.py  .
COPY testHostingJoiningConnections.py  .
COPY TestImageHandler.py  .
COPY testP2PNetwork.py  .
# run
CMD [ "python", "./TestCases.py" ]



