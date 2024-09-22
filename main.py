import random
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class ImageRevealGame:
    def __init__(self, display, image_path, question, answers, correct_answer):

        self.display = display
        self.display.title("Game")

        self.original_img = Image.open(image_path)
        self.width, self.height = 600, 400
        self.original_img = self.original_img.resize((self.width, self.height))
        self.photo = ImageTk.PhotoImage(self.original_img)

        self.canvas = tk.Canvas(display, width=self.width, height=self.height)
        self.canvas.pack()

        self.canvas_img = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

        self.rectangles = []
        self.create_rects()

        self.shown_rects = []

        self.canvas.bind("<Button-1>", self.on_click)

        self.question = question
        self.answers = answers
        self.correct_answer = correct_answer

        self.selected = tk.StringVar()
        self.selected.trace_add("write", self.update_btn)

        self.questions_ui()

    def create_rects(self):
        rows, cols = 15, 20
        width, height = self.width // cols, self.height // rows

        for row in range(rows):
            for col in range(cols):
                x1, y1 = col * width, row * height
                x2, y2 = x1 + width, y1 + height

                if col == cols - 1:
                    x2 = self.width
                if row == rows - 1:
                    y2 = self.height

                rect = self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=self.get_color(), outline=""
                )
                self.rectangles.append(rect)

    def get_color(self):
        color = random.randint(100, 200)
        return f'#{color:02x}{color:02x}{color:02x}'

    def on_click(self, event):
        clicked = self.canvas.find_closest(event.x, event.y)[0]
        if clicked in self.rectangles and clicked not in self.shown_rects:
            self.reveal(clicked)

    def reveal(self, rect):
        self.canvas.itemconfig(rect, state='hidden')
        self.shown_rects.append(rect)

        if len(self.shown_rects) > 3:
            oldest = self.shown_rects.pop(0)
            self.canvas.itemconfig(oldest, state='normal')

    def questions_ui(self):
        frame = ttk.Frame(self.display)
        frame.pack(pady=10)

        question_label = ttk.Label(frame, text=self.question, font=('Arial', 14))
        question_label.pack()

        for answer in self.answers:
            radio_button = ttk.Radiobutton(
                frame,
                text=answer,
                variable=self.selected,
                value=answer
            )
            radio_button.pack(pady=5)

        self.check_btn = ttk.Button(frame, text="Check Answer", command=self.check_answer)
        self.check_btn.pack(pady=10)
        self.check_btn.config(state=tk.DISABLED)

    def update_btn(self, *_):
        if self.selected.get():
            self.check_btn.config(state=tk.NORMAL)
        else:
            self.check_btn.config(state=tk.DISABLED)

    def check_answer(self):
        selected = self.selected.get()
        if selected == self.correct_answer:
            result = "Correct!"
        else:
            result = "Incorrect!"

        for rect in self.rectangles:
            self.canvas.itemconfig(rect, state='hidden')
        self.check_btn.config(state=tk.DISABLED)
        messagebox.showinfo("Result", result)


if __name__ == "__main__":
    root = tk.Tk()
    game = ImageRevealGame(
        root, "img.jpg",
        "Who is it?",
        ["Albert Einstein", "Marie Curie", "Isaac Newton", "Nikola Tesla"],
        "Albert Einstein"
    )
    root.mainloop()
