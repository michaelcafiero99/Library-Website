"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from .models import Customers
from .models import Items
from .models import RentedBooks
from .models import Employees
from .models import Rooms
from django.db import connection

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Library MS',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About the project',
            'message':'',
            'year':datetime.now().year,
        }
    )

def myRent(request):
    """Renders the myRent page. (shows items the customer has rented.)"""
    assert isinstance(request, HttpRequest)

    # Get the current customer Id from the session.
    customers = Customers.objects.raw('SELECT * FROM app_customers WHERE userName = %s', [request.session['username']])
    userId = -1
    for customer in customers:
        userId = int(customer.id)

    # Get the Items rented by the current customer.
    rentedItems = RentedBooks.objects.raw('SELECT * FROM app_rentedbooks WHERE renterId_id=%s', [userId])
    rentedItemNames = []
    for item in rentedItems:
        currItem = Items.objects.raw('SELECT * FROM app_items WHERE id=%s', [item.itemId_id])
        for newItem in currItem:
            rentedItemNames.append(newItem.itemName)

    # render the page that displays the items the customer has rented.
    return render(
        request,
        'app/myRent.html',
        {
            'title':'library',
            'user':request.session['username'],
            'message':'Library MS HomePage',
            'rentedItems':rentedItemNames,
            'year':datetime.now().year,
        }
    )

def returns(request):
    """Function to return a book"""
    assert isinstance(request, HttpRequest)

    # check if the form returned a post. (the form to return a book)
    if request.method == 'POST':
        query = request.POST['returnedItem']

        # get the current customer Id.
        customers = Customers.objects.raw('SELECT * FROM app_customers WHERE userName = %s', [request.session['username']])
        userId = -1
        for customer in customers:
            userId = int(customer.id)

        # Get the id of the item to return from the name of the item from the post.
        returnedItems = Items.objects.raw('SELECT * FROM app_items WHERE itemName=%s', [query])
        itemId = -1
        for returnedItem in returnedItems:
            itemId = returnedItem.id

        # add one to items left in the database.
        # remove the item from the rentedBooks table.
        with connection.cursor() as cursor:
            cursor.execute("UPDATE app_items SET itemsLeft = itemsLeft + 1 WHERE id=%s", [itemId])
            cursor.execute("DELETE FROM app_rentedbooks WHERE itemId_id=%s AND renterId_id=%s", [itemId, userId])
    return myRent(request)

def rent(request, rented):
    """Renders the library page."""
    assert isinstance(request, HttpRequest)
    customers = Customers.objects.raw('SELECT * FROM app_customers WHERE userName = %s', [request.session['username']])
    userId = -1
    for customer in customers:
        userId = int(customer.id)

    # check if the current user has already rented the same book out
    sameRental = RentedBooks.objects.raw('SELECT * FROM app_rentedbooks WHERE renterId_id = %s AND itemId_id = %s', [userId, rented])
    flag = True
    for i in sameRental:
        flag = False

    # check if the user has rented 5 items.
    userRentals = RentedBooks.objects.raw('SELECT * FROM app_rentedbooks WHERE renterId_id = %s', [userId])
    rentalCount = 0
    for i in userRentals:
        rentalCount += 1

    # if user has rented 5 items, then redirect to library page without renting a new one.
    if rentalCount == 5:
        return library(request, request.session['username'])

    if flag:
        with connection.cursor() as cursor:
            # rent the book.(add one to rental count, subtract one from items left and add the record to rentedBooks)
            cursor.execute("UPDATE app_items SET itemsLeft = itemsLeft - 1 WHERE id=%s", [rented])
            cursor.execute("UPDATE app_items SET rentedCount = rentedCount + 1 WHERE id=%s", [rented])
            cursor.execute("INSERT INTO app_rentedbooks (itemId_id, renterId_id) VALUE (%s,%s)", [int(rented), int(userId)])

    return library(request, request.session['username'])

def library(request, user):
    """Renders the library page."""
    assert isinstance(request, HttpRequest)
    mostRented = Items.objects.raw('SELECT * FROM app_items ORDER BY rentedCount DESC')

    # Get the top three most rented items as a list.
    top3 = []
    for i in range(3):
        top3.append(mostRented[i])
    print(top3)

    # render the library with the top 3 items.
    return render(
        request,
        'app/library.html',
        {
            'title':'library',
            'message':'Library MS HomePage',
            'user':user,
            'mostRented':top3,
            'year':datetime.now().year,
        }
    )

def libraryStr(request, user):
    # an intermediate function to call the library function.
    return library(request, user)

