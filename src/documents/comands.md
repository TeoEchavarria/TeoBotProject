# TeoBot Commands Guide

This guide provides a comprehensive list of commands available for interacting with TeoBot. These commands are designed to help you easily manage your notes, search for information, and configure TeoBot for personalized use.

## Basic Commands

- **/start**: Initializes the chatbot and provides an introduction on how to use TeoBot.
- **/credentials**: Displays information on how to configure the necessary API keys for TeoBot.
- **/page**: Displays the current page of notes.
- **/search <query>**: Searches through your notes using embeddings, allowing TeoBot to find the most relevant content.
- **/clear**: Clears the current saved context to start a new session.
- **/look**: Displays the current context that TeoBot is using.

## Credentials Configuration Commands

- **/pinecone <pinecone_key>**: Sets up the Pinecone API key for embedding-based searches.
- **/openai <openai_key>**: Sets up the OpenAI API key for generating embeddings and answering questions.
- **/mongo <mongo_key>**: Sets up the MongoDB connection URI to store all notes and embeddings.
- **/github <username> <repository> <directory_path>**: Configures access to your notes stored in a GitHub repository.

## Additional Commands

- **/update**: Updates TeoBot with the latest markdown files from the GitHub repository.

## General Usage Tips

- Ensure you have provided all required credentials before attempting to use commands related to searching or managing notes.
- You can update your credentials at any time by re-entering the relevant command with the new key.

If you have any questions or need further assistance with the commands, feel free to reach out through the community or check the README documentation for more details.
