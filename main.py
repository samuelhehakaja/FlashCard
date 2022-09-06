from tkinter import *
import pandas
import random


BACKGROUND_COLOR = "#B1DDC6"
random_number = 0

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    old_data = pandas.read_csv("data/french_words.csv")
    data_dict = old_data.to_dict(orient="records")
else:
    data_dict = data.to_dict(orient="records")


def next_card():
    global random_number, flip_timer
    flip_timer = window.after_cancel(flip_card)
    random_number = random.randint(0, len(data_dict))
    canvas.itemconfig(canvas_image, image=card_front)
    canvas.itemconfig(title, text="French", fill="black")
    canvas.itemconfig(word, text=f"{data_dict[random_number]['French']}", fill="black")
    flip_timer = window.after(3000, flip_card)


def flip_card():
    global random_number
    canvas.itemconfig(canvas_image, image=card_back)
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word, text=f"{data_dict[random_number]['English']}", fill="white")


def right_button():
    global random_number
    data_dict.remove(data_dict[random_number])
    data_to_learn = pandas.DataFrame(data_dict)
    data_to_learn.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# Window
window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, flip_card)

# Cards
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front)
title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

# Correct Button
correct_image = PhotoImage(file="images/right.png")
correct_button = Button(image=correct_image, highlightthickness=0, command=right_button)
correct_button.grid(column=1, row=1)

# Wrong Button
wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
wrong_button.grid(column=0, row=1)

next_card()
window.mainloop()
