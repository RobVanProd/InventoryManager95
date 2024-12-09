# Changelog

All notable changes to InventoryManager95 will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Automated Reordering System
  - ReorderPoint model for configuring reorder rules
  - StockAlert model for tracking low stock and stockouts
  - Automated purchase order generation
  - Stock level monitoring and alerts
  - Celery integration for periodic stock checks
  - API endpoints for managing reorder points and alerts
  - Admin interface integration
- Supplier Management System
  - Added Supplier model with performance metrics tracking
  - Added SupplierContact model for managing multiple contacts
- Purchase Order Management System
  - Added PurchaseOrder model for managing orders
  - Added PurchaseOrderItem model for line items
- Enhanced Inventory Management
  - Added unit price tracking to InventoryItem
  - Added active status tracking across models
  - Added default values for numerical fields
  - Made location fields optional with defaults
- Supplier Management System
  - Supplier model with performance metrics
  - Additional contacts management
  - Supplier code validation
- Purchase Order System
  - PO creation and management
  - Line item tracking
  - Delivery status monitoring
  - Automatic supplier performance updates
  - Currency and cost tracking
- Automated Reordering System
  - Added ReorderPoint model for configuring reorder rules
  - Added StockAlert model for tracking low stock and stockouts
  - Implemented automatic purchase order generation
  - Added seasonal adjustment factors for reorder quantities
  - Added safety stock management
- Enhanced Admin Interface
  - Added admin views for ReorderPoint and StockAlert models
  - Added fieldsets for better organization
  - Added readonly fields for system-managed values
- New API Endpoints
  - Added endpoints for managing reorder points
  - Added endpoints for managing stock alerts
  - Added manual reorder check functionality
  - Added alert resolution endpoints

### Changed
- Reorganized models into separate files for better maintainability
- Updated database schema with proper defaults and null constraints
- Improved model relationships and foreign key constraints

### Planned Features
- Advanced reporting and analytics
- Mobile application support
- Barcode scanning integration
- E-commerce platform integrations
- Enhanced user roles and permissions
- Automated inventory forecasting
- Email notifications system

### In Development
- Performance optimizations
- Additional test coverage
- Enhanced error handling
- Improved user interface
- Extended API documentation

## [1.0.0] - 2024-12-09

### Added
- Initial release of InventoryManager95
- Core inventory management functionality
- Dashboard with real-time statistics
- Multi-warehouse support
- User authentication and authorization
- RESTful API endpoints
- Modern React-based frontend
- Comprehensive documentation

### Dashboard Features
- Total items counter
- Total warehouses display
- Low stock items tracking
- Recent items list
- Total inventory value calculation
- Items by warehouse breakdown

### API Endpoints
- `/api/dashboard/stats/` for dashboard statistics
- `/api/items/` for inventory management
- `/api/warehouses/` for warehouse operations
- `/api/auth/` for user authentication

### Security
- JWT authentication implementation
- Input validation and sanitization
- CORS configuration
- Error handling and logging

### Documentation
- Comprehensive README
- API documentation
- Contributing guidelines
- Security policy
- Code of conduct
