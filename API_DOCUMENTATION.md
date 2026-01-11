# API Documentation - PTJobs


## 1. Users API (`/users/`)

### 1.1. Register Account
- **URL:** `POST /users/`
- **Access:** Public (no login required)
- **Description:** Create new account for user (Candidate or Company)
- **Content-Type:** `multipart/form-data`

**Input:**
```json
{
  "username": "string (required)",
  "password": "string (required)",
  "first_name": "string (required)",
  "last_name": "string (required)",
  "email": "string (required, unique)",
  "phone": "string (required, unique, 10 characters)",
  "role": "CANDIDATE | COMPANY (required)",
  "avatar": "file (required)",
  "profile": "string (JSON, required)"
}
```

**Profile for CANDIDATE:**
```json
{
  "gender": "MALE | FEMALE | OTHER (optional)",
  "dob": "YYYY-MM-DD (optional)"
}
```

**Profile for COMPANY:**
```json
{
  "name": "string (required, unique)",
  "tax_number": "string (required, unique)",
  "address": "string (optional)"
}
```

**Output (201 Created):**
```json
{
  "username": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "phone": "string",
  "role": "string",
  "avatar": "url",
  "profile": {
    "id": "number",
    ...profile_fields
  }
}
```

### 1.2. Get Current User Information
- **URL:** `GET /users/current-user/`
- **Access:** Authenticated user
- **Description:** Get detailed information of current user

**Output (200 OK):**
```json
{
  "username": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "phone": "string",
  "role": "string",
  "avatar": "url",
  "profile": {
    "id": "number",
    ...profile_fields
  }
}
```

### 1.3. Update Current User Information
- **URL:** `PATCH /users/current-user/`
- **Access:** Authenticated user
- **Description:** Update user and profile information
- **Content-Type:** `multipart/form-data`

**Input (all optional):**
```json
{
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "phone": "string",
  "avatar": "file",
  "password": "string (requires old_password)",
  "old_password": "string (required when changing password)",
  "profile": "string (JSON)"
}
```

**Output (200 OK):** Same as GET /users/current-user/

---

## 2. Companies API (`/companies/`)

### 2.1. List Companies
- **URL:** `GET /companies/`
- **Access:** Public
- **Description:** Get list of all active companies
- **Pagination:** Yes

**Query Parameters:**
- `name`: Search by company name (contains)

**Output (200 OK):**
```json
{
  "count": "number",
  "next": "url | null",
  "previous": "url | null",
  "results": [
    {
      "id": "number",
      "name": "string",
      "tax_number": "string",
      "address": "string",
      "avatar": "url | null",
      "job_post_count": "number"
    }
  ]
}
```

### 2.2. Company Details
- **URL:** `GET /companies/{id}/`
- **Access:** Public
- **Description:** Get detailed information of a company

**Output (200 OK):**
```json
{
  "id": "number",
  "name": "string",
  "tax_number": "string",
  "address": "string",
  "avatar": "url | null",
  "images": ["url1", "url2", "url3"],
  "is_followed": "boolean (only shown when user is authenticated CANDIDATE)"
}
```

### 2.3. Company Reviews List
- **URL:** `GET /companies/{id}/reviews/`
- **Access:** Public
- **Description:** Get list of reviews from candidates about the company (only CANDIDATE reviews)
- **Pagination:** Yes

**Output (200 OK):**
```json
{
  "count": "number",
  "next": "url | null",
  "previous": "url | null",
  "results": [
    {
      "id": "number",
      "comment": "string",
      "created_at": "datetime",
      "job_post": {
        "name": "string"
      },
      "user": {
        "name": "string",
        "avatar": "url | null"
      },
      "application": {
        "start_date": "DD/MM/YYYY | null",
        "end_date": "DD/MM/YYYY | null"
      }
    }
  ]
}
```

---

## 3. Candidates API (`/candidates/`)

### 3.1. Candidate Details
- **URL:** `GET /candidates/{id}/`
- **Access:** Public
- **Description:** Get detailed information of a candidate

**Output (200 OK):**
```json
{
  "id": "number",
  "gender": "string",
  "dob": "YYYY-MM-DD",
  "full_name": "string",
  "email": "string",
  "phone": "string",
  "avatar": "url | null"
}
```

