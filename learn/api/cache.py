# learning two types of cache in drf
#1 for static data we can use cache_page decorator
#2 for dynamic data we can use cache.set(),cache.get() methods




from django.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.views import APIView


class testcache1(APIView):
    @method_decorator(cache_page(60*2))  # Cache the response for 2 minutes
    def get(self,request):
        return Response({"message": "This is a cached response for static data."})

#this is the easy method to cache the page but this one cahes the whole response for given time so ,,,, if kae page ma chamge vayo within tyo time such as two minutes right now the response will be same for other users until the cache time ecpires . so just use this when the data is not going to chnage for the long period of time ..abs



from django.core.cache import cache



cahce_time = 60*2  # Cache time in seconds (2 minutes)

class testcache2(APIView):
    
    def get(self, request):
        cached_data="list of employees"
        data=cache.get(cached_data)  # Try to get the data from cache
        
        if data is None:
            list1=lists.objects.all()
            serializer=listsserializer(list1,many=True)
            data=serializer.data
            cache.set(cached_data, data, cahce_time)  # Store the data in cache for 2 minutes
            return Response(data, status=status.HTTP_200_OK)
        
        return Response(data, status=status.HTTP_200_OK)
        
    def post(self, request):
        serializer = listsserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            cache.delete("list of employees")  # Invalidate the cache when new data is added
            
            
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
#so in this method we are checking if we have already storde the chache if yes then that is shown if not then we cache the data , and if any change such as post is done to the data the cache is deletedea and new cahcne will be made when users hits the request.
    
    
    