---
# https://vitepress.dev/reference/default-theme-home-page
layout: home

hero:
  name: "Al"
  text: "A conversational Discord.py AI chat-bot"
  tagline: Chat with AI in your Discord server!
  actions:
    - theme: brand
      text: Docs
      link: /introduction
    - theme: alt
      text: Invite to server
      link: https://discord.com/oauth2/authorize?client_id=1394016191537741957

features:
  - title: Conversational AI
    details: Powered by a local Ollama model (default llama3), Al engages in dynamic, context-aware conversations.
  - title: Contextual Memory
    details: Stores all user messages and bot responses in a persistent memory file to maintain conversation history and improve replies.
  - title: Flexible Interaction
    details: Responds when directly pinged or when a user replies to Al's messages, making conversations natural and seamless.
  - title: Typing Indicator
    details: Shows a “typing…” indicator in Discord while generating a response for a better user experience.
  - title: Self-Hosted and Private
    details: Runs locally with Ollama and Discord bot token, ensuring data privacy and control.

---
