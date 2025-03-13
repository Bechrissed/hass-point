# Changelog

## [1.2.1] - 2024-03-13

### Fixed
- Restored config flow functionality
- Added missing translations
- Added voluptuous dependency

## [1.2.0] - 2024-03-13

### Changed
- Switched to official Minut API v8 using OAuth2 authentication
- Removed web scraping in favor of direct API access
- Improved error handling and token management

### Added
- OAuth2 password grant authentication
- Direct API access for device data
- Better error messages and logging
- Automatic token refresh handling

### Fixed
- More reliable authentication process
- Improved device data retrieval
- Better handling of API responses

## [1.1.0] - 2024-03-12

### Changed
- Switched to HTTP request-based API communication
- Improved error handling and reconnection logic
- Added proper device class mappings for all sensors

### Added
- Binary sensors for device status:
  - Motion detection
  - Online status
  - Charging status
  - Mount status
- Proper state classes for all sensors
- Better error reporting during setup

### Fixed
- More reliable login process
- Better handling of device metrics
- Improved error handling for network issues

## [1.0.8] - 2024-03-11

### Changed
- Initial release with web scraping approach 