import os
import csv
import joblib
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk

# Colors
LIGHTCORAL = "#CD5555"
GRAY90 = "#F7F7F7"
LIGHTSALMON4 = "#8B5742"
INDIANRED = "#8B3A3A"
HOVER_BG = "#FFE4E1"

CREDENTIALS_FILE = "credentials.csv"

BASE = r"K:\Kritika\Internship Project\AI Skin type Predictor\skin\ingredients"

ingredient_images = {
    "Raw milk": fr"{BASE}\raw_milk.jpg",
    "Turmeric": fr"{BASE}\turmeric.jpg",
    "Sandalwood": fr"{BASE}\sandalwood.jpg",
    "Honey": fr"{BASE}\honey.jpg",
    "Aloe vera": fr"{BASE}\aloe_vera.jpg",
    "Lemon": fr"{BASE}\lemon.jpg",
    "Ice": fr"{BASE}\ice.jpg",
    "Neem": fr"{BASE}\neem.jpg",
    "Rose water": fr"{BASE}\rose_water.jpg",
    "Cucumber extract": fr"{BASE}\cucumber_extract.jpg",
    "Multani mitti": fr"{BASE}\multani_mitti.jpg",
    "Avocado oil": fr"{BASE}\avocado_oil.jpg",
    "Coconut oil": fr"{BASE}\coconut_oil.jpg",
    "Yogurt": fr"{BASE}\yogurt.jpg",
    "Almond oil": fr"{BASE}\almond_oil.jpg",
    "Shea butter": fr"{BASE}\shea_butter.jpg",
    "Castor oil": fr"{BASE}\castor_oil.jpg",
    "Oatmeal": fr"{BASE}\oatmeal.jpg",
    "Green tea": fr"{BASE}\green_tea.jpg",
    "Chamomile": fr"{BASE}\chamomile.jpg",
    "Niacinamides": fr"{BASE}\niacinamides.jpg",
    "Apple cider vinegar": fr"{BASE}\apple_cider_vinegar.jpg",
    "Centella asiatica": fr"{BASE}\centella_asiatica.jpg",
    "Spirulina": fr"{BASE}\spirulina.jpg",
    "Oat extract": fr"{BASE}\oat_extract.jpg",
    "Tea tree oil": fr"{BASE}\tea_tree_oil.jpg",
    "Cucumber": fr"{BASE}\cucumber_extract.jpg"
}

# =======================
# Helper to check if user accounts exist
# =======================
def users_exist():
    return os.path.exists(CREDENTIALS_FILE) and os.path.getsize(CREDENTIALS_FILE) > 0

