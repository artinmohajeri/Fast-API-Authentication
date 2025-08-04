import customtkinter as ctk
from tkinter import messagebox
from APIs import *
import json

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Window setup
        self.title("User System")
        self.geometry("600x700")
        self.resizable(True, True)
        
        # Theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        
        # Main container
        self.container = ctk.CTkFrame(self, corner_radius=16)
        self.container.pack(pady=40, padx=40, fill="both", expand=True)
        
        # Toggle between login/signup
        self.toggle_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.toggle_frame.pack(pady=20)
        
        self.toggle_var = ctk.StringVar(value="login")
        self.login_tab = ctk.CTkButton(
            self.toggle_frame, 
            text="Login",
            command=lambda: self.toggle_view("login"),
            width=100,
            corner_radius=8,
            fg_color=("#3a7ebf", "#1f538d") if self.toggle_var.get() == "login" else "transparent",
            hover_color=("#3a7ebf", "#1f538d"),
            border_width=2,
            border_color="#1f538d"
        )
        self.login_tab.pack(side="left", padx=5)
        
        self.signup_tab = ctk.CTkButton(
            self.toggle_frame, 
            text="Sign Up",
            command=lambda: self.toggle_view("signup"),
            width=100,
            corner_radius=8,
            fg_color=("#3a7ebf", "#1f538d") if self.toggle_var.get() == "signup" else "transparent",
            hover_color=("#3a7ebf", "#1f538d"),
            border_width=2,
            border_color="#1f538d"
        )
        self.signup_tab.pack(side="left", padx=5)
        
        # Login Frame
        self.login_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        
        self.login_label = ctk.CTkLabel(
            self.login_frame, 
            text="Login to your account",
            font=("Arial", 16)
        )
        self.login_label.pack(pady=10)
        
        self.login_username = ctk.CTkEntry(
            self.login_frame,
            placeholder_text="Username",
            width=220,
            height=40,
            corner_radius=8
        )
        self.login_username.pack(pady=10)
        
        self.login_password = ctk.CTkEntry(
            self.login_frame,
            placeholder_text="Password",
            width=220,
            height=40,
            corner_radius=8,
            show="*"
        )
        self.login_password.pack(pady=10)
        
        self.login_button = ctk.CTkButton(
            self.login_frame,
            text="Login",
            command=self.login_action,
            width=220,
            height=40,
            corner_radius=8,
            hover_color="#2a6fc7"
        )
        self.login_button.pack(pady=20)
        
        # Signup Frame
        self.signup_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        
        self.signup_label = ctk.CTkLabel(
            self.signup_frame, 
            text="Create new account",
            font=("Arial", 16)
        )
        self.signup_label.pack(pady=10)
        
        self.signup_username = ctk.CTkEntry(
            self.signup_frame,
            placeholder_text="Username",
            width=220,
            height=40,
            corner_radius=8
        )
        self.signup_username.pack(pady=10)
        
        self.signup_password = ctk.CTkEntry(
            self.signup_frame,
            placeholder_text="Password",
            width=220,
            height=40,
            corner_radius=8,
            show="*"
        )
        self.signup_password.pack(pady=10)
        
        self.signup_button = ctk.CTkButton(
            self.signup_frame,
            text="Sign Up",
            command=self.signup_action,
            width=220,
            height=40,
            corner_radius=8,
            hover_color="#2a6fc7"
        )
        self.signup_button.pack(pady=20)
        
        # User List Frame (hidden initially)
        self.user_list_frame = ctk.CTkFrame(self, fg_color="transparent")
        
        self.user_list_label = ctk.CTkLabel(
            self.user_list_frame,
            text="Registered Users",
            font=("Arial", 16)
        )
        self.user_list_label.pack(pady=20)
        
        self.user_listbox = ctk.CTkScrollableFrame(
            self.user_list_frame,
            width=400,
            height=300,
            fg_color=("#f0f0f0", "#2b2b2b"),
            corner_radius=8
        )
        self.user_listbox.pack()
        
        self.back_button = ctk.CTkButton(
            self.user_list_frame,
            text="Back to Login",
            command=self.show_login,
            width=220,
            height=40,
            corner_radius=8,
            hover_color="#2a6fc7"
        )
        self.back_button.pack(pady=20)
        
        # Show initial view
        self.toggle_view("login")
    
    def toggle_view(self, view):
        self.toggle_var.set(view)
        
        if view == "login":
            self.login_tab.configure(fg_color=("#3a7ebf", "#1f538d"))
            self.signup_tab.configure(fg_color="transparent")
            self.signup_frame.pack_forget()
            self.user_list_frame.pack_forget()
            self.login_frame.pack()
        else:
            self.signup_tab.configure(fg_color=("#3a7ebf", "#1f538d"))
            self.login_tab.configure(fg_color="transparent")
            self.login_frame.pack_forget()
            self.user_list_frame.pack_forget()
            self.signup_frame.pack()
    
    def show_user_list(self):
        self.login_frame.pack_forget()
        self.signup_frame.pack_forget()
        self.user_list_frame.pack(pady=40, padx=40, fill="both", expand=True)
        
        # Clear existing users
        for widget in self.user_listbox.winfo_children():
            widget.destroy()
        
        # Add sample users (replace with your actual users later)
        sample_users = ["user1", "user2", "user3"]
        all_users_result = get_all_users_fetch()
        all_users_result_list = json.loads(all_users_result.text)["users"]
        print(all_users_result)
        for user in all_users_result_list:
            user_frame = ctk.CTkFrame(
                self.user_listbox,
                corner_radius=8,
                fg_color=("#e0e0e0", "#3a3a3a")
            )
            ctk.CTkButton(
                bg_color="red",
                text="delete",
            )
            user_frame.pack(fill="x", pady=5, padx=5)
            
            ctk.CTkLabel(
                user_frame,
                text=user,
                font=("Arial", 12)
            ).pack(pady=8, padx=10)
    
    def show_login(self):
        self.user_list_frame.pack_forget()
        self.toggle_view("login")
    
    def login_action(self):
        username = self.login_username.get()
        password = self.login_password.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill all fields")
            return
        
        login_result = login_fetch(username=username, passowrd=password)
        
        if login_result.status_code == 200:
            messagebox.showinfo("Success", "Login successful ✅✅✅")
            self.show_user_list()
        else:
            login_result = json.loads(login_result.text)
            print(login_result)
            messagebox.showerror("Error", f"{login_result["detail"]}")
            return
    
    def signup_action(self):
        username = self.signup_username.get()
        password = self.signup_password.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill all fields")
            return
    
        signup_result = signup_fetch(username=username, password=password)

        
        if signup_result.status_code == 200:
    
            messagebox.showinfo("Success", "Account created successfully ✅✅✅")
            self.toggle_view("login")
        else:
            signup_result = json.loads(signup_result.text)
            print(signup_result)
            messagebox.showerror("Error", f"{signup_result["detail"]}")
            return

if __name__ == "__main__":
    app = App()
    app.mainloop()