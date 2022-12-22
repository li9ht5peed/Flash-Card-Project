from tkinter import *
from pandas import *
import random

BACKGROUND_COLOR = "#B1DDC6"
rand_word = {}
data_dict = {}

try:
    data = read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    origin_data = read_csv("data/french_words.csv")
    data_dict = origin_data.to_dict(orient="records")
else:
    data_dict = data.to_dict(orient="records")


def next_card():
    global rand_word, flip_timer
    window.after_cancel(flip_timer)
    rand_word = random.choice(data_dict)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=rand_word["French"], fill="black")
    canvas.itemconfig(card_bg, image=card_front)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=rand_word["English"], fill="white")
    canvas.itemconfig(card_bg, image=card_back)


def is_known():
    data_dict.remove(rand_word)
    remaining = DataFrame(data_dict)
    remaining.to_csv("data/words_to_learn.csv", index=False)
    next_card()


window = Tk()
window.title("Flash")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
card_bg = canvas.create_image(400, 263, image=card_front)
card_title = canvas.create_text(
    400, 150, text="", font=("Arial", 40, "italic"))
card_word = canvas.create_text(
    400, 263, text="", font=("Arial", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

cross = PhotoImage(file="images/wrong.png")
no_button = Button(image=cross, highlightthickness=0, command=next_card)
no_button.grid(row=1, column=0)

check = PhotoImage(file="images/right.png")
yes_button = Button(image=check, highlightthickness=0, command=is_known)
yes_button.grid(row=1, column=1)

next_card()

window.mainloop()
