# StoryWithMe

An innovative AI-driven companion
that aims to transform the way children engage with stories.

![Alt text](/client/public/family.png)

## Issues

Parental involvement significantly impacts children's well-being. However, according to the U.S. Bureau of Labor Statistics, in 2023, parents spent an average of only 3.6 minutes per day reading to children under 6. Picture books, which are powerful educational tools for young children, often lack representation of specific cultural heritages, limiting their impact.

![Alt text](/client/public/average_hours_per_day.png)

## Our Solution

To address these issues, we propose StoryWithMe, an AI-driven companion that co-creates imaginative stories with young children. This solution not only fills the gap when parents are unavailable, reducing stress for children, but also promotes self-awareness and cultural understanding by personalizing stories to reflect diverse backgrounds. Our project aligns with the UN Sustainable Development Goals (SDG 4) "Quality Education" and (SDG 3) "Good Health and Well-Being" by offering enriching learning experiences tailored to children's needs, helping them grow both cognitively and emotionally.

## Features

- Co-create personalized stories
- Immersive stories with illustration, voice narration, and animation
- Adapts storylines based on the child’s real-time response

## Demo

[Demo Video](https://youtu.be/l8IowmqNNk4)

## Application Pipeline

![Alt text](/client/public/pipeline.png)

## Local Installation

### Prerequisites

To run this app, you'll need:

- [Python 3.11.5](https://www.python.org/downloads/)
- [OpenAI API Key](https://openai.com/blog/openai-api)
- [ElevenLabs API Key](https://elevenlabs.io/api)

### How to run

- Open server folder > Install dependencies > Run the server

```
cd server

pip install -r requirements.txt

flask run
```

- Open client folder > Create another terminal > Install libraries > Run the client

```
cd client

npm install

npm start
```

## Tech Stacks

**Backend:** Flask, Python

**Frontend:** React, JavaScript, TailwindCSS, DaisyUI

**LLM Models:** GPT-4o, Gemini 1.5 Flash-8B, Stable Image Core, Eleven Multilingual v2

**Tools:** Portkey.ai, LangChain, Postman

---

Make with ❤️ at **TED**AI Hackathon 2024
