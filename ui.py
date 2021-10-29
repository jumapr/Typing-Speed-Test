import tkinter as tk
from tkinter import messagebox
from test_data import TypingTest

INSTRUCTIONS = "Type as much as you can in one minute. Click in the box to start the test."
BG_COLOR = '#dddddd'


class Interface:
    """Handles all GUI operations"""

    def __init__(self):
        # create an instance of a Typing Test
        self.test = TypingTest()

        # Create the main window
        self.window = tk.Tk()
        self.window.title('Typing Speed Test')
        self.window.configure(padx=30, pady=30, bg=BG_COLOR)

        # Create the change test button
        self.change_test_button = tk.Button(self.window, text='Change test', font='Verdana', background='#6fa8dc',
                                            command=self.change_test)
        self.change_test_button.grid(row=0, column=0)

        # Create the test instructions
        self.instructions = tk.Label(self.window, text=INSTRUCTIONS, font='Verdana', bg=BG_COLOR)
        self.instructions.grid(row=0, column=1)

        # Create high score label
        self.high_score_label = tk.Label(self.window, text=f"Best score: {self.test.high_score}", font='Verdana',
                                         bg=BG_COLOR)
        self.high_score_label.grid(row=0, column=0, padx=10, pady=20, sticky='w')

        # Create the paragraph for the user to type
        self.text_to_type = tk.Label(self.window, text=self.test.test_text, font=('Arial', 12), wraplength=600,
                                     justify='left', bg='white', relief='ridge')
        self.text_to_type.grid(row=1, column=0, padx=10, pady=20, sticky='ns')

        # Create a text widget to type in
        self.typing_area = tk.Text(self.window, font=('Arial', 12))
        self.typing_area.grid(row=1, column=1, pady=20)
        # start the test when the user clicks on the text widget
        self.typing_area.bind('<FocusIn>', self.start_test)
        self.is_test_in_progress = False

        # Create the timer
        self.timer_frame = tk.Frame(self.window, bg=BG_COLOR)
        self.timer_frame.grid(row=1, column=2, padx=20, pady=20, sticky='n')
        self.timer_label = tk.Label(self.timer_frame, text='Seconds remaining:', font='Verdana', bg=BG_COLOR)
        self.timer_label.grid(row=0, column=0)
        self.seconds_remaining = tk.IntVar()
        self.seconds_remaining.set(60)
        self.seconds = tk.Label(self.timer_frame, textvariable=self.seconds_remaining, font='Verdana', bg=BG_COLOR)
        self.seconds.grid(row=1, column=0)

        self.window.mainloop()

    def start_test(self, event: tk.Event):
        """Starts the test when a text widget <FocusIn> event occurs"""
        if not self.is_test_in_progress:
            self.is_test_in_progress = True
            print('starting test')
            # remove the test instructions from the screen
            self.instructions.grid_remove()
            self.change_test_button.grid_remove()
            # schedule decrementing the time every second for 60 seconds
            for i in range(60):
                self.window.after(i*1000, self.decrement_timer)

    def decrement_timer(self):
        """Decrements the timer, which is `seconds_remaining` IntVar. Calls end_test once seconds_remaining gets to 0."""
        self.seconds_remaining.set(self.seconds_remaining.get()-1)
        self.window.update()
        if self.seconds_remaining.get() == 0:
            print('Ending test')
            self.end_test()

    def end_test(self):
        """Grades the test and checks if the user wants to restart. Either resets the test or destroys the main window"""
        # count words typed
        typed_input = self.typing_area.get("1.0", "end-1c")
        score = self.test.grade(typed_input)
        end_message = f"Your typing speed was {score} words per minute. Would you like to try again?"
        try_again = messagebox.askyesno(title='Test complete', message=end_message)
        if try_again:
            self.reset_test()
        else:
            self.window.destroy()

    def reset_test(self):
        """Performs GUI operations to reset the test"""
        # put the instructions and change test buttons back on the screen
        self.instructions.grid()
        self.change_test_button.grid()
        self.high_score_label.configure(text=f"Best score: {self.test.high_score}")
        # reset the timer
        self.seconds_remaining.set(60)
        # delete the typed text
        self.typing_area.delete("1.0", "end")
        # remove focus from the typing_area so a new <FocusIn> event can occur
        self.window.focus()
        # set Bool to false so start_test function can be called
        self.is_test_in_progress = False

    def change_test(self):
        """Calls the TypingTest method get_new_test to get a new string to type and update the Label"""
        self.test.get_new_test()
        self.text_to_type.config(text=self.test.test_text)
