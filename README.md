
# Skin Type Predictor 🧴✨

A machine learning project that predicts a user’s skin type based on various parameters. The project includes a Tkinter-based frontend for easy interaction.

---

## 🚀 Features

* Predicts skin type using trained ML models.
* User-friendly Tkinter GUI interface.
* Accepts multiple input parameters related to skin.
* Provides recommendations for skincare ingredients.

---

## 🛠️ Tech Stack

* Python 3
* Tkinter (frontend GUI)
* Scikit-learn / XGBoost (machine learning models)
* Pandas, NumPy (data preprocessing)
* Pickle (.pkl) for model storage

---

## 📂 Project Structure

SkinTypePredict/
│
├── app.py                  - Main GUI application
├── train\_model.py          - Model training script
├── skin\_model.pkl          - Trained ML model
├── ingredients/            - Images of skincare ingredients
├── \*.pkl                   - Encoders and preprocessing files
├── \*.csv                   - Dataset files
└── README.md               - Project documentation

---

## ▶️ How to Run

1. Clone the repository:
   git clone [https://github.com/KRI940/SkinTypePredict.git](https://github.com/KRI940/SkinTypePredict.git)
   cd SkinTypePredict

2. Install dependencies:
   pip install -r requirements.txt

3. Run the application:
   python app.py

---

## 📊 Dataset

* The model is trained on a custom dataset containing parameters like skin texture, oiliness, dryness, sensitivity, etc.
* Data preprocessing is handled using label encoders and scalers.

---

## 💡 Future Improvements

* Add support for deep learning models (CNN for image-based skin analysis).
* Improve frontend with modern GUI frameworks (PyQt / Web app).
* Deploy as a web application for broader access.

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch (git checkout -b feature-name)
3. Commit changes (git commit -m "Added new feature")
4. Push to branch (git push origin feature-name)
5. Open a Pull Request

---

## 📜 License

This project is open source and available under the MIT License.

---

👩‍💻 Author: Kritika ([https://github.com/KRI940](https://github.com/KRI940))