### 3.2. Candidate Reviews List
- **URL:** `GET /candidates/{id}/reviews/`
- **Access:** Public
- **Description:** Get list of reviews from companies about the candidate (only COMPANY reviews)
- **Pagination:** Yes

**Output (200 OK):**
```json
{
  "count": "number",
  "next": "url | null",
  "previous": "url | null",
  "results": [
    {
      "id": "number",
      "comment": "string",
      "created_at": "datetime",
      "user": {
        "name": "string (company name)",
        "avatar": "url | null"
      },
      "job_post": {
        "name": "string"
      },
      "application": {
        "start_date": "DD/MM/YYYY | null",
        "end_date": "DD/MM/YYYY | null"
      }
    }
  ]
}
```

---

## 4. Job Posts API (`/jobposts/`)

### 4.1. List Job Posts
- **URL:** `GET /jobposts/`
- **Access:** Public
- **Description:** Get list of all active job posts
- **Pagination:** Yes

**Query Parameters:**
- `category`: Job category ID
- `company`: Company ID
- `address`: Search by address (contains)
- `start_time`: Start time (0-23)
- `end_time`: End time (0-23)
- `day`: Day of week (MON, TUE, WED, THU, FRI, SAT, SUN)

**Output (200 OK):**
```json
{
  "count": "number",
  "next": "url | null",
  "previous": "url | null",
  "results": [
    {
      "id": "number",
      "name": "string",
      "description": "string",
      "salary": "decimal",
      "address": "string",
      "deadline": "YYYY-MM-DD",
      "vacancy": "number",
      "company": "number",
      "category": "number | null",
      "created_at": "datetime"
    }
  ]
}
```

### 4.2. Create Job Post
- **URL:** `POST /jobposts/`
- **Access:** Authenticated COMPANY user with activated account
- **Description:** Create new job post

**Input:**
```json
{
  "name": "string (required)",
  "description": "string (required)",
  "salary": "decimal (required)",
  "address": "string (required)",
  "deadline": "YYYY-MM-DD (required)",
  "vacancy": "number (required)",
  "category": "number (optional)",
  "work_times": [
    {
      "day": "MON | TUE | WED | THU | FRI | SAT | SUN (required)",
      "start_time": "HH:MM:SS (required)",
      "end_time": "HH:MM:SS (required)"
    }
  ]
}
```

**Output (201 Created):**
```json
{
  "id": "number",
  "name": "string",
  "description": "string",
  "salary": "decimal",
  "address": "string",
  "deadline": "YYYY-MM-DD",
  "vacancy": "number",
  "company": "number",
  "category": "number | null",
  "created_at": "datetime"
}
```

**Note:** 
- Company account must upload at least 3 images and be activated by admin to post jobs
- System will automatically send email notifications to candidates following the company

### 4.3. Job Post Details
- **URL:** `GET /jobposts/{id}/`
- **Access:** Public
- **Description:** Get detailed information of a job post

**Output (200 OK):**
```json
{
  "id": "number",
  "name": "string",
  "description": "string",
  "salary": "decimal",
  "address": "string",
  "deadline": "YYYY-MM-DD",
  "vacancy": "number",
  "category": "number | null",
  "created_at": "datetime",
  "company": {
    "name": "string",
    "avatar": "url | null"
  },
  "work_times": [
    {
      "day": "string",
      "start_time": "HH:MM:SS",
      "end_time": "HH:MM:SS",
      "job_post": "number"
    }
  ]
}
```

### 4.4. Update Job Post
- **URL:** `PATCH /jobposts/{id}/`
- **Access:** Job post owner (COMPANY)
- **Description:** Update job post information

**Input (all optional):**
```json
{
  "name": "string",
  "description": "string",
  "salary": "decimal",
  "address": "string",
  "deadline": "YYYY-MM-DD",
  "vacancy": "number",
  "category": "number",
  "active": "boolean",
  "work_times": [
    {
      "day": "string",
      "start_time": "HH:MM:SS",
      "end_time": "HH:MM:SS"
    }
  ]
}
```

**Output (200 OK):** Same as GET /jobposts/{id}/

**Note:** Cannot update `created_at` and `company` fields

### 4.5. Delete Job Post
- **URL:** `DELETE /jobposts/{id}/`
- **Access:** Job post owner (COMPANY)
- **Description:** Delete (soft delete) job post

**Output (204 No Content):** No body

