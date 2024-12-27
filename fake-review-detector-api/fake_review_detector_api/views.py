import os
import time

import requests
import json
from dotenv import load_dotenv
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.exceptions import NotAcceptable
from rest_framework.throttling import AnonRateThrottle

load_dotenv()

MODEL_NAME = "ibrahim-haji-abdi/longformer-fake-review-detector-combined"
ENDPOINT = "https://api-inference.huggingface.co/models/" + MODEL_NAME
RETRIES = 5
DELAY = 3


@api_view(["POST"])
@permission_classes([HasAPIKey])
@throttle_classes([AnonRateThrottle])
def detection_response(request):
    print(request)
    if request.method == "POST":
        # verifies the input is in the correct form
        inputs = request.data.get("inputs")
        if inputs is None:
            raise NotAcceptable(
                "Please enter an input to detect fake reviews in the body of the request with the format"
                "{'inputs': '<review>'}, reviews can be in a list"
            )
        print(f"query: {inputs}")
        # checks if it is a singular review or a batch and checks if the length of the review is below token limit
        if isinstance(inputs, str):
            if len(inputs) > 4096:
                raise NotAcceptable("Please enter a review less than 4096 characters")
        elif isinstance(inputs, list):
            for review in inputs:
                if len(review) > 4096:
                    raise NotAcceptable("Please make sure all reviews are less than 4096 characters")
        # sends the review(s) to the inference API
        response = inference_request(ENDPOINT, inputs)
        print(response)
        return JsonResponse(response, safe=False)


@api_view(["GET"])
def home(request):
    if request.method == "GET":
        # checks if there is a review in session, to see if it was passed via the form
        # else it loads the normal, empty home page
        review = request.session.get("review")
        if review:
            # sends review to inference API
            del request.session["review"]
            response = inference_request(ENDPOINT, review)
            # handles the error of the model not being loaded on the inference API
            print(response)
            if "error" in response:
                time = float(response["estimated_time"])
                time = round(time)
                time = str(time) + "s"
                error = f"Error: {response['error']}\nEstimated time: {time}"
                return render(request, "base.html", {
                    "label": error,
                })
            # gets the appropriate label and score
            labels = response[0]
            label = labels[0]
            result = label["score"]
            result = str(round(float(result) * 100.0)) + "%"
            label = str.capitalize(label["label"]) + "ness"
            return render(request, "base.html", {
                "review": review,
                "label": label,
                "result": result
            })
        return render(request, "base.html")


@api_view(["POST"])
def submit_form(request):
    if request.method == "POST":
        review = request.POST.get("review")
        request.session["review"] = review
        print(review)
        return redirect("/")

def retry_on_exception(request_function: callable):
    def wrapper(*args, **kwargs):
        for _ in range(RETRIES):
            try:
                return request_function(*args, **kwargs)
            except:
                pass
            time.sleep(DELAY)
    return wrapper

@retry_on_exception
def inference_request(endpoint: str, input: str):
    try:
        response = requests.post(endpoint, json=input, headers={
            "Authorization": "Bearer {token}".format(token=os.getenv("READ_TOKEN"))
        })
        return response.json()
    except:
        raise