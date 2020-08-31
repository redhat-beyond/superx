# SuperX
## Team members:
### 1. Oded Hellman
### 2. Yoav Ben Hur
### 3. Aryeh Klein
### 4. Tzachi Elrom
### 5. Shai Brown

________________________________

## Initial System Spesification:

**SuperX purpose:** prices comparison between supermarkets in Israel
  
#### User Story:
1. User logs in to the website and chooses his relevant grocery
2. The user enters "Prices Comparison" button
3. A get request is sent to the prices' table in the server
4. The user gets a list of supermarkets' prices around him, cheapest first
*There are details about the prices of each product
5. The user gets an option to order the grocery list directly from the wanted supermarket by clicking "order" button

*There's an option to show the supermarkets only in a certain radius from user's location

*Catching mistakes- there is more thinking to do about how to deal with products that are sold in one supermarket but not in another (maybe suggest similar products)

#### Front-End:

1. "Add product" Bar- with automatic completion of text based on our products DB
2. Detailed list of the products, grouped by 3 in a row, divided to categories

#### Back-End:

1. Python based script that sends request to the supermarkets server every defined period of time, and downloads the prices files from them.

2. Python based parser that reads the xml prices files and sends them to the relevant spot in the DB

#### Database:

1. Contains system's data- products prices by firm, branch & date
2. Saves users' copmared shopping carts' prices
*MySQL based

#### MVP:

Our first MVP is focused on technological POC:
1. Download xml files from supermarkets' servers script
2. Parser to read those xml files and allocate them to the right place on the DB
3. MySQL based DB to contain all the relevant data
4. Basic UI to represent the data to the user, Django/Flusk based
*For the MVP stage, we will focus on one branch of Shufersal firm

#### Value Proposition:

1. Money saving
2. Wise consumption
3. Online grocery shopping by click
4. Focus & shopping experience

Cheers to SuperX!
