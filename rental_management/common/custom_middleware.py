from django.http import JsonResponse


class CustomErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 500:
            problem_description = (
                "Internal Server Error Occurred. Please contact support"
            )
            return JsonResponse({"message": problem_description}, status=500)
        elif response.status_code == 404:
            problem_description = "Page Not Found"
            return JsonResponse({"message": problem_description}, status=404)

        return response
