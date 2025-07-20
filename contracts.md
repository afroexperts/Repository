# Afro Experts Website - Backend Integration Contracts

## Overview
This document defines the API contracts and integration protocol for converting the Afro Experts frontend from mock data to a fully functional backend-integrated application.

## Current Mock Data Structure (from mock.js)

### Company Information
- Static company details (name, tagline, mission, vision, description)
- Office locations with contact details
- Team information (CEO message, details)

### Services & Products
- IT Services array (4 services with features, descriptions, images)
- IT Solutions array (4 solutions with features)  
- Products array (Starlink kits, POS systems, ERP solutions)
- Partners information

### Dynamic Data (Needs Backend)
- Contact form submissions
- Quote requests
- Service inquiries
- Newsletter subscriptions
- Impact statistics (currently static numbers)

## Required API Endpoints

### 1. Contact Management APIs

#### POST /api/contact/submit
**Purpose**: Handle contact form submissions from Contact Us page
**Request Body**:
```json
{
  "name": "string (required)",
  "email": "string (required, email format)",
  "phone": "string (optional)",
  "country": "string (required, enum: rwanda|car|other)",
  "service": "string (required)",
  "message": "string (required)",
  "source": "string (contact_form)"
}
```
**Response**:
```json
{
  "success": true,
  "message": "Message sent successfully",
  "id": "submission_id"
}
```

#### POST /api/quote/request
**Purpose**: Handle quote requests from CTA buttons
**Request Body**:
```json
{
  "name": "string (required)",
  "email": "string (required)",
  "phone": "string (optional)", 
  "company": "string (optional)",
  "service_type": "string (starlink|network|software|other)",
  "message": "string (optional)",
  "urgent": "boolean (default: false)"
}
```

### 2. Service Inquiry APIs

#### POST /api/services/inquiry
**Purpose**: Handle service-specific inquiries from Services pages
**Request Body**:
```json
{
  "service_id": "number (1-4, maps to services array)",
  "contact_name": "string",
  "contact_email": "string", 
  "contact_phone": "string",
  "company": "string (optional)",
  "project_details": "string",
  "timeline": "string (asap|1month|3months|6months)"
}
```

### 3. Newsletter/Updates APIs

#### POST /api/newsletter/subscribe
**Purpose**: Newsletter subscription from footer
**Request Body**:
```json
{
  "email": "string (required)",
  "interests": "array[string] (optional)",
  "country": "string (optional)"
}
```

### 4. Analytics/Stats APIs

#### GET /api/stats/impact
**Purpose**: Get real impact statistics for homepage
**Response**:
```json
{
  "communities_connected": "number",
  "businesses_served": "number", 
  "people_online": "number",
  "countries_active": "number",
  "last_updated": "datetime"
}
```

### 5. Content Management APIs

#### GET /api/content/testimonials
**Purpose**: Get testimonials for homepage
**Response**:
```json
{
  "testimonials": [
    {
      "id": "number",
      "name": "string",
      "title": "string", 
      "location": "string",
      "message": "string",
      "rating": "number (1-5)",
      "verified": "boolean",
      "date_added": "datetime"
    }
  ]
}
```

## Database Models Required

### 1. ContactSubmission
```javascript
{
  _id: ObjectId,
  name: String (required),
  email: String (required, indexed),
  phone: String,
  country: String (enum: rwanda|car|other),
  service: String, 
  message: String (required),
  source: String (default: 'contact_form'),
  status: String (enum: new|contacted|converted|closed, default: 'new'),
  created_at: Date (default: now),
  updated_at: Date,
  assigned_to: String (optional)
}
```

### 2. QuoteRequest  
```javascript
{
  _id: ObjectId,
  name: String (required),
  email: String (required),
  phone: String,
  company: String,
  service_type: String,
  message: String,
  urgent: Boolean (default: false),
  status: String (enum: pending|quoted|accepted|rejected, default: 'pending'),
  quote_amount: Number (optional),
  quote_details: String (optional),
  created_at: Date,
  updated_at: Date
}
```

