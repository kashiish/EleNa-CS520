import tkinter as tk
import sys

def main(path):
    root = tk.Tk()

    canvas1 = tk.Canvas(root, width = 700, height = 600,  relief = 'raised')
    canvas1.pack()

    label_title = tk.Label(root, text='EleNa')
    label_title.config(font=('helvetica', 14))
    canvas1.create_window(350, 25, window=label_title)

    textbox = tk.Text(root)
    textbox.insert(tk.END, path)
    canvas1.create_window(350, 250, window=textbox)

    label_totalElevation = tk.Label(root, text='Total Elevation:')
    label_totalElevation.config(font=('helvetica', 10))
    canvas1.create_window(350, 500, window=label_totalElevation)

    label_totalElevationValue = tk.Label(root, text='0')
    label_totalElevationValue.config(font=('helvetica', 10))
    canvas1.create_window(400, 500, window=label_totalElevationValue)

    label_totalDistance = tk.Label(root, text='Total Distance:')
    label_totalDistance.config(font=('helvetica', 10))
    canvas1.create_window(350, 530, window=label_totalDistance)

    label_totalDistanceValue = tk.Label(root, text='0')
    label_totalDistanceValue.config(font=('helvetica', 10))
    canvas1.create_window(400, 530, window=label_totalDistanceValue)

    root.mainloop()

if __name__ == "__main__":
    #main(sys.argv[1])

    main("")
    