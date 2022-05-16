from tkinter import *
from subprocess import check_output, call
import time

class App():
	def __init__(self, root_tk_obj):

		self.root_tk_obj = root_tk_obj
		self.process_box = None

	def kill_process(self, process_pid):

		log_kill_ps = open("kill_pss.log", "a")
		
		from tkinter import messagebox

		if process_pid == "":
			messagebox.showerror("Ошибка", "Пустой запрос.")
			log_kill_ps.write(time.asctime( time.localtime(time.time()))+"		False(' ')\n")
			log_kill_ps.close()
			return

		try:	
			info_ps = check_output(["ps", "-p", process_pid], universal_newlines = True)
		
		except:
			messagebox.showerror("Ошибка", f"Процесс {process_pid} невозможно остановить.")
			log_kill_ps.write(time.asctime( time.localtime(time.time()))+" "+process_pid+"		False\n")
			log_kill_ps.close()
			return

		return_code = call(["kill", process_pid])

		if return_code == 0:
			messagebox.showinfo("Успешно", f"Процесс {process_pid} остановлен.")
			log_kill_ps.write(time.asctime( time.localtime(time.time()))+" "+info_ps+"		True\n")
			log_kill_ps.close()
			return

	def func_update_button(self):
		
		list_ps = check_output(["ps", "-e"], universal_newlines = True).split("\n")[::-1]

		for ps in list_ps:
			self.process_box.insert(0, ps)

		self.process_box.place(height = 700, width = 1450, relx = 0.017 , rely =.02)

	def start(self):

		self.process_box = Listbox(self.root_tk_obj, bg="#484848", fg = "#ffffff", font = ("Ubuntu", 12))

		scrollbarY = Scrollbar(self.process_box, bg = "#311a10", orient = "vertical", troughcolor = "#484848", command = self.process_box.yview)
		scrollbarX = Scrollbar(self.process_box, bg = "#311a10", orient = "horizontal", troughcolor = "#484848", command = self.process_box.xview)

		self.process_box["yscrollcommand"] = scrollbarY.set
		self.process_box["xscrollcommand"] = scrollbarX.set

		self.func_update_button()

		#
		photo = PhotoImage(file = r"img/update_ico.png")
		photoimage = photo.subsample(13, 13)

		button_update = Button(self.root_tk_obj, bg="#311a29", fg = "#ffffff", font = ("Ubuntu", 12), text = "Обновить", image = photoimage, compound = LEFT, command = self.func_update_button)

		#
		scrollbarY.pack(side = RIGHT, fill = BOTH)
		scrollbarX.pack(side = BOTTOM, fill = BOTH)

		#
		var_entry_ps = StringVar()
		entry_kill_ps = Entry(self.root_tk_obj, textvariable = var_entry_ps, bg = "#311a29", fg = "#ffffff", font = ("Ubuntu", 12))

		button_kill_ps = Button(self.root_tk_obj, bg="#311a29", fg = "#ffffff", font = ("Ubuntu", 12), text = "kill", command = lambda: self.kill_process(var_entry_ps.get()))

		#
		button_update.place(height = 48, width = 144, relx = .888 , rely = .81)

		entry_kill_ps.place(height = 48, width = 96, relx = .0175, rely = .81)
		button_kill_ps.place(height = 48, width = 72, relx = .09, rely = .81)

		self.root_tk_obj.mainloop()

def main():
	window = Tk()
	window.title("Processes Administration")
	window.geometry("1500x900")
	window["bg"]= "#300a24"
	window.resizable(False, False)

	app_start = App(window)
	app_start.start()
