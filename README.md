# Room Rental API

## Overview
Room Rental API is a RESTful API designed for a room rental platform. It facilitates the interaction between landlords and customers by providing endpoints for managing room listings, inquiries, and user authentication.

## Tech Stack

**Server:** Django, Django Rest Framework

**Authentication:** JSON Web Tokens (JWT)

**Database:** SQLite

## Features

- **JWT Authentication:** Secure authentication mechanism using JSON Web Tokens to ensure authorized access to API endpoints.
- **Landlord and Customer Functionality:** Users can register as landlords to manage room listings or as customers to browse and inquire about available rooms.
- **Email Notifications:** Integration of email functionality to notify landlords upon receiving inquiries from potential customers, facilitating communication.
- **Search Functionality:** Enables users to search for room listings based on title and apply filters to find rooms that match their preferences.
- **Scalable Architecture:** Built using Django and DRF, ensuring a robust and scalable architecture suitable for handling large-scale applications.

## Getting Started

1. **Clone the repository:**
```bash
git clone https://github.com/anishbista/Room-Rental-API.git
```
## Installation

1. **Navigate to the project directory**

```bash
cd rental_management
```
2. **Create a virtual environment**
```bash
python -m venv myenv
source myenv/bin/activate 
```
3. **Install required packages**
```bash
pip install -r requirements.txt
```
4. **Set up environment variables for email configuration**
```bash
cd rental_management
Create .env including following:

EMAIL_USER=your_email@example.com
EMAIL_PASS=your_email_password
EMAIL_FROM=your_email@example.com
```
5. **Apply migrations**
```bash
python manage.py migrate
```
6. **Create SuperUser**
```bash
python manage.py createsuperuser
```
7. **Run the development server**
```bash
python manage.py runserver
```
## **Access the API documentation** 
Visit `http://127.0.0.1:8000/api/schema/swagger-ui/` for all the endpoints.


## Support

For any inquiries or support, email anishbista9236@gmail.com 






    