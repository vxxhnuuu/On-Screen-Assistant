import tkinter as tk
from tkinter import Toplevel
from PIL import Image, ImageGrab, ImageTk
import google.generativeai as genai
import html
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the API_KEY from the environment variables
API_KEY = os.getenv("API_KEY")
CUSTOM_PROMPT = "Give Solution to all questions in the image and return both question and its answer."


class FloatingRoundWindowApp:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)  # Remove window borders
        self.root.geometry("50x50")  # Set the window size smaller for a smaller button
        self.root.attributes("-topmost", True)  # Keep window always on top

        # Make the window background transparent (Windows specific)
        self.root.wm_attributes("-transparentcolor", "black")

        # Create a canvas with a black background to match the transparent color
        self.canvas = tk.Canvas(root, width=50, height=50, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Draw the gradient button
        self.draw_gradient_circle()

        # Bind the floating button click to take a screenshot
        self.canvas.tag_bind("circle", "<Button-1>", self.take_screenshot)

        # Bind the canvas for dragging
        self.canvas.bind("<Button-1>", self.start_move)
        self.canvas.bind("<B1-Motion>", self.on_move)
        self.canvas.bind("<ButtonRelease-1>", self.stop_move)

        self.is_dragging = False  # Flag to check if the button is being dragged

    def draw_gradient_circle(self):
        """Draw a gradient circle transitioning from blue to white."""
        for i in range(20):
            color = self.get_gradient_color(i / 20)
            # Create a slightly smaller oval for each step in the gradient
            self.canvas.create_oval(5 + i, 5 + i, 45 - i, 45 - i, fill=color, outline="", tags="circle")

    def get_gradient_color(self, t):
        """Generate a color in the gradient from blue to white."""
        r = int(255 * t)  # Red value increases from 0 to 255
        g = int(255 * t)  # Green value increases from 0 to 255
        b = 255  # Blue value remains constant
        return f'#{r:02x}{g:02x}{b:02x}'  # Return the hex color code

    def take_screenshot(self, event):
        """Take a screenshot of the entire screen and display it in a new window."""
        # Capture the entire screen
        self.screenshot = ImageGrab.grab()  # Capture the entire screen
        self.show_screenshot_window(self.screenshot)  # Show the screenshot in a new window

    def show_screenshot_window(self, screenshot):
        """Display the screenshot in a new window with half screen dimensions."""
        # Create a new window for the screenshot
        self.screenshot_window = Toplevel(self.root)
        self.screenshot_window.title("Screenshot")

        # Get the screen dimensions
        screen_width = self.screenshot_window.winfo_screenwidth()
        screen_height = self.screenshot_window.winfo_screenheight()

        # Resize the screenshot to half the screen dimensions
        new_width = screen_width // 2
        new_height = screen_height // 2 + 100  # Increase the height by 100 pixels for the button
        screenshot = screenshot.resize((new_width, new_height - 100), Image.LANCZOS)  # Adjust for button height

        # Convert the screenshot to PhotoImage for display
        self.photo = ImageTk.PhotoImage(screenshot)

        # Create a label to display the image
        image_label = tk.Label(self.screenshot_window, image=self.photo)
        image_label.pack()

        # Set the window size to half the screen dimensions with increased height
        self.screenshot_window.geometry(f"{new_width}x{new_height}")

        # Center the window on the screen
        x = (screen_width // 2) - (new_width // 2)
        y = (screen_height // 2) - (new_height // 2)
        self.screenshot_window.geometry(f"+{x}+{y}")

        # Create a frame for the button at the bottom
        button_frame = tk.Frame(self.screenshot_window)
        button_frame.pack(side=tk.BOTTOM, pady=20)  # Add padding at the bottom

        # Create "Generate Response" button to save the screenshot
        generate_button = tk.Button(button_frame, text="Generate Response",
                                     command=lambda: self.generate_response(screenshot, self.screenshot_window))
        generate_button.pack(side=tk.LEFT, padx=20)  # Add padding to the button
        generate_button.config(width=20)  # Set button width

        # Create "Close" button to close the screenshot window
        close_button = tk.Button(button_frame, text="Close", command=self.screenshot_window.destroy)
        close_button.pack(side=tk.RIGHT, padx=20)  # Add padding to the button
        close_button.config(width=20)  # Set button width

    def configure_api(self):
        """Configure the Gemini API."""
        if not API_KEY:
            raise ValueError("API key is not set.")
        genai.configure(api_key=API_KEY)

    def generate_response(self, image, screenshot_window):
        """Generate a response from the image captured."""
        self.configure_api()  # Configure API

        # Combine the custom prompt with the user's text input
        prompt_full = CUSTOM_PROMPT
        
        try:
            # Load the image using PIL
            image_path = "screenshot.png"
            image.save(image_path)  # Save the image temporarily for API processing
            
            # Initialize the model (replace 'gemini-1.5-pro' with your actual model identifier)
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            # Send the combined text prompt and image to the model
            response = model.generate_content([prompt_full, image])

            if response:
                # Decode HTML entities and clean up any extra symbols in the response
                decoded_response = html.unescape(response.text)
                cleaned_response = decoded_response.replace('*', '').replace('**', '').strip()  # Clean response
                
                # Close the screenshot window
                screenshot_window.destroy()
                
                # Display the response in a new window
                self.display_response_window(cleaned_response)  # Open a new window to display the response
            else:
                print("No response generated.")
        
        except Exception as e:
            print(f"Error: {str(e)}")  # Print error message

    def display_response_window(self, response_text):
        """Display the generated response in a new window."""
        response_window = Toplevel(self.root)
        response_window.title("Generated Response")

        # Create a label to display the response
        response_label = tk.Label(response_window, text=response_text, wraplength=400, justify="left")
        response_label.pack(padx=20, pady=20)

        # Create a close button for the response window
        close_button = tk.Button(response_window, text="Close", command=response_window.destroy)
        close_button.pack(pady=10)

    def start_move(self, event):
        # Record the starting point
        self.x = event.x
        self.y = event.y
        self.is_dragging = True  # Set dragging flag

    def on_move(self, event):
        # Calculate the new position
        x_offset = event.x - self.x
        y_offset = event.y - self.y
        new_x = self.root.winfo_x() + x_offset
        new_y = self.root.winfo_y() + y_offset
        # Move the window to the new position
        self.root.geometry(f"+{new_x}+{new_y}")

    def stop_move(self, event):
        self.is_dragging = False  # Clear dragging flag


# Initialize and run the app
if __name__ == "__main__":
    root = tk.Tk()
    FloatingRoundWindowApp(root)
    root.mainloop()
