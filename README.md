# Tone Deaf Newcastle

As a developer, I've been tasked with creating a program to aid in the running of the box office for a brand new music venue in Newcastle.

This project is written in Python with data stored on a Google worksheet.

[Here is the live version of this project]()

# Screenshots

---

## Project Goals

The main goals of this project are:
- To read and input to a data model, (created via pages in a Google Worksheet), which stores the essential information about each event, ie event name, capacity, sales, and availability across three worksheets.
- Provide the user the ability to sell tickets for an event, should they be available, with those sales being updated on the Google worksheet.
- Provide the user the tools to create a brand new event and set a total capacity, which can then be sold and updated with the rest of the program.
- Provide the user the tools to create an up-to-date 'sales report', providing total capacity, sales, and availability for each event.

## Project values

With these four pillars, the user could run a functioning box office, and the program is flexible enough to be developed and added to in the long term to fill any future needs of the business.

Because the program automates the selling of a ticket and the updating of records, it eliminates any room for human error that may occur. The last thing a music venue wants is to have a larger audience than they can host, running overcapacity. Because the availability for an event is based on the total entered capacity on event creation, minus any processed sales, the figure will always be correct, with validation included stopping the availability of an event from dropping below zero.

Though the venue may have a total set capacity, this may change from event to event, due to factors such as merchandise being sold in the venue, extra bar sale points, or even just for public safety. The created event may even be happening outside the venue at a separate location. The program was made to be able to set any capacity with this in mind.

The creation of a new event is quick and easy, only requiring a title and capacity to be created. This is useful for those new events just announced or even for a last-minute request for a VIP section!

To ease in the running of the events and also in the marketing and sales of the venue, it was a requirement that the program could create an up-to-date and instantly readable sales report.

---

## Features

### Existing Features

#### Welcome screen
- (command_required function). The Welcome page identifies the venue name 'Tone Deaf Newcastle' and offers a welcome to the user. The user is then presented with a list of tasks that the program can perform, and they're then prompted to enter a specific task number from the aforementioned list. I decided to use task numbers rather than task names to reduce the required input from the user, making the whole program more user-friendly and quicker overall to use. Visually all print lines are spaced apart or on separate lines for increased readability.
- (invalid_task function). As with any user input, there are likely to be mistakes / incorrect entries. Should an invalid task number be entered, an error is raised and printed to the user, asking them to enter a number between 1 and 4, displaying the value that they entered. This has been included to provide a better user experience and also to provide guiding feedback to the user.

#### Sell Event
- (sell_event function). The ability to sell tickets for an event is obviously crucial to a project like this. The user is first given confirmation of what task they're performing, in this case, 'Sell Existing Event'. They are also shown a list of all existing events stored on the sales page of the worksheet, this performs a similar role to the welcome screen, displaying all available options to the user. As the event data is pulled from the worksheet directly, it is always updated should an extra event be created, as detailed later in the features section.
- The user is then required to input the name of the event they're wanting to sell for and also told if they want to exit the sell task, enter n which will take them back to the welcome screen. The input is then validated by checking the created list of events that was printed earlier, against the user input. If there isn't a match, an error is raised and printed to the user, again pointing them in the right direction.
- Once an existing event has been selected, the user is then prompted to input how many tickets they'd like to purchase.
- (validate_tickets function). The input registering how many tickets are due to be sold is then passed through validation making sure that it is below 9. This ticket limit of eight is an industry-standard.
- Once this validation is complete, the entered ticket number is then checked against the number of tickets left available, data that is stored in the 'availability' page of the worksheet. If availability would drop below zero an error is raised and printed to the user explaining that there aren't enough tickets available to complete the order, and also showing them how many tickets are left. If the availability is greater to or equal to the entered number, the new sales data is entered into the 'sales' page of the worksheet, and the 'availability' page is also updated to reflect the sale. The user is given confirmation of the order's success, with a summary of the order printed back to them, along with how many tickets are left available, information that could prove useful at a glance should there be a rush for that event.

