# Suggested exercises:

1. Write a simple load monitoring tool consisting of:
    - a producer publishing load of the current machine averaged over 1, 5 and 15 minutes.
    - a client consuming this messages (e.g. printing them or logging using `logging` library).
    
   Load average can be obtained using `os.getloadavg()` or `psutil.getloadavg()` (the `psutil` version should work on MS Windows). You can also think of designing your program in such a way, that it is possible to subscribe only to load averaged
   over specific interval.
   
2. Write  a tool that downloads a batch of random doge images and stores them in some specified directory. 
   The tool should consist of
   the following components:
   - a producer that can be run on demand (i.e. as a command line script), that will schedule download tasks. The task should consist of number of images to download and name of the subdirectory in which the requested batch should be stored.
   - a worker that consumes tasks and downloads the images. You can use this API: https://shibe.online/
   
   If you don't like Shiba Inu you can use the same API to download cat or bird images. Or better yet, make it possible
   to choose the animal type in your producer.
   
3. This exercise is a slight modification to the exercise 2. Write a producer publishing links to random dog, cat
   and bir images at some regular interval. You can get links to images from the API in previous exercises.
   Then, write a worker that downloads images published by the producer. Design your program in such a way that:
   - It is possible to have multiple workers subscribed to published links
   - It is possible to subscribe only to the links of pictures of some specific animals (e.g. only cats).
