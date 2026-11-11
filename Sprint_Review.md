# Epidermix AI - Sprint Review

---

## Week 1: Application Architecture & UI Prototype

**1. Sprint Date and Goal:** 
- **Date:** Week 1 
- **Goal:** Set up the Streamlit frontend framework, design the user interface, and build the initial visual mockups for Epidermix.

**2. User Stories Assigned:**
- *As a user, I want a clean, professional landing page so that I can easily navigate the skin analysis protocol.*
- *As a user, I want to upload an image so that the system can process it.*

**3. Tasks Assigned:**
- Initialize Python Streamlit application settings.
- Implement custom CSS styling, fonts, and the hero banner.
- Build the "Ritual Guide" layout with interactive hover cards.
- Create the dummy image upload portal.

**4. Acceptance Criteria & Tests:**
- **Given** a user opens the application, **When** they land on the homepage, **Then** they should see the complete hero banner and the 'Analyse Skin Now' button without styling errors.
- **Given** a user navigates to the Analysis page, **When** they drag-and-drop a skin image, **Then** the image should visually render on the screen.

**5. Estimated Effort vs. Actual Effort:**
- **Estimated:** 15 hours | **Actual:** 12 hours

---

## Week 2: Backend Integration & Reporting Engine

**1. Sprint Date and Goal:** 
- **Date:** Week 2
- **Goal:** Implement secure user authentication, persistent scan history via SQLite, and professional PDF generation.

**2. User Stories Assigned:**
- *As a registered user, I want to authenticate and view my past scans so I can track my skin's evolution.*
- *As a patient, I want to download a PDF report of my scan so I can share it with my doctor.*

**3. Tasks Assigned:**
- Build `database.py` to handle SQLite user credentials and scan logging.
- Implement session state toggles for "Guest" vs "Authenticated" viewing.
- Integrate `fpdf` to dynamically generate a diagnostic document.
- Generate image processing mock heatmaps using OpenCV.

**4. Acceptance Criteria & Tests:**
- **Given** a new user is on the sidebar, **When** they enter a new username and password, **Then** their credentials should be saved to the database.
- **Given** a user has completed an analysis, **When** they click "Download Official System Report", **Then** a cleanly formatted PDF containing their name, the diagnosis, and the system recommendations should download.

**5. Estimated Effort vs. Actual Effort:**
- **Estimated:** 20 hours | **Actual:** 22 hours (PDF formatting logic required slight rework).

---

## Week 3: Cloud AI Integration & Rate Limit Handling

**1. Sprint Date and Goal:** 
- **Date:** Week 3
- **Goal:** Connect the mock frontend into real AI using the Google Gemini Vision API and implement grace-period error handling.

**2. User Stories Assigned:**
- *As a user, I want my image analyzed by a real vision neural network so I can get a highly intelligent medical prediction.*
- *As a user, I want the system to handle request errors smoothly so the app doesn't crash.*

**3. Tasks Assigned:**
- Formulate a strict JSON-forcing prompt for dermatological analysis.
- Connect `google-generativeai` and pass PIL images to the Gemini API.
- Implement a `max_retries` system to catch Free Tier Quota (429) errors.

**4. Acceptance Criteria & Tests:**
- **Given** an image is submitted, **When** the Gemini API returns a payload, **Then** the application must successfully decode the exact JSON parameters (diagnosis, severity, description, status).
- **Given** the user hits an API rate limit, **When** they prompt the system, **Then** a warning indicating "API free tier quota limit reached" should display and block the UI from fully crashing while it retries.

**5. Estimated Effort vs. Actual Effort:**
- **Estimated:** 10 hours | **Actual:** 15 hours (Rate limiting issues extended development time).

---

## Week 4: Offline Edge AI Transformation (Hugging Face)

**1. Sprint Date and Goal:** 
- **Date:** Week 4
- **Goal:** Completely eliminate cloud API constraints and transition to a specialized, locally-hosted Hugging Face Transformer pipeline.

**2. User Stories Assigned:**
- *As a user, I want no restrictions on how many scans I can run so I use Epidermix offline without API keys.*
- *As a developer, I want the system to accurately map raw machine labels to human-friendly UI alerts.*

**3. Tasks Assigned:**
- Gut all dependencies relating to `google-generativeai`.
- Install `torch`, `torchvision`, and `transformers`.
- Implement `Anwarkh1/Skin_Cancer-Image_Classification` pipeline in `app.py`.
- Build a robust `label_map` python dictionary connecting raw class labels to custom severities and recommendations.

**4. Acceptance Criteria & Tests:**
- **Given** the Epidermix environment is freshly loaded, **When** it boots, **Then** it should pull model weights into the local `.cache` using `st.cache_resource`.
- **Given** the HF model predicts "basal_cell_carcinoma", **When** mapping the label, **Then** the UI must force the severity attribute to "High" and flag the status as "danger".

**5. Estimated Effort vs. Actual Effort:**
- **Estimated:** 18 hours | **Actual:** 18 hours (The large 2.5 GB dependency installation matched expected downtime).

---

# Individual Reflection

### Proposed Improvements and Enhancements
Looking back on the development cycle, there are a few areas that could be targeted for future sprints to significantly elevate Epidermix:
1. **Containerization:** Running Epidermix inside a Docker container would isolate the heavy `torch` dependencies and solve cross-platform pathing issues natively.
2. **Local Model Fine-Tuning:** The current Hugging Face model distinguishes between 7 raw classes. Gathering a larger clinical dataset to fine-tune the pipeline specifically for Edge UI deployments could increase our confidence scores and reduce false positive "warning" states.
3. **Password Security:** The SQLite database currently handles credentials linearly. Implementing `bcrypt` password hashing is vital for production before bringing on actual patients.

### Learning & Development Evaluation
- **Technology & Software:** The transition from Cloud APIs (Gemini) to Edge APIs (Hugging Face) was an intense software learning curve. Dealing with `JSONDecodeError`s from cloud platforms vs. strict pipeline outputs from a local PyTorch tensor model radically expanded my understanding of AI engineering and data sanitization. 
- **Hardware Limitations:** Moving to local inference explicitly highlighted hardware limitations. Initially relying on cloud rendering hid the compute cost of AI vision. Downloading a local vision transformer taught me to appreciate memory caching mechanisms (like Streamlit's `@st.cache_resource`) to prevent catastrophic hardware locking.
- **Agile Adaptability:** Tackling the unexpected 429 Quota errors in Sprint 3 prepared the team to pivot immediately in Sprint 4. The agile sprint model heavily rewarded making rapid, modular architectural shifts instead of being locked into a failing tech stack.
