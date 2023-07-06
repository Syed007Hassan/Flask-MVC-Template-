import os
from flask import Flask, jsonify
import google.generativeai as palm
palm.configure(api_key=os.environ['PALM_API_KEY'])

def palm_create_response(prompt1):
    
    try:
        response =palm.generate_text(prompt=prompt1, max_output_tokens=800, temperature=0.7)
        print(response.result)
        return response.result
    except Exception as e:
        print("Error generating response: " + str(e))
        return Exception("Error generating response: " + str(e))