#### Create Event
- (create_event function). Along with hitting another key project goal, creating an event to sell and audit is a necessary task for any box office program. In this program it is achieved by having the user input an event name, updating that event name into the worksheet's pages, and then taking an event capacity from the user which is then also input into the worksheet 'capacity' and 'availability' pages. The created event is then put into a dictionary which is printed back to the user, offering a confirmation that the event has been created and is ready to be sold.

#### Sales Report
- (sales_report function). This feature of the program is all about taking the data present in the data model and then printing it back to the user in as readable a format as possible. This was achieved through the use of nested dictionaries. The outer dictionaries were created first containing event names with nested dictionaries created to store capacity, sales, and availability specific to each event.

### Future Features
- The created program handles sales and events on an attendance level. However it does not cover the financial side of a box office, so this would currently have to be done separately. This could however be included in a future release of the program, expanding the data model and the functions of the existing project. The inclusion of finances would branch out into many different areas.
    - An extra layer would have to be added to the data model to store ticket prices and then total sales which could be achieved by multiplying sales data with ticket price.
    - This data would then need to be accessed via each of the key present features, sell event, create event and sales report. 
    - To make sure the daily takings were correct, the program could create a daily 'session' when first run, which could then be input into the data model and printed back to the user as a separate form.

--- 

## Data Model

![https://i.imgur.com/ifA5L0f](https://i.imgur.com/ifA5L0f.jpg "Data Model")

My chosen data model is created through three pages of a Google worksheet. As displayed in the image above, the tying link between the three pages is the event name. It is through the event name, working as the identifying link, that the changeable data, capacity, sales, and availability are read and written to. To be able to access this data, I'm using the [gspread](https://docs.gspread.org/en/latest/) Python library.

---

## Testing

Flow chart created to map out project's logic:

![https://i.imgur.com/lCpZ6u4](https://i.imgur.com/lCpZ6u4.jpg "Logic flow chart") 

To avoid the user having to restart the program in the case of an incorrect entry I implemented while loops into the functions that required an input from the user. I also included 'return True' in both separate input checking functions, validate_tickets, and invalid_task. This increases the program's usability and user experience. In a similar vein, I included ValueErrors to help guide the user with a printed description of what the issue was and how to correct the error. I had to expand on errors created for the inputs that were required to be integers. The original errors only functioned if the input was an integer, rather than a string or a float so I added more generic ValueErrors where appropriate. This issue was discovered through manual testing to ensure the program did not throw back an unreadable error for the user, or close the program where it wouldn't be expected to.

Adding these loops to accommodate the errors cause some areas of the code to become quite long and heavily indented, causing issues with overall line length. This wasn't an issue I'd dealt with before but I found some useful documentation [here](https://www.python.org/dev/peps/pep-0008/#indentation) which explained the process.

This manual testing also highlighted the need for an 'escape' from a selected task, so I added a simple 'enter n to exit' line in the first input sections of sell_ticket and create_event, along with an if statement to match, should the user have selected the wrong task by accident.

Making sure all printed information was displayed in a readable format was very important, particularly in the sales report. The best manner I found to format the data was to 
create a dictionary with a key for each event, then create a nested dictionary with the keys of Capacity, Sales, and Availability. I then input the data taken from the for loop of variables as values for the nested dictionary and then printed with indentation and a structure detailed [here.](https://thispointer.com/python-4-ways-to-print-items-of-a-dictionary-line-by-line/)

### PEP8 Validator and Pylint

Throughout the project, all python code has been checked by linter Pylint within Gitpod and also run through PEP8's online checker to ensure there are no errors or warnings to be amended.

[PEP8](http://pep8online.com/)
[Pylint](https://pylint.org/)

---

## Deployment procedure



---

## Credits

Initial project creation, deployment, importing of libraries and code structure was built from the [Code Institute Love Sandwiches walkthrough project.](https://github.com/CMecrow/love-sandwiches)
Information on how to split longer lines of code was taken from [here.](https://www.python.org/dev/peps/pep-0008/#indentation)
Printing dictionaries in a readable form was found [here.](https://thispointer.com/python-4-ways-to-print-items-of-a-dictionary-line-by-line/)