from dotenv import load_dotenv
import os

print('cwd', os.getcwd())
load_dotenv()
openai = os.getenv('OPENAI_API_KEY')
groq = os.getenv('GROQ_API_KEY')
print('OPENAI repr', repr(openai))
print('OPENAI length', len(openai) if openai else 0)
print('GROQ repr', repr(groq))
print('GROQ length', len(groq) if groq else 0)