### 4.6. Job Post Reviews List
- **URL:** `GET /jobposts/{id}/reviews/`
- **Access:** Public
- **Description:** Get list of reviews about the job post (only reviews with parent)
- **Pagination:** Yes

**Output (200 OK):**
```json
{
  "count": "number",
  "next": "url | null",
  "previous": "url | null",
  "results": [
    {
      "id": "number",
      "comment": "string",
      "created_at": "datetime",
      "user": {
        "name": "string",
        "avatar": "url | null"
      },
      "application": {
        "start_date": "DD/MM/YYYY | null",
        "end_date": "DD/MM/YYYY | null"
      },
      "parent": {
        "id": "number",
        "comment": "string",
        "created_at": "datetime",
        "user": {
          "name": "string",
          "avatar": "url | null"
        }
      }
    }
  ]
}
```

---

## 5. Job Categories API (`/job-categories/`)

### 5.1. List Job Categories
- **URL:** `GET /job-categories/`
- **Access:** Public
- **Description:** Get list of all job categories

**Output (200 OK):**
```json
[
  {
    "id": "number",
    "name": "string"
  }
]
```

---

## 6. Applications API (`/applications/`)

### 6.1. List Applications
- **URL:** `GET /applications/`
- **Access:** Authenticated user
- **Description:** 
  - For CANDIDATE: Get list of own applications
  - For COMPANY: Get list of applications to company's job posts
- **Pagination:** Yes

**Query Parameters:**
- `status`: Filter by status (REVIEWING | EMPLOYED | REJECTED | TERMINATED)

**Output for CANDIDATE (200 OK):**
```json
{
  "count": "number",
  "next": "url | null",
  "previous": "url | null",
  "results": [
    {
      "id": "number",
      "start_date": "YYYY-MM-DD | null",
      "end_date": "YYYY-MM-DD | null",
      "status": "REVIEWING | EMPLOYED | REJECTED | TERMINATED",
      "resume": "number",
      "candidate": "number",
      "job_post": {
        "name": "string",
        "company": {
          "name": "string",
          "avatar": "url | null"
        }
      }
    }
  ]
}
```

**Output for COMPANY (200 OK):**
```json
{
  "count": "number",
  "next": "url | null",
  "previous": "url | null",
  "results": [
    {
      "id": "number",
      "start_date": "YYYY-MM-DD | null",
      "end_date": "YYYY-MM-DD | null",
      "status": "REVIEWING | EMPLOYED | REJECTED | TERMINATED",
      "resume": "number",
      "candidate": {
        "name": "string",
        "avatar": "url | null"
      },
      "job_post": {
        "name": "string"
      }
    }
  ]
}
```

### 6.2. Create Application
- **URL:** `POST /applications/`
- **Access:** Authenticated CANDIDATE user
- **Description:** Create new application

**Input:**
```json
{
  "resume": "number (required, resume ID)",
  "job_post": "number (required, job post ID)"
}
```

**Output (201 Created):**
```json
{
  "id": "number",
  "start_date": null,
  "end_date": null,
  "status": "REVIEWING",
  "resume": "number",
  "candidate": "number",
  "job_post": "number"
}
```

**Note:** 
- Job post must be valid and have vacancy
- Each candidate can only submit 1 application per job post

### 6.3. Application Details
- **URL:** `GET /applications/{id}/`
- **Access:** Application owner (CANDIDATE) or company owning the job post
- **Description:** Get detailed application information

**Output for CANDIDATE (200 OK):**
```json
{
  "id": "number",
  "start_date": "YYYY-MM-DD | null",
  "end_date": "YYYY-MM-DD | null",
  "status": "string",
  "resume": "url (cloudinary URL)",
  "candidate": "number",
  "job_post": {
    "name": "string"
  },
  "company": {
    "name": "string",
    "avatar": "url | null"
  }
}
```

**Output for COMPANY (200 OK):**
```json
{
  "id": "number",
  "start_date": "YYYY-MM-DD | null",
  "end_date": "YYYY-MM-DD | null",
  "status": "string",
  "resume": "url (cloudinary URL)",
  "job_post": {
    "name": "string"
  },
  "candidate": {
    "name": "string",
    "avatar": "url | null"
  }
}
```

### 6.4. Update Application Status
- **URL:** `PATCH /applications/{id}/`
- **Access:** Company owning the job post
- **Description:** Update application status

**Input:**
```json
{
  "status": "REVIEWING | EMPLOYED | REJECTED | TERMINATED (required)"
}
```

