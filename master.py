from tkinter import *
import time
import winsound

class MasterBar:
    def __init__(self, root):
        super().__init__()
        self.root = root

        self.root.title("Pomodoro Helper")
        self.root.geometry("700x500")
        self.root.configure(bg = "IndianRed")

        menu_bar = Menu(root)
        root.configure(menu=menu_bar)
        
    #User Statistics Option
        def user_data():
            pass

    #Achievement Badges Option
        def badges_user():
            pass

    #Calendar Option
        def calendar_user():
            pass

    #Study List Option
        def studylist_user():
            pass

    #Default Mode Option
        def default_mode():
            hide_frames()
            mode_default_frame.pack(fill = BOTH, expand = TRUE)
    
    #Study Mode Option
        def study_mode():
            hide_frames()
            mode_study_frame.pack(fill = BOTH, expand = TRUE)

    #Relax Mode Option
        def relax_mode():
            hide_frames()
            mode_relax_frame.pack(fill = BOTH, expand = TRUE)

        def hide_frames():
            mode_default_frame.pack_forget()
            mode_study_frame.pack_forget()
            mode_relax_frame.pack_forget()

    #User Menu (Statistics, Achievements, Calendar, Study List)
        user_menu = Menu(menu_bar, tearoff = 0)
        menu_bar.add_cascade(label="User", menu=user_menu)
        user_menu.add_command(label="Statistics", command=user_data)
        user_menu.add_command(label="Achievements", command=badges_user)
        user_menu.add_separator()
        user_menu.add_command(label="Calendar", command=calendar_user)
        user_menu.add_command(label="Study List", command=studylist_user)

    #Mode Menu (Default, Study, Relax)
        mode_menu = Menu(menu_bar, tearoff = 0)
        menu_bar.add_cascade(label="Mode", menu=mode_menu)
        mode_menu.add_command(label="Default Mode", command=default_mode)
        mode_menu.add_command(label="Study Mode", command=study_mode)
        mode_menu.add_command(label="Relax Mode", command=relax_mode)

    #Frames for Mode (Default, Study, Relax)
        mode_default_frame = Frame(root, width= 700, height = 500, bg = "IndianRed")
        mode_study_frame = Frame(root, width= 700, height = 500, bg = "cornflowerblue")
        mode_relax_frame = Frame(root, width= 700, height = 500, bg = "mediumseagreen")

    
if __name__ == "__main__":
    root = Tk()
    app = MasterBar(root)
    root.mainloop()
