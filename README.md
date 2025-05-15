# NarrativeVerse

## Overview

NarrativeVerse is an innovative framework designed to create dynamic storytelling experiences and intelligent non-player characters (NPCs) in modern games. The project aims to revolutionize how stories are told in interactive environments, allowing NPCs to evolve and adapt their dialogues based on player choices, creating a unique and personalized experience for each gaming session.

Unlike traditional dialogue systems that follow predetermined paths, NarrativeVerse uses advanced artificial intelligence technologies to orchestrate natural conversations and narrative branches that organically respond to player actions. This results in a more vibrant and responsive game world, where each decision carries weight and meaning in the development of the story.

## Technologies

NarrativeVerse is built on a modular and scalable architecture that integrates several cutting-edge technologies:

The system's foundation uses advanced language models through integration with Hugging Face Transformers, enabling the generation of contextually relevant and natural dialogues. For efficient prompt management and reasoning chains, we implement Langchain, which facilitates the creation of logical thought sequences for our NPCs.

Efficient storage and retrieval of character memories and contexts are managed by Pinecone, a vector database solution that allows for fast semantic queries. This enables NPCs to "remember" past interactions with the player and adjust their behavior accordingly.

The system architecture has been designed with performance and scalability in mind, allowing game developers to implement complex narratives without sacrificing performance, even in games with many characters and intertwined storylines.

## Key Features

The heart of NarrativeVerse lies in its ability to create truly dynamic NPCs. Each character has a detailed profile that includes not only basic information such as name and class, but also moral alignment, background story, and personality traits that directly influence how they interact with the player.

The story branching system allows developers to create non-linear narratives that adapt to player choices. Instead of following a predetermined path, the story evolves organically, creating a unique experience for each player. This is made possible by our prompt orchestration engine, which dynamically adjusts the tone, content, and direction of the narrative based on decisions made.

Integration with game engines like Unity is simplified through our dedicated plugin, which provides an intuitive interface to connect the NarrativeVerse system to your game project. This allows developers of all experience levels to implement dynamic narratives without requiring deep knowledge of artificial intelligence.

## Installation and Setup

To start using NarrativeVerse in your project, follow these steps:

Clone this repository to your local machine using `git clone`. Install the necessary dependencies by running `pip install -r requirements.txt` in the project's root directory. For Unity projects, import the unity_plugin folder into your existing project.

Configure NPC profiles by editing the npc_profiles.json file or creating new profiles following the example format. Customize the prompt orchestration engine in manus_engine.py according to your game's specific needs.

Explore the story_branching.ipynb notebook to understand how to create effective branching narratives and adapt them to your own game universe. Refer to additional documentation in the docs folder for detailed tutorials and implementation examples.

## Contribution

Contributions to NarrativeVerse are welcome! If you have ideas to improve the system, found bugs, or want to add new features, feel free to open an issue or submit a pull request. Check our contribution guide for more information on how to participate in development.

## License

NarrativeVerse is licensed under the MIT License. See the LICENSE file for more details.

Copyright (c) 2025 NowGo Holding