def showSearch(request):
    """Renders the search page."""
    assert isinstance(request, HttpRequest)

    # check if the search bar form has been filled.
    if request.method == 'POST':
        query = request.POST['search']

        # get all the items with the matching item names.
        items = Items.objects.raw('SELECT * FROM app_items WHERE itemName = %s', [query])
        itemList = {}
        for item in items:
            itemList[item.itemName] = item.id

        # render the show Items with the search results.
        return render(
            request,
            'app/showSearch.html',
            {
                'title':'library',
                'message':'Library MS HomePage',
                'user':request.session['username'],
                'query':query,
                'itemList':items,
                'year':datetime.now().year,
            }
        )

    # If the form was not submitted, then render the search page again.
    else:
        return render(
            request,
            'app/showSearch.html',
            {
                'title':'library',
                'message':'Library MS HomePage',
                'year':datetime.now().year,
            }
        )
def rooms(request):
    assert isinstance(request, HttpRequest)

    customers = Customers.objects.raw('SELECT * FROM app_customers WHERE userName = %s', [request.session['username']])
    userId = -1
    for customer in customers:
        userId = int(customer.id)

    currRoomRaw = Rooms.objects.raw('SELECT * FROM app_rooms WHERE renterId_id =%s', [userId] )
    # Get the Items rented by the current customer.

    currRoom = -1
    for room in currRoomRaw:
        currRoom = room.id
    
    rooms = Rooms.objects.raw('SELECT * FROM app_rooms WHERE renterId_id = 7')

    roomsList = []
    for room in rooms:
        roomsList.append(room)
        
    return render(
        request,
        'app/rooms.html',
        {
            'title':'rooms',
            'user':request.session['username'],
            'message':'Library MS HomePage',
            'rooms':roomsList,
            'currRoom': currRoom,
            'year':datetime.now().year,
        }
    )

def leaveRoom(request):
    assert isinstance(request, HttpRequest)
    print("in leave room")
    customers = Customers.objects.raw('SELECT * FROM app_customers WHERE userName = %s', [request.session['username']])
    userId = -1
    for customer in customers:
        userId = int(customer.id)
    print("user is: ", userId)
    currRoomRaw = Rooms.objects.raw('SELECT * FROM app_rooms WHERE renterId_id =%s', [userId] )
    # Get the Items rented by the current customer.

    currRoom = -1
    for room in currRoomRaw:
        currRoom = room.id
    print("current room is: ", currRoom)

    if 'leaveRoom' in request.POST:
        function = request.POST['leaveRoom']
        print("setting function to: ", function)
        if function == "Leave" or function == "leave":
            print("function is correct")
            
            with connection.cursor() as cursor:
                print("updating SQL")
                cursor.execute("UPDATE app_rooms SET currState = 'free' WHERE id=%s", [currRoom])
                cursor.execute("UPDATE app_rooms SET renterId_id = 7 WHERE id=%s", [currRoom])
                currRoom = -1

    return rooms(request)

def joinRoom(request):
    assert isinstance(request, HttpRequest)

    customers = Customers.objects.raw('SELECT * FROM app_customers WHERE userName = %s', [request.session['username']])
    userId = -1
    for customer in customers:
        userId = int(customer.id)

    currRoomRaw = Rooms.objects.raw('SELECT * FROM app_rooms WHERE renterId_id =%s', [userId] )
    # Get the Items rented by the current customer.

    currRoom = -1
    for room in currRoomRaw:
        currRoom = room.id

    #return rooms(request)

    if 'joinRoom' in request.POST:
        roomId = request.POST['joinRoom']
        #check if user already in a room
        if currRoom == -1:
            #check if room is really available
            currRoomRaw = Rooms.objects.raw('SELECT * FROM app_rooms WHERE id = %s', [roomId])[0]
            currState = currRoomRaw.currState
            if currState == "free":
                with connection.cursor() as cursor:
                    currRoom = roomId
                    cursor.execute("UPDATE app_rooms SET renterId_id =%s  WHERE id=%s", [userId, roomId])
                    cursor.execute("UPDATE app_rooms SET currState = 'rented' WHERE id=%s", [roomId])
    return rooms(request)


    #display all the rooms
    #display current room
    #leave button
