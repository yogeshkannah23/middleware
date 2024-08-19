from login.models import User,Post
from rest_framework.exceptions import AuthenticationFailed
import jwt,json
from login.serializers import UserSerializers,PostSerializers
from django.http import JsonResponse

class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Initialization code can go here (optional)

    def __call__(self, request):
        # Code executed for each request before
        # the view (and later middleware) are called.  

        paths_to_apply = ['/post_list/']
        if request.path in paths_to_apply:
            try:
                self.process_request(request)
            except Exception as e:
            # Handle the exception
                response = self.process_exception(request, e)
                return response

        response = self.get_response(request)

        # Code executed for each request/response after
        # the view is called.
        if request.path in paths_to_apply:
            response = self.process_response(request, response)
        
        return response
    
    
    def process_request(self, request):
        # This code is executed after the view is called.
        # print("Processing response:", response.status_code) 
        # You can modify the response here.

        token = request.body.decode('utf-8')
        jwt_token = json.loads(token)
        try:
            payload = jwt.decode(jwt_token['jwt'],'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated!')
        
        


        post = Post.objects.filter(author=payload['id'])
        
        request.posts = post

    def process_response(self, request, response):
        print(response)
        # Optionally add posts data to the response
        # if hasattr(request, 'posts'):
        #     response_data = json.loads(response.content)
        #     response_data = request.posts.data
        #     response.content = json.dumps(response_data)
        out=dict()

        for idx,data in enumerate(response.data):
            print(f"The id is {data['id']} and the author of the data is {data['author']} and the title is {data['title']} and discription is {data['discription']} and it is created on {data['created_on']}")
            out[idx] = f"The id is {data['id']} and the author of the data is {data['author']} and the title is {data['title']} and discription is {data['discription']} and it is created on {data['created_on']}"
        response.data = out
        response.content = response.rendered_content
        return response
    
    def process_exception(self,request, exception):
        return JsonResponse({'error': 'Something went wrong!', 'details': str(exception)}, status=500)

        
