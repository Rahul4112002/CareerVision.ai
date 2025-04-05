# CareerVision.ai 🚀

Welcome to **CareerVision.ai**, a web application designed to guide users in their career journey by predicting suitable job roles, providing personalized learning paths, and offering recent job and internship opportunities. 🎯




https://github.com/user-attachments/assets/26824c9b-b59d-407d-92de-30831e79d7d0





## Features 🌟

- **AI-Powered Job Role Prediction**: Utilizes a Deep Learning-based Multi-Layer Perceptron (MLP) classifier to suggest job roles tailored to user inputs.
- **Personalized Learning Paths**: Recommends courses and resources to bridge skill gaps and enhance career prospects.
- **Real-Time Job Listings**: Fetches the latest job and internship opportunities using the Adzuna API.

## Tech Stack 🛠️

- **Backend**: Django
- **Frontend**: HTML, CSS, Tailwind CSS (via CDN)
- **Machine Learning**: Deep Learning with MLP Classifier
- **Job Listings**: Adzuna API

## Installation Guide 📝

Follow these steps to set up the project locally:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Rahul4112002/CareerVision.ai.git
   cd CareerVision.ai
   ```

2. **Set Up Virtual Environment**:

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**:

   ```bash
   python manage.py migrate
   ```

5. **Run the Development Server**:

   ```bash
   python manage.py runserver
   ```

   Access the application at `http://127.0.0.1:8000/`.

## File Structure 📂

```
CareerVision.ai/
├── jobroleprediction/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── templates/
├── static/
├── rbl_ann.ipynb
├── student_placement_data.csv
└── manage.py
```

## Usage Instructions 📚

1. **Navigate to the Home Page**: Explore the intuitive user interface built with Tailwind CSS via CDN.
2. **Input Your Details**: Provide necessary information to receive job role predictions.
3. **Review Recommendations**: Explore suggested job roles, learning paths, and current job listings.

## Contributing 🤝

We welcome contributions! Please fork the repository and create a pull request with your proposed changes.


## Acknowledgements 🙏

- **Django-Tailwind Integration**: Using Tailwind via CDN for seamless styling.
- **Adzuna API**: Job data powered by [Adzuna](https://developer.adzuna.com/).

## Contact 📩

For questions or feedback, please open an issue in this repository.

