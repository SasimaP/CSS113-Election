#search code
import tkinter as tk
import tkinter.messagebox

class VotingApp:
    def __init__(self):
        self.candidates = {
            "A": 0,
            "B": 0,
            "C": 0,
            "D": 0,
        }

        self.root = tk.Tk()
        self.root.title("Nigeria Presidential Election Voting App")

        self.label = tk.Label(self.root, text="Please select a candidate:")
        self.label.pack()

        self.radio_var = tk.StringVar(value="peter obi")
        for candidate in self.candidates:
            radio_button = tk.Radiobutton(self.root, text=candidate, variable=self.radio_var, value=candidate)
            radio_button.pack()

        self.vote_button = tk.Button(self.root, text="Vote", command=self.vote)
        self.vote_button.pack()

        self.results_button = tk.Button(self.root, text="Results", command=self.results)
        self.results_button.pack()

        self.quit_button = tk.Button(self.root, text="Quit", command=self.root.quit)
        self.quit_button.pack()

    def vote(self):
        candidate = self.radio_var.get()
        self.candidates[candidate] += 1
        tk.messagebox.showinfo("Thanks for voting!", f"You voted for {candidate}.")

    def results(self):
        result_str = "Current vote count:\n"
        for candidate, votes in self.candidates.items():
            result_str += f"{candidate}: {votes}\n"
        tk.messagebox.showinfo("Results", result_str)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = VotingApp()
    app.run()