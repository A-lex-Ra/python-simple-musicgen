import tkinter as tk
from tkinter import messagebox
from musicgen import PromptToMusicGenerator
from pygame import mixer

class Interface:
    def __init__(self, master, on_slider_release_functions, generate_text_functions, update_playback_functions, stop_functions, play_functions):
        self.master = master
        self.master.title("Text Generator")
        self.master.geometry("400x300")

        self.current_time = 0
        self.is_playing = False

        self.on_slider_release_functions = on_slider_release_functions
        self.generate_text_functions = generate_text_functions
        self.update_playback_functions = update_playback_functions
        self.stop_functions = stop_functions
        self.play_functions = play_functions

        self.setup_ui()

    def setup_ui(self):
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_rowconfigure(2, weight=1)
        self.master.grid_rowconfigure(3, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.text_input = tk.Text(self.master, height=5, width=40)
        self.text_input.insert("1.0", "Введите текст")
        self.text_input.config(fg='grey')
        self.text_input.grid(row=0, pady=10, padx=20, sticky='nsew')
        self.text_input.bind("<FocusIn>", self.clear_field_text)
        self.text_input.bind("<FocusOut>", self.restore_field_text)

        self.seconds_input = tk.Entry(self.master)
        self.seconds_input.insert(0, "Введите время в секундах")
        self.seconds_input.config(fg='grey')
        self.seconds_input.grid(row=1, pady=30, padx=20, sticky='nsew')
        self.seconds_input.bind("<FocusIn>", self.clear_field_seconds)
        self.seconds_input.bind("<FocusOut>", self.restore_field_seconds)

        self.generate_button = tk.Button(self.master, text="Generate", command=self.generate_text)
        self.generate_button.grid(row=2, pady=5, padx=20, sticky='nsew')

        self.slider = tk.Scale(self.master, from_=0, to=300, orient=tk.HORIZONTAL)
        self.slider.grid_remove()

        self.slider_value_label = tk.Label(self.master, text="")
        self.slider_value_label.grid_remove()

        self.play_button = tk.Button(self.master, text="Play", command=self.play)
        self.play_button.grid_remove()

        self.stop_button = tk.Button(self.master, text="Stop", command=self.stop)
        self.stop_button.grid_remove()
        
        self.slider.bind("<ButtonRelease-1>", self.on_slider_release)

    def generate_text(self):
        self.current_time = 0
        input_text = self.text_input.get("1.0", tk.END).strip()
        seconds = self.seconds_input.get().strip()
        if input_text and seconds.isdigit():
            seconds = int(seconds)

            if self.generate_text_functions:
                self.generate_text_functions[0](input_text, seconds)

            self.slider.config(to=seconds)
            self.slider.set(0)
            self.update_slider(0)

            self.slider.grid(row=3, pady=10, padx=80, sticky='ew')
            self.slider_value_label.grid(row=4, pady=5, padx=60, sticky='nsew')
            self.play_button.grid(row=5, pady=5, padx=20, sticky='nsew')
            self.stop_button.grid(row=6, pady=5, padx=20, sticky='nsew')

            self.text_input.grid_remove()
            self.seconds_input.grid_remove()
            self.generate_button.grid_remove()
        else:
            messagebox.showwarning("Ошибка ввода", "Пожалуйста, введите корректное время в секундах и текст запроса.")

    def update_slider(self, value):
        value = int(value)
        minutes = value // 60
        remaining_seconds = value % 60
        self.slider_value_label.config(text=f"Время трека: {minutes} : {remaining_seconds}")

    def play(self):
        if not self.is_playing:
            if self.play_functions:
                for func in self.play_functions:
                    func(self.current_time)
            self.is_playing = True
            self.update_playback()

    def stop(self):
        self.is_playing = False
        if self.stop_functions:
            for func in self.stop_functions:
                func()

    def update_playback(self):
        if self.is_playing and self.current_time < self.slider.cget("to"):
            self.current_time += 1
            self.slider.set(self.current_time)
            self.update_slider(self.current_time)
            self.master.after(1000, self.update_playback)
        elif self.current_time >= self.slider.cget("to"):
            self.stop()

    def on_slider_release(self, event):
        # вызов функций on_slider_release_functions
        if self.on_slider_release_functions:
            for func in self.on_slider_release_functions:
                func(self.slider.get())

        self.current_time = self.slider.get()
        self.update_slider(self.current_time)

    def clear_field_seconds(self, event):
        if self.seconds_input.get() == "Введите время в секундах":
            self.seconds_input.delete(0, tk.END)
            self.seconds_input.config(fg='black')

    def restore_field_seconds(self, event):
        if self.seconds_input.get() == "":
            self.seconds_input.insert(0, "Введите время в секундах")

    def clear_field_text(self, event):
        if self.text_input.get("1.0", tk.END).strip() == "Введите текст":
            self.text_input.delete("1.0", tk.END)
            self.text_input.config(fg='black')

    def restore_field_text(self, event):
        if self.text_input.get("1.0", tk.END).strip() == "":
            self.text_input.insert("1.0", "Введите текст")

main_window = tk.Tk()
g = PromptToMusicGenerator()

mixer.init()
def play_music(from_time):
    mixer.music.load("musicgen_out.wav")
    mixer.music.play(start=from_time)

# добавляем функции, которые хотим вызвать
app = Interface(
    main_window,
    on_slider_release_functions=[],
    generate_text_functions=[g.generate],
    update_playback_functions=[],
    stop_functions=[mixer.music.stop],
    play_functions=[play_music]
)
main_window.mainloop()
