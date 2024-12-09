# InventoryManager95

A modern inventory management system built with Django and Django REST Framework.

## Features

- Warehouse and Sub-warehouse Management
- Inventory Item Tracking
- Stock Level Monitoring
- User Authentication and Authorization
- RESTful API
- Admin Interface

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/InventoryManager95.git
cd InventoryManager95
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## API Documentation

The API documentation is available at `/api/docs/` when running the server.

## Roadmap 🗺️
Our development roadmap is organized into several key areas:

### Phase 1: Advanced Inventory Features
[x] Supplier & Vendor Management System
  - Supplier profiles and performance tracking
  - Automated purchase order generation
  - Lead time tracking and analytics
[x] Purchase Order Management
  - Order creation and tracking
  - Line item management
  - Order status workflow
[ ] Automated Reordering System
  - Configurable reorder points
  - Email/SMS notifications
  - Integration with supplier systems
[ ] Batch & Lot Tracking
  - Expiration date management
  - FIFO/LIFO support
  - Batch-level quality control

### Phase 2: Integration and Mobile Support
- [ ] Mobile Application
  - iOS and Android apps
  - Barcode scanning
  - Mobile inventory counts
- [ ] External System Integration
  - Accounting software integration
  - Shipping carrier integration
  - EDI support

### Phase 3: Advanced Analytics
- [ ] Predictive Analytics
  - Demand forecasting
  - Optimal stock level prediction
  - Seasonal trend analysis
- [ ] Business Intelligence
  - Custom dashboard creation
  - Real-time analytics
  - Advanced visualization

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## Security

For security issues, please read [SECURITY.md](SECURITY.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes.