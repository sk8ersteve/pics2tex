# THacks18


Pics2Tex

#Live Project URL: http://pics2tex.eastus.cloudapp.azure.com

Our project is an Azure-web-hosted application that processes and examines images of mathematical expressions -- typically through the medium of well-formatted image captures of handwriting -- by virtue of a robustly trained convolutional neural network developed with the help of a combination of Computer Vision APIs and Microsoft Azure's Data Science Virtual Machine and Cloud Services. 


#What we built
An easy to use tool that allows the porting of pdf documents to tex documents

#How we built it:

Our project consisted of several interworking pieces. The Data Science Virtual Machine, provided in Microsoft Azure, gave us a basis for completing the work for much of our project. 

##Evan fill out computer vision, preprocessing images, character extraction, BB operations and Tex generation

##Alex fill out deep learning, Azure training

##Anupam, fill out spline transformations to blow up size of our training set and increase test accuracy

While all the image to latex processing happened in python, our platform for using this tool was done in NodeJS, this NodeJS application was deployed from the Virtual Machine. Bootstrap was used to give the platform a more pleasing appearance. The app was programmed so that submitting a picture would call our python program, which prints out Latex code that we capture back in our NodeJS program. Using the server, the connection between these parts was seamless.

#Why we built it:

We are lazy CS students tired of having to Latex our homework, research, and other documents.  We just want an easy, simple, and functional product to save us time.

As current or former TAs, we have also had to deal with students’ who are unwilling to Latex and upload their docs.  We hope that this tool will help encourage them to do so in the future.

#Where this is going:


