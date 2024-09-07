# TeoBot: Your Personalized Knowledge Companion

TeoBot is a personalized chatbot designed to help you manage and interact with your personal notes while also learning more about you. It's an intelligent tool that organizes your information, retrieves insights, and responds to queries based on the data you provide. TeoBot can be your ultimate companion for enhancing productivity, learning, and personal growth.

### Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

### Features

- **Personal Note Management**: TeoBot allows you to manage, search, and interact with your personal notes seamlessly.
- **Context-Aware Conversations**: It uses advanced natural language processing to understand the context and provide meaningful responses based on your notes and preferences.
- **Efficient Embedding Retrieval**: Instead of processing all your notes and consuming unnecessary tokens, TeoBot utilizes embeddings to fetch only the most relevant notes, saving time and resources.
- **Personal Insights**: TeoBot can provide personalized recommendations, reminders, and insights to help you achieve your goals.
- **Integration Ready**: Easily integrate TeoBot with your existing note-taking tools, such as Obsidian, Typst, or any markdown-based note system.
- **Future Features**: Planned integrations include image understanding capabilities and audio response options to enhance interactions.

### Installation

To get started with TeoBot, follow these simple steps:

1. Clone this repository:

    ```bash
    git clone https://github.com/TeoEchavarria/TeoBotProject.git
    ```

2. Navigate to the project directory:

3. Create a `.env` file in the root directory and add your API keys and tokens:

    ```env
    OPENAI_API_KEY=your_openai_api_key
    MONGODB_URI=your_mongodb_uri
    PINECONE_API_KEY=your_pinecone_api_key
    TELEGRAM_TOKEN=your_telegram_bot_token
    MARKDOWN_NOTES=your_markdown_dirpath
    CONTEXT=""
    ```

4. Create a `validusernames.txt` file in the root directory, separated by commas, containing the Telegram usernames of the users you want to grant access to:

    ```
    username1,username2,username3
    ```

5. Install the required dependencies and set up the project:

    ```bash
    pip install -r requirements.txt
    ```

6. Run TeoBot:

    ```bash
    python setup.py
    ```

### Usage

TeoBot is designed to be intuitive and user-friendly. Here’s how to get started:


### Configuration

You can configure TeoBot to better suit your needs:

- **Note Sources**: Configure the paths to your note directories or integrate with cloud-based note services.
- **Customization**: Modify TeoBot’s settings to customize the way it interacts with you, such as tone, depth of responses, and more.
- **API Integrations**: Connect TeoBot with APIs of your favorite productivity tools.

### Contributing

We welcome contributions from the community! If you'd like to contribute to TeoBot, please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/YourFeature`.
3. Commit your changes: `git commit -m 'Add new feature'`.
4. Push to the branch: `git push origin feature/YourFeature`.
5. Open a Pull Request.