### 3. ServiceInquiry
```javascript
{
  _id: ObjectId,
  service_id: Number,
  service_name: String, // derived from services array
  contact_name: String,
  contact_email: String,
  contact_phone: String,
  company: String,
  project_details: String,
  timeline: String,
  status: String (enum: new|reviewing|quoted|closed),
  created_at: Date,
  updated_at: Date
}
```

### 4. NewsletterSubscription
```javascript
{
  _id: ObjectId,
  email: String (required, unique),
  interests: [String],
  country: String,
  status: String (enum: active|unsubscribed, default: 'active'),
  subscribed_at: Date,
  unsubscribed_at: Date (optional)
}
```

### 5. ImpactStats
```javascript
{
  _id: ObjectId,
  communities_connected: Number,
  businesses_served: Number,
  people_online: Number,
  countries_active: Number,
  date: Date (unique, daily updates),
  created_at: Date
}
```

### 6. Testimonial
```javascript
{
  _id: ObjectId,
  name: String,
  title: String,
  location: String,
  message: String,
  rating: Number (1-5),
  verified: Boolean (default: false),
  active: Boolean (default: true),
  date_added: Date,
  image_url: String (optional)
}
```

## Frontend Integration Plan

### Phase 1: Form Integrations
**Files to Update:**
- `/app/frontend/src/pages/Contact.js` - Replace mock form submission
- `/app/frontend/src/components/Layout.js` - Add newsletter subscription to footer
- `/app/frontend/src/pages/Home.js` - Replace quote request buttons
- `/app/frontend/src/pages/Services.js` - Add service inquiry forms

**Changes Required:**
- Replace `toast()` success messages with actual API calls
- Add loading states during form submissions
- Add proper error handling and validation
- Replace mock data with API responses

### Phase 2: Dynamic Content
**Files to Update:**
- `/app/frontend/src/pages/Home.js` - Use dynamic impact stats and testimonials
- `/app/frontend/src/mock.js` - Keep static content, remove dynamic data

**Changes Required:**
- Add `useEffect` hooks to fetch dynamic data
- Add loading skeletons for data fetching
- Handle empty states gracefully

## Error Handling Strategy

### API Error Responses
```json
{
  "success": false,
  "error": "error_code",
  "message": "Human readable error message",
  "details": {} // optional validation details
}
```

### Frontend Error States
- Form validation errors (display inline)
- Network errors (show retry option)  
- Server errors (show generic message)
- Loading states (skeletons/spinners)

## Security Considerations

1. **Input Validation**: All form inputs validated on backend
2. **Rate Limiting**: Implement rate limiting on form submission endpoints
3. **CORS**: Properly configured for frontend domain
4. **Data Sanitization**: Sanitize all text inputs
5. **Email Validation**: Verify email formats and existence
6. **Spam Protection**: Consider implementing basic spam detection

## Integration Testing Checklist

### Backend APIs
- [ ] All endpoints return correct response formats
- [ ] Database models save data correctly
- [ ] Validation works as expected
- [ ] Error handling returns appropriate messages

### Frontend Integration  
- [ ] Forms submit successfully and show success messages
- [ ] Error states display correctly
- [ ] Loading states work properly
- [ ] Dynamic data loads and renders correctly
- [ ] Mobile responsiveness maintained

### End-to-End Testing
- [ ] Contact form submission workflow
- [ ] Quote request workflow  
- [ ] Service inquiry workflow
- [ ] Newsletter subscription workflow
- [ ] Admin can view submitted data

## Post-Integration Enhancements (Optional)

1. **Admin Dashboard**: Simple admin interface to view submissions
2. **Email Notifications**: Send emails to admin on new submissions
3. **Auto-responders**: Send confirmation emails to users
4. **Analytics**: Track form submission rates and popular services
5. **CRM Integration**: Export leads to external CRM systems

## Migration Strategy

1. **Keep mock.js**: Retain for static content (company info, services list)
2. **Gradual Integration**: Replace dynamic features one by one
3. **Fallback Handling**: Gracefully handle API failures with cached data
4. **Testing**: Test each integration thoroughly before moving to next

This contract serves as the complete protocol for seamless backend integration while maintaining the professional frontend experience already built.