import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

# --- Ana Pencere Ayarları ---
window = tk.Tk()
window.geometry("1080x640")
window.wm_title("Trading Dashboard")

# PanedWindow Yapısı
pw = ttk.PanedWindow(window, orient=tk.HORIZONTAL)
pw.pack(fill=tk.BOTH, expand=True)

w2 = ttk.PanedWindow(pw, orient=tk.VERTICAL)

frame1 = ttk.Frame(pw, width=360, relief=tk.SUNKEN)
frame2 = ttk.Frame(pw, width=720, height=400, relief=tk.SUNKEN)
frame3 = ttk.Frame(pw, width=720, height=240, relief=tk.SUNKEN)

w2.add(frame2)
w2.add(frame3)
pw.add(w2)
pw.add(frame1)

# --- Global Değişkenler ---
selected_item = ""
running = False
update_job = None  # After döngüsünü durdurmak için
data_close_array = np.array([])
future_array = []
current_ax_line = None
current_line = None
current_ax_scatter = None
current_scat = None
current_ma_line = None
current_ma_scat = None
canvas_line = None
canvas_scatter = None

# --- Yardımcı Fonksiyon: Veri Yükleme/Oluşturma ---
def load_data(pair_name):
    # Dosya varsa oku, yoksa rastgele veri üret (Test amaçlı)
    filename = pair_name.lower().replace("/", "") + ".csv"
    
    if os.path.exists(filename):
        df = pd.read_csv(filename)
    else:
        # Demo veri oluşturucu
        print(f"{filename} bulunamadı, rastgele veri üretiliyor...")
        dates = pd.date_range(start='1/1/2023', periods=2000)
        start_price = 1.10 if "EUR" in pair_name else 100
        returns = np.random.normal(0, 0.002, 2000)
        price_data = start_price * np.exp(np.cumsum(returns))
        df = pd.DataFrame({"close1": price_data})
    
    # Veriyi böl
    if len(df) > 1000:
        future = df.iloc[-1000:]
        past = df.iloc[:-1000]
    else:
        # Veri çok azsa yarısını al
        mid = len(df) // 2
        future = df.iloc[mid:]
        past = df.iloc[:mid]

    return past["close1"].values, list(future["close1"].values)

def moving_average(a, n=50):
    if len(a) < n:
        return np.array([])
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n-1:] / n

# --- Event Handlerlar ---
def on_tree_select(event):
    global selected_item
    # Tıklanan öğenin ID'sini al
    selection = treeview.selection()
    if selection:
        item_id = selection[0]
        # ID'den metin değerini al (Örn: EUR/USD)
        item_text = treeview.item(item_id, "text")
        
        # Sadece parite isimlerini seç (Major/Minor başlıklarını ele)
        if "/" in item_text:
            selected_item = item_text
            print(f"Seçildi: {selected_item}")

def readNews(pair_name):
    textBox.delete('1.0', tk.END) # Önceki yazıyı temizle
    filename = "news_" + pair_name.replace("/", "") + ".txt"
    
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                news = f.read()
            textBox.insert(tk.INSERT, news)
        except Exception as e:
            textBox.insert(tk.INSERT, f"Haber dosyası okunamadı: {e}")
    else:
        textBox.insert(tk.INSERT, f"{pair_name} için güncel haber bulunamadı (Demo Modu).")

def openTrade():
    global data_close_array, future_array
    global current_ax_line, current_line, canvas_line
    global current_ax_scatter, current_scat, canvas_scatter
    global current_ma_line, current_ma_scat
    global update_job, running

    if not selected_item:
        messagebox.showwarning("Uyarı", "Lütfen listeden bir parite seçin (Örn: EUR/USD)")
        return

    # Eğer önceki döngü çalışıyorsa durdur
    if update_job:
        window.after_cancel(update_job)
        update_job = None
    running = False
    start_button.config(state="normal")
    
    # Önceki grafikleri temizle
    if canvas_line:
        canvas_line.get_tk_widget().destroy()
    if canvas_scatter:
        canvas_scatter.get_tk_widget().destroy()

    # Veriyi yükle
    data_close_array, future_array = load_data(selected_item)
    readNews(selected_item)

    # --- Grafik 1: Çizgi (Line) ---
    fig1 = plt.Figure(figsize=(5, 4), dpi=100)
    current_ax_line = fig1.add_subplot(111)
    current_line, = current_ax_line.plot(range(len(data_close_array)), data_close_array, color="blue")
    # MA çizgisi için boş bir yer tutucu
    current_ma_line, = current_ax_line.plot([], [], linestyle="--", color="red") 

    canvas_line = FigureCanvasTkAgg(fig1, master=tab1)
    canvas_line.draw()
    canvas_line.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # --- Grafik 2: Scatter ---
    fig2 = plt.Figure(figsize=(5, 4), dpi=100)
    current_ax_scatter = fig2.add_subplot(111)
    # Scatter için başlangıç
    current_ax_scatter.scatter(range(len(data_close_array)), data_close_array, s=1, alpha=0.5, color="blue")
    # MA çizgisi (Scatter tabında da çizgi olarak gösteriyoruz)
    current_ma_scat, = current_ax_scatter.plot([], [], linestyle="--", color="red")

    canvas_scatter = FigureCanvasTkAgg(fig2, master=tab2)
    canvas_scatter.draw()
    canvas_scatter.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    print(f"{selected_item} yüklendi.")