**Output (200 OK):** Same as GET /applications/{id}/

**Status Transition Rules:**
- Cannot revert back to `REVIEWING`
- `REVIEWING` → `EMPLOYED`: Decrease job post vacancy by 1, set start_date = today
- `REVIEWING` → `REJECTED`: Reject application
- `EMPLOYED` → `TERMINATED`: Increase job post vacancy by 1, set end_date = today
- Can only transition from `REVIEWING` to `EMPLOYED` or `REJECTED`
- Can only transition from `EMPLOYED` to `TERMINATED`

### 6.5. Delete Application
- **URL:** `DELETE /applications/{id}/`
- **Access:** Application owner (CANDIDATE)
- **Description:** Delete (soft delete) application

**Output (204 No Content):** No body

**Note:** Can only delete applications with `REVIEWING` status

### 6.6. Application Reviews List
- **URL:** `GET /applications/{id}/reviews/`
- **Access:** Authenticated user
- **Description:** Get list of reviews about the application
- **Pagination:** Yes

**Output (200 OK):**
```json
{
  "count": "number",
  "next": "url | null",
  "previous": "url | null",
  "results": [
    {
      "id": "number",
      "comment": "string",
      "created_at": "datetime",
      "user": {
        "name": "string",
        "avatar": "url | null"
      },
      "parent": {
        "id": "number",
        "comment": "string",
        "created_at": "datetime",
        "user": {
          "name": "string",
          "avatar": "url | null"
        }
      }
    }
  ]
}
```

### 6.7. Create Application Review
- **URL:** `POST /applications/{id}/reviews/`
- **Access:** Application owner (CANDIDATE) or company owning the job post
- **Description:** Create review for application

**Input:**
```json
{
  "comment": "string (required)"
}
```

**Output (201 Created):**
```json
{
  "id": "number",
  "comment": "string",
  "user": "number",
  "created_at": "datetime"
}
```

**Note:** 
- Each application can have maximum 2 reviews (1 from candidate, 1 from company)
- Second review will automatically be marked as reply to the first review

---

## 7. Resumes API (`/resumes/`)

### 7.1. List Resumes
- **URL:** `GET /resumes/`
- **Access:** Authenticated CANDIDATE user
- **Description:** Get list of current candidate's resumes
- **Pagination:** Yes

**Output (200 OK):**
```json
{
  "count": "number",
  "next": "url | null",
  "previous": "url | null",
  "results": [
    {
      "id": "number",
      "file": "url (cloudinary URL)",
      "candidate": "number"
    }
  ]
}
```

### 7.2. Create Resume
- **URL:** `POST /resumes/`
- **Access:** Authenticated CANDIDATE user
- **Description:** Upload new resume
- **Content-Type:** `multipart/form-data`

**Input:**
```json
{
  "file": "file (required, PDF, DOC, DOCX, etc.)"
}
```

**Output (201 Created):**
```json
{
  "id": "number",
  "file": "url (cloudinary URL)",
  "candidate": "number"
}
```

### 7.3. Delete Resume
- **URL:** `DELETE /resumes/{id}/`
- **Access:** Resume owner (CANDIDATE)
- **Description:** Delete (soft delete) resume

**Output (204 No Content):** No body

---

## 8. Company Images API (`/company-images/`)

### 8.1. List Company Images
- **URL:** `GET /company-images/`
- **Access:** Authenticated COMPANY user
- **Description:** Get list of current company's images

**Output (200 OK):**
```json
[
  {
    "id": "number",
    "image": "url (cloudinary URL)",
    "company": "number",
    "created_at": "datetime"
  }
]
```

### 8.2. Create Company Image
- **URL:** `POST /company-images/`
- **Access:** Authenticated COMPANY user
- **Description:** Upload new image for company
- **Content-Type:** `multipart/form-data`

**Input:**
```json
{
  "image": "file (required)"
}
```

**Output (201 Created):**
```json
{
  "id": "number",
  "image": "url (cloudinary URL)",
  "company": "number",
  "created_at": "datetime"
}
```

**Note:** Company needs at least 3 images to be activated by admin

### 8.3. Delete Company Image
- **URL:** `DELETE /company-images/{id}/`
- **Access:** Image owner (COMPANY)
- **Description:** Delete (hard delete) image

**Output (204 No Content):** No body

