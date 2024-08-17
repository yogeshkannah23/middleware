from login.models import User,Post
from rest_framework.exceptions import AuthenticationFailed
import jwt,json
from login.serializers import UserSerializers,PostSerializers

class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Initialization code can go here (optional)

    def __call__(self, request):
        # Code executed for each request before
        # the view (and later middleware) are called.       
        # self.process_request(request)

        response = self.get_response(request)

        # Code executed for each request/response after
        # the view is called.
        self.process_response(request, response)
        
        return response
    
    
    def process_request(self, request):
        # This code is executed after the view is called.
        # print("Processing response:", response.status_code) 
        # You can modify the response here.

        token = request.body.decode('utf-8')
        jwt_token = json.loads(token)
        try:
            payload = jwt.decode(jwt_token.get['jwt'],'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated!')
        
        


        post = Post.objects.filter(author=payload['id'])
        posts = PostSerializers(post,many=True)
        request.posts = posts

    def process_response(self, request, response):
        # Optionally add posts data to the response
        if hasattr(request, 'posts'):
            response_data = json.loads(response.content)
            response_data = request.posts.data
            response.content = json.dumps(response_data)
        
        return response

        
