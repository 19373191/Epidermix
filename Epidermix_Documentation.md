# Epidermix AI - System Documentation

## 1. Overview
Epidermix is an advanced, offline-capable Python web application designed for dermatological image analysis. By leveraging a local Deep Learning Vision Transformer (ViT) and a robust Streamlit user interface, Epidermix allows users to upload images of skin lesions, analyze them locally without internet dependence or API limits, and generate official medical-style PDF reports.

---

## 2. Core Features
- **Local AI Edge Processing**: Utitilizes a `transformers` pipeline to run advanced AI models completely offline. 
- **Persisted Authentication**: Includes a custom authentication and member-portal system powered by SQLite, keeping patient/scan histories secure and logged.
- **Diagnostic Mapping UI**: Dynamically interprets string prediction outputs from machine learning models into highly-readable HTML statuses, descriptions, and clinical recommendations.
- **Dynamic PDF Reporting**: Programmatically writes professional-grade PDF documents of the findings that users can download.
- **Vision Pre-processing**: Overlays visual heatmaps onto uploaded imagery using OpenCV processing matrices.

---

## 3. Codebase Structure

### `app.py`
This is the **Main Application Shell**. It is the entry point for the Streamlit server.
- **Routing**: Handles multi-page layouts (Home page with the 'Ritual Guide' vs. the Analysis Dashboard).
- **AI Core (`analyse_skin_image`)**: This function invokes the Hugging Face `transformers` library, pushes the uploaded image array through the `Anwarkh1/Skin_Cancer-Image_Classification` model, reads the tensor outputs, and uses a hardcoded dictionary map (`label_map`) to translate raw biological classes (like `actinic_keratoses`) into frontend alerts (e.g., Severity: Moderate, Status: Warning).
- **PDF Generation**: Houses the `generate_pdf_report()` helper which constructs an FPDF layout on the fly. 

### `database.py` (Backend)
This is the **Storage Handler**, interacting directly with the `epidermix.db` SQLite file.
- **Authentication**: Checks and encrypts user logins (`authenticate_user`, `register_user`).
- **Scan History**: Commits records of previous diagnostic scans (`save_scan`, `get_user_scans`) linking the specific severity and confidence levels back to the logged-in user session.

### `image_utils.py` (Vision Engine)
This is the **Augmentation & Vision Utility**.
- Uses OpenCV arrays and Pillow bounds to execute transformations on the input skin images, such as drawing artificial intelligent heatmaps (`generate_mock_heatmap`) to visualize the problem zones in the Streamlit UI.

### `/assets`
Directory containing local graphic icons, the logo, and the static stylistic images used in the "Ritual Guide" component grid.

---

## 4. Technical Stack
- **Web Framework**: Streamlit
- **Machine Learning**: PyTorch (`torch`) and Hugging Face `transformers`
- **Image Processing**: OpenCV (`opencv-python-headless`) and Pillow
- **Database Engine**: Python built-in `sqlite3`
- **Document Rendering**: `fpdf2`

## 5. Running the Application locally
To spin up Epidermix on a new machine:
1. Ensure a Python 3.10+ environment is initialized.
2. Install dependencies: `pip install -r requirements.txt` (This will pull roughly ~2.5GB due to PyTorch).
3. Start the server: `python -m streamlit run app.py` 
4. *Note: Upon executing the first skin analysis protocol, the system will pause temporarily to cache the neural network weights from Hugging Face into your environment.*