def login(request):
    """Renders the login page."""
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        # get the username and password from the form.
        username = request.POST['username']
        password = request.POST['password']
        # get customer with the same credentials.
        customers = Customers.objects.raw('SELECT * FROM app_customers WHERE userName = %s AND password = %s', [username, password])
        for customer in customers:
            if customer.userName == username and customer.password == password:
                request.session['username'] = username
                
                # render the library page.
                return library(request, username)
            else:
                return render(
                    request,
                    'app/login.html',
                    {
                        'title':'login',
                        'message':'This is the new log in page of the library MS',
                        'year':datetime.now().year,
                    }
                )

        return render(
            request,
            'app/login.html',
            {
                'title':'login',
                'message':'This is the new log in page of the library MS',
                'year':datetime.now().year,
            }
        )
    else:
        return render(
            request,
            'app/login.html',
            {
                'title':'login',
                'message':'This is the new log in page of the library MS',
                'year':datetime.now().year,
            }
        )

def employeeLogin(request):
    """Renders the login page."""
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        # get the username and password from the form.
        username = request.POST['username']
        password = request.POST['password']
        # get customer with the same credentials.
        employees = Employees.objects.raw('SELECT * FROM app_employees WHERE userName = %s AND password = %s', [username, password])
        for employee in employees:
            if employee.userName == username and employee.password == password:
                request.session['username'] = username
                print("----------------------------------------------------")
                # render the library page.
                return addBook(request)
                #return render(request, 'app/employee.html')
           
            else:
                print("else1")
                return render(
                    request,
                    'app/employeeLogin.html',
                    {
                        'title':'login',
                        'message':'This is the new log in page of the library MS',
                        'year':datetime.now().year,
                    }
                )

        return render(
            request,
            'app/employeeLogin.html',
            {
                'title':'login',
                'message':'This is the new employee log in page of the library MS',
                'year':datetime.now().year,
            }
        )
    else:
        print("else2")
        return render(
            request,
            'app/employeeLogin.html',
            {
                'title':'login',
                'message':'This is the new employee log in page of the library MS',
                'year':datetime.now().year,
            }
        )

def addBook(request):
    """Adds a book to the database"""
    assert isinstance(request, HttpRequest) 
    print("here")
    if request.method == 'POST':
        print("+++++++++++++++++++++++++++++", request)
        name = request.POST['name']
        author = request.POST['author']
        type = request.POST['type']
        count = request.POST['count']
        rentedCount = 0
        print(name)
        #if book already exists, add count to it
        #if not, add new entry to the database
        if(name != ""):
            identicalItem = Items.objects.raw('SELECT id, itemName FROM app_items WHERE itemName = %s', [name])
            print("3")
            if len(identicalItem) != 0:
                print("item already exists")
                return render(
                request,
                'app/addBook.html',
                {
                    'title':'add books',
                    'message':'Add books to the library here',
                    'year':datetime.now().year,
                })
            else:
                # insert user into the database as a new user.
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO app_items (itemType, itemName, author, itemsLeft, rentedCount) VALUE (%s,%s,%s,%s,%s)", [type, name, author, count, rentedCount])
                return render(
                    request,
                    'app/addBook.html',
                    {
                    'title':'add books',
                    'message':'Add books to the library here',
                    'year':datetime.now().year,
                        })
                # set the session. and log into the library.
            #return addBook(request)
        
        else: 
            print("1")
            return render(
                request,
                'app/addBook.html',
                    {
                    'title':'add books',
                    'message':'Add books to the library here',
                    'year':datetime.now().year,
                        })
    
    else: 
        print("2")
        return render(
            request,
            'app/addBook.html',
                {
                'title':'add books',
                'message':'Add books to the library here',
                'year':datetime.now().year,
                    })
    
def signup(request):
    """Renders the signup page."""
    assert isinstance(request, HttpRequest)

    # get the username and password from the form.
    if request.method == 'POST':
        userName = request.POST['username']
        password = request.POST['password']
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        email = request.POST['email']

        # get customer with the same credentials.
        authenticated = Customers.objects.raw('SELECT id, userName FROM app_customers WHERE userName = %s', [userName])
        
        # if there was another record with the same credentials, then render the signup page again.
        if len(authenticated) != 0:
            print("user already exists")
            return render(
            request,
            'app/signup.html',
            {
                'title':'signUp',
                'message':'This is the new signup page of the library MS',
                'year':datetime.now().year,
            }
        )
        else:
            # insert user into the database as a new user.
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO app_customers (userName, password, firstName, lastName, emailAddress) VALUE (%s,%s,%s,%s,%s)", [userName, password, firstName, lastName, email])

            # set the session. and log into the library.
            request.session['username'] = userName
            return library(request, userName)

    else:
        return render(
            request,
            'app/signup.html',
            {
                'title':'signUp',
                'message':'Please sign up: ',
                'year':datetime.now().year,
            }
        )