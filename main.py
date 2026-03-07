import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM


# Load environment variables from the .env file
load_dotenv()

# Verify that the GROQ_API_KEY is set
if not os.getenv("GROQ_API_KEY") or os.getenv("GROQ_API_KEY") == "your_free_groq_api_key_here":
    print("Error: Please set your GROQ_API_KEY in the .env file before running.")
    print("You can get a free key from: https://console.groq.com/keys")
    exit(1)

# Set the Groq API key in the environment for LiteLLM to find
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Use the model name string directly. CrewAI will handle the rest.
llm = "groq/llama-3.1-8b-instant"





# 1. Define the Agents
researcher = Agent(
    role='Senior Tech Researcher',
    goal='Uncover groundbreaking technologies and trends in {topic}',
    backstory='You are a curious researcher who excels at finding the latest and most accurate information on complex topics.',
    verbose=True,
    allow_delegation=False,
    llm=llm
)

writer = Agent(
    role='Content Writer',
    goal='Craft compelling and engaging blog posts about {topic}',
    backstory='You are an expert storyteller and content creator. You translate complex research into easy-to-understand and engaging blog posts.',
    verbose=True,
    allow_delegation=False,
    llm=llm
)

editor = Agent(
    role='Chief Editor',
    goal='Ensure the blog post is perfectly formatted, free of errors, and optimized for SEO.',
    backstory='You are a meticulous editor with an eye for detail. You shape raw drafts into polished masterpieces.',
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# 2. Define the Tasks
research_task = Task(
    description='Search for the latest information, key points, and exciting developments regarding "{topic}".',
    expected_output='A comprehensive bulleted list of the top key points and trends related to the topic.',
    agent=researcher
)

write_task = Task(
    description='Using the research provided, write an engaging blog post covering "{topic}". Make it at least 3 paragraphs long and use a professional yet conversational tone.',
    expected_output='A drafted blog post containing an introduction, body paragraphs, and a conclusion.',
    agent=writer
)

edit_task = Task(
    description='Review the drafted blog post. Fix any grammatical errors, improve the flow, and format it beautifully in Markdown with appropriate headings. Add an SEO meta description at the top.',
    expected_output='A final, polished, and beautifully formatted Markdown blog post ready for publication.',
    agent=editor
)

# 3. Form the Crew
blog_crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, write_task, edit_task],
    process=Process.sequential,
    verbose=True
)

def main():
    print("Welcome to the CrewAI Blog Writer!")
    topic = input("Enter the topic you want to write a blog post about: ")
    print(f"\nStarting the crew with the topic: '{topic}'...\n")

    # Run the crew!
    result = blog_crew.kickoff(inputs={'topic': topic})

    print("\n\n#####################################")
    print("FINAL BLOG POST:")
    print("#####################################\n")
    print(result)

    # Optionally, save it to a markdown file
    with open("blog_post_output.md", "w", encoding="utf-8") as f:
        f.write(str(result))
    print("\n[The final post has been saved to 'blog_post_output.md']")

if __name__ == "__main__":
    main()
