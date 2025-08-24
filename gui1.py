import os
import tkinter as tk
from tkinter import ttk, messagebox
import joblib
from PIL import Image, ImageTk

# ==========================
# Color Palette
# ==========================
LIGHTCORAL = "#CD5555"
GRAY90 = "#F7F7F7"
LIGHTSALMON4 = "#8B5742"
INDIANRED = "#8B3A3A"
HOVER_BG = "#FFE4E1"  # soft pink

# --------------------------
# Globals for login entries
# --------------------------
username_entry = None
password_entry = None
login_root = None

# ==========================
# Main App (opens as Toplevel)
# ==========================
def open_main_app(parent):
    """
    parent: the login_root to withdraw (keeps single Tk instance).
    Opens the main predictor window as a Toplevel.
    """
    # Hide login window
    try:
        if parent:
            parent.withdraw()
    except Exception:
        pass

    # Create Toplevel window
    main_win = tk.Toplevel()
    main_win.title("Skin Type Predictor")
    main_win.geometry("900x600")
    main_win.resizable(True, True)

    # Attempt to load model files (catch failures and show message)
    model = None
    target_encoder = None
    encoders = {}
    try:
        # adjust path if needed
        os.chdir(r"K:\Kritika\Internship Project\AI Skin type Predictor\skin")
        model = joblib.load("skin_model.pkl")
        target_encoder = joblib.load("target_encoder.pkl")
        encoders = {
            "gender": joblib.load("gender_encoder.pkl"),
            "weather": joblib.load("weather_encoder.pkl"),
            "oiliness": joblib.load("oiliness_encoder.pkl"),
            "acne": joblib.load("acne_encoder.pkl"),
            "tightness_after_wash": joblib.load("tightness_after_wash_encoder.pkl"),
            "makeup_usage": joblib.load("makeup_usage_encoder.pkl"),
            "flaking": joblib.load("flaking_encoder.pkl"),
            "redness_itchiness": joblib.load("redness_itchiness_encoder.pkl")
        }
    except Exception as e:
        messagebox.showerror("Model Load Error", f"Failed to load model files:\n{e}")
        # If models not available, still let user see a basic UI (or you can return)
        encoders = {
            "gender": type("X", (), {"classes_": ["Male", "Female"]})(),
            "weather": type("X", (), {"classes_": ["Hot", "Cold", "Moderate"]})(),
            "oiliness": type("X", (), {"classes_": ["Low", "Normal", "High"]})(),
            "acne": type("X", (), {"classes_": ["No", "Mild", "Severe"]})(),
            "tightness_after_wash": type("X", (), {"classes_": ["Yes", "No"]})(),
            "makeup_usage": type("X", (), {"classes_": ["Daily", "Sometimes", "Never"]})(),
            "flaking": type("X", (), {"classes_": ["No", "Mild", "Yes"]})(),
            "redness_itchiness": type("X", (), {"classes_": ["No", "Sometimes", "Yes"]})(),
        }
        model = None
        target_encoder = None

    def predict_skin_type():
        if model is None or target_encoder is None:
            messagebox.showwarning("No Model", "Model files not loaded. Prediction unavailable.")
            return
        try:
            user_input = [
                int(fields["Age"].get()),
                encoders["gender"].transform([fields["Gender"].get()])[0],
                float(fields["Water Intake (liters)"].get()),
                encoders["weather"].transform([fields["Weather"].get()])[0],
                encoders["oiliness"].transform([fields["Oiliness"].get()])[0],
                encoders["acne"].transform([fields["Acne"].get()])[0],
                encoders["tightness_after_wash"].transform([fields["Tightness After Wash"].get()])[0],
                encoders["makeup_usage"].transform([fields["Makeup Usage"].get()])[0],
                encoders["flaking"].transform([fields["Flaking"].get()])[0],
                encoders["redness_itchiness"].transform([fields["Redness/Itchiness"].get()])[0]
            ]
            prediction = model.predict([user_input])
            skin_type = target_encoder.inverse_transform([prediction[0]])[0]
            result_label.config(text=f"Predicted Skin Type: {skin_type}", fg=INDIANRED)
        except Exception as e:
            result_label.config(text=f"Error: {e}", fg=INDIANRED)

    # ===== Background Image =====
    try:
        bg_image_main = Image.open("img.jpg")
    except Exception:
        bg_image_main = None

    bg_canvas = tk.Canvas(main_win, highlightthickness=0)
    bg_canvas.pack(fill="both", expand=True)
    bg_image_tk_main = None

    form_frame_main = tk.Frame(bg_canvas, bg="#ffffff", padx=20, pady=20)

    def add_hover_effect(widget, normal_bg):
        def on_hover(e): 
            try: widget.configure(background=HOVER_BG)
            except Exception: pass
        def on_leave(e): 
            try: widget.configure(background=normal_bg)
            except Exception: pass
        widget.bind("<Enter>", on_hover)
        widget.bind("<Leave>", on_leave)

    fields = {
        "Age": tk.Entry(form_frame_main, bg=GRAY90, fg=INDIANRED, relief="flat"),
        "Gender": ttk.Combobox(form_frame_main, values=encoders["gender"].classes_.tolist()),
        "Water Intake (liters)": tk.Entry(form_frame_main, bg=GRAY90, fg=INDIANRED, relief="flat"),
        "Weather": ttk.Combobox(form_frame_main, values=encoders["weather"].classes_.tolist()),
        "Oiliness": ttk.Combobox(form_frame_main, values=encoders["oiliness"].classes_.tolist()),
        "Acne": ttk.Combobox(form_frame_main, values=encoders["acne"].classes_.tolist()),
        "Tightness After Wash": ttk.Combobox(form_frame_main, values=encoders["tightness_after_wash"].classes_.tolist()),
        "Makeup Usage": ttk.Combobox(form_frame_main, values=encoders["makeup_usage"].classes_.tolist()),
        "Flaking": ttk.Combobox(form_frame_main, values=encoders["flaking"].classes_.tolist()),
        "Redness/Itchiness": ttk.Combobox(form_frame_main, values=encoders["redness_itchiness"].classes_.tolist())
    }

    for label_text, widget in fields.items():
        tk.Label(form_frame_main, text=label_text, bg="#ffffff", fg=LIGHTCORAL).pack(pady=3, anchor="w")
        widget.pack(pady=3, fill="x")
        if isinstance(widget, tk.Entry):
            add_hover_effect(widget, GRAY90)
        elif isinstance(widget, ttk.Combobox):
            try:
                widget.configure(background="white")
            except Exception:
                pass
            add_hover_effect(widget, "white")

    result_label = tk.Label(form_frame_main, text="", font=("Arial", 12), fg=LIGHTCORAL, bg="#ffffff")
    result_label.pack(pady=10)

    predict_button = tk.Button(form_frame_main, text="Predict", bg=LIGHTCORAL, fg="white", relief="flat", command=predict_skin_type)
    predict_button.pack(pady=5)

    def btn_on_enter(e): predict_button.config(highlightthickness=2, highlightbackground=LIGHTSALMON4, highlightcolor=LIGHTSALMON4)
    def btn_on_leave(e): predict_button.config(highlightthickness=0)
    predict_button.bind("<Enter>", btn_on_enter)
    predict_button.bind("<Leave>", btn_on_leave)

    def resize_main_bg(event=None):
        nonlocal bg_image_tk_main
        if bg_image_main is None:
            bg_canvas.configure(bg="#f0f0f0")
            return
        width = main_win.winfo_width()
        height = main_win.winfo_height()
        if width < 10 or height < 10:
            return
        resized_main_bg = bg_image_main.resize((width, height), Image.LANCZOS)
        bg_image_tk_main = ImageTk.PhotoImage(resized_main_bg)
        bg_canvas.delete("all")
        bg_canvas.create_image(0, 0, image=bg_image_tk_main, anchor="nw")
        # Put form centered
        bg_canvas.create_window(width//2, height//2, window=form_frame_main)

    main_win.bind("<Configure>", resize_main_bg)
    resize_main_bg()


# ==========================
# Login Screen
# ==========================
def check_login():
    """
    Called when Log In button pressed.
    Uses the module-level username_entry/password_entry variables.
    """
    global username_entry, password_entry, login_root
    if username_entry is None or password_entry is None:
        messagebox.showerror("Internal Error", "Login entries not initialized.")
        return

    username = username_entry.get()
    password = password_entry.get()
    if username == "admin" and password == "1234":
        # Open main app in a Toplevel (avoid multiple Tk instances)
        open_main_app(login_root)
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password")


def create_rounded_entry(parent, show_char=""):
    """
    Returns (frame, entry) where frame contains a plain Entry widget.
    Hover changes the Entry background to HOVER_BG and back to normal.
    """
    frame = tk.Frame(parent, bg="#ffffff")
    entry = tk.Entry(frame, bd=0, bg=GRAY90, fg=INDIANRED, insertbackground="white",
                     font=("Arial", 10), relief="flat", show=show_char)
    entry.pack(ipadx=6, ipady=6)

    def on_hover(e): entry.config(bg=HOVER_BG)
    def on_leave(e): entry.config(bg=GRAY90)

    entry.bind("<Enter>", on_hover)
    entry.bind("<Leave>", on_leave)

    return frame, entry


# ===== Login Window =====
def build_login_window():
    global username_entry, password_entry, login_root
    login_root = tk.Tk()
    login_root.title("Login Page")
    login_root.geometry("600x520")
    login_root.minsize(480, 420)

    # Background image canvas
    try:
        bg_image_login = Image.open("img.jpg")
    except Exception:
        bg_image_login = None

    bg_canvas_login = tk.Canvas(login_root, highlightthickness=0)
    bg_canvas_login.pack(fill="both", expand=True)

    # Rounded rectangle function on a canvas
    def draw_rounded_rect(canvas, x1, y1, x2, y2, r=30, fill="#ffffff", outline=GRAY90, width=2):
        # create a rounded rectangle by polygon smoothed
        points = [
            x1 + r, y1,
            x2 - r, y1,
            x2, y1,
            x2, y1 + r,
            x2, y2 - r,
            x2, y2,
            x2 - r, y2,
            x1 + r, y2,
            x1, y2,
            x1, y2 - r,
            x1, y1 + r,
            x1, y1
        ]
        canvas.create_polygon(points, smooth=True, fill=fill, outline=outline, width=width)

    # Create a login_box_canvas (this is a real widget placed above bg_canvas_login)
    login_box_canvas = tk.Canvas(login_root, width=420, height=380, bg="#ffffff", highlightthickness=0)
    draw_rounded_rect(login_box_canvas, 2, 2, 418, 378, r=28, fill="#ffffff", outline=GRAY90, width=2)

    # Form frame that will be embedded into login_box_canvas
    form_frame = tk.Frame(login_box_canvas, bg="#ffffff")

    tk.Label(form_frame, text="Login", font=("Arial", 22, "bold"), bg="#ffffff", fg=LIGHTCORAL).pack(pady=(18, 8))
    tk.Label(form_frame, text="Username or Email Address", bg="#ffffff", font=("Arial", 10), fg=LIGHTCORAL).pack(anchor="w", padx=20)

    username_frame, username_entry = create_rounded_entry(form_frame)
    username_frame.pack(pady=8, padx=20, fill="x")

    tk.Label(form_frame, text="Password", bg="#ffffff", font=("Arial", 10), fg=LIGHTCORAL).pack(anchor="w", padx=20)
    password_frame, password_entry = create_rounded_entry(form_frame, show_char="*")
    password_frame.pack(pady=8, padx=20, fill="x")

    # expose these entries to module-level variables
    globals()["username_entry"] = username_entry
    globals()["password_entry"] = password_entry

    login_btn = tk.Button(form_frame, text="Log In", bg=LIGHTCORAL, fg="white", font=("Arial", 12, "bold"),
                          relief="flat", activebackground=LIGHTCORAL, bd=0, padx=40, pady=7,
                          command=check_login)
    login_btn.pack(pady=(12, 20))

    def btn_on_enter(e): login_btn.config(highlightthickness=2, highlightbackground=LIGHTSALMON4, highlightcolor=LIGHTSALMON4)
    def btn_on_leave(e): login_btn.config(highlightthickness=0)
    login_btn.bind("<Enter>", btn_on_enter)
    login_btn.bind("<Leave>", btn_on_leave)
    login_btn.bind("<FocusIn>", btn_on_enter)
    login_btn.bind("<FocusOut>", btn_on_leave)

    # Put login_box_canvas centered with .place (it stays centered automatically on resize)
    login_box_canvas.place(relx=0.5, rely=0.5, anchor="center")
    # Put form_frame inside login_box_canvas (center coordinates)
    login_box_canvas.create_window(210, 190, window=form_frame)

    # Resize background image on window resize
    bg_image_tk_login = None

    def on_resize_login(event=None):
        nonlocal bg_image_tk_login
        width = login_root.winfo_width()
        height = login_root.winfo_height()
        if bg_image_login is None:
            bg_canvas_login.configure(bg="#f6f6f6")
            return
        if width < 10 or height < 10:
            return
        resized_img = bg_image_login.resize((width, height), Image.LANCZOS)
        bg_image_tk_login = ImageTk.PhotoImage(resized_img)
        bg_canvas_login.delete("all")
        bg_canvas_login.create_image(0, 0, image=bg_image_tk_login, anchor="nw")
        # login_box_canvas placed with place(relx...) will remain centered automatically

    login_root.bind("<Configure>", on_resize_login)
    on_resize_login()

    login_root.mainloop()


if __name__ == "__main__":
    build_login_window()
