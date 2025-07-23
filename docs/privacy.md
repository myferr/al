# Privacy Policy

*Last updated: July 23rd, 2025*

This Privacy Policy describes how **Al**, the conversational AI Discord bot (“we”, “us”, or “our”), handles your data when you interact with the bot on Discord.

## 1. Data Collection

* **Al does not collect personal data** beyond what is necessary to function as a Discord bot.
* When you interact with Al:

  * Your message content and Al’s replies may be stored in a local **MongoDB database**.
  * A **hashed version of your Discord user ID** may be stored to maintain user-specific memory while reducing identifiability.
  * Your **display name** may be stored to personalize responses.

This data is used solely for maintaining long-term memory and context using a Retrieval-Augmented Generation (RAG) system to improve conversations.

## 2. Local Storage Only

* All data is stored **locally** on the device where the bot is hosted, inside a self-hosted MongoDB database.
* No data is transmitted to any third-party service, server, or analytics provider.
* If you are running the bot yourself, **you control all stored data.**

## 3. Discord Information

* Al uses the Discord API to read and respond to messages.
* Al only accesses:

  * Your message content (if you mention the bot or reply to it),
  * Your username, user ID (hashed if stored), and display name,
  * The server and channel the message was sent in.
* Al does not read private DMs unless explicitly invited into them.

## 4. Data Retention

* Messages and embeddings used in the RAG system are stored persistently in the local MongoDB database.
* Data is retained until manually removed by the bot operator or via a bot-provided deletion command (if implemented).
* If you are not the host of the bot, you should contact the server owner or bot operator regarding stored data.

## 5. Your Rights

* Since Al stores data locally, the bot operator is responsible for managing that data.
* If you would like your stored data (including message history or embeddings) to be removed, please contact the server owner or the person running the instance of the bot.

## 6. Security

* Data is stored in plaintext within a local MongoDB instance.
* Hashed user IDs are used to minimize identifiability.
* It is the responsibility of the bot host to secure the device and database where Al is running, including access controls and system-level security.

## 7. Changes to this Policy

* We may update this Privacy Policy from time to time.
* Updates will be posted publicly wherever the bot’s code or documentation is hosted.

## 8. Contact

For questions about this Privacy Policy, please contact the bot developer or maintainer listed on the [GitHub repository](https://github.com/myferr/al) or via [e-mail](mailto:contactme.myfer@protonmail.com)
