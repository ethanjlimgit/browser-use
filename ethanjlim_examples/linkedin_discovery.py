from langchain_anthropic import ChatAnthropic
from browser_use import Agent, Browser, BrowserConfig, Controller
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
load_dotenv()

import asyncio

class Post(BaseModel):
    url: str
    name: str
    role: str
    location: str
    # date: str
    # likes: int
    # comments: int

class Posts(BaseModel):
    posts: List[Post]

controller = Controller(output_model=Posts)

# Configure the browser to connect to your Chrome instance
browser = Browser(
    config=BrowserConfig(
        # Specify the path to your Chrome executable
        chrome_instance_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',  # macOS path
        # For Windows, typically: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
        # For Linux, typically: '/usr/bin/google-chrome'
    )
)


# Initialize the model
llm = ChatAnthropic(
    model_name="claude-3-5-sonnet-20240620",
    temperature=0.0,
    timeout=100, # Increase for complex tasks
)
 

async def main():
    initial_actions = [
	{'open_tab': {'url': 'https://www.linkedin.com/company/openai/people/'}},
	# {'open_tab': {'url': 'https://en.wikipedia.org/wiki/Randomness'}},
	# {'scroll_down': {'amount': 1000}},
    ]
    agent = Agent(
        task="Find OpenAI's employees on the Operator team and their LinkedIn profile links",
        llm=llm,
        browser=browser,
        controller=controller,
        initial_actions=initial_actions,
    )
    result = await agent.run()
    print(result.final_result)
    data = result.final_result()
    parsed: Posts = Posts.model_validate_json(data)
    # parsed.posts[0].caption
    await browser.close()

asyncio.run(main())