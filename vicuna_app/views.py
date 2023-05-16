from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .gptq_model import load_model  
from .models import License  

class ChatBotView(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model, self.tokenizer = load_model()

    def post(self, request, *args, **kwargs):
        # Check for a license key
        license_key = request.data.get('license_key', None)
        if not license_key:
            return Response({'error': 'Missing license key'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the license key is valid
        license = License.objects.filter(key=license_key).first()
        if not license:
            return Response({'error': 'Invalid license key'}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate the user
        user = authenticate(username=license.user.username, password=request.data.get('password', ''))
        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # Extract the prompt
        prompt = request.data.get('prompt', None)
        if not prompt:
            return Response({'error': 'Missing prompt'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate a response from the model
        inputs = self.tokenizer.encode(prompt, return_tensors="pt")
        outputs = self.model.generate(inputs, max_length=1000, do_sample=True)
        generated = self.tokenizer.decode(outputs[:, inputs.shape[-1]:][0], skip_special_tokens=True)

        return Response({'response': generated}, status=status.HTTP_200_OK)
