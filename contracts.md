# Cyber Airways Application Contracts

## API Contracts

### Flight Readiness Check Endpoint
- **Route**: `POST /api/flight-readiness`
- **Request Body**:
  ```json
  {
    "bookingReference": "string",
    "lastName": "string"
  }
  ```
- **Response**:
  ```json
  {
    "status": "string", // "ready", "delayed", "cancelled", "unknown"
    "message": "string",
    "flightNumber": "string",
    "departure": "string",
    "gate": "string"
  }
  ```

## Mock Data Integration

Currently, the frontend makes actual API calls to the backend for flight readiness checks. No mock data is being used - the form inputs are directly sent to the backend API.

## Backend Implementation Tasks

1. **Create Flight Readiness Endpoint**
   - Implement `POST /api/flight-readiness` route
   - Accept booking reference and last name
   - Return mock flight status data
   - Include proper error handling

2. **Database Models** (Optional for demo)
   - Since this is a demo, we can use mock data responses
   - No actual database integration needed

## Frontend & Backend Integration

1. **API Communication**
   - Frontend uses axios to make POST request to `/api/flight-readiness`
   - Success responses show flight status via toast notification
   - Error responses show error message via toast
   - Loading states are handled with button disabled state

2. **Error Handling**
   - Form validation for empty fields
   - Network error handling
   - User feedback via toast notifications

3. **Data Flow**
   - User enters booking reference and last name
   - Form validation occurs on submit
   - API request sent to backend
   - Response displayed to user via toast

## Testing Requirements

- Test flight readiness API endpoint
- Verify form validation works
- Test error scenarios (invalid booking, network errors)
- Verify toast notifications display correctly