**Note:** Cannot delete if company only has 3 images

---

## 9. Following API (`/following/`)

### 9.1. List Followed Companies
- **URL:** `GET /following/`
- **Access:** Authenticated CANDIDATE user
- **Description:** Get list of companies that candidate is following

**Output (200 OK):**
```json
[
  {
    "id": "number",
    "created_at": "datetime",
    "candidate": "number",
    "company": {
      "name": "string",
      "avatar": "url | null"
    }
  }
]
```

### 9.2. Follow Company
- **URL:** `POST /following/`
- **Access:** Authenticated CANDIDATE user with email
- **Description:** Follow a company

**Input:**
```json
{
  "company": "number (required, company ID)"
}
```

**Output (201 Created):**
```json
{
  "id": "number",
  "created_at": "datetime",
  "candidate": "number",
  "company": "number"
}
```

**Note:** 
- User must have email to follow company
- When company posts new job, email notification will be sent to candidate

### 9.3. Unfollow Company
- **URL:** `DELETE /following/{id}/`
- **Access:** Follow owner (CANDIDATE)
- **Description:** Unfollow company

**Output (204 No Content):** No body

---

## 10. Reviews API (`/reviews/`)

### 10.1. Update Review
- **URL:** `PATCH /reviews/{id}/`
- **Access:** Review owner
- **Description:** Update review content

**Input:**
```json
{
  "comment": "string (required)"
}
```

**Output (200 OK):**
```json
{
  "id": "number",
  "comment": "string",
  "user": "number",
  "created_at": "datetime"
}
```

**Note:** Can only update `comment` field

### 10.2. Delete Review
- **URL:** `DELETE /reviews/{id}/`
- **Access:** Review owner
- **Description:** Delete review (hard delete - remove from database)

**Output (204 No Content):** No body

---

## Access Permissions Summary Table

| Endpoint | Method | Access |
|----------|--------|--------|
| `/users/` | POST | Public |
| `/users/current-user/` | GET, PATCH | Authenticated |
| `/companies/` | GET | Public |
| `/companies/{id}/` | GET | Public |
| `/companies/{id}/reviews/` | GET | Public |
| `/candidates/{id}/` | GET | Public |
| `/candidates/{id}/reviews/` | GET | Public |
| `/jobposts/` | GET | Public |
| `/jobposts/` | POST | COMPANY (activated) |
| `/jobposts/{id}/` | GET | Public |
| `/jobposts/{id}/` | PATCH | Owner (COMPANY) |
| `/jobposts/{id}/` | DELETE | Owner (COMPANY) |
| `/jobposts/{id}/reviews/` | GET | Public |
| `/job-categories/` | GET | Public |
| `/applications/` | GET | Authenticated |
| `/applications/` | POST | CANDIDATE |
| `/applications/{id}/` | GET | Owner or company |
| `/applications/{id}/` | PATCH | Company owning job post |
| `/applications/{id}/` | DELETE | Owner (CANDIDATE) |
| `/applications/{id}/reviews/` | GET | Authenticated |
| `/applications/{id}/reviews/` | POST | Owner or company |
| `/resumes/` | GET | CANDIDATE |
| `/resumes/` | POST | CANDIDATE |
| `/resumes/{id}/` | DELETE | Owner (CANDIDATE) |
| `/company-images/` | GET | COMPANY |
| `/company-images/` | POST | COMPANY |
| `/company-images/{id}/` | DELETE | Owner (COMPANY) |
| `/following/` | GET | CANDIDATE |
| `/following/` | POST | CANDIDATE (with email) |
| `/following/{id}/` | DELETE | Owner (CANDIDATE) |
| `/reviews/{id}/` | PATCH | Owner |
| `/reviews/{id}/` | DELETE | Owner |

---

## Notes

### Application Status
- **REVIEWING:** Under review
- **EMPLOYED:** Hired
- **REJECTED:** Rejected
- **TERMINATED:** Contract terminated

### Company Account Activation Process
1. Register COMPANY account (default `active=False`)
2. Upload at least 3 company images
3. Contact admin to activate account
4. After activation, can post job posts

### Application Process
1. Candidate uploads resume
2. Candidate creates application with resume and job_post
3. Company views application list and updates status
4. Both candidate and company can create reviews for application

### Email Notifications
- When company posts new job, all following candidates receive email notification
- Candidate needs email to follow company

