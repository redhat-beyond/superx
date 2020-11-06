# Contirbuting to SuperX
:tada:Thank you for wanting to contribute and help people save money!:tada:

Before contributing to SuperX, first create an issue or search previous issues to see if it has already been raised. 
Explain clearly what you intend on contributing and an owner will review nd comment on the issue

### Contents:
[Before you get started](#Before-you-get-started)
  * [Git Flow](#Git-flow)
  * [Issues](#issues)
  * [Coding guidlines](#Coding-guidlines)

[How to contibute](#How-to-contibute)
  * [Adding a super market](#Adding-a-super-market) 
  * [Information extractors](#Information-extractors)

## Before you get started
### Git flow
#### We here at Superx use [Git Flow](https://guides.github.com/introduction/flow/index.html), all changes to the code are through pull requests

1. Fork the repo and create a new branch from branch from `master`.
2. All code that requires testing should be added with tests!
3. Ensure the tests pass.
4. Make sure to write a meaningfull PR and commit message, and comment on the code where needed
5. Issue that pull request!
6. A developer will review it and accept it when all comments have been resolved.

### Issues:
* Always search issues to find if it has already been raised.
* Explain clearly the behaviour of your suggested change, or bug that you have found.
* When reporting a bug, try to include a description of the source of the bug, and if possible a pr with a failing test case

### Coding guidlines
**All code submitted for review must be:**
* Tested - All code submitted must be tested by the coder, and if need be submitted with tests.
* Clean and well written - Code submitted must have comments where neccesary and must be **Readable**.
* All python code should conform to the [PEP8](https://www.python.org/dev/peps/pep-0008/) standard
* Third party code **must** adhere to the Superx licensing.

**Any code that violates these guidlines will not be accepted.**

## How to contibute
### Adding a super market

One of the main contributions to superx is adding a new supermarket to the system so that consumers can see its prices as well.
All supermarkets are required to upload xml files containing all product and branch information to be viewed publicly.
This information can be found [Here](https://www.consumers.org.il/item/transparency_price).

Adding a supermarket involves a number of actions.
1. The supermarket must be added properly to the information extractor script
2. A new column must be added to the front end of the SuperX website.

#### Adding a new column 

> **Note**: currently this part is hard coded into the code. 
We are working to make this a general so that when a supermarket is added to the extractors this will update the columns automatically. 

In order to add a new column you must alter a number of the html templates found under Superx --> templates

Routes.home.py will be able to detect the new super market after following the steps of adding to the information extractors.


 
#### Information extractors
The SuperX project uses 2 scripts for extracting the wanted information from the supermarkets.
* branch_info_extractor - is incharge of getting all the branch data from each chain
* item_info_extractor - is incharge of getting all the product data and price-per-branch from each supermarket.

In [app.py](https://github.com/beyond-io/superx/blob/master/superx/app.py) a dictionary containing all the information needed to add a new supermarket is kept.

To add a new supermarekt all that is needed it to add a new entry into the dictionary with all the relevant values.

> **Note** after adding an entry to the dictionary you still need to run the extractors and check they work!

* **The main keys of the dictionary are the supermarkets names**
* **url**: string - Is the url leading to the chins website that holds all the relevant zip files.
* **multiple_pages**: Boolean - Does the website have multiple pages?  
* **zip_link_prefix**: string- On some websites, the zipfile links are not complete and so a prefix is needed
* **item_attr_name**: string - the attribute name for the items xml file. This varies from supermaket to supermarket.
* **price_full**: string - The variation of 'PriceFull' that the chain uses in the zip file names
* **is_weighted_attr_name**: string - The variation of 'bIsWeighted' that the xml file uses
* **item_date_format**: string - the format of the date in the xml files. see [here](https://docs.python.org/3/library/datetime.html) for more information
* **branch_url**: string - The url of the single branch information document or a path to download the zingle branch zip file (depends on the supermarket)
* **needs_web_scraping**: Boolean- Does the **branch url** need web scraping to get the zip link or not
* **need_zip_prefix**: Boolean - Does the branch zip file need to a prefix
* **encoding**: string - The endocind of the branch xml files.
* **link_attrs_name**: string - For branch files that need webscraping. Usual value is 'Stores' or 'StoresFull' 
* **attr_path**: string - The path inside the xml file to the wanted child ode (branch information extractor)
* **chain_id**: int - the id of the chain
* **attrs**: a nested dictionary containg the unique attribute names of store, store id, store name, address, city, sub chain id. This varies from supermarket to supermarket

