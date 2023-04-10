from nis import cat
from django.shortcuts import render
from rest_framework.views import APIView
import openai
from rest_framework.response import Response
from rest_framework import status
import json
import os
from model_switcher.utils import preprocess_prompt, get_prompt_category, summarize_article, get_suduko_solver, get_resume_summarized, get_lstm_prompt_prediction, convert_audio_to_text
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

class ModelSwitcherGetCategoryView(APIView):

    def get(self, request): 
        prompt = request.GET.get('prompt', '')
        if not prompt:
            return Response(data={"message": "Prompt is a required field"}, status=status.HTTP_400_BAD_REQUEST)
        print(prompt)
        processed_prompt = preprocess_prompt(prompt)
        category = get_prompt_category(processed_prompt)
        lstm_category = get_lstm_prompt_prediction(prompt)
        print(category, lstm_category)
        if lstm_category != category:
            return Response(data={"message": "Need more info"}, status=status.HTTP_204_NO_CONTENT)
        return Response(data={"category": category}, status=status.HTTP_200_OK)    

class ModelSwitcherBlogSummaryView(APIView):

    def post(self, request):
        link = request.POST.get('medium_link', '')
        if not link:
            return Response(data={"message": "medium_link is a required field"}, status=status.HTTP_400_BAD_REQUEST)
        summarized_article = summarize_article(link)
        if not summarized_article:
            return Response(data={"message": "Failed to get article summary, please try after some time"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(data={"summary": summarized_article}, status=status.HTTP_200_OK)

class ModelSwitcherResumeSummaryView(APIView):

    def post(self, request):
        if not 'resume' in request.FILES:
            return Response({"message": f"file with name 'resume' is missing from the request"}, status=status.HTTP_400_BAD_REQUEST)
        summarized_resume = get_resume_summarized(request.FILES['resume'])
        if not summarized_resume:
            return Response(data={"message": "Failed to get article summary, please try after some time"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(data={"summary": summarized_resume}, status=status.HTTP_200_OK)

class ModelSwitcherSudukoView(APIView):

    def post(self, request):
        if not 'suduko' in request.FILES:
            return Response({"message": f"file with name 'suduko' is missing from the request"}, status=status.HTTP_400_BAD_REQUEST)
        # summarized_resume = get_resume_summarized(request.FILES[file_name])
        suduko_result = get_suduko_solver(request.FILES['suduko'])
        res = ""
        for i in suduko_result:
            res += str(i) + "\n"

        if not res:
            return Response(data={"message": "Failed to get article summary, please try after some time"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(data={"summary": res}, status=status.HTTP_200_OK)

class ModelSwitcherAudioView(APIView):

    def post(self, request):
        if not 'audio' in request.FILES:
            return Response({"message": f"file with name 'audio' is missing from the request"}, status=status.HTTP_400_BAD_REQUEST)
        audio_to_text = convert_audio_to_text(request.FILES['audio'])
        # suduko_result = "this is dummy data"
        if not audio_to_text:
            return Response(data={"message": "Failed to get audio_to_text, please try after some time"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(data={"transcript": audio_to_text}, status=status.HTTP_200_OK)

class ModelSwitcherTestView(APIView):

    def post(self, request): 
        prompt = request.POST.get('prompt', '')
        if not prompt:
            return Response(data={"message": "Prompt is a required field"}, status=status.HTTP_400_BAD_REQUEST)
        print(prompt)
        processed_prompt = preprocess_prompt(prompt)
        category = get_prompt_category(processed_prompt)
        lstm_category = get_lstm_prompt_prediction(prompt)
        if lstm_category != category:
            return Response(data={"message": "Need more info"}, status=status.HTTP_)
        if category == "blog":
            link = request.POST.get('medium_link', '')
            if not link:
                return Response(data={"message": "medium_link is a required field"}, status=status.HTTP_400_BAD_REQUEST)
            summarized_article = summarize_article(link)
            if not summarized_article:
                return Response(data={"message": "Failed to get article summary, please try after some time"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(data={"summary": summarized_article}, status=status.HTTP_200_OK)    
        elif category == "resume":
            file_name = request.POST.get('file_name', '')
            if not file_name or not file_name in request.FILES:
                return Response({"message": f"field file_name and file with name {file_name} is missing from the request"}, status=status.HTTP_400_BAD_REQUEST)
            get_resume_summarized(request.FILES[file_name])
        return Response(data={"message": f"User is asking to use {category}"}, status=status.HTTP_200_OK)