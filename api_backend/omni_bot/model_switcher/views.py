from django.shortcuts import render
from rest_framework.views import APIView
import openai
from rest_framework.response import Response
from rest_framework import status
import json
import os
from dotenv import load_dotenv

## Loading Env Variables
load_dotenv()

GPT_SECRET_KEY = os.getenv('GPT_SECRET_KEY')
# Create your views here.
class ModelSwitcherView(APIView):

    def get(self, request):
        res = []
        data = json.load(open('/Users/raghukapur/private-projects/OmniBot/api_backend/omni_bot/model_switcher/suduko_prompts.json'))
        openai.api_key = GPT_SECRET_KEY
        i=0
        for line in data["sample"][::-1]:
            print(i)
            i+=1
            p = f'''
                Please categorize the following prompt into one of these four categories (Sudoku Puzzle, Object Detection, Blog Scraping, Normal Conversation), based on the task they are performing. Please assign one of the mentioned category to the prompt:

                Prompt: {line}
            '''
            response = openai.Completion.create(
                engine="davinci-instruct-beta-v3",
                # engine = "davinci",
                prompt=p,
                temperature=.7,
                # max_tokens=500,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                # stop=['(e.g. "Category: Blog Scraping Confidence: 50%")']
                )

            # grab our text from the repsonse
            text = response['choices'][0]['text']
            if "Sudoku Puzzle" in text:
                res.append("Sudoku Puzzle")
            elif "Object Detection" in text:
                print(f"Prompt {line} -> res {text}")
                res.append("Object Detection")
            elif "Blog Scraping" in text:
                print(f"Prompt {line} -> res {text}")
                res.append("Blog Scraping")
            elif "Normal Conversation" in text:
                print(f"Prompt {line} -> res {text}")
                res.append("Normal Conversation")
            else:
                print(f"Prompt {line} -> res {text}")
                res.append("Not Sure")
        return Response(data={"message": res}, status=status.HTTP_200_OK)