def update():
    global data_close_array, future_array, update_job, running
    
    if not running:
        return

    # Veri bitti mi kontrolü
    if len(future_array) == 0:
        print("Simülasyon bitti.")
        running = False
        start_button.config(state="normal")
        return

    # Yeni veriyi ekle
    new_val = future_array.pop(0)
    data_close_array = np.append(data_close_array, new_val)

    # UI Label güncelleme
    spread = 0.0002
    buy_value.config(text=f"{(new_val - spread):.5f}")
    sell_value.config(text=f"{(new_val + spread):.5f}")

    # Grafik güncelleme
    x_data = range(len(data_close_array))
    
    # 1. Line Grafiğini güncelle (Yeniden çizmek yerine set_data kullanıyoruz - Performans)
    current_line.set_ydata(data_close_array)
    current_line.set_xdata(x_data)
    current_ax_line.set_xlim(0, len(data_close_array) + 10)
    current_ax_line.set_ylim(min(data_close_array)*0.999, max(data_close_array)*1.001)

    # 2. Scatter Grafiğini güncelle
    # Scatter'ı güncellemek zordur, bu yüzden clear yapıp tekrar çizmek en kolayıdır ama yavaştır.
    # Performans için sadece yeni noktayı ekleyebiliriz ama kod basitliği için burada clear kullanacağız
    # veya sadece Line grafiğini güncelleyip Scatter'ı daha az sıklıkla güncelleyebiliriz.
    # Burada temizleyip tekrar çiziyoruz:
    current_ax_scatter.clear()
    current_ax_scatter.scatter(x_data, data_close_array, s=1, alpha=0.5, color="blue")
    current_ax_scatter.set_xlim(0, len(data_close_array) + 10)
    
    # Hareketli Ortalama (MA) Hesaplama
    ma_n = 50 if method.get() == "m1" else 200
    ma_color = "red" if method.get() == "m1" else "green"
    
    if len(data_close_array) > ma_n:
        ma_values = moving_average(data_close_array, ma_n)
        ma_x = range(ma_n - 1, len(data_close_array))
        
        # Line Tabındaki MA
        current_ma_line.set_data(ma_x, ma_values)
        current_ma_line.set_color(ma_color)
        
        # Scatter Tabındaki MA (Tekrar plot etmek gerekiyor çünkü clear() yaptık)
        current_ax_scatter.plot(ma_x, ma_values, linestyle="--", color=ma_color)

    canvas_line.draw()
    canvas_scatter.draw()

    # Döngü
    update_job = window.after(100, update) # 500ms yavaş olabilir, 100ms yaptım

def startTrading():
    global running
    if not selected_item:
        return
    running = True
    start_button.config(state="disabled")
    update()

# --- Arayüz Bileşenleri (Devam) ---

# Treeview
treeview = ttk.Treeview(frame1)
treeview.grid(row=0, column=1, padx=25, pady=25)
treeview.insert("", "0", "Major", text="Major")
treeview.insert("Major", "1", "EUR/USD", text="EUR/USD")
treeview.insert("", "2", "Minor", text="Minor")
treeview.insert("Minor", "3", "EUR/GBR", text="EUR/GBR")
treeview.bind("<<TreeviewSelect>>", on_tree_select) # Doğru event budur

# Button
open_button = tk.Button(frame1, text="Open Trading", command=openTrade)
open_button.grid(row=2, column=1, padx=5, pady=5)

# Text Box
textBox = tk.Text(frame3, width=70, height=10, wrap="word")
textBox.grid(row=0, column=0, padx=25, pady=25)
scroll = tk.Scrollbar(frame3, orient=tk.VERTICAL, command=textBox.yview)
scroll.grid(row=0, column=1, sticky=tk.N + tk.S, pady=10)
textBox.config(yscrollcommand=scroll.set)

# Tabs
tabs = ttk.Notebook(frame2, width=540, height=300)
tabs.place(x=25, y=25)
tab1 = ttk.Frame(tabs)
tab2 = ttk.Frame(tabs)
tabs.add(tab1, text="Line")
tabs.add(tab2, text="Scatter")

# Radio Buttons
method = tk.StringVar(value="m1")
tk.Radiobutton(frame2, text="MA (50)", value="m1", variable=method).place(x=580, y=100)
tk.Radiobutton(frame2, text="MA (200)", value="m2", variable=method).place(x=580, y=125)

# Result Labels
label_frame = tk.LabelFrame(frame2, text="Result", width=100, height=150)
label_frame.place(x=580, y=25)
tk.Label(label_frame, text="Buy: ", bd=3).grid(row=0, column=0)
tk.Label(label_frame, text="Sell: ", bd=3).grid(row=1, column=0)

buy_value = tk.Label(label_frame, text="---", bd=3)
buy_value.grid(row=0, column=1)
sell_value = tk.Label(label_frame, text="---", bd=3)
sell_value.grid(row=1, column=1)

# Start Button
start_button = tk.Button(frame2, text="Start Trading", command=startTrading)
start_button.place(x=580, y=150)
start_button.config(state="disabled")

window.mainloop()