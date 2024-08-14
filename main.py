from tkinter import ttk
from tkinter import *
from PIL import Image, ImageFont, ImageDraw
from tkinterdnd2 import TkinterDnD, DND_FILES


# ---------- WATERMARK TEXT ----------
def text_watermark(image_file_paths, user_input):
    for file in image_file_paths:
        # open image
        image = Image.open(file)

        # make watermark image able to be drawn on
        draw = ImageDraw.Draw(image)
        # watermark text
        watermark_text = user_input

        # set font and font size based on image size
        img_width, img_height = image.size
        font_size = min(img_width, img_height) // 20

        font = ImageFont.load_default(font_size)

        # add Watermark
        _, _, text_width, text_height = draw.textbbox((0, 0), watermark_text, font=font)
        position = (img_width - text_width - 5, img_height - text_height - 5)  # 10px of padding
        draw.text(position, text=watermark_text, fill=(0, 0, 0), font=font, anchor='ms')
        return image.show()


# ---------- WATERMARK IMAGE ----------
def image_watermark(image_file_paths, watermark_file_paths):
    for watermark in watermark_file_paths:
        for images in image_file_paths:
            # open image
            image = Image.open(images)
            watermark_image = Image.open(watermark)

            # size up the watermark image
            target_width = 100

            aspect_ratio = float(target_width) / watermark_image.width
            target_height = int(watermark_image.height * aspect_ratio)

            watermark = watermark_image.resize((target_width, target_height))

            # position watermark
            position = (image.width - watermark.width - 20, image.height - watermark.height - 20)
            # apply watermark
            image.paste(watermark, position, watermark.convert("L") if watermark != "L" else watermark)
            # show end result
            image.show()


def error_window():
    # Create window
    error_popup = Toplevel(window)
    error_popup.title('Error')
    error_popup.minsize(width=100, height=100)
    error_popup.config(padx=10, pady=10)

    # display error message
    error_text = Label(error_popup,
                       text='Please submit one image at a time')
    error_text.grid(row=0, column=0, pady=20)

    close_button = Button(error_popup, text='close', command=error_popup.destroy, width=10, relief='groove')
    close_button.grid(row=2, column=0, sticky='e')


def clear_drop_box(dropbox, frame):
    dropbox.delete(0, END)
    if frame == window:
        window_file_paths.clear()
    else:
        dynamic_window_file_paths.clear()


def drag_and_drop_box(frame):
    # Create a Listbox to display the dropped files
    listbox = Listbox(frame, width=80, height=10)
    listbox.pack(pady=10)

    # Function to handle dropped files
    def drop(event):
        files = frame.tk.splitlist(event.data)
        for file in files:
            listbox.insert(END, file)

            if frame == window:
                # allows one file at a time
                if len(window_file_paths) < 1:
                    window_file_paths.append(file)
                else:
                    error_window()
                    listbox.delete(0, END)
                    window_file_paths.clear()
                    break
            else:
                # allows one file at a time
                if len(dynamic_window_file_paths) < 1:
                    dynamic_window_file_paths.append(file)
                else:
                    error_window()
                    listbox.delete(0, END)
                    dynamic_window_file_paths.clear()
                    break

    # Register the Listbox as a drop target
    listbox.drop_target_register(DND_FILES)
    listbox.dnd_bind('<<Drop>>', drop)

    clear_button = Button(frame, text="Clear", command=lambda: clear_drop_box(listbox, frame))
    clear_button.pack(pady=5)


def on_select(event):
    # get the option the user chose
    selected_option = selection.get()

    # remove the following widgets when a different option is selected
    for widget in dynamic_window.winfo_children():
        widget.destroy()

    if selected_option == options[0]:  # Text method watermark
        input_label = Label(dynamic_window, text="Enter the Text to be used as a Watermark:")
        input_label.pack(pady=5)

        # user input text to be used as watermark
        user_input = Entry(dynamic_window, width=15)
        user_input.pack(pady=5)

        submit_button = Button(dynamic_window,
                               text="Submit",
                               command=lambda: text_watermark(window_file_paths, user_input.get()))
        submit_button.pack(pady=5)

    elif selected_option == options[1]:  # Image method watermark
        drag_and_drop_box(dynamic_window)
        submit_button = Button(dynamic_window,
                               text="Submit",
                               command=lambda: image_watermark(window_file_paths, dynamic_window_file_paths))
        submit_button.pack(pady=5)


# Stored File paths
window_file_paths = []
dynamic_window_file_paths = []

# ---------- GUI ----------

# Create the main application window
window = TkinterDnD.Tk()
window.title("Drag and Drop Files")
window.geometry("600x400")

drop_img_label = Label(window, text="Drag and Drop Files to be Watermarked Here:", font=("ThaleahFat", 20))
drop_img_label.pack(pady=10)

# Create drag and drop box
drag_and_drop_box(window)

select_watermark_method_label = Label(window, text="Select Method of Watermarking", font=("ThaleahFat", 20))
select_watermark_method_label.pack(pady=10)

# Create dropdown selection
options = ["Watermark with text", "Watermark with an image"]
selection = ttk.Combobox(window, values=options, state="readonly")
selection.set("Select an option")
selection.pack()

# create a container for the widgets created after selecting an option
dynamic_window = Frame(window)
dynamic_window.pack(pady=5)

# Bind the select event
selection.bind("<<ComboboxSelected>>", on_select)

window.mainloop()
