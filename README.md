# TeoBot: Your Personal Knowledge Companion

TeoBot is a personalized chatbot designed to help you manage and interact with your personal notes. It is an intelligent tool that organizes your information, retrieves insights, and responds to your queries based on the provided data. TeoBot is your ideal companion for enhancing productivity, learning, and personal growth.

## How to Use TeoBot

To start using TeoBot, you first need to provide some credentials that enable its functionality. These credentials are:

- **Pinecone API Key**: Required for searching notes using embeddings, allowing TeoBot to find the most relevant notes based on your query.
- **OpenAI API Key**: Used to answer questions and create embeddings for your notes.
- **MongoDB Key**: Used to store all your notes along with their embeddings, enabling efficient information management.
- **GitHub Repository and Path**: Specifies the GitHub repository where your notes are stored and the directory path where they can be found.

### Providing Credentials

You can provide the credentials using the following commands within the Telegram chatbot:

- **Pinecone API Key**: Use the command `/pinecone <pinecone_key>`.
- **OpenAI API Key**: Use the command `/openai <openai_key>`.
- **MongoDB Key**: Use the command `/mongo <mongo_key>`.
- **GitHub Notes Configuration**: Use the command `/github <username> <repository> <directory_path>`.

If you need more information on how to obtain these keys, refer to the documentation of each provider:

- **Pinecone**: Visit [Pinecone Documentation](https://docs.pinecone.io/) and follow the instructions to create an account and generate an API key.
- **OpenAI**: Visit [OpenAI API Documentation](https://platform.openai.com/docs/api-reference/authentication) to obtain your API key.
- **MongoDB**: Refer to the [MongoDB Atlas Guide](https://www.mongodb.com/docs/atlas/getting-started/) to set up a database and obtain the URI.
- **GitHub**: To configure access to your notes, you need a GitHub repository that contains your notes in markdown format. Follow the [GitHub Guide](https://docs.github.com/en/get-started) to create a repository and get the necessary access.

## Basic Commands of TeoBot

To get a complete list of TeoBot's basic commands, please refer to the [comandos.md](https://github.com/TeoEchavarria/TeoBotProject/blob/master/src/documents/comands.md) file within the repository.

## Contribution

We welcome community contributions. If you wish to contribute to TeoBot, please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/YourFeature`.
3. Make your changes: `git commit -m 'Add new feature'`.
4. Push the branch: `git push origin feature/YourFeature`.
5. Open a Pull Request.

## License

This project is licensed under the MIT License. For more details, refer to the LICENSE file.