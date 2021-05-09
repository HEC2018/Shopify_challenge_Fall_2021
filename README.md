# Shopify_challenge_Fall_2021
### Shopify Fall 2021 Back-end Developer / Data Developer Intern Challenge Question (image repo)
### Created by Xinhai Wei. (x67wei@uwaterloo.ca)

In this project, I designed a creative image repository, with the functionality of purchasing products and putting up new products.

## How I built it

Technology: I leveraged two useful platforms: Python _Flask_ and  _Sqlite3_, and used four different programming languages: Python, HTML5(with Bootstrap), CSS, and SQLite3. 
For this project, _Flask_ is a framework that not only manage for a creative and user-friendly web interface but also handle the particular functionalities of the webiste, including purchasing and uploading images. _Sqlite3_, as database management tool, stores the image information, business transaction, also avoids adding duplicate images.

For the backend design, I utilized Python _Flask_ and _Sqlite3_ for image uploading, storing and duplicate checking purposes. In particular, we used the HTTP post action to trigger the upload process of images, and built-in functionality of HTML5 to check the data integrity. (i.e. whether the user's input is a valid number). Since the application requires uploading files, which shall be treated extremely seriously, I also put a very strict secure requirement on file's name and extension, using secure_filename from werkzeug.utils, which is a useful python package that basically determines if a file is safe to store. A cool feature I implemented is that I use some _Sqlite3_ code to check a if a certain image of the same price has appeared on the website or not. If it does, I will treat the new upload of images as adding stocks but not putting up new images for sell.   

For the frontend, I mainly uses HTML5 with Bootstrap 5.0 for our clear and easy-understanding user interface. _Flask_'s render_template function is used for updating data from past transactions. For the current stage, I automatically change every submitted image file to 256x256 pixels because of the website's capacity. I also have built a file-upload page which make a good use of the form component of Bootstrap. Besides, a message website is included to remind the user if a purchase of image is successful or not. The message webisite uses an alert component which makes user have a better sense to the new transaction.

## Usage

Requirements: Python3( Packages: Flask, sqlite3, werkzeug )
First,

    $ git clone https://github.com/HEC2018/Shopify_challenge_Fall_2021.git

To run this application, run `python3 server.py` from the command line, which will create the database tables and start the Flask server automatically.

Then, open a web browser at the address given by Flask (http://127.0.0.1:5000). The main website has a list of images with their related data, like their name, price, stock, and a sample. All of this data are pulled from _Sqlite3_ DB table and rendered through _Flask_. Initially some images are appeared on the page as a sample test to the website. The initial images are stored within the static/images folder locally. However, by clicking "Clear all images" button on the website, user may reach to an empty site and starts to upload images that his favors. For developing and testing purposes, a button named "Reset" can resotre the page to the very beginning stage, with sampled pictures shown.

By clicking "Upload a picture for sell" button, the user will be directed to a uploading page where he can choose the file he wants to put up for sale, where the images come locally from his device, and makes up the price and number of images that he wants to put up. For security reasons, the uploading files must end with one of .jpg, .png, .jpeg, or .gif. (Also any uppercase form of these extensions). Strict requirement to these files are necessary since I need to ensure that nothing vulnerable will be saved. Besides, for protecting purposes of database, I also put a security check on the file's name, using werkzeug.utils. The step is necessary since the file's name will be stoed into the database and retrived later as the product's name showned on the top page. 

The user can also try to purchase any images he want by clicking the "Purchase one" button next to the image on the main page (at the rightmost column). This step will
check the inventory whether there are enough image stock remains, and recorded the transaction (time when transaction happens, image name, price of image) in the transactions table of database. The process will also update the product's inventory in Databse appropriately. 

A small design for user is a navigation bar that shows how much the images that a customer has purchased on this website. The number is showed on the right side of the bar on top, counted in rounded dollars. 

## Test guides

For testing purposes, the "tests" directory contains some pictures that can be used to put up as test. Testers can try to upload these pictures one by one with different prices or multiple of them with same price. After uploading, testers can first verify the new rows that put up on the website, representing the new added images, ensuring them with correct price and quantity. For adding some past existed images, testers shall validate the new quantity/stock of them. After uploading, testers can try to purchase some of images (a combination of sample images from server or new added images) and see the total value of images.

Also, tester shall be aware of the exhibition of sample images of size 256x256 pixels. The resize function is strict and may cause partial of uploaded image does not show.

To start a blank test, tester shall click "Clear all" for initial environment setup. Remind that Reset will restore the sample images from the server.

## What's next for this repo

I could add features that requires login or access control. By allowing that, the website allows different users to surf the website at the same time. I can implement a personal wallet that represents that credit that a customer can use on the websire. The wallet can also be used to collect the money from other customers, as well as users may purchase some images from other people and re-sell again. We could implement such feature by a login form of HTML5 that would give the browser an access token, allowing the application to serve some administrative tools to users, such as viewing earnings or managing stock. Customers purchase images would prefer using the money from wallet to filling a lot of transaction information when using some common checkout methods, like visa card or paypal. Users only need to put money in the wallet at the very begining, then purchasing and selling images will be extremely easy by just clivking buttons. 

## Demo link

Youtube: https://youtu.be/8P_WeGQONUM