# =======================
# LANDING PAGE WINDOW
# =======================
def open_landing_page():
    landing_root = tk.Tk()
    landing_root.title("SkinSaathi")
    landing_root.state("zoomed")

    NAV_BG = "#ffffff"   # white
    NAV_HOVER = "#F7F7F7" # hover color
    NAV_FG = "#8B3A3A"    # brownish text

    # ===== NAVBAR =====
    navbar = tk.Frame(landing_root, bg=NAV_BG, height=900)  # increased height
    navbar.pack(side="top", fill="x")

    # --- Logo ---
    try:
        logo_img = Image.open("logo.png").resize((90, 90), Image.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_img)
        logo_label = tk.Label(navbar, image=logo_photo, bg=NAV_BG)
        logo_label.image = logo_photo
        logo_label.pack(side="left", padx=(10, 5), pady=10)
    except:
        logo_label = tk.Label(navbar, text="SkinSaathi", fg=NAV_FG, bg=NAV_BG,
                              font=("Arial", 20, "bold"))
        logo_label.pack(side="left", padx=10, pady=10)

    title_label = tk.Label(navbar, text="SkinSaathi", fg=NAV_FG, bg=NAV_BG,
                           font=("Arial", 22, "bold"))
    title_label.pack(side="left", padx=(5, 40), pady=10)

    # Hover effect
    def add_hover(btn, normal_bg):
        btn.bind("<Enter>", lambda e: btn.config(bg=NAV_HOVER))
        btn.bind("<Leave>", lambda e: btn.config(bg=normal_bg))

    # --- Navigation actions ---
    def open_main():
        if not users_exist():
            messagebox.showwarning("No Account", "No users registered yet! Please create an account first.")
            try:
                reg_logo_img = Image.open("logo.png").resize((150, 150), Image.LANCZOS)
                reg_logo_photo = ImageTk.PhotoImage(reg_logo_img)
            except:
                reg_logo_photo = None
            create_new_account(landing_root, reg_logo_photo)
        else:
            messagebox.showwarning("Login Required", "Please log in first to access the main app.")
            landing_root.destroy()
            build_login_window()

    def open_risks():
        messagebox.showinfo("Navigation", "Risk Detection Page Placeholder")
    def open_features():
        messagebox.showinfo("Navigation", "Features Page Placeholder")
    def open_how_it_works():
        messagebox.showinfo("Navigation", "How it Works Page Placeholder")
    def open_faq():
        messagebox.showinfo("Navigation", "FAQ Page Placeholder")
    def open_register():
        try:
            reg_logo_img = Image.open("logo.png").resize((150, 150), Image.LANCZOS)
            reg_logo_photo = ImageTk.PhotoImage(reg_logo_img)
        except:
            reg_logo_photo = None
        create_new_account(landing_root, reg_logo_photo)
    def open_login():
        landing_root.destroy()
        build_login_window()

    nav_buttons = [
        ("Main App", open_main),
        ("Risk Detection", open_risks),
        ("Features", open_features),
        ("How it works", open_how_it_works),
        ("FAQ", open_faq),
        ("Register", open_register),
        ("Login", open_login)
    ]

    for text, cmd in nav_buttons:
        btn = tk.Button(navbar, text=text, fg=NAV_FG, bg=NAV_BG,
                        font=("Arial", 16, "bold"), relief="flat",
                        activebackground=NAV_HOVER, activeforeground="white",
                        command=cmd)
        btn.pack(side="left", padx=12, pady=25)
        add_hover(btn, NAV_BG)

    # ===== Background that resizes =====
    bg_canvas = tk.Canvas(landing_root, highlightthickness=0, bd=0)
    bg_canvas.pack(fill="both", expand=True)

    try:
        bg_image_orig = Image.open("img1.JPG")
    except:
        bg_image_orig = None
        bg_canvas.configure(bg="#FFDAB9")

    bg_tk = None  # reference for dynamic image

    def resize_bg(event=None):
        nonlocal bg_tk
        bg_canvas.delete("all")
        if bg_image_orig:
            resized = bg_image_orig.resize((landing_root.winfo_width(), landing_root.winfo_height()), Image.LANCZOS)
            bg_tk = ImageTk.PhotoImage(resized)
            bg_canvas.create_image(0, 0, image=bg_tk, anchor="nw")
        else:
            bg_canvas.configure(bg="#FFDAB9")

    landing_root.bind("<Configure>", resize_bg)
    resize_bg()

    landing_root.mainloop()

