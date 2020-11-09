![superx](superx/static/img/superx.JPG)


## **Main Goal** 
**Comparing prices between supermarkets by using accessible data- to save money**

SuperX is an open-source platform for everyone and anyone that allows comparing prices of one's personal grocery carts between different supermarkets in Isreal. 

Thanks to a law passed in 2014, supermarkets must publish the price of all their goods, from every branch To allow for easy comparison between supermarkets.
This allows SuperX to retrieve the prices of all the products daily and update them so that the user will always be shown the most updated price!

So open Superx, create a user, build your own cart, save your cart for future use, update an existing cart, and continue on to compare the price between supermarkets in your area!

- To activate and use the app- please follow the instructions in [User's_Guide file](User's_Guide.md)

## Project Architecture
The project runs on Vagrant VM & uses flask as a web framework.
To create the project's environment- bootstrap.sh file is triggered when the app starts running.

### **Frontend** 
Client UI to choose the products to compare and the city where the client lives. <br>
<u>Languages</u>- HTML, CSS, JS

### **Backend**
Information extractor scripts that web scrape supermarket urls, extract the relevant information and places it into the db.<br>
<u>Language</u>- Python

### **Database** 
MySQL relational database, stored in the cloud.<br>
<u>ORM</u>- SQLAlchemy

![structure](superx/static/img/app_run_diagram.JPG)

- For a better understanding of the code structure & different files please visit [Architecture guide](Project_Architecture.md)

### Contribute :tada:
- At this point, we compare between 3 major supermarkets - Mega, Shufersal & Victory
- To help us compare more products and more supermarkets- please read [CONTRIBUTING file](CONTRIBUTING.md)

## Team
- Oded Hellman
- Yoav Ben Hur  
- Aryeh Klein
- Shai Brown


