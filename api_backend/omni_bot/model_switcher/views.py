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
        # data = json.load(open('/Users/raghukapur/private-projects/OmniBot/api_backend/omni_bot/model_switcher/suduko_prompts.json'))
        openai.api_key = GPT_SECRET_KEY
        prompt = request.GET.get('prompt', '')
        medium_link = request.GET.get('medium_link', '')
        if not prompt:
            return Response(data={"message": "Prompt is a required field"}, status=status.HTTP_400_BAD_REQUEST)
        # i=0
        # for line in data["sample"][::-1]:
        #     print(i)
        #     i+=1
        user_prompt = f'''
            Please categorize the following prompt into one of these four categories (Sudoku Puzzle, Object Detection, Blog Scraping, Normal Conversation), based on the task they are performing. If the prompt is asking for summarizing of medium blog, then it is likely blog scraping. Please assign one of the mentioned category to the prompt:

            Prompt: {prompt}
        '''
        response = openai.Completion.create(
            engine="davinci-instruct-beta-v3",
            prompt=user_prompt,
            temperature=.7,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            )

        # grab our text from the repsonse
        text = response['choices'][0]['text'].lower().lstrip().rstrip()
        text = text.replace("\n","")
        if "sudoku puzzle" in text:
            res.append("Sudoku Puzzle")
        elif "object detection" in text:
            print(f"Prompt {user_prompt} -> res {text}")
            res.append("Object Detection")
        elif "blog scraping" in text:
            print(f"Prompt {user_prompt} -> res {text}")
            if not medium_link:
                return Response(data={"message": "Medium Link is required as the user is asking for summarize a medium article"}, status=status.HTTP_400_BAD_REQUEST)
            res.append("Blog Scraping")
        elif "normal conversation" in text:
            print(f"Prompt {user_prompt} -> res {text}")
            res.append("Normal Conversation")
        else:
            print(f"Prompt {user_prompt} -> res {text}")
            res.append("Not Sure")
        return Response(data={"message": f"User is asking to use {text}"}, status=status.HTTP_200_OK)