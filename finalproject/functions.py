import random
from .models import Profile
def calculate_score(request):
    x = random.randint(10,100)
    request["profile"].score = x
    request["profile"].save()
    print("RANDOM NUMBER", x)
    print("PROFILE: ", request["profile"].profile_name)
    
    
