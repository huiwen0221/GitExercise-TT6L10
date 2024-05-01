from tkinter import *

class MasterBar:
    def __init__(self, root):
        super().__init__()
        self.root = root

        self.root.title("Pomodoro Helper")
        self.root.geometry("700x500")
        self.root.configure(bg = "IndianRed")

        menu_bar = Menu(root)
        root.configure(menu=menu_bar)

        def user_data():
            pass
        
        def badges_user():
            pass

        def calendar_user():
            pass

        def studylist_user():
            pass

        def study_mode():
            pass

        def relax_mode():
            pass

        user_menu = Menu(menu_bar, tearoff = 0)
        menu_bar.add_cascade(label="User", menu=user_menu)
        user_menu.add_command(label="Statistics", command=user_data)
        user_menu.add_command(label="Achievements", command=badges_user)
        user_menu.add_command(label="Calendar", command=calendar_user)
        user_menu.add_command(label="Study List", command=studylist_user)

        mode_menu = Menu(menu_bar, tearoff = 0)
        menu_bar.add_cascade(label="Mode", menu=mode_menu)
        mode_menu.add_command(label="Study Mode", command=study_mode)
        mode_menu.add_command(label="Relax Mode", command=relax_mode)

        
if __name__ == "__main__":
    root = Tk()
    app = MasterBar(root)
    root.mainloop()
