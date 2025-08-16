# ALX Travel App API

A comprehensive Django REST API for a travel booking platform that allows users to manage property listings and bookings. This project demonstrates modern backend development practices using Django REST Framework with complete API documentation via Swagger.

## 🚀 Features

### Core Functionality
- **Property Listings Management**: Create, read, update, and delete travel property listings
- **Booking System**: Complete booking management with date validation
- **User Management**: Integration with Django's built-in user authentication system
- **Review System**: User reviews and ratings for properties (model implemented)
- **Payment Integration**: Secure payment workflow using Chapa API for bookings

### API Features
- **RESTful API Design**: Clean, intuitive API endpoints following REST conventions
- **Full CRUD Operations**: Complete Create, Read, Update, Delete functionality for all resources
- **Interactive API Documentation**: Swagger UI and ReDoc integration for easy API exploration
- **JSON Responses**: All endpoints return properly formatted JSON data
- **CORS Support**: Configured for frontend integration
- **Chapa Payment Endpoints**: Endpoints to initiate and verify payments, and track payment status

## 🛠️ Technology Stack

- **Backend Framework**: Django 5.2.4
- **API Framework**: Django REST Framework
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Documentation**: drf-yasg (Swagger/OpenAPI)
- **Environment Management**: django-environ
- **CORS**: django-cors-headers
- **Python Version**: 3.12+

## 📋 API Endpoints

### Listings
- `GET /api/listings/` - List all property listings
- `POST /api/listings/` - Create a new listing
- `GET /api/listings/{id}/` - Retrieve a specific listing
- `PUT /api/listings/{id}/` - Update a listing (full update)
- `PATCH /api/listings/{id}/` - Partially update a listing
- `DELETE /api/listings/{id}/` - Delete a listing

### Bookings
- `GET /api/bookings/` - List all bookings
- `POST /api/bookings/` - Create a new booking
- `GET /api/bookings/{id}/` - Retrieve a specific booking
- `PUT /api/bookings/{id}/` - Update a booking (full update)
- `PATCH /api/bookings/{id}/` - Partially update a booking
- `DELETE /api/bookings/{id}/` - Delete a booking

### Payments
- `POST /api/payments/initiate/` - Initiate a payment for a booking (returns Chapa checkout link)
- `POST /api/payments/verify/` - Verify payment status with Chapa and update booking/payment status

### Documentation
- `GET /swagger/` - Interactive Swagger API documentation
- `GET /redoc/` - ReDoc API documentation

## 🗄️ Database Models

### Listing Model
```python
- title: CharField(max_length=255)
- description: TextField
- price: DecimalField(max_digits=10, decimal_places=2)
- owner: ForeignKey(User)
```

### Booking Model
```python
- listing: ForeignKey(Listing)
- guest: ForeignKey(User)
- check_in_date: DateField
- check_out_date: DateField
```


### Payment Model
```python
- booking: OneToOneField(Booking)
- amount: DecimalField
- status: CharField (pending, completed, failed, cancelled)
- transaction_id: CharField
- created_at: DateTimeField
- updated_at: DateTimeField
```

### Review Model
```python
- listing: ForeignKey(Listing)
- guest: ForeignKey(User)
- rating: IntegerField
- comment: TextField
```
## 💳 Payment Workflow

1. **Booking Creation**: When a user creates a booking, the API automatically initiates a payment with Chapa and returns a checkout URL.
2. **User Payment**: The user is redirected to Chapa to complete the payment securely.
3. **Payment Verification**: After payment, the API verifies the transaction with Chapa and updates the payment status ("completed" or "failed").
4. **Email Confirmation**: On successful payment, a confirmation email is sent to the user (using Celery for background tasks).
5. **Error Handling**: Any payment errors or failures are handled gracefully, and the payment status is updated accordingly.

**Note:** You must set your Chapa secret key in your environment variables as `CHAPA_SECRET`.

## 🚀 Quick Start

### Prerequisites
- Python 3.12 or higher
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd alx_travel_app
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r alx_travel_app/requirement.txt
   ```

4. **Environment Setup**
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   DATABASE_URL=sqlite:///db.sqlite3
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Database Setup**
   ```bash
   python manage.py migrate
   python manage.py seed  # Load sample data
   ```

6. **Create Superuser (Optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

   The API will be available at: `http://127.0.0.1:8000/api/`

## 📚 API Documentation

Once the server is running, you can explore the API documentation:

- **Swagger UI**: http://127.0.0.1:8000/swagger/
- **ReDoc**: http://127.0.0.1:8000/redoc/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## 🧪 Testing the API

### Using cURL

**Get all listings:**
```bash
curl -X GET http://127.0.0.1:8000/api/listings/
```

**Create a new booking:**
```bash
curl -X POST http://127.0.0.1:8000/api/bookings/ \
  -H "Content-Type: application/json" \
  -d '{
    "listing": 1,
    "guest": 1,
    "check_in_date": "2025-08-10",
    "check_out_date": "2025-08-15"
  }'
```

### Using Python Requests
```python
import requests

# Get all listings
response = requests.get('http://127.0.0.1:8000/api/listings/')
listings = response.json()

# Create a booking
booking_data = {
    'listing': 1,
    'guest': 1,
    'check_in_date': '2025-08-10',
    'check_out_date': '2025-08-15'
}
response = requests.post('http://127.0.0.1:8000/api/bookings/', json=booking_data)
booking = response.json()
```

## 🏗️ Project Structure

```
alx_travel_app/
├── alx_travel_app/          # Django project settings
│   ├── __init__.py
│   ├── settings.py          # Project configuration
│   ├── urls.py             # Main URL routing
│   ├── wsgi.py
│   └── asgi.py
├── listings/                # Main app
│   ├── models.py           # Database models
│   ├── views.py            # API ViewSets
│   ├── serializers.py      # Data serializers
│   ├── urls.py             # App URL routing
│   ├── admin.py            # Django admin config
│   ├── management/         # Custom commands
│   │   └── commands/
│   │       └── seed.py     # Database seeding
│   └── migrations/         # Database migrations
├── db.sqlite3              # SQLite database
├── manage.py               # Django management script
└── README.md              # Project documentation
```

## 🔧 Development Features

### Management Commands
- `python manage.py seed` - Populate database with sample data
- `python manage.py migrate` - Apply database migrations
- `python manage.py runserver` - Start development server

### API Documentation Features
- Auto-generated Swagger documentation
- Interactive API testing interface
- Detailed request/response schemas
- Authentication integration ready

## 🌐 Frontend Integration

The API is CORS-enabled and ready for frontend integration. Supported origins can be configured in `settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",    # React default
    "http://127.0.0.1:3000",
    "http://your-frontend-domain.com",
]
```

## 📦 Dependencies

Key packages used in this project:
- `Django>=5.2.4` - Web framework
- `djangorestframework` - REST API framework
- `drf-yasg` - Swagger/OpenAPI documentation
- `django-cors-headers` - CORS handling
- `django-environ` - Environment variable management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is part of the ALX Backend Development curriculum.


## 🔮 Future Enhancements

- [ ] User authentication and authorization
- [ ] Payment refund support
- [ ] Image upload for listings
- [ ] Search and filtering capabilities
- [ ] Email notifications
- [ ] Rate limiting
- [ ] Caching implementation
- [ ] Docker containerization
- [ ] Production deployment configuration

---

**Built with ❤️ as part of the ALX Backend Development Program**