# =======================
# Main App Window
# =======================
def open_main_app(parent):
    try:
        if parent:
            parent.withdraw()
    except Exception:
        pass

    main_win = tk.Toplevel()
    main_win.title("Skin Type Predictor")
    main_win.state("zoomed")

    # --- Ingredient recommendations (keys all lowercase) ---
    skin_care_ingredients = {
        "oily": [
            "Raw milk", "Turmeric", "Sandalwood", "Honey", "Aloe vera",
            "Lemon", "Ice", "Neem", "Rose water", "Cucumber extract", "Multani mitti"
        ],
        "dry": [
            "Honey", "Avocado oil", "Coconut oil", "Yogurt", "Aloe vera",
            "Cucumber extract", "Almond oil", "Shea butter", "Castor oil", "Oatmeal"
        ],
        "sensitive": [
            "Aloe vera", "Green tea", "Chamomile", "Niacinamides",
            "Apple cider vinegar", "Honey", "Centella asiatica", "Spirulina",
            "Raw milk", "Turmeric", "Oat extract", "Sandalwood", "Neem", "Tea tree oil"
        ],
        "normal": [
            "Raw milk", "Honey", "Yogurt", "Multani mitti", "Aloe vera",
            "Castor oil", "Coconut oil", "Ice", "Rose water", "Cucumber", "Lemon"
        ]
    }

    skin_care_remedies = {
    "oily": [
        "Turmeric & Multani Mitti Mask – Mix 2 tsp multani mitti + ½ tsp turmeric + rose water. Apply 15 mins.",
        "Neem & Cucumber Pack – Grind neem leaves + 2 tbsp cucumber juice. Apply 20 mins.",
        "Lemon-Honey Cleanser – Mix 1 tsp lemon juice + 1 tsp honey. Massage, then rinse.",
        "Aloe Vera & Ice Rub – Apply aloe vera gel, rub ice cube for 2 mins.",
        "Turmeric + Honey Spot Treatment → Dab on pimples, wash after 10 mins.",
        "Multani Mitti + Lemon Pack → Oil control + brightening.",
        "Neem + Aloe Vera Gel → Apply overnight for acne.",
        "Rose Water + Ice Cube Rub → Tightens pores."
        ],
    "dry": [
        "Honey & Yogurt Mask – Mix 2 tsp honey + 1 tsp yogurt. Apply 20 mins.",
        "Avocado Oil & Almond Oil Massage – Mix equal parts. Massage before bed.",
        "Oatmeal & Aloe Vera Pack – Blend 2 tbsp oatmeal + 1 tbsp aloe vera. Apply 15 mins.",
        "Shea Butter & Coconut Oil Cream – Whip shea butter + coconut oil. Apply daily.",
        "Oatmeal + Honey Scrub → Gentle exfoliation + hydration.",
        "Aloe Vera + Coconut Oil Mask → Intense moisturization.",
        "Avocado Oil + Yogurt Pack → Restores suppleness.",
        "Shea Butter Night Cream → Locks in moisture overnight."
        ],
    "sensitive": [
        "Chamomile & Aloe Vera Gel – Brew chamomile tea + aloe vera. Apply 15 mins.",
        "Green Tea & Honey Mask – Brew green tea, mix with honey. Apply 15 mins.",
        "Oat Extract & Spirulina Pack – Mix oat powder + spirulina + rose water. Apply 20 mins.",
        "Neem & Sandalwood Paste – Mix neem + sandalwood + raw milk. Apply 10–15 mins.",
        "Diluted Apple Cider Vinegar – Mix 1 part ACV + 3 parts water. Use as toner.",
        "Chamomile + Aloe Vera Pack → Soothes irritation.",
        "Green Tea + Honey Mask → Anti-redness + mild glow.",
        "Neem + Sandalwood Paste → Gentle acne control.",
        "Spirulina + Oat Extract Pack → Calms inflammation."
        ],
    "normal": [
        "Raw Milk & Honey Cleanser – Mix raw milk + honey. Massage & rinse.",
        "Aloe Vera & Cucumber Pack – Mix aloe vera gel + cucumber juice. Apply 15 mins.",
        "Multani Mitti & Rose Water Pack – Mix multani mitti + rose water. Apply 20 mins.",
        "Coconut Oil Night Massage – Apply coconut oil before bed.",
        "Ice & Lemon Rub – Freeze lemon juice + water into cubes, rub on face weekly.",
        "Milk + Lemon Cleanser → Brightens skin.",
        "Aloe Vera + Cucumber Gel → Refreshing hydration.",
        "Multani Mitti + Rose Water Pack → Detox & glow.",
        "Coconut Oil Massage (weekly) → Maintains balance."
        ]
    }

    # Load model files
    model = None
    target_encoder = None
    encoders = {}
    try:
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

    # Store last predicted skin type
    predicted_skin_type = tk.StringVar(value="")

    def predict_skin_type():
        if model is None or target_encoder is None:
            messagebox.showwarning("No Model", "Model files not loaded.")
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
            skin_type = target_encoder.inverse_transform([prediction[0]])[0].lower()
            predicted_skin_type.set(skin_type)

            result_label.config(
                text=f"Predicted Skin Type: {skin_type.capitalize()}",
                fg=INDIANRED, justify="left"
            )
            recommendation_label.config(text="")
        except Exception as e:
            result_label.config(text=f"Error: {e}", fg=INDIANRED)
            predicted_skin_type.set("")
            recommendation_label.config(text="")

    def show_recommendations():
        stype = predicted_skin_type.get()
        if not stype:
            messagebox.showinfo("No Prediction", "Please predict skin type first.")
            return

        ingredients = skin_care_ingredients.get(stype, [])
        if not ingredients:
            messagebox.showinfo("No Data", "No recommendations found for this skin type.")
            return

        # New window
        rec_win = tk.Toplevel(main_win)
        rec_win.title(f"{stype.capitalize()} Skin Recommendations")
        rec_win.state("zoomed")

        # Back button OUTSIDE the scroll area
        back_btn = tk.Button(rec_win, text="← Back", bg=LIGHTCORAL, fg="white",font=("Arial", 10, "bold"), relief="flat",command=rec_win.destroy)
        back_btn.place(x=20, y=20)

        # Container to leave space for back button
        container = tk.Frame(rec_win, bg="white")
        container.pack(fill="both", expand=True, pady=(50, 0))  # 50px top space

        # Canvas + scrollbar
        rec_canvas = tk.Canvas(container, bg="white", highlightthickness=0)
        rec_canvas.pack(side="left", fill="both", expand=True)

        v_scroll = tk.Scrollbar(container, orient="vertical", command=rec_canvas.yview)
        v_scroll.pack(side="right", fill="y")
        rec_canvas.configure(yscrollcommand=v_scroll.set)

        # Scrollable frame inside canvas
        scroll_frame = tk.Frame(rec_canvas, bg="white")
        rec_canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

        def on_frame_configure(event):
            rec_canvas.configure(scrollregion=rec_canvas.bbox("all"))
        scroll_frame.bind("<Configure>", on_frame_configure)


        # Optional mouse scroll support
        def _on_mousewheel(event):
            rec_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        rec_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        rec_canvas.bind_all("<Button-4>", lambda e: rec_canvas.yview_scroll(-3, "units"))  # Linux up
        rec_canvas.bind_all("<Button-5>", lambda e: rec_canvas.yview_scroll(3, "units"))   # Linux down

        # ====== Split into two exact halves ======
        left_frame = tk.Frame(scroll_frame, bg="white")
        right_frame = tk.Frame(scroll_frame, bg="white")

        left_frame.grid(row=0, column=0, sticky="nsew")
        right_frame.grid(row=0, column=1, sticky="nsew")

        right_frame.grid_configure(padx=(50, 20))  # extra space on left side


        # Force equal space: 50-50 split
        scroll_frame.grid_columnconfigure(0, weight=1)
        scroll_frame.grid_columnconfigure(1, weight=2)
        scroll_frame.grid_rowconfigure(0, weight=1)

        # Keep references to PhotoImage objects on the window to prevent GC
        rec_win.image_refs = []

        # ===== INGREDIENT GRID (LEFT) =====
        COLS = 4
        for idx, ingredient in enumerate(ingredients):
            row = idx // COLS
            col = idx % COLS

            img_path = ingredient_images.get(ingredient)
            try:
                if img_path and os.path.exists(img_path):
                    img = Image.open(img_path).resize((200, 200), Image.LANCZOS)
                else:
                    raise FileNotFoundError(f"Image not found: {img_path}")
                img_tk = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"[WARN] {ingredient}: {e}")
                img = Image.new("RGB", (200, 200), color="lightgray")
                img_tk = ImageTk.PhotoImage(img)

            rec_win.image_refs.append(img_tk)

            # Card
            card = tk.Frame(left_frame, bg="white", bd=2, relief="groove")
            card.grid(row=row, column=col, padx=10, pady=10, sticky="n")

            tk.Label(card, image=img_tk, bg="white").pack(padx=6, pady=6)
            tk.Label(card, text=ingredient, font=("Arial", 11, "bold"),
                     bg="white", fg=INDIANRED).pack(pady=(0, 6))

        # ===== REMEDIES LIST (RIGHT) =====
        # Allow both frames to expand vertically
        scroll_frame.grid_rowconfigure(0, weight=1)

        # Remedies container: stretch fully
        remedies_container = tk.Frame(right_frame, bg="white")
        remedies_container.pack(fill="both", expand=True, anchor="n")  # expand vertically too

        tk.Label(
            remedies_container, text="Home Remedies",
            font=("Arial",20, "bold"), bg="white", fg=INDIANRED
        ).pack(anchor="w", pady=(0, 15))

        remedies = skin_care_remedies.get(stype, [])
        WRAP = 520  # line wrap length

        tk.Label(
            remedies_container,
            text=f"Skin Type: {stype.capitalize()} • {len(remedies)} remedies",
            font=("Arial", 10, "italic"), bg="white", fg="#555"
        ).pack(anchor="w", pady=(0, 10))

        for remedy in remedies:
            tk.Label(
                remedies_container, text=f"• {remedy}",
                wraplength=WRAP, justify="left",
                font=("Arial", 14), bg="white", fg="black"
            ).pack(anchor="w", pady=8)

  


    # Background
    try:
        bg_image_main = Image.open("img.jpg")
    except Exception:
        bg_image_main = None

    bg_canvas = tk.Canvas(main_win, highlightthickness=0)
    bg_canvas.pack(fill="both", expand=True)
    bg_image_tk_main = None

    form_frame_main = tk.Frame(bg_canvas, bg="#ffffff", padx=20, pady=20)

    def add_hover_effect(widget, normal_bg):
        widget.bind("<Enter>", lambda e: widget.configure(background=HOVER_BG))
        widget.bind("<Leave>", lambda e: widget.configure(background=normal_bg))

    # Larger font & bigger entry boxes
    entry_font = ("Arial", 12, "bold")
    label_font = ("Arial", 12, "bold")

    fields = {
        "Age": tk.Entry(form_frame_main, bg=GRAY90, fg=INDIANRED, relief="flat", font=entry_font, width=20),
        "Gender": ttk.Combobox(form_frame_main, values=encoders["gender"].classes_.tolist(), font=entry_font, width=18, foreground=INDIANRED),
        "Water Intake (liters)": tk.Entry(form_frame_main, bg=GRAY90, fg=INDIANRED, relief="flat", font=entry_font, width=20),
        "Weather": ttk.Combobox(form_frame_main, values=encoders["weather"].classes_.tolist(), font=entry_font, width=18, foreground=INDIANRED),
        "Oiliness": ttk.Combobox(form_frame_main, values=encoders["oiliness"].classes_.tolist(), font=entry_font, width=18, foreground=INDIANRED),
        "Acne": ttk.Combobox(form_frame_main, values=encoders["acne"].classes_.tolist(), font=entry_font, width=18, foreground=INDIANRED),
        "Tightness After Wash": ttk.Combobox(form_frame_main, values=encoders["tightness_after_wash"].classes_.tolist(), font=entry_font, width=18, foreground=INDIANRED),
        "Makeup Usage": ttk.Combobox(form_frame_main, values=encoders["makeup_usage"].classes_.tolist(), font=entry_font, width=18, foreground=INDIANRED),
        "Flaking": ttk.Combobox(form_frame_main, values=encoders["flaking"].classes_.tolist(), font=entry_font, width=18, foreground=INDIANRED),
        "Redness/Itchiness": ttk.Combobox(form_frame_main, values=encoders["redness_itchiness"].classes_.tolist(), font=entry_font, width=18, foreground=INDIANRED)
    }

    # Arrange in 5 columns, label above input
    items = list(fields.items())
    col_count = 5
    for i, (label_text, widget) in enumerate(items):
        col = i % col_count
        row = (i // col_count) * 2

        tk.Label(form_frame_main, text=label_text, bg="#ffffff", fg=LIGHTCORAL, font=label_font)\
            .grid(row=row, column=col, padx=10, pady=(5, 0), sticky="w")

        widget.grid(row=row+1, column=col, padx=10, pady=(0, 15), sticky="we")
        add_hover_effect(widget, GRAY90 if isinstance(widget, tk.Entry) else "white")

    total_rows = ((len(items) + col_count - 1) // col_count) * 2
    result_label = tk.Label(form_frame_main, text="", font=("Arial", 14, "bold"),
                            fg=LIGHTCORAL, bg="#ffffff", justify="left")
    result_label.grid(row=total_rows, column=0, columnspan=col_count, pady=10)

    predict_button = tk.Button(form_frame_main, text="Predict", bg=LIGHTCORAL, fg="white",
                               font=("Arial", 12, "bold"), relief="flat", command=predict_skin_type)
    predict_button.grid(row=total_rows+1, column=0, columnspan=col_count, pady=5)

    recommend_button = tk.Button(form_frame_main, text="Show Recommendations", bg=LIGHTCORAL, fg="white",
                             font=("Arial", 12, "bold"), relief="flat", command=show_recommendations)

    recommend_button.grid(row=total_rows+2, column=0, columnspan=col_count, pady=5)

    recommendation_label = tk.Label(form_frame_main, text="", font=("Arial", 12 , "bold"),
                                     fg=INDIANRED, bg="#ffffff", justify="left")
    recommendation_label.grid(row=total_rows+3, column=0, columnspan=col_count, pady=10)

    back_button = tk.Button(main_win, text="← Back", bg=LIGHTCORAL, fg="white",
                            font=("Arial", 10, "bold"), relief="flat",
                            command=lambda: (main_win.destroy(), parent.deiconify()))

    def resize_main_bg(event=None):
        nonlocal bg_image_tk_main
        width = main_win.winfo_width()
        height = main_win.winfo_height()
        bg_canvas.delete("all")
        if bg_image_main:
            resized_main_bg = bg_image_main.resize((width, height), Image.LANCZOS)
            bg_image_tk_main = ImageTk.PhotoImage(resized_main_bg)
            bg_canvas.create_image(0, 0, image=bg_image_tk_main, anchor="nw")
        else:
            bg_canvas.configure(bg="#f0f0f0")
        bg_canvas.create_window(width // 2, height // 2, window=form_frame_main)
        bg_canvas.create_window(20, 20, window=back_button, anchor="nw")

    main_win.bind("<Configure>", resize_main_bg)
    resize_main_bg()

    
# =======================
# Create New Account
# =======================
def create_new_account(parent, logo_photo):
    reg_win = tk.Toplevel(parent)
    reg_win.title("Create New Account")
    reg_win.state("zoomed")

    try:
        bg_image = Image.open("img.jpg")
    except:
        bg_image = None

    bg_canvas = tk.Canvas(reg_win, highlightthickness=0)
    bg_canvas.pack(fill="both", expand=True)

    outer_frame = tk.Frame(bg_canvas, bg="#ffffff")

    # Logo on left
    logo_frame = tk.Frame(outer_frame, bg="#ffffff", padx=20, pady=20)
    if logo_photo:
        tk.Label(logo_frame, image=logo_photo, bg="#ffffff").pack(expand=True)
    logo_frame.grid(row=0, column=0, sticky="nsew")

    # Hover effect
    def add_hover_effect(widget, normal_bg):
        widget.bind("<Enter>", lambda e: widget.configure(background=HOVER_BG))
        widget.bind("<Leave>", lambda e: widget.configure(background=normal_bg))

    # Unified font
    unified_font = ("Arial", 11, "bold")

    # Form on right
    form_box = tk.Frame(outer_frame, bg="#ffffff", padx=30, pady=30)

    # Back Button
    back_button = tk.Button(form_box, text="← Back", bg=LIGHTCORAL, fg="white",
                            font=("Arial", 10, "bold"), relief="flat",
                            command=lambda: (reg_win.destroy(), parent.deiconify()))
    back_button.pack(anchor="w", pady=(0, 15))
    add_hover_effect(back_button, LIGHTCORAL)

    tk.Label(form_box, text="Create a SkinSaathi Account", font=("Arial", 18, "bold"), bg="#ffffff", fg=LIGHTCORAL)\
        .pack(pady=(0, 15))

    tk.Label(form_box, text="Full Name", bg="#ffffff", font=unified_font, fg=LIGHTCORAL).pack(anchor="w")
    full_name = tk.Entry(form_box, bg=GRAY90, fg=INDIANRED, relief="flat", font=unified_font)
    full_name.pack(pady=5, fill="x")
    add_hover_effect(full_name, GRAY90)

    tk.Label(form_box, text="Username", bg="#ffffff", font=unified_font, fg=LIGHTCORAL).pack(anchor="w")
    new_username = tk.Entry(form_box, bg=GRAY90, fg=INDIANRED, relief="flat", font=unified_font)
    new_username.pack(pady=5, fill="x")
    add_hover_effect(new_username, GRAY90)

    tk.Label(form_box, text="Password", bg="#ffffff", font=unified_font, fg=LIGHTCORAL).pack(anchor="w")
    new_password = tk.Entry(form_box, show="*", bg=GRAY90, fg=INDIANRED, relief="flat", font=unified_font)
    new_password.pack(pady=5, fill="x")
    add_hover_effect(new_password, GRAY90)

    tk.Label(form_box, text="Confirm Password", bg="#ffffff", font=unified_font, fg=LIGHTCORAL).pack(anchor="w")
    confirm_password = tk.Entry(form_box, show="*", bg=GRAY90, fg=INDIANRED, relief="flat", font=unified_font)
    confirm_password.pack(pady=5, fill="x")
    add_hover_effect(confirm_password, GRAY90)

    def save_user():
        if not all([full_name.get().strip(), new_username.get().strip(), new_password.get().strip(), confirm_password.get().strip()]):
            messagebox.showerror("Error", "All fields are required!")
            return
        if new_password.get().strip() != confirm_password.get().strip():
            messagebox.showerror("Error", "Passwords do not match!")
            return
        file_exists = os.path.exists(CREDENTIALS_FILE)
        if file_exists:
            with open(CREDENTIALS_FILE, newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row["username"] == new_username.get().strip():
                        messagebox.showerror("Error", "Username already exists!")
                        return
        with open(CREDENTIALS_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["name", "username", "password"])
            writer.writerow([full_name.get().strip(), new_username.get().strip(), new_password.get().strip()])
        messagebox.showinfo("Success", "Account created successfully!")
        reg_win.destroy()

    create_btn = tk.Button(form_box, text="Create Account", command=save_user,
                           bg=LIGHTCORAL, fg="white", font=("Arial", 12, "bold"), relief="flat")
    create_btn.pack(pady=15)
    add_hover_effect(create_btn, LIGHTCORAL)

    form_box.grid(row=0, column=1, sticky="nsew")

    def resize_bg(event=None):
        if bg_image:
            resized_bg = bg_image.resize((reg_win.winfo_width(), reg_win.winfo_height()), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(resized_bg)
            bg_canvas.image = img_tk
            bg_canvas.delete("all")
            bg_canvas.create_image(0, 0, image=img_tk, anchor="nw")
        else:
            bg_canvas.configure(bg="#f0f0f0")
        bg_canvas.create_window(reg_win.winfo_width() // 2, reg_win.winfo_height() // 2, window=outer_frame)

    reg_win.bind("<Configure>", resize_bg)
    resize_bg()


# =======================
# Login Window
# =======================
def build_login_window():
    login_root = tk.Tk()
    login_root.title("Login Page")
    login_root.state("zoomed")

    # Load logo after root exists
    try:
        logo_img = Image.open(r"K:\Kritika\Internship Project\AI Skin type Predictor\skin\logo.png").resize((200, 200), Image.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_img)
    except Exception as e:
        logo_photo = None
        print("Logo load error:", e)

    try:
        bg_image_login = Image.open("img.jpg")
    except:
        bg_image_login = None

    bg_canvas_login = tk.Canvas(login_root, highlightthickness=0)
    bg_canvas_login.pack(fill="both", expand=True)

    outer_frame = tk.Frame(bg_canvas_login, bg="#ffffff")

    # Logo on left
    logo_frame = tk.Frame(outer_frame, bg="#ffffff", padx=20, pady=20)
    if logo_photo:
        tk.Label(logo_frame, image=logo_photo, bg="#ffffff").pack(expand=True)
    logo_frame.grid(row=0, column=0, sticky="nsew")

    # Hover effect function
    def add_hover_effect(widget, normal_bg):
        widget.bind("<Enter>", lambda e: widget.configure(background=HOVER_BG))
        widget.bind("<Leave>", lambda e: widget.configure(background=normal_bg))

    # Unified fonts
    unified_font = ("Arial", 11, "bold")

    # Login form on right
    form_box = tk.Frame(outer_frame, bg="#ffffff", padx=30, pady=30)

    # ===== BACK BUTTON =====
    back_button = tk.Button(form_box, text="← Back", bg=LIGHTCORAL, fg="white",
                            font=("Arial", 10, "bold"), relief="flat",
                            command=lambda: (login_root.destroy(), open_landing_page()))
    back_button.pack(anchor="w", pady=(0, 15))
    add_hover_effect(back_button, LIGHTCORAL)
    
    tk.Label(form_box, text="Login", font=("Arial", 22, "bold"), bg="#ffffff", fg=LIGHTCORAL).pack(pady=(18, 8))

    tk.Label(form_box, text="Username or Email Address", bg="#ffffff", font=unified_font, fg=LIGHTCORAL).pack(anchor="w")
    username_entry = tk.Entry(form_box, bg=GRAY90, fg=INDIANRED, relief="flat", font=unified_font)
    username_entry.pack(pady=5, fill="x")
    add_hover_effect(username_entry, GRAY90)

    tk.Label(form_box, text="Password", bg="#ffffff", font=unified_font, fg=LIGHTCORAL).pack(anchor="w")
    password_entry = tk.Entry(form_box, show="*", bg=GRAY90, fg=INDIANRED, relief="flat", font=unified_font)
    password_entry.pack(pady=5, fill="x")
    add_hover_effect(password_entry, GRAY90)

    def check_login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        if not os.path.exists(CREDENTIALS_FILE):
            messagebox.showerror("Login Failed", "No users registered yet!")
            return
        with open(CREDENTIALS_FILE, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["username"] == username and row["password"] == password:
                    open_main_app(login_root)
                    return
        messagebox.showerror("Login Failed", "Invalid Username or Password")

    login_btn = tk.Button(form_box, text="Log In", bg=LIGHTCORAL, fg="white", font=("Arial", 12, "bold"), relief="flat",
                          command=check_login)
    login_btn.pack(pady=(12, 10))
    add_hover_effect(login_btn, LIGHTCORAL)

    create_account_btn = tk.Button(form_box, text="Create New Account", bg="white", fg="blue", font=("Arial", 10, "bold"),
                                   relief="flat", command=lambda: create_new_account(login_root, logo_photo))
    create_account_btn.pack(pady=(0, 20))
    add_hover_effect(create_account_btn, "white")

    form_box.grid(row=0, column=1, sticky="nsew")

    def on_resize_login(event=None):
        if bg_image_login:
            resized_img = bg_image_login.resize((login_root.winfo_width(), login_root.winfo_height()), Image.LANCZOS)
            bg_img_tk = ImageTk.PhotoImage(resized_img)
            bg_canvas_login.image = bg_img_tk
            bg_canvas_login.delete("all")
            bg_canvas_login.create_image(0, 0, image=bg_img_tk, anchor="nw")
        else:
            bg_canvas_login.configure(bg="#f6f6f6")
        bg_canvas_login.create_window(login_root.winfo_width() // 2, login_root.winfo_height() // 2, window=outer_frame)

    login_root.bind("<Configure>", on_resize_login)
    on_resize_login()
    login_root.mainloop()


if __name__ == "__main__":
    open_landing